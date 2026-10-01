import time
from pathlib import Path
import json
import discord

from game.player import players, save_players
from game.room_items import room_items, save_room_items
from game.map import ROOMS
from utils.constants import DEAD_ROLE_ID, GAME_ROLE_ID
from game.room_visibility import (
    clear_player_room_visibility,
    get_room_channel,
    get_room_command_channel,
)
from game.status_effects import (
    POISON_STATUS,
    get_due_poison_warnings,
    get_expired_statuses,
    ensure_status_effects,
)

GAME_DURATION_SECONDS = int(60 * 60 * 24 * 10.5)
KILL_BONUS_SECONDS = 60 * 60 * 24

GAME_STATE_FILE = Path(__file__).resolve().parent.parent / "data" / "game.json"

GAME = {
    "running": False,
    "end_time": 0,
    "guild_id": None,
}


def save_game_state():
    """Save the current game state to JSON"""
    GAME_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with GAME_STATE_FILE.open("w", encoding="utf-8") as file:
        json.dump(GAME, file, indent=4)


def load_game_state():
    """Load game state from JSON if it exists"""
    global GAME
    if GAME_STATE_FILE.exists():
        try:
            with GAME_STATE_FILE.open("r", encoding="utf-8") as file:
                loaded_state = json.load(file)
                GAME.update(loaded_state)
        except Exception as e:
            print(f"Error loading game state: {e}")
            save_game_state()
    else:
        save_game_state()


def start_game(guild):
    GAME["running"] = True
    GAME["end_time"] = time.time() + GAME_DURATION_SECONDS
    GAME["guild_id"] = guild.id
    save_game_state()


def time_remaining():
    return max(0, int(GAME["end_time"] - time.time()))


async def register_kill(guild):
    if not GAME["running"] or GAME["guild_id"] != guild.id:
        return

    GAME["end_time"] += KILL_BONUS_SECONDS
    save_game_state()
    await check_win_conditions(guild)


async def check_win_conditions(guild):
    if not GAME["running"] or GAME["guild_id"] != guild.id:
        return False

    alive_murderers = sum(
        player["alive"] and player["role"] == "murderer"
        for player in players.values()
    )
    alive_good = sum(
        player["alive"] and player["role"] != "murderer"
        for player in players.values()
    )

    if alive_murderers == 0:
        await end_game(guild, "good")
        return True

    if alive_good == 0:
        await end_game(guild, "murderers")
        return True

    return False


async def end_game(guild, winner):
    if not GAME["running"] or GAME["guild_id"] != guild.id:
        return

    GAME["running"] = False
    GAME["end_time"] = 0
    GAME["guild_id"] = None
    save_game_state()

    winner_text = "The murderers" if winner == "murderers" else "The good guys"
    role_sections = (
        ("murderer", "Murderers", "<:Knife:1448502216796147842>"),
        ("vigilante", "Vigilantes", "<:Revolver:1446659751927611412>"),
        ("passenger", "Passengers", "<:Keys:1453900262698651749>"),
    )
    role_reveal = "\n\n".join(
        "\n".join(
            [f"## {emoji} {role_name}"]
            + [
                f"* {player['nickname']} ({'alive' if player['alive'] else 'dead'})"
                for player in players.values()
                if player["role"] == role_id
            ]
        )
        for role_id, role_name, emoji in role_sections
    )

    announcement_channel = guild.get_channel(1441558590295900200)

    if announcement_channel is not None:
        full_message = f"# Game ended - {winner_text} win!\n\n{role_reveal}"

        # Discord's message limit is 2000 characters
        if len(full_message) <= 2000:
            await announcement_channel.send(full_message)
        else:
            # Send header first
            await announcement_channel.send(f"# Game ended - {winner_text} win!")

            # Split role sections and send separately if needed
            current_chunk = ""
            for section in role_reveal.split("\n\n"):
                if len(current_chunk) + len(section) + 2 > 1900:  # Leave buffer for safety
                    if current_chunk:
                        await announcement_channel.send(current_chunk)
                    current_chunk = section
                else:
                    current_chunk += ("\n\n" if current_chunk else "") + section

            if current_chunk:
                await announcement_channel.send(current_chunk)

    game_role = guild.get_role(GAME_ROLE_ID)
    dead_role = guild.get_role(DEAD_ROLE_ID)

    dock_channel = get_room_channel(guild, "train_dock")

    for user_id in list(players):
        member = guild.get_member(int(user_id))

        if member is not None:
            await clear_player_room_visibility(guild, member)

            if dock_channel is not None:
                await dock_channel.set_permissions(member, view_channel=True)

            if game_role is not None:
                await member.remove_roles(game_role)

            if dead_role is not None:
                await member.remove_roles(dead_role)

    for items in room_items.values():
        items.clear()

    players.clear()
    save_players()
    save_room_items()


async def process_status_effects(guild):
    """Apply effects whose timers have elapsed."""
    now = time.time()

    for user_id, player in list(players.items()):
        if not player.get("alive", False):
            continue

        member = guild.get_member(int(user_id))
        if member is None:
            try:
                member = await guild.fetch_member(int(user_id))
            except (discord.NotFound, discord.Forbidden, discord.HTTPException) as error:
                print(
                    f"Poisoned player {user_id} isn't available in guild {guild.id}; "
                    f"processing their game death without member role or DM updates: {error}"
                )

        status_changed = False
        for status in ensure_status_effects(player):
            warnings = get_due_poison_warnings(status, now)
            for warning in warnings:
                if member is None:
                    continue
                try:
                    await member.send(f"## Something is wrong...\n\n{warning}")
                except (discord.Forbidden, discord.HTTPException) as error:
                    print(f"Couldn't send poison warning to {user_id}: {error}")
                status_changed = True

        if status_changed:
            save_players()

        expired = get_expired_statuses(player, now)
        poison = next(
            (status for status in expired if status.get("name") == POISON_STATUS),
            None,
        )
        if poison is None:
            continue

        from game.player import kill_player

        room_id = player["room"]
        room_channel = get_room_command_channel(guild, room_id)
        if room_channel is None:
            try:
                room_channel = await guild.fetch_channel(
                    ROOMS[room_id]["command_channel_id"]
                )
            except (discord.NotFound, discord.Forbidden, discord.HTTPException) as error:
                print(
                    f"Couldn't fetch room channel for poisoned death of {user_id}: "
                    f"{error}"
                )

        if room_channel is None:
            room_channel = get_room_channel(guild, room_id)

        if room_channel is None:
            print(
                f"Couldn't announce poisoned death for {user_id}: "
                f"no channel found for room {room_id}"
            )
        else:
            try:
                await room_channel.send(
                    f"**{player['nickname']}** suddenly collapses and dies."
                )
            except (discord.Forbidden, discord.HTTPException) as error:
                print(f"Couldn't announce poisoned death for {user_id}: {error}")

        await kill_player(guild, member, user_id)
        player["status"] = [
            status
            for status in player.get("status", [])
            if status.get("name") != POISON_STATUS
        ]
        save_players()

        if member is not None:
            try:
                await member.send(
                    "## The poison finally takes hold.\n\n"
                    "*You are dead. You may act out your final moments, or roleplay as a corpse, "
                    "but you can no longer use game commands.*"
                )
            except (discord.Forbidden, discord.HTTPException) as error:
                print(f"Couldn't send poison death DM to {user_id}: {error}")

        await register_kill(guild)

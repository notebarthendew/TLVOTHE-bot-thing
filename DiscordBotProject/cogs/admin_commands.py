# FEAR ME
from discord import app_commands
import discord

import random
import asyncio

from game.player import players, create_player, remove_player, save_players
from game.items import ITEMS
from utils.constants import ADMIN_ROLE_ID
from utils.constants import GAME_ROLE_ID
from utils.constants import DEAD_ROLE_ID
from utils.helpers import check_player_status
from game.map import ROOMS
from game.room_items import room_items, save_room_items
from game.game_state import GAME, end_game, register_kill, start_game
from game.room_visibility import set_player_room, clear_player_room_visibility


def setup_commands(bot):

    # --- PLAYER STUFF ----

    async def room_autocomplete(
        interaction,
        current: str
    ):
        return [
            app_commands.Choice(
                name=f"Room {room_id}",
                value=room_id
            )
            for room_id in ROOMS.keys()
            if current.lower() in room_id.lower()
        ][:25]

    async def role_autocomplete(
        interaction,
        current: str
    ):
        return [
            app_commands.Choice(
                name=f"Passenger",
                value="passenger"
            ),

            app_commands.Choice(
                name=f"Vigilante",
                value="vigilante"
            ),

            app_commands.Choice(
                name=f"Murderer",
                value="murderer"
            ),

            app_commands.Choice(
                name=f"None",
                value="none"
            )

        ][:25]

    async def item_autocomplete(
        interaction,
        current: str
    ):
        return [
            app_commands.Choice(
                name=data["name"],
                value=item_id
            )
            for item_id, data in ITEMS.items()
            if (
                current.lower() in item_id.lower() 
                or
                current.lower() in data["name"].lower()
            )
            
        ][:25]

    async def player_nickname_autocomplete(
        interaction,
        current: str
    ):
        return [
            app_commands.Choice(
                name=pdata["nickname"],
                value=pid
            )
            for pid, pdata in players.items()
            if current.lower() in pdata["nickname"].lower()
        ][:25]

    async def remove_autocomplete(interaction, current: str):
        choices = []

        if "everyone".startswith(current.lower()) or "all".startswith(current.lower()):
            choices.append(
                app_commands.Choice(
                    name="Everyone in the game",
                    value="__all__"
                )
            )

        choices.extend(
            app_commands.Choice(
                name=pdata["nickname"],
                value=pid
            )
            for pid, pdata in players.items()
            if current.lower() in pdata["nickname"].lower()
        )

        return choices[:25]

    async def room_player_autocomplete(interaction, current: str):
        user_id = str(interaction.user.id)
        
        if user_id not in players:
            return []

        current_room = players[user_id]["room"]
        
        return [
            app_commands.Choice(
                name=players[pid]["nickname"],
                value=pid
            )
            for pid, pdata in players.items()
            if pid != user_id and pdata["room"] == current_room
            and current.lower() in pdata["nickname"].lower()
        ][:25]

    @bot.tree.command(
        name="startgame",
        description="(ADMIN) Starts a game of TLVOTHE."
    )

    async def startgame(interaction: discord.Interaction):

        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:
            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return

        if GAME["running"]:
            await interaction.response.send_message(
                "A game is already running.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        alive_players = [
            pid for pid in players
            if players[pid]["alive"]
        ]

        role_pool = alive_players.copy()

        if len(alive_players) < 5:
            await interaction.edit_original_response(
                content="You need at least 5 players."
            )
            return

        random.shuffle(role_pool)

        murderers = [
            role_pool.pop(),
            role_pool.pop()
        ]

        vigilantes = [
            role_pool.pop(),
            role_pool.pop(),
            role_pool.pop()
        ]

        for pid in role_pool:
            players[pid]["role"] = "passenger"

        for pid in murderers:
            players[pid]["role"] = "murderer"

        for pid in vigilantes:
            players[pid]["role"] = "vigilante"

        for pid in alive_players:

            role = players[pid]["role"]

            if role == "murderer":
                players[pid]["inventory"] = ["keys"]

            elif role == "vigilante":
                players[pid]["inventory"] = ["keys", "gun"]

            else:
                players[pid]["inventory"] = ["keys"]


        SPAWN_ROOMS = [
            "front",
            "cafeteria",
            "library",
            "infirmary",
            "front_dorm",
            "mid_dorm",
            "back_dorm",
        ]

        for pid in alive_players:

            spawn_room = random.choice(SPAWN_ROOMS)

            role = players[pid]["role"]

            players[pid]["room"] = spawn_room

            member = interaction.guild.get_member(int(pid))

            if member is None:
                continue

            await set_player_room(interaction.guild, member, spawn_room)

            save_players()

            ROLE_OBJECTIVES = {

                "murderer":
                    "Eliminate all passengers along your with Co-hort before time runs out.",

                "vigilante":
                    "Eliminate any murderers and protect the passengers.",

                "passenger":
                    "Stay safe and survive till the end of the ride.",

                "bodyguard":
                    "Protect your assigned passenger at all costs.",

                "detective":
                    "Use your clues to uncover the murderer's identity."

            }

            if role == "murderer":
                cohort_id = next(mid for mid in murderers if mid != pid)
                cohort_nickname = players[cohort_id]["nickname"]
                cohort_emoji = players[cohort_id].get("emoji", "")
                cohort_display = f"{cohort_nickname} ({cohort_emoji})" if cohort_emoji else cohort_nickname

                murderer_text = (
                    f"Your murderer co-hort is **{cohort_display}**. "
                    f"Work together to be undetected."
                )
            else:
                murderer_text = ""

            print(f"Sending DM to {member} ({pid})")
            print(member)
            print(member.guild.name)


            try:
                await member.send(
                    f"""# Welcome aboard, **{role.upper()}!**

            -.-.-.-.-.-.-.-.-.-

            There are 2 killers aboard the train.

            {ROLE_OBJECTIVES[role]}
            {murderer_text}
            """
                )
                print(f"DM sent to {member}")

            except Exception as e:
                print(f"Couldn't DM {member}: {e}")

        start_game(interaction.guild)
        await interaction.edit_original_response(
            content="Game started!"
        )

    @bot.tree.command(
        name="endgame",
        description="(ADMIN) End the current game."
    )
    @app_commands.choices(winner=[
        app_commands.Choice(name="Good guys", value="good"),
        app_commands.Choice(name="Murderers", value="murderers"),
    ])
    async def endgame(
        interaction: discord.Interaction,
        winner: app_commands.Choice[str],
    ):
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:
            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )
            return

        if not GAME["running"]:
            await interaction.response.send_message(
                "There isn't a game running right now.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        await end_game(interaction.guild, winner.value)
        await interaction.edit_original_response(content="Game ended.")

    @bot.tree.command(
        name="info",
        description="(ADMIN) View all player information."
    )
    async def info(interaction: discord.Interaction):

        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:
            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )
            return

        pages = []
        current = "# Player Information\n\n"

        for pid, pdata in players.items():

            member = interaction.guild.get_member(int(pid))

            username = member.name if member else "Unknown"
            
            emoji = pdata.get("emoji", "")
            nickname_display = f"{pdata['nickname']} ({emoji})" if emoji else pdata['nickname']

            line = (
                f"**{nickname_display}** "
                f"({username})\n"
                f"ID: `{pid}` | "
                f"{'🟢' if pdata['alive'] else '🔴'} | "
                f"**{pdata['role'] or 'None'}** | "
                f"📍 {pdata['room']} | "
                f"🎒 {', '.join(pdata['inventory']) if pdata['inventory'] else 'Empty'}\n\n"
            )

            if len(current) + len(line) > 1900:
                pages.append(current)
                current = ""

            current += line

        if current:
            pages.append(current)

        if not pages:
            await interaction.response.send_message(
                "There are no players in the game.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            pages[0],
            ephemeral=True
        )

        for page in pages[1:]:
            await interaction.followup.send(
                page,
                ephemeral=True
            )

    @bot.tree.command(
        name="say",
        description="(snowy dodo only hah) Make the bot say something."
    )

    async def say(
            interaction: discord.Interaction,
            message: str
    ):

        if interaction.user.id != 1087129816416919613:
            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return

        await interaction.response.defer(ephemeral=True)

        typing_time = min(
            random.uniform(0.5, 1.2) + len(message) * random.uniform(0.02, 0.05),
            8
        )

        async with interaction.channel.typing():
            await asyncio.sleep(typing_time)

        await interaction.channel.send(message)

        await interaction.followup.send(
            "Sent.",
            ephemeral=True
        )

    @bot.tree.command(
        name="add",
        description="(ADMIN) Add a player to the game"
    )

    @app_commands.describe(
        member="The player to add"
    )

    @app_commands.autocomplete(
        role=role_autocomplete,
        spawn_room=room_autocomplete
    )

    async def add(
        interaction: discord.Interaction,
        member: discord.Member,
        nickname: str,
        role: str,
        spawn_room: str,
        emoji: str | None = None
    ):

        # Check admin role
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:

            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return

        user_id = str(member.id)

        # Already in game
        if user_id in players:

            await interaction.response.send_message(
                f"{member.mention} is already in the game.",
                ephemeral=True
            )

            return

        if spawn_room not in ROOMS:

            await interaction.response.send_message(
                "That room does not exist.",
                ephemeral=True
            )

            return
        
        # Create player
        print("ADD COMMAND REACHED")
        create_player(user_id, nickname, role, spawn_room, emoji)

        # Give game role
        game_role = interaction.guild.get_role(
            GAME_ROLE_ID
        )

        await member.add_roles(game_role)

        await set_player_room(interaction.guild, member, spawn_room)

        await interaction.response.send_message(
            f"{member.mention} joined the game in room {spawn_room}.",
            ephemeral=True
        )

    @bot.tree.command(
        name="addall",
        description="(ADMIN) Add EVERYONE in the server to the game (chaos mode 😈)"
    )

    @app_commands.autocomplete(
        role=role_autocomplete,
        spawn_room=room_autocomplete
    )

    async def addall(
        interaction: discord.Interaction,
        role: str,
        spawn_room: str,
        emoji: str | None = None
    ):
        # Check admin role
        has_admin_role = any(
            r.id == ADMIN_ROLE_ID
            for r in interaction.user.roles
        )

        if not has_admin_role:
            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )
            return

        if spawn_room not in ROOMS:
            await interaction.response.send_message(
                "That room does not exist.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        added_count = 0
        skipped_count = 0

        for member in interaction.guild.members:
            if member.bot:
                skipped_count += 1
                continue

            user_id = str(member.id)

            if user_id in players:
                skipped_count += 1
                continue

            nickname = member.display_name
            create_player(user_id, nickname, role, spawn_room, emoji)

            game_role = interaction.guild.get_role(GAME_ROLE_ID)
            if game_role is not None:
                await member.add_roles(game_role)

            await set_player_room(interaction.guild, member, spawn_room)
            added_count += 1

        await interaction.edit_original_response(
            content=f"🎉 **CHAOS MODE ACTIVATED** 🎉\n\nAdded **{added_count}** player(s) to the game!\n(Skipped {skipped_count} bot(s) and already-added player(s))"
        )

    @bot.tree.command(
        name="remove",
        description="(ADMIN) Remove a player from the game"
    )

    @app_commands.describe(
        target="The player to remove, or everyone in the game"
    )

    @app_commands.autocomplete(
        target=remove_autocomplete
    )

    async def remove(
        interaction: discord.Interaction,
        target: str,
    ):

        await interaction.response.defer(ephemeral=True)

        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:
            await interaction.edit_original_response(
                content="You cant do that silly."
            )

            return
            
        if target == "__all__":
            player_ids = list(players)
        elif target in players:
            player_ids = [target]
        else:
            await interaction.edit_original_response(
                content="That player isn't in the game."
            )
            return

        game_role = interaction.guild.get_role(
            GAME_ROLE_ID
        )
        dead_role = interaction.guild.get_role(
            DEAD_ROLE_ID
        )

        for user_id in player_ids:
            member = interaction.guild.get_member(int(user_id))

            if member is not None:
                await clear_player_room_visibility(interaction.guild, member)

                if game_role is not None:
                    await member.remove_roles(game_role)

                if dead_role is not None:
                    await member.remove_roles(dead_role)

            remove_player(user_id)

        if target == "__all__":
            await interaction.edit_original_response(
                content=f"Removed {len(player_ids)} player(s) from the game."
            )
        else:
            await interaction.edit_original_response(
                content="The player was removed from the game."
            )
    
    @bot.tree.command(name="checkplayers")
    async def checkplayers(interaction: discord.Interaction):

        has_admin_role = any(
                role.id == ADMIN_ROLE_ID
                for role in interaction.user.roles
            )

        if not has_admin_role:

            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return
        
        await interaction.response.send_message(
            f"```py\n{players}\n```",
            ephemeral=True
        )

    @bot.tree.command(name="itemgive")

    @app_commands.describe(
        target="The player to give the item to"
    )

    @app_commands.autocomplete(
        item=item_autocomplete,
        target=player_nickname_autocomplete
    )
    
    async def itemgive(
        interaction: discord.Interaction,
        target: str,
        item: str
    ):

        print("ITEMGIVE REACHED")
        
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:

            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return

        user_id = target

        if user_id not in players:

            await interaction.response.send_message(
                f"That player is not in the game.",
                ephemeral=True
            )

            return

        print(item)
        
        if item not in ITEMS:

            await interaction.response.send_message(
                "That item does not exist.",
                ephemeral=True
            )

            return

        players[user_id]["inventory"].append(item)
        save_players()

        target_nickname = players[user_id]["nickname"]
        target_emoji = players[user_id].get("emoji", "")
        target_display = f"{target_nickname} ({target_emoji})" if target_emoji else target_nickname
        await interaction.response.send_message(
            f"Gave **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})** to {target_display}.",
            ephemeral=True
        )

    @bot.tree.command(
    name="kill",
    description="(ADMIN) Kill a player"
    )
    @app_commands.describe(target="The player to kill")
    @app_commands.autocomplete(
        target=player_nickname_autocomplete
    )
    async def kill(
        interaction: discord.Interaction,
        target: str
    ):

        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:

            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return
        
        target_id = target

        if target_id not in players:

            await interaction.response.send_message(
                "That player is not in the game.",
                ephemeral=True
            )

            return

        players[target_id]["alive"] = False
        save_players()

        dead_role = interaction.guild.get_role(DEAD_ROLE_ID)
        game_role = interaction.guild.get_role(GAME_ROLE_ID)

        # Get the Discord member to update roles
        target_member = interaction.guild.get_member(int(target_id))
        if target_member:
            await target_member.remove_roles(game_role)
            await target_member.add_roles(dead_role)

        target_nickname = players[target_id]["nickname"]
        target_emoji = players[target_id].get("emoji", "")
        target_display = f"{target_nickname} ({target_emoji})" if target_emoji else target_nickname

        current_room = players[target_id]["room"]
        room_channel = interaction.guild.get_channel(ROOMS[current_room]["channel_id"])

        await interaction.response.send_message(
            f"*{target_display} has been killed.*",
            ephemeral=True
        )
        await room_channel.send(
            f"*{target_display} has died.*"
        )
        await register_kill(interaction.guild)

    @bot.tree.command(name="itemspawn")

    @app_commands.describe(
        item="(ADMIN) Spawn an item on a room."
    )

    @app_commands.autocomplete(
        item=item_autocomplete,
        room=room_autocomplete
    )
    
    async def itemspawn(
        interaction: discord.Interaction,
        item: str,
        room: str
    ):
        
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:

            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return
        
        if room not in ROOMS:

            await interaction.response.send_message(
                "That room does not exist.",
                ephemeral=True
            )

            return

        if item not in ITEMS:

            await interaction.response.send_message(
                "That item does not exist.",
                ephemeral=True
            )

            return
        
        room_items[room].append({
            "id": item
        })
        save_room_items()

        await interaction.response.send_message(
            f"Spawned **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})** in room {room}.",
            ephemeral=True
        )

        return

    @bot.tree.command(
        name="revive",
        description="(ADMIN) Revive a dead player"
    )
    @app_commands.describe(target="The player to revive")
    @app_commands.autocomplete(target=player_nickname_autocomplete)
    async def revive(
        interaction: discord.Interaction,
        target: str
    ):
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:
            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )
            return

        target_id = target

        if target_id not in players:
            await interaction.response.send_message(
                "That player is not in the game.",
                ephemeral=True
            )
            return

        players[target_id]["alive"] = True
        save_players()

        dead_role = interaction.guild.get_role(DEAD_ROLE_ID)
        game_role = interaction.guild.get_role(GAME_ROLE_ID)

        target_member = interaction.guild.get_member(int(target_id))
        if target_member:
            await target_member.remove_roles(dead_role)
            await target_member.add_roles(game_role)
            
            # Restore room visibility
            player_room = players[target_id]["room"]
            await set_player_room(interaction.guild, target_member, player_room)

        target_nickname = players[target_id]["nickname"]
        target_emoji = players[target_id].get("emoji", "")
        target_display = f"{target_nickname} ({target_emoji})" if target_emoji else target_nickname

        await interaction.response.send_message(
            f"Revived {target_display}.",
            ephemeral=True
        )

    @bot.tree.command(
        name="tp",
        description="(ADMIN) Teleport a player to a room"
    )
    @app_commands.describe(target="The player to teleport", room="The room to teleport them to")
    @app_commands.autocomplete(target=player_nickname_autocomplete, room=room_autocomplete)
    async def tp(
        interaction: discord.Interaction,
        target: str,
        room: str
    ):
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:
            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )
            return

        target_id = target

        if target_id not in players:
            await interaction.response.send_message(
                "That player is not in the game.",
                ephemeral=True
            )
            return

        if room not in ROOMS:
            await interaction.response.send_message(
                "That room does not exist.",
                ephemeral=True
            )
            return

        players[target_id]["room"] = room
        save_players()

        target_nickname = players[target_id]["nickname"]
        target_emoji = players[target_id].get("emoji", "")
        target_display = f"{target_nickname} ({target_emoji})" if target_emoji else target_nickname

        await interaction.response.send_message(
            f"Teleported {target_display} to {room}.",
            ephemeral=True
        )

    @bot.tree.command(
        name="givecoins",
        description="(ADMIN) Give coins to a player"
    )
    @app_commands.describe(target="The player to give coins to", amount="Number of coins")
    @app_commands.autocomplete(target=player_nickname_autocomplete)
    async def givecoins(
        interaction: discord.Interaction,
        target: str,
        amount: int
    ):
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:
            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )
            return

        target_id = target

        if target_id not in players:
            await interaction.response.send_message(
                "That player is not in the game.",
                ephemeral=True
            )
            return

        players[target_id]["coins"] = players[target_id].get("coins", 0) + amount
        save_players()

        target_nickname = players[target_id]["nickname"]
        target_emoji = players[target_id].get("emoji", "")
        target_display = f"{target_nickname} ({target_emoji})" if target_emoji else target_nickname

        await interaction.response.send_message(
            f"Gave <:Coin:1512937188751446269> {amount} to {target_display}.",
            ephemeral=True
        )

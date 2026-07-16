# code for each player contesting in thvothe

import json
from pathlib import Path
from utils.constants import GAME_ROLE_ID, DEAD_ROLE_ID
from game.map import ROOMS

players = {}

PLAYERS_FILE = Path(__file__).resolve().parent.parent / "data" / "players.json"

def save_players():

    print("SAVE PLAYERS CALLED")
    print(players)
    
    PLAYERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PLAYERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(players, file, indent=4)

def load_players():
    if PLAYERS_FILE.exists():
        with PLAYERS_FILE.open("r", encoding="utf-8") as file:

            content = file.read()
            
            print("FILE CONTENTS:")
            print(repr(content))

            file.seek(0)
    
            players.clear()
            players.update(json.load(file))
    else:
        players.clear()
        save_players()

def create_player(user_id, nickname, spawn_room):

    players[user_id] = {
        "room": spawn_room,
        "alive": True,
        "role": None,
        "inventory": [],
        "status": [],
        "cooldowns": {},
        "edge_warnings": 0,
        "nickname": nickname
    }
    print(f"Created player: {user_id}")
    print(players)
    save_players()

def remove_player(user_id):

    if user_id in players:
        del players[user_id]
        save_players()

async def kill_player(
    guild: discord.Guild,
    member: discord.Member,
    user_id: str
):

    players[user_id]["alive"] = False

    save_players()

    game_role = guild.get_role(GAME_ROLE_ID)
    dead_role = guild.get_role(DEAD_ROLE_ID)

    if game_role is not None:
        await member.remove_roles(game_role)

    if dead_role is not None:
        await member.add_roles(dead_role)

    for room_data in ROOMS.values():

        channel = guild.get_channel(room_data["channel_id"])

        if channel is None:
            channel = guild.get_thread(room_data["channel_id"])

        if channel is not None:
            await channel.set_permissions(
                member,
                overwrite=None
            )
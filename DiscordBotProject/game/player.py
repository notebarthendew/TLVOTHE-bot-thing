# code for each player contesting in tlvothe

import json
from pathlib import Path
import discord
from utils.constants import GAME_ROLE_ID, DEAD_ROLE_ID
from game.room_visibility import hide_all_game_rooms

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

def create_player(user_id, nickname, role, spawn_room, emoji):

    players[user_id] = {
        "room": spawn_room,
        "alive": True,
        "role": role,
        "inventory": [],
        "status": [],
        "cooldowns": {},
        "edge_warnings": 0,
        "coins": 0,
        "picked_up_gun": False,
        "nickname": nickname,
        "emoji": emoji
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

    await hide_all_game_rooms(guild, member)

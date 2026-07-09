# code for each player contesting in thvothe

import json
from pathlib import Path

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
        "nickname": nickname
    }
    print(f"Created player: {user_id}")
    print(players)
    save_players()

def remove_player(user_id):

    if user_id in players:
        del players[user_id]
        save_players()

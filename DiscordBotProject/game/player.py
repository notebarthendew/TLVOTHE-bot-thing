# code for each player contesting in thvothe

import json

players = {}

def save_players():

    with open(
        "players.json",
        "w"
    ) as file:

        json.dump(
            players,
            file,
            indent=4
        )

def load_players():

    try:

        with open(
            "players.json",
            "r"
        ) as file:

            players.clear()
            players.update(
                json.load(file)
            )

    except FileNotFoundError:

        players.clear()

def create_player(user_id, nickname, spawn_room):

    players[user_id] = {
        "room": spawn_room,
        "alive": True,
        "role": None,
        "inventory": [],
        "status": [],
        "nickname": nickname
    }
    print(f"Created player: {user_id}")
    print(players)
    save_players()

def remove_player(user_id):

    if user_id in players:
        del players[user_id]
        save_players()

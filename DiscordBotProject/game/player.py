# code for each player contesting in thvothe

players = {}

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

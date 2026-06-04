# code for each player contesting in thvothe

players = {}

def create_player(user_id):

    players[user_id] = {
        "room": "1",
        "alive": True,
        "role": None,
        "inventory": [],
        "status": [],
    }
    print(f"Created player: {user_id}")
    print(players)

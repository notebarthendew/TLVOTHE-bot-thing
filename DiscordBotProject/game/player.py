# code for each player contesting in thvothe

players = {}

def create_player(user_id):

    players[user_id] = {
        "room": "cafeteria",
        "alive": True,
        "role": None,
        "inventory": []
        "status": []
    }

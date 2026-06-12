
from game.player import players

def check_player_status(user_id):
    if user_id not in players:
        return "You are not in a train vrotato."
    if not players[user_id]["alive"]:
        return "You are dead. *The train rattles on without you.*"
    return None

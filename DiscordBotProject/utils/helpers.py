
from game.player import players

def check_player_status(user_id):
    if user_id not in players:
        return "You are not in a train vrotato."
    if not players[user_id]["alive"]:
        return "You are dead. (Not a big surprise.)"
    return None

def format_time(seconds):

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if hours:
        return f"{hours}h {minutes}m"

    return f"{minutes}m"

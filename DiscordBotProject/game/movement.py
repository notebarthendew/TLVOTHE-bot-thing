# the main code for moving around the map

from game.map import ROOMS

def move_player(player_data, direction):

    current_room = player_data["room"]

    if direction not in ROOMS[current_room]:
        return None
    
    new_room = ROOMS[current_room][direction]
    
    if new_room is None:
        return None
    
    player_data["room"] = new_room

    return new_room

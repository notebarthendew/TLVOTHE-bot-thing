# the map structure
# currently features 6 rooms for debugging

from utils.constants import (
    ROOM1_ID,
    ROOM2_ID,
    ROOM3_ID,
    ROOM4_ID,
    ROOM5_ID,
    ROOM6_ID,
    ROOM6_THREAD_ID
)

ROOMS = {

    "1": {
        "channel_id": ROOM1_ID,
        "command_channel_id": ROOM1_ID,
        "front": None,
        "back": "2",
        "look_descriptions": [
            "This the description for room onem, wowz.",
            "im going clinically insane also this is the desc for room 1.",
            "as you already know this is room one :3."
        ]
    },

    "2": {
        "channel_id": ROOM2_ID,
        "command_channel_id": ROOM2_ID,
        "front": "1",
        "back": "3",
        "look_descriptions": [
            "Room 2: electric boogaloo.",
            "fuck",
            "can a butterflies' flap really birth a hurricane?."
        ]
    },

    "3": {
        "channel_id": ROOM3_ID,
        "command_channel_id": ROOM3_ID,
        "front": "2",
        "back": "4",
        "look_descriptions": [
            "the.. is 3 enough for a saga?",
            "hoy me comi una salchipapa",
            "as you already know this is room 3 :**3**."
        ]
    },

    "4": {
        "channel_id": ROOM4_ID,
        "command_channel_id": ROOM4_ID,
        "front": "3",
        "back": "5",
        "look_descriptions": [
            "murder",
            "there a mountains of dead dummies here",
            "i wuw murdur."
        ]
    },

    "5": {
        "channel_id": ROOM5_ID,
        "command_channel_id": ROOM5_ID,
        "front": "4",
        "back": "6",
        "look_descriptions": [
            "nothing much happens here excpet for room 6 stuff",
            "guh",
            "i wish more people notices this server"
        ]
    },

    "6": {
        "channel_id": ROOM6_ID,
        "command_channel_id": ROOM6_THREAD_ID,
        "front": "5",
        "back": None,
        "look_descriptions": [
            "GETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHERE",
            "GETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHERE",
            "GETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHEREGETMEOUTOFHERE"
        ]
    }

}

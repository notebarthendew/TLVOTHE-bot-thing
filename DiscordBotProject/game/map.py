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
            "This the description for room one.",
            "This is another description for room one",
            "This is yet another description for room one."
        ]
    },

    "2": {
        "channel_id": ROOM2_ID,
        "command_channel_id": ROOM2_ID,
        "front": "1",
        "back": "3",
        "look_descriptions": [
            "This the description for room two.",
            "This is another description for room two",
            "This is yet another description for room two."
        ]
    },

    "3": {
        "channel_id": ROOM3_ID,
        "command_channel_id": ROOM3_ID,
        "front": "2",
        "back": "4",
        "look_descriptions": [
            "This the description for room three.",
            "This is another description for room three",
            "This is yet another description for room three."
        ]
    },

    "4": {
        "channel_id": ROOM4_ID,
        "command_channel_id": ROOM4_ID,
        "front": "3",
        "back": "5",
        "look_descriptions": [
            "This the description for room four.",
            "This is another description for room four",
            "This is yet another description for room four."
        ]
    },

    "5": {
        "channel_id": ROOM5_ID,
        "command_channel_id": ROOM5_ID,
        "front": "4",
        "back": "6",
        "look_descriptions": [
            "This the description for room five.",
            "This is another description for room five",
            "This is yet another description for room five."
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

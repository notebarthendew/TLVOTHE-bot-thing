# the map structure
# currently features 6 rooms for debugging

from utils.constants import (
    ROOM1_ID,
    ROOM2_ID,
    ROOM3_ID,
    ROOM4_ID,
    ROOM5_ID,
    ROOM6_ID
)

ROOMS = {

    "1": {
        "channel_id": ROOM1_ID,
        "front": None,
        "back": "2"
    },

    "2": {
        "channel_id": ROOM2_ID,
        "front": "1",
        "back": "3"
    },

    "3": {
        "channel_id": ROOM3_ID,
        "front": "2",
        "back": "4"
    },

    "4": {
        "channel_id": ROOM4_ID,
        "front": "3",
        "back": "5"
    },

    "5": {
        "channel_id": ROOM5_ID,
        "front": "4",
        "back": "6"
    },

    "6": {
        "channel_id": ROOM6_ID,
        "front": "5",
        "back": None
    }

}

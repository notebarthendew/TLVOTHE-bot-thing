# the map structure
# currently features 6 rooms for debugging

from utils.constants import (
    ROOM1_ID,
    ROOM2_ID,
    ROOM3_ID,
    ROOM4_ID,
    ROOM5_ID,
    ROOM6_ID,
    ROOM6_THREAD_ID,
    COCKPIT_ID,
    OUTSIDE_FRONT_ID,
    FRONT_ID,
    DINING_ID,
    KITCHEN_ID,
    FRONT_DORM_ID,
    FRONT_DORM_THREAD_ID,
    LUGGAGE_ID,
    LIBRARY_ID,
    INFIRMARY_ID,
    MID_DORM_ID,
    MID_DORM_THREAD_ID,
    CAFETERIA_ID,
    STORAGE_ID,
    BATHROOM_ID,
    BACK_DORM_ID,
    BACK_DORM_THREAD_ID,
    ENGINE_ID,
    OUTSIDE_BACK_ID,
)

ROOMS = {

    "cockpit": {
        "channel_id": COCKPIT_ID,
        "command_channel_id": COCKPIT_ID,
        "front": None,
        "back": "outside_front",
        "look_descriptions": [
            "This is the place where someone important probably drives the train. Probably.\nA giant horn sits here, waiting for someone to ring it and annoy every single person aboard.\nThe controls look complicated enough that touching anything might either save the train or make everyone explode.",
            "The conductor's sacred workplace, now mostly used for people pressing buttons and pulling levers they shouldn't.\nThe horn echoes through every room when activated, reminding everyone that peace was never an option.",
            "The cockpit contains the steering equipment, several suspicious levers, and one extremely loud horn.\nNobody knows why the horn exists.\nEveryone knows someone will pull on it anyway."
        ]
    },

    "outside_front": {
        "channel_id": OUTSIDE_FRONT_ID,
        "command_channel_id": OUTSIDE_FRONT_ID,
        "front": "cockpit",
        "back": "front",
        "look_descriptions": [
            "An open cabin area at the front of the train.\nFresh air, a nice view, and a very convenient lack of walls. Try not to stand too close to the edge unless you trust everyone around you.",
            "The outside front platform. A beautiful place to admire the scenery and also a perfect place to suddenly remember gravity exists.",
            "Wind blows through the front cabin area. The view is amazing. The safety rails are questionable. The people are worse."
        ]
    },

    "front": {
        "channel_id": FRONT_ID,
        "command_channel_id": FRONT_ID,
        "front": "outside_front",
        "back": "dining_room",
        "look_descriptions": [
            "The front hallway of the train. A normal-looking corridor with absolutely nothing suspicious about it.\nIgnore the stains.\nIgnore the noises.\n*Keep walking.*",
            "A hallway connecting the front sections of the train. Many people have walked here. Not all of them have walked away.",
            "bleh"
        ]
    },

    "dining_room": {
        "channel_id": ROOM2_ID,
        "command_channel_id": ROOM2_ID,
        "front": "front",
        "back": "kitchen",
        "look_descriptions": [
            "Its a fancy place where passengers can eat peacefully while pretending nobody is secretly planning anything horrible.",
            "Tables, chairs, and a suspiciously clean eating area. The food is probably safe. The company is questionable.",
            "A room designed for dinner conversations, awkward silence, and people dramatically accusing each other while holding forks."
        ]
    },

    "kitchen": {
        "channel_id": KITCHEN_ID,
        "command_channel_id": KITCHEN_ID,
        "front": "dining_room",
        "back": "front_dorm",
        "look_descriptions": [
            "Where meals are prepared and where every object somehow looks like it could become a weapon.",
            "Pots, pans, knives, and enough cooking equipment to make everyone suddenly very nervous.",
            "The kitchen smells great. Unfortunately, it also contains everything needed for a cooking show or a crime documentary."
        ]
    },

    "front_dorm": {
        "channel_id": FRONT_DORM_ID,
        "command_channel_id": FRONT_DORM_THREAD_ID,
        "front": "kitchen",
        "back": "luggage_room",
        "look_descriptions": [
            "A collection of passenger rooms where people sleep, hide things, and definitely do not plan suspicious activities.",
            "Rows of tiny rooms (don't mind the Cabin Suite) belonging to passengers.\nCozy enough to rest. Isolated enough to make everyone wonder what happened inside.",
            "The sleeping area near the front of the train. Everyone has a room. Everyone has secrets."
        ]
    },

    "luggage_room": {
        "channel_id": LUGGAGE_ID,
        "command_channel_id": LUGAGGE_ID,
        "front": "front_dorm",
        "back": "library",
        "look_descriptions": [
            "Bags, boxes, and mysterious objects that nobody admits belong to them.",
            "A storage area filled with everyone's belongings. If something goes missing, nobody knows who took it.\nConvenient.",
            "The sleeping area near the front of the train. Everyone has a room. Everyone has secrets."
        ]
    },    

    "library": {
        "channel_id": LIBRARY_ID,
        "command_channel_id": LIBRARY_ID,
        "front": "luggage_room",
        "back": "infirmary",
        "look_descriptions": [
            "A quiet place filled with books and a drink tray for anyone who wants to relax before everything goes horribly wrong.",
            'Shelves full of knowledge and a tray of drinks waiting nearby. Reading helps pass time. Alcohol helps people make bad decisions faster.',
            "A peaceful library with comfortable seats, old books, and beverages that may or may not explain tomorrow's regrets."
        ]
    }, 

    "infirmary": {
        "channel_id": INFIRMARY_ID,
        "command_channel_id": INFIRMARY_ID,
        "front": "library",
        "back": "mid_dorm",
        "look_descriptions": [
            "A place meant for healing passengers. Hopefully there won't be too much work for it.\n-# Hopefully.",
            'Medical supplies line the room. The room is prepared for anything. Unfortunately, "anything" keeps happening.',
            "A clean medical room full of equipment and uncomfortable reminders that this train ride is not normal."
        ]
    },

    "mid_dorm": {
        "channel_id": MID_DORM_ID,
        "command_channel_id": MID_DORM_THREAD_ID,
        "front": "infirmary",
        "back": "cafeteria",
        "look_descriptions": [
            "Passenger rooms located safely in the middle of the train, away from danger.\nProbably.",
            "Another sleeping area filled with tired passengers and locked doors. A perfect place to rest or hide.",
            "The central dorm section. Quiet rooms, long hallways, and the occasional suspicious noise."
        ]
    },  

    "cafeteria": {
        "channel_id": CAFETERIA_ID,
        "command_channel_id": CAFETERIA_ID,
        "front": "mid_dorm",
        "back": "storage",
        "look_descriptions": [
            "A food tray sits ready for passengers. Finally, something normal on this train.",
            "Tables, chairs, and a large food tray waiting to be served. Everyone gathers here eventually.\nThat is either convenient or terrifying.",
            "The cafeteria provides meals, conversations, and the perfect place for everyone to stop eating when someone starts accusing another person."
        ]
    },  

    "storage": {
        "channel_id": STORAGE_ID,
        "command_channel_id": STORAGE_ID,
        "front": "cafeteria",
        "back": "bathroom",
        "look_descriptions": [
            "Full of random supplies that may be useful or completely useless.",
            "Boxes and equipment fill the room. Nobody remembers putting half of this stuff here.",
            "A cramped storage area containing everything the train needs. And probably a few things it doesn't."
        ]
    },  

    "bathroom": {
        "channel_id": BATHROOM_ID,
        "command_channel_id": BATHROOM_ID,
        "front": "storage",
        "back": "storage",
        "look_descriptions": [
            "Full of random supplies that may be useful or completely useless.",
            "Boxes and equipment fill the room. Nobody remembers putting half of this stuff here.",
            "A cramped storage area containing everything the train needs. And probably a few things it doesn't."
        ]
    },  
    
    # OLD / TESTING TRAIN
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

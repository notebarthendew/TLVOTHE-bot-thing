ITEMS = {

    "knife": {

        "name": "Knife (<:Knife:1448502216796147842>)",

        "description": (
            "A sharp kitchen knife."
        ),

        "usable": True,

        "consumable": False,

        # maybe do somethign abt cooldown with import time and time.time()
        
        "target_type": "player",

        "action": "kill",

        "kill_messages": [

            "{user} plunged the knife into {target}.",

            "{target} was stabbed to death by {user}.",

            "{user} buried the knife into {target}'s chest.",

            "{target} never saw the blade coming.",

        ],

        "self_kill_messages": [

            "{user} stabbed themselves. (what a way to go out vro)",

            "{user} somehow managed to lose a fight against their own knife.",

            "{user} decided life wasn't worth it anymore."

        ]

    },

    "sirenenote": {

        "name": "Note (<:Note:1522803594313601114>)",

        "description": (
            "Friendly note that La Siréne left you with when boarding."
        ),

        "text": "Welcome to TLVOTHE, thank you for testing the game in its closed alpha stage.\nYou have manny different commands at your disposal, which you can see with the /game_commands command.\nPlease report any inconcistencies, bugs, whatever, and thank you once more for testing the game",

        "usable": True,

        "consumable": False,

        "target_type": "none"
        
    }

}

# Available target_type thingamagigs: "none", "player", "room", "corpse", "self".

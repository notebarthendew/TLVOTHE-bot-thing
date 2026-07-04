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

            "<:KnifeAction:1448502320261496852> {user} plunged the knife into {target}.",

            "<:KnifeAction:1448502320261496852> {target} was stabbed to death by {user}.",

            "<:KnifeAction:1448502320261496852> {user} buried the knife into {target}'s chest.",

            "<:KnifeAction:1448502320261496852> {target} never saw the blade coming.",

        ],

        "self_kill_messages": [

            "<:KnifeAction:1448502320261496852> {user} stabbed themselves. (what a way to go out vro)",

            "<:KnifeAction:1448502320261496852> {user} somehow managed to lose a fight against their own knife.",

            "<:KnifeAction:1448502320261496852> {user} decided life wasn't worth it anymore."

        ]

    },

    "sirenenote": {

        "name": "Note (<:Note:1522803594313601114>)",

        "description": (
            "Friendly note that La Siréne left you with when boarding."
        ),

        "text": "<:NoteAction:1522803643881885858>\nWelcome to TLVOTHE, thank you for testing the game in its closed alpha stage.\nYou have manny different commands at your disposal, which you can see with the /game_commands command.\nPlease report any inconcistencies, bugs, whatever, and thank you once more for testing the game",

        "usable": True,

        "consumable": False,

        "target_type": "none"
        
    }

}

# Available target_type thingamagigs: "none", "player", "room", "corpse", "self".

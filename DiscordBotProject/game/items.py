ITEMS = {

    "knife": {

        "name": "Knife",

        "description": (
            "A sharp kitchen knife."
        ),

        "usable": True,

        "consumable": False,

        # maybe do somethign abt cooldown with import time and time.time()
        
        "target_type": "player",

        "action": "kill"

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

        "name": "Note",

        "description": (
            "Friendly note that La Siréne left you with when boarding."
        ),

        "text": "vro ong you aint coming back, believe me, youre so dead its not even funny. jk it is get rekt bozo.",

        "usable": True,

        "consumable": False,

        "target_type": "none"
        
    }

}

# Available target_type thingamagigs: "none", "player", "room", "corpse", "self".

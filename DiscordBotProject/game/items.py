ITEMS = {

    "knife": {

        "name": "Knife",

        "emoji": "<:Knife:1448502216796147842>",
        
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

        ],

        "death_messages": [

            "You felt a sharp object pierce your body.",

            "A sudden stabbing pain shoots through your body.",

            "The last thing you feel is cold steel sinking into you.",

            "Your legs give out as the knife finds its mark."

        ]
        
    },

    "sirenenote": {

        "name": "Note",

        "emoji": "<:Note:1522803594313601114>",
        
        "description": (
            "Friendly note that La Siréne left you with when boarding."
        ),

        "text": "<:NoteAction:1522803643881885858>\nWelcome to TLVOTHE, thank you for testing the game in its closed alpha stage.\nYou have manny different commands at your disposal, which you can see with the /game_commands command.\nPlease report any inconcistencies, bugs, whatever, and thank you once more for testing the game",

        "usable": True,

        "consumable": False,

        "target_type": "none"
        
    },

    
    "keys": {

        "name": "Keys",

        "emoji": "<:Keys:1453900262698651749>",
        
        "description": (
            "The keys to your cabin. You can't get in if you lose them, so keep them close to you."
        ),


        "usable": False,

        "consumable": False,

        "target_type": "na"
        
    },


    "gun": {

        "name": "Revolver",

        "emoji": "<:Revolver:1446659751927611412>",
        
        "description": (
            "A powerful firearm, capable of killing anyone with one bullet"
        ),


        "usable": True,

        "consumable": False,

        "target_type": "player",

        "action": "kill",

        "kill_messages": [

            "<:RevolverAction:1446671822090403900> {user} fired a shot straight into {target}.",

            "<:RevolverAction:1446671822090403900> A gunshot echoed through the train as {user} shot {target}.",

            "<:RevolverAction:1446671822090403900> {target} collapsed after being shot by {user}.",

            "<:RevolverAction:1446671822090403900> {user} pulled the trigger. {target} never got back up.",

            "<:RevolverAction:1446671822090403900> One deafening shot later, caused by {user}, {target} laid dead.",

            "<:RevolverAction:1446671822090403900> {user} fired without hesitation, killing {target}.",

            "<:RevolverAction:1446671822090403900> The revolver barked, and {target} hit the floor.",

            "<:RevolverAction:1446671822090403900> Smoke drifted from the revolver {user} fired as {target} fell.",

            "<:RevolverAction:1446671822090403900> {user} introduced {target} to the second amendment."
            
        ],

        "self_kill_messages": [

            "<:RevolverAction:1446671822090403900> {user} accidentally shot themselves. Nice one.",

            "<:RevolverAction:1446671822090403900> {user} looked down the wrong end of the revolver.",

            "<:RevolverAction:1446671822090403900> {user} forgot basic firearm safety.",

            "<:RevolverAction:1446671822090403900> A single shot rang out. {user} wasn't getting back up.",

            "<:RevolverAction:1446671822090403900> {user} somehow became their own target.",

            "<:RevolverAction:1446671822090403900> {user} proved that talking things out was overrated."

        ],

        "death_messages": [

            "A gunshot rings out, followed by an unbearable pain in your chest.",

            "Something slams into you with terrifying force.",

            "You hear the shot a split second before everything goes dark.",

            "The impact knocks the breath out of you as you collapse."

        ]
    },

    
    "platearmor": {

        "name": "Plate Armor",

        "emoji": "<:PlateArmor:1523352005240684694>",
        
        "description": (
            "Apply it to someone, and it might just save them from a killing blow. Also light enough for the person to be wearing it to not notice."
        ),


        "usable": False,

        "consumable": False,

        "target_type": "na"
        
    },
    
}
# Available target_type thingamagigs: "none", "player", "room", "corpse", "self", "na".

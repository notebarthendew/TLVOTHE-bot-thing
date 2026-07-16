ITEMS = {

    "knife": {

        "name": "Knife",

        "emoji": "<:Knife:1448502216796147842>",
        
        "description": (
            "A sharp kitchen knife."
        ),

        "usable": True,

        "consumable": False,

        "cooldown": 60 * 60 * 8, # eit horcus
        
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

        "cooldown": 60 * 60 * 5, # fiv horcus

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

        "target_type": "player",

        "action": "protect",
        
        "cooldown": 60 * 60 * 5 # fiv horcus
        
    },

    "poisonbottle": {

        "name": "Poison Bottle",

        "emoji": "<:Keys:1453900262698651749>",
        
        "description": (
            "Apply it to a food or drink tray and if someone eats it, it will guarantee their death... slowly but surely."
        ),


        "usable": False,

        "consumable": True,

        "target_type": "room",

        "action": "poison"
        
    },

    "martini": {

        "name": "Martini",

        "emoji": ":worried:",
        
        "description": (
            "An imppecable beverage to have in this millenium. Don't... drink too much, please."
        ),


        "usable": False,

        "consumable": True,

        "target_type": "na"

    },

    "fries": {

        "name": "Fries",

        "emoji": ":fries:",
        
        "description": (
            "ALL OUR FOOD KEEPS BLOWING U-!"
        ),


        "usable": False,

        "consumable": True,

        "target_type": "na"

    },

    "soda": {

        "name": "Cherry Soda",

        "emoji": "<:CherrySoda:1527067200748261386>",

        "description": (
            "A very delectable an modern soda, using an elongated soup can to store it's cherry flavour.\nTruly one of the inventions of the era!\n-# Don't mind that the liquid shoots out in one direction when you open it."
        ),

        "usable": False,

        "consumable": True,

        "target_type": "na"

    },

    "newspaper_1": {

        "name": "Newspaper",

        "emoji": "<:Note:1522803594313601114>", # its a reading thing so it has teh note thing

        "description": (
            'A newspaper dated before January 1st. Oh hey! It\'s "The Harpy Herald"! I like them.'
        ),

        "text": "# 📰 THE HARPY HERALD\n\n"
        "*Keeping the rails informed since 1894.*\n\n"
        "## LOCAL NEWS\n\n"
        "**MYSTERIOUS DELAYS OUTSIDE GREYRIDGE**\n"
        "Yesterday's Harpy Express was delayed after debris was found on the tracks. Railway officials insist there was no danger, though workers continue to whisper about \"someone walking beside the rails at night.\"\n\n"
        "## TRAVEL & ETIQUETTE\n\n"
        "**A REMINDER TO ALL PASSENGERS**\n"
        "- Do not enter cabins that are not yours.\n"
        "- Keep your belongings with you.\n"
        "- Unattended luggage may be inspected.\n"
        "- Do not lean over the outside platforms while the train is moving.\n\n"
        "## MARKET REPORT\n\n"
        "**Coal prices continue to rise** as industrial demand increases. Railway officials expect no disruption to scheduled services.\n\n"
        "## SOCIAL COLUMN\n\n"
        "Miss Eleanor Winslow of Eastbridge celebrated her engagement aboard the Harpy Express yesterday. Fellow passengers offered congratulations, tea, and more advice than requested.\n\n"
        "## CLASSIFIEDS\n\n"
        "**FOR SALE**\n"
        "Pocket watch. Slightly scratched. Keeps perfect time. Ask the gentleman in the brown waistcoat.\n\n"
        "**LOST**\n"
        "Leather suitcase containing clothes, a journal, and one rather unhappy pet canary. Please notify train staff if found.\n\n"
        "## OPINION\n\n"
        "\"The dining carriage's tomato soup has improved considerably. Whether this is due to a better recipe or lower expectations remains uncertain.\"\n"
        "— Anonymous Passenger\n\n"
        "## WEATHER\n\n"
        "Clear skies are expected throughout today's journey. Evening temperatures may become chilly; passengers visiting the open-air platforms are advised to bring a coat.\n\n"
        "---\n"
        "*The Harpy Herald is printed every morning. Remember: gossip isn't news... unless it's entertaining enough.*",

        "usable": True,

        "consumable": False,

        "target_type": "none"

    },

}

# Available target_type thingamagigs: "none", "player", "room", "corpse", "self", "na".

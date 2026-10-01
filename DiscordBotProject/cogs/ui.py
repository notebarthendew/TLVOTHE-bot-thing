

from __future__ import annotations
import random
import asyncio

from discord import ButtonStyle
import discord
from discord import app_commands

from game.items import ITEMS
from game.map import ROOMS


# -----------------------------------------

ROLE_INFO = {
    "passenger": {
        "emoji": "<:Keys:1453900262698651749>",
        "title": "Passenger",
        "goal": "Stay alive until the journey ends and help the good side identify the murderers.",
        "extra": "Passengers cannot perform kills through the current item system.",
    },
    "vigilante": {
        "emoji": "<:Revolver:1446659751927611412>",
        "title": "Vigilante",
        "goal": "Find and eliminate the murderers while protecting the passengers.",
        "extra": "Vigilantes start with a revolver. Do not waste it on guesses: killing an innocent with the revolver causes it to be dropped afterward.",
    },
    "murderer": {
        "emoji": "<:Knife:1448502216796146852>",
        "title": "Murderer",
        "goal": "Eliminate the entire good side before the game ends.",
        "extra": "Murderers know their co-hort, cannot kill each other, earn coins from kills, and receive passive coins over time.",
    },
}


SECTION_ORDER = [
    "intro",
    "overview",
    "concepts",
    "getting_started",
    "movement",
    "commands",
    "items",
    "roles",
    "murderer",
    "vigilante",
    "sound",
    "winning",
    "advanced",
    "wip",
]

SECTION_LABELS = {
    "intro": ("<:uranium:1532463952716370103>", "Choose a category"),
    "overview": ("<:Keys:1453900262698651749> ", "Overview"),
    "concepts": ("<:PlateArmorAction:1523352095908958258>", "How the Game Works"),
    "getting_started": ("<:KeysAction:1453900340343865465>", "Getting Started"),
    "movement": ("<:NoteAction:1522803643881885858>", "Rooms & Movement"),
    "commands": ("<:Revolver:1446659751927611412>", "Commands"),
    "items": ("<:Note:1522803594313601114>", "Items & Inventory"),
    "roles": ("<:Knife:1448502216796147842>", "Roles"),
    "murderer": ("<:KnifeAction:1448502320261496852>", "Murderer Playbook"),
    "vigilante": ("<:RevolverAction:1446671822090403900>", "Vigilante Playbook"),
    "sound": ("<:Coin:1512937188751446269>", "Sound & Awareness"),
    "winning": ("<:PlateArmorAction:1523352095908958258>", "Win Conditions"),
    "advanced": ("<:PoisonVial:1453889650404884571>", "Advanced Tips"),
    "wip": ("<:PlateArmor:1523352005240684694>", "Current WIP / Limits"),
}



def _clean_item_name(item_id: str) -> str:
    data = ITEMS.get(item_id, {})
    return f"{data.get('emoji', '')} {data.get('name', item_id)}".strip()



def _active_items_text() -> str:
    usable = []
    passive = []

    for item_id, data in ITEMS.items():
        name = data.get("name", item_id)
        if data.get("usable"):
            target = data.get("target_type", "none")
            if target == "player":
                suffix = " — targets a player in your room"
            elif target == "room":
                suffix = " — room-targeted"
            else:
                suffix = " — self/read use"
            usable.append(f"• **{name}**{suffix}")
        else:
            passive.append(f"• **{name}** — currently not usable through `/use`")

    return "\n".join(usable), "\n".join(passive)



def _train_route_text() -> str:
    route = [
        "cockpit",
        "outside_front",
        "front",
        "dining_room",
        "kitchen",
        "front_dorm",
        "luggage_room",
        "library",
        "infirmary",
        "mid_dorm",
        "cafeteria",
        "storage",
        "bathroom",
        "back_dorm",
        "printer_room",
        "engine_room",
        "outside_back",
    ]

    names = {
        "outside_front": "Outside Front",
        "dining_room": "Dining Room",
        "front_dorm": "Front Dorm",
        "luggage_room": "Luggage Room",
        "mid_dorm": "Mid Dorm",
        "back_dorm": "Back Dorm",
        "printer_room": "Printer Room",
        "engine_room": "Engine Room",
        "outside_back": "Outside Back",
        "cockpit": "Cockpit",
        "front": "Front Hall",
        "kitchen": "Kitchen",
        "library": "Library",
        "infirmary": "Infirmary",
        "cafeteria": "Cafeteria",
        "storage": "Storage",
        "bathroom": "Bathroom",
    }

    return " → ".join(names.get(room, room) for room in route)



def build_guide_embed(section: str) -> discord.Embed:
    icon, label = SECTION_LABELS[section]

    embed = discord.Embed(
        title=f"{icon} TLVOTHE Guide — {label}",
        colour=discord.Colour.dark_red(),
    )
    embed.set_footer(text="The Last Voyage of the Harpy Express • Player Guide")

    if section == "intro":
        embed.description = ("the onle and only")

    if section == "overview":
        embed.description = (
            "**The Last Voyage of the Harpy Express** is a long-form murder mystery played inside Discord. "
            "You move around a train, talk to other passengers, manage items, hear events from nearby rooms, "
            "and try to figure out who can be trusted.\n\n"
            "The bot handles the mechanical parts. **Players create the actual investigation through roleplay, "
            "observation, accusations, alliances, and deception.**"
        )
        embed.add_field(
            name="The basic loop",
            value=(
                "1. Check where you are.\n"
                "2. Look around.\n"
                "3. Talk to people.\n"
                "4. Move when useful.\n"
                "5. Track suspicious events and item changes.\n"
                "6. Survive long enough to reach a win condition."
            ),
            inline=False,
        )

    elif section == "concepts":
        embed.description = (
            "Before touching any commands, here's the game explained at a rules level, the kind of "
            "explanation you'd give someone who's never played and just wants to understand what's "
            "actually going on."
        )
        embed.add_field(
            name="How many players do you need?",
            value=(
                "A game needs **at least 5 players** to start. There's currently no upper limit, the "
                "role split below stays fixed no matter how many people join beyond that minimum."
            ),
            inline=False,
        )
        embed.add_field(
            name="The three roles",
            value=(
                "Every game has exactly **2 Murderers** and **3 Vigilantes**, everyone else is a "
                "**Passenger**. These numbers don't scale with player count, a 5-player game and a "
                "30-player game both have exactly 2 Murderers and 3 Vigilantes."
            ),
            inline=False,
        )
        embed.add_field(
            name="Passenger vs. Vigilante, what's actually different",
            value=(
                "Mechanically, almost nothing. Both are on the same side, both want to survive and help "
                "identify the Murderers, and neither can perform kills through the item system on their "
                "own... except a Vigilante starts the game holding a Revolver, which they can use to kill "
                "a suspected Murderer outright. A Passenger has no built-in way to kill anyone. That one "
                "item is the entire mechanical difference between the two roles."
            ),
            inline=False,
        )
        embed.add_field(
            name="What each side is trying to do",
            value=(
                "**Good side (Passengers + Vigilantes):** figure out who the Murderers are before it's "
                "too late, using conversation, movement patterns, and sounds as evidence.\n\n"
                "**Murderers:** eliminate everyone on the good side while making each death look "
                "unclear or unconnected to them. The two Murderers know each other from the start and "
                "coordinate."
            ),
            inline=False,
        )
        embed.add_field(
            name="How a side actually wins",
            value=(
                "The good side wins the moment every living Murderer is eliminated. The Murderers win "
                "the moment every living non-Murderer is eliminated. There's also a game-length timer "
                "running in the background, if it expires before either side wins outright, the good "
                "side is credited with the win by default."
            ),
            inline=False,
        )


    elif section == "getting_started":

        embed.description = (

            "Once a game begins, the bot randomly assigns every player a role and a starting room. "

            "Your role is sent to you privately (usually by DM or an ephemeral message — meaning only "

            "you can see it) and stays secret from other players unless you choose to reveal it yourself. "

            "Murderers are the one exception: they're told who their fellow murderer is."

        )

        embed.add_field(

            name="Your first four moves",

            value=(

                "**1.** Run `/me` — this shows your role, your current room, and your goal.\n"

                "**2.** Run `/inventory` — see what items you're starting with.\n"

                "**3.** Run `/look` — check who else is in your room and what's around.\n"

                "**4.** Say something in the room's channel — talking in character is most of the game."

            ),

            inline=False,

        )

        embed.add_field(

            name="Starting equipment by role",

            value=(

                "• **Passenger:** Keys\n"

                "• **Vigilante:** Keys + Revolver\n"

                "• **Murderer:** Keys\n\n"

                "You can find more items around the train, or unlock them through role-specific systems "

                "like the Murderer shop."

            ),

            inline=False,

        )

        embed.add_field(

            name="How many players does it take?",

            value=(

                "A game needs **at least 5 players** to start. Out of everyone playing, **2 are secretly "

                "made Murderers** and **3 are made Vigilantes** — everyone else is a Passenger."

            ),

            inline=False,

        )


    elif section == "movement":

        embed.description = (

            "Think of the train as one long hallway of rooms, front to back. You can only move to a room "

            "that's directly connected to the one you're in — no teleporting around. Each room corresponds "

            "to its own Discord channel, and you can only send messages in the channel for the room you're "

            "currently in."

        )

        embed.add_field(

            name="The full route, front to back",

            value=_train_route_text(),

            inline=False,

        )

        embed.add_field(

            name="How to move",

            value=(

                "Run **`/move`** and choose **Front** or **Back**. You'll move one room in that direction.\n\n"

                "There's a **12-second cooldown** between moves, so you can't rapidly bounce between rooms "

                "to dodge people or scout everything at once — pace yourself.\n\n"

                "You have to use `/move` from the channel of the room you're currently standing in."

            ),

            inline=False,

        )

        embed.add_field(

            name="Watch yourself at the ends of the train",

            value=(

                "The rear outside platform is dangerous: if you keep trying to move past the very back of "

                "the train, you can eventually fall off and die. Don't wander out there carelessly."

            ),

            inline=False,

        )

        embed.add_field(

            name="You can only see your own room",

            value=(

                "You only see what's happening in your current room's channel. You can't peek into other "

                "rooms, and you can't scroll back through a room's message history after you leave it — "

                "that's intentional, so everyone plays with limited information."

            ),

            inline=False,

        )


    elif section == "commands":

        embed.description = (

            "All commands below are **slash commands** — type `/` in any channel and Discord will show you "

            "the list, or just type the command name directly like it's written here."

        )

        command_lines = [

            "`/guide` — Open this guide.",

            "`/me` — Show your role, room, objective, and murderer coins (if you're a murderer).",

            "`/look` — See who and what is in your current room, including corpses and exits.",

            "`/move` — Move one room toward the front or back of the train.",

            "`/inventory` — View the items you're carrying and any cooldowns on them.",

            "`/inspect` — Read the description/text of an item you own.",

            "`/take` — Pick up an item that's available in your current room.",

            "`/give` — Hand an item to another living player in your room.",

            "`/use` — Use an item that's marked usable; some need a target player in the same room.",

            "`/horn` — Sound the train horn from the cockpit (120-second cooldown).",

            "`/shop` — Murderer-only black market for buying items.",

            "`/timer` — Murderer-only: check how much time is left in the game.",

        ]

        embed.add_field(name="Player commands", value="\n".join(command_lines), inline=False)

        embed.add_field(

            name="If a command won't work",

            value=(

                "Most commands only work in the channel that matches your current room. If the bot tells "

                "you a command failed because of your location, switch to the channel for the room you're "

                "actually standing in and try again."

            ),

            inline=False,

        )


    elif section == "items":

        usable_text, passive_text = _active_items_text()

        embed.description = (

            "Every player has an inventory that persists for the whole game. You can pick items up off "

            "the floor, look at what they do, and — if they're marked usable — use them with `/use`."

        )

        embed.add_field(name="Items you can currently use with /use", value=usable_text or "None", inline=False)

        embed.add_field(name="Items that exist but aren't usable yet", value=passive_text or "None", inline=False)

        embed.add_field(

            name="How items work, step by step",

            value=(

                "• `/inventory` — see everything you're holding and any active cooldowns.\n"

                "• `/inspect` — read an item's description or any text written on it.\n"

                "• `/give` — hand an item to someone, but they must be alive and in your room.\n"

                "• `/take` — pick up items that are placed in your room or dropped on the floor.\n"

                "• `/use` — the bot checks your room, your target, cooldowns, and your role before "

                "letting the action go through."

            ),

            inline=False,

        )

        embed.add_field(

            name="Murderer shop prices (via /shop)",

            value=(

                "**Knife:** 200 coins\n"

                "**Revolver:** 400 coins\n"

                "**Poison Bottle:** 250 coins\n\n"

                "Only Murderers can access the shop."

            ),

            inline=False,

        )


    elif section == "roles":

        embed.description = (

            "There are three roles in the game right now. When a game starts, exactly **2 players become "

            "Murderers** and **3 become Vigilantes** — everyone else is a Passenger."

        )

        for key in ("passenger", "vigilante", "murderer"):
            info = ROLE_INFO[key]

            embed.add_field(

                name=f"{info['emoji']} {info['title']}",

                value=f"**Objective:** {info['goal']}\n{info['extra']}",

                inline=False,

            )

        embed.add_field(

            name="How the two sides break down",

            value=(

                "**Good side:** Passengers + Vigilantes — their goal is to survive and root out the killers.\n"

                "**Killer side:** Murderers — their goal is to eliminate everyone else.\n\n"

                "Murderers are shown who their fellow Murderer is as soon as the game starts, so they can "

                "coordinate."

            ),

            inline=False,

        )


    elif section == "murderer":

        embed.description = (

            "As a Murderer, killing people is only half the job. The real goal is making every death look "

            "unclear, accidental, or unconnected to you — because the longer the game runs, the more "

            "witnesses, sounds, and movement records pile up against you."

        )

        embed.add_field(

            name="What being a Murderer gives you",

            value=(

                "• You're shown who your fellow Murderer is at the start of the game.\n"

                "• Each confirmed kill earns you **100 coins**.\n"

                "• You passively earn **10 coins every 5 minutes** just for staying alive.\n"

                "• You can spend coins in `/shop`.\n"

                "• `/timer` shows how much game time is left."

            ),

            inline=False,

        )

        embed.add_field(

            name="What's in the shop right now",

            value=(

                "**Knife — 200 coins**\n"

                "**Revolver — 400 coins**\n"

                "**Poison Bottle — 250 coins**\n\n"

                "Right now only the Knife and Revolver actually have a working kill action through `/use`. "

                "The Poison Bottle is purchasable but doesn't do anything yet — see the WIP section."

            ),

            inline=False,

        )

        embed.add_field(

            name="One rule you can't get around",

            value=(

                "You cannot kill your fellow Murderer — the game won't let you. Focus on working together "

                "instead."

            ),

            inline=False,

        )

        embed.add_field(

            name="Staying uncaught",

            value=(

                "Think ahead about where you were, where you moved from, who might have seen or heard you, "

                "and whether your inventory and cooldowns line up with a story you could actually tell if "

                "someone questions you."

            ),

            inline=False,

        )

        embed.add_field(

            name="Remember the clock",

            value=(

                "You're racing a timer, not just other players. If the timer runs out before the good side "

                "is eliminated, you lose automatically — and every kill you land adds a day to the timer, "

                "so killing also buys you more time."

            ),

            inline=False,

        )


    elif section == "vigilante":

        embed.description = (

            "The Vigilante starts with the strongest weapon in the game, but that's exactly why you "

            "shouldn't use it on a hunch. Shooting the wrong person can cost your side the game."

        )

        embed.add_field(

            name="Starting weapon",

            value=(

                "You start with a **Revolver**. It can be fired at any living player who is currently in "

                "your room with you."

            ),

            inline=False,

        )

        embed.add_field(

            name="The catch",

            value=(

                "If you shoot someone and they turn out to be innocent, the Revolver is dropped to the "

                "floor right after. Anyone nearby can pick up on that — a wrong guess doesn't just cost a "

                "life, it can expose you too."

            ),

            inline=False,

        )

        embed.add_field(

            name="How to actually play it well",

            value=(

                "Narrow down suspects through conversation and movement patterns before you ever consider "

                "shooting. Someone sounding confident isn't the same as having real evidence. Pay attention "

                "to who arrives, who leaves, and who reacts oddly to events around them."

            ),

            inline=False,

        )


    elif section == "sound":

        embed.description = (

            "Sound is one of the main ways you get information without seeing something directly. When "

            "certain events happen, the bot sends a message (usually by DM) to nearby living players "

            "describing what they heard."

        )

        embed.add_field(

            name="What can trigger a sound notification",

            value=(

                "• **Gunshots**\n"

                "• **Something being dropped or knocked over**\n"

                "• **A player arriving in a room**\n"

                "• **The train horn**, which is announced to the whole train at once\n\n"

                "For the first two, exactly what you're told depends on how close you were to it."

            ),

            inline=False,

        )

        embed.add_field(

            name="Closer means clearer",

            value=(

                "If you're in the same room as the event, you get a more detailed description. If you're "

                "in a nearby room, you usually just get a directional hint, like knowing a gunshot came "

                "from somewhere toward the front of the train. It narrows things down without giving away "

                "the full answer."

            ),

            inline=False,

        )

        embed.add_field(

            name="The train horn",

            value=(

                "`/horn` can only be used from the cockpit, and it has a **120-second cooldown**. Since "

                "it's heard everywhere on the train at once, it's useful as a shared timestamp everyone "

                "can reference later."

            ),

            inline=False,

        )


    elif section == "winning":

        embed.description = (

            "A game can end in one of two ways: one side eliminates the other, or the game's timer runs out."

        )

        embed.add_field(

            name="Good side wins when...",

            value="**every living Murderer has been eliminated.**",

            inline=False,

        )

        embed.add_field(

            name="Murderers win when...",

            value="**every living non-Murderer has been eliminated.**",

            inline=False,

        )

        embed.add_field(

            name="Or, if time runs out first",

            value=(

                "The game currently lasts **10.5 days**, and every confirmed kill adds **1 extra day** to "

                "that timer. If the timer hits zero before either side wins outright, the game ends in "

                "favor of the **good side**."

            ),

            inline=False,

        )

        embed.add_field(

            name="What happens after you die",

            value=(

                "Once you're dead, you lose access to normal game-room channels and can no longer use "

                "player commands. You're still welcome to roleplay your character's final moments however "

                "your server allows it."

            ),

            inline=False,

        )


    elif section == "advanced":

        embed.description = (

            "Once you're comfortable with the commands, TLVOTHE really becomes a game about managing and "

            "cross-checking information."

        )

        embed.add_field(

            name="Keep a timeline",

            value=(

                "Try to remember who was in which room and roughly when. A sound clue becomes much more "

                "useful once you can place specific people around it."

            ),

            inline=False,

        )

        embed.add_field(

            name="Track movement patterns",

            value=(

                "Arrival and departure messages, combined with your own memory of the train's layout, can "

                "rule out stories that just aren't physically possible."

            ),

            inline=False,

        )

        embed.add_field(

            name="Don't lock onto one clue",

            value=(

                "A single suspicious moment is weak evidence on its own. Several independent clues pointing "

                "the same direction are much more convincing."

            ),

            inline=False,

        )

        embed.add_field(

            name="Items tell a story too",

            value=(

                "Who's carrying a weapon, who suddenly got one, and where a dropped gun turns up can all "

                "change how you read a murder."

            ),

            inline=False,

        )

        embed.add_field(

            name="Being nearby isn't proof",

            value=(

                "Being able to reach the murder room only shows opportunity. You still need something "

                "connecting that specific person to the actual event."

            ),

            inline=False,

        )

        embed.add_field(

            name="If you're a Murderer",

            value=(

                "Your best defense is a consistent story. If your movements don't add up, your timing is "

                "impossible, or people remember hearing something you claimed not to, it will eventually "

                "catch up with you."

            ),

            inline=False,

        )

        embed.add_field(

            name="The single most useful habit",

            value=(

                "Keep your own notes outside the game. TLVOTHE runs over a long stretch of time on purpose, "

                "so relying only on memory for every movement and conversation is how mistakes happen."

            ),

            inline=False,

        )


    elif section == "wip":

        embed.description = (

            "This section is here so you know what's still unfinished — don't build a strategy around "

            "anything listed here."

        )

        embed.add_field(

            name="Evidence system",

            value=(

                "`game/evidence.py` is currently just a placeholder file. There is **no working evidence "

                "mechanic yet** — don't expect one in-game."

            ),

            inline=False,

        )

        embed.add_field(

            name="Poison Bottle & Plate Armor",

            value=(

                "Both items are defined in the item data and can be bought or found. Poison Bottles "

                "can be applied to food or drinks through `/use`; poisoned players receive escalating "

                "DM warnings before the poison kills them."

            ),

            inline=False,

        )

        embed.add_field(

            name="Old test rooms",

            value=(

                "The map file still has some old numbered debug rooms left over from testing. They aren't "

                "part of the real train route and aren't covered by this guide."

            ),

            inline=False,

        )

        embed.add_field(

            name="This can all change",

            value=(

                "TLVOTHE is actively being developed. If something here ever disagrees with how the game "

                "actually behaves, trust the live bot over this guide — it means the guide's due for an "

                "update."

            ),

            inline=False,

        )

    return embed


# ---------------------------------------------------------------------------


class GuideSelect(discord.ui.Select):
    def __init__(self, owner_id: int, initial_section: str = "intro"):
        self.owner_id = owner_id
        options = []
        for value in SECTION_ORDER:
            emoji, label = SECTION_LABELS[value]
            options.append(
                discord.SelectOption(
                    label=label,
                    value=value,
                    emoji=emoji,
                    description=_select_description(value),
                    default=value == initial_section,
                )
            )

        super().__init__(
            placeholder="Choose a guide section...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id=f"tlvothe_guide:{owner_id}",
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "no.",
                ephemeral=True,
            )
            return

        section = self.values[0]
        for option in self.options:
            option.default = option.value == section

        await interaction.response.edit_message(
            embed=build_guide_embed(section),
            view=self.view,
        )



def _select_description(section: str) -> str:
    descriptions = {
        "intro": "Choose a damn category already.",
        "overview": "What TLVOTHE is and the core gameplay loop.",
        "concepts": "Roles, player counts, and how a side wins",
        "getting_started": "What happens when you join a game.",
        "movement": "Rooms, route, visibility, and movement cooldowns.",
        "commands": "Quick reference for the player commands.",
        "items": "Inventory, items, shop prices, and item rules.",
        "roles": "Passenger, Vigilante, and Murderer basics.",
        "murderer": "Killer-side mechanics and strategy.",
        "vigilante": "Combat rules and avoiding bad shots.",
        "sound": "Gunshots, arrivals, the horn, and directional alerts.",
        "winning": "How the game can end and who wins.",
        "advanced": "Information, timelines, and higher-level strategy.",
        "wip": "Mechanics that are currently incomplete or stale.",
    }
    return descriptions[section]


class GuideView(discord.ui.View):
    def __init__(self, owner_id: int):
        super().__init__(timeout=15 * 60)
        self.add_item(GuideSelect(owner_id))

    @discord.ui.button(label="Close guide", style=discord.ButtonStyle.secondary, emoji="✖️")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        select = next((item for item in self.children if isinstance(item, GuideSelect)), None)
        if select is not None and interaction.user.id != select.owner_id:
            await interaction.response.send_message(
                "no.",
                ephemeral=True,
            )
            return

        await interaction.response.edit_message(content="Try to survive, yeah?", embed=None, view=None)


GIFS = {
    "waiting": "https://cdn.discordapp.com/attachments/1441505092405821531/1546317676656468038/The_dicehostidle.gif.webp?ex=6a9f580f&is=6a9e068f&hm=491eb86f131ca67f86f04c64581bc2a5ee07e6016a50eacbd0d7eaf9dd38ea3d&",   # idle/anticipation gif
    "rolling": "https://cdn.discordapp.com/attachments/1441505092405821531/1546316814634459166/Dice_host_dice_roll.webp?ex=6a9f5741&is=6a9e05c1&hm=7c9fbcec49a5ca6650d5dec5cb7f0ec88d9030308a8c6ff59ee71e914b73fb03&",   # die-rolling gif
    "result": "https://cdn.discordapp.com/attachments/1441505092405821531/1546317676656468038/The_dicehostidle.gif.webp?ex=6a9f580f&is=6a9e068f&hm=491eb86f131ca67f86f04c64581bc2a5ee07e6016a50eacbd0d7eaf9dd38ea3d&",    # someone won/lost a round
    "victory": "https://cdn.discordapp.com/attachments/1523867230381670581/1535716483051688008/ezgif-3aaa3d04094916e1.gif",   # duel over
}

DICE_RESULT_GIFS = {
    1: "https://cdn.discordapp.com/attachments/1441558590295900200/1547023443382378537/sprites_selected3-ezgif.com-resize.gif?ex=6aa1e95b&is=6aa097db&hm=e9f7cc66c4aa2eab9dc76194c6beacadc41f8e009c549a46539652da6d6efb97&",
    2: "https://cdn.discordapp.com/attachments/1441505092405821531/1547041695906926622/sprites_selected4-ezgif.com-resize.gif?ex=6aa1fa5a&is=6aa0a8da&hm=7d66ef6c9c6b9194831f0eb295612c5db7f8c9c701ab2b42bc80d69aa2c39246&",
    3: "https://cdn.discordapp.com/attachments/1441505092405821531/1547042074073894953/sprites_selected5-ezgif.com-resize.gif?ex=6aa1fab5&is=6aa0a935&hm=31eca5f3b53ffa59401ec357ef3421c67437ff9f4a8b81199be1f8dd30422397&",
    4: "https://cdn.discordapp.com/attachments/1441505092405821531/1547043654311612416/sprites_selected6-ezgif.com-resize.gif?ex=6aa1fc2d&is=6aa0aaad&hm=e285630ded864b95fe78b697fa70b01de2fb309cbbda2863d51f24a74838d6ec&",
    5: "https://cdn.discordapp.com/attachments/1441505092405821531/1547044207351435334/sprites_selected7-ezgif.com-resize.gif?ex=6aa1fcb1&is=6aa0ab31&hm=370262bb3d03e1d8e1a24395828aed3d3a92dc04c2cad23191caf810e2739849&",
    6: "https://cdn.discordapp.com/attachments/1441505092405821531/1547044542459678813/sprites_selected8-ezgif.com-resize.gif?ex=6aa1fd01&is=6aa0ab81&hm=46731796b319cfcb10b174148ef692bcb318719fdcf458e41894216ab9446c51&",
}

def build_round_embed(game, status: str, gif_key: str, lines=None):
    embed = discord.Embed(
        title=f"Dice Duel, Round {game['round']}",
        description=(
            "Guess whether the die will land **lower** (1-2), **higher** (4-6), or exactly **three**. "
            "Guessing three right is worth double. First to 8 points wins."
        ),
        color=discord.Color.dark_gold(),
    )
    if lines:
        embed.description += "\n\n" + "\n".join(lines)
    embed.add_field(
        name="Score",
        value=f"{game['p1'].display_name}: {_score_track(game, game['p1'])}\n"
              f"{game['p2'].display_name}: {_score_track(game, game['p2'])}",
        inline=False,
    )
    embed.add_field(name="Status", value=status, inline=False)
    embed.set_image(url=GIFS[gif_key])
    return embed


def build_dice_result_embed(game, roll: int, lines, status="Showing the result..."):
    embed = build_round_embed(game, status, "result", lines)
    embed.set_image(url=DICE_RESULT_GIFS[roll])
    return embed


def _score_track(game, player):
    score = min(game["scores"][player.id], 8)
    last_round_points = min(game.get("last_round_points", {}).get(player.id, 0), score)
    return (
        "🟢" * last_round_points
        + "⚪" * (score - last_round_points)
        + "⚫" * (8 - score)
    )


class PersonalGuessView(discord.ui.View):
    def __init__(self, game, player):
        super().__init__(timeout=120)
        self.game = game
        self.player = player

    async def lock_in(self, interaction: discord.Interaction, guess: str):
        game = self.game

        if interaction.user.id != self.player.id:
            await interaction.response.send_message("mah man.", ephemeral=True)
            return

        if interaction.user.id in game["guesses"]:
            await interaction.response.send_message("You already locked in a guess this round.", ephemeral=True)
            return

        game["guesses"][interaction.user.id] = guess

        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            content=f"Locked in: **{guess}**. Waiting on your opponent...", view=self
        )

        other = game["p2"] if interaction.user.id == game["p1"].id else game["p1"]

        if other.bot:
            game["guesses"][other.id] = random.choice(("lower", "three", "higher"))
        elif len(game["guesses"]) < 2:
            waiting_embed = build_round_embed(game, f"Waiting on {other.mention} to lock in a guess...", "waiting")
            await game["message"].edit(embed=waiting_embed, view=game["announce_view"])
            return

        rolling_embed = build_round_embed(game, "Rolling the die...", "rolling")
        await game["message"].edit(embed=rolling_embed, view=None)
        await asyncio.sleep(3)

        game["last_round_points"] = {
            game["p1"].id: 0,
            game["p2"].id: 0,
        }
        roll = random.randint(1, 6)
        if roll == 3:
            outcome = "three"
        elif roll > 3:
            outcome = "higher"
        else:
            outcome = "lower"

        lines = [f"The die landed on **{roll}**."]
        for player in (game["p1"], game["p2"]):
            g = game["guesses"][player.id]
            if g == outcome:
                points = 2 if outcome == "three" else 1
                game["scores"][player.id] += points
                game["last_round_points"][player.id] = points
                lines.append(f"{player.mention} guessed **{g}** and was right (+{points}).")
            else:
                lines.append(f"{player.mention} guessed **{g}** and was wrong.")

        winner = None
        if game["scores"][game["p1"].id] >= 8:
            winner = game["p1"]
        elif game["scores"][game["p2"].id] >= 8:
            winner = game["p2"]

        if winner:
            lines.append(f"{winner.mention} wins the duel!")
            result_embed = build_dice_result_embed(game, roll, lines)
            await game["message"].edit(embed=result_embed, view=None)
            await asyncio.sleep(5)
            final_embed = build_round_embed(game, "Duel over.", "victory", lines)
            await game["message"].edit(embed=final_embed, view=None)
            return

        result_embed = build_dice_result_embed(game, roll, lines)
        await game["message"].edit(embed=result_embed, view=None)
        await asyncio.sleep(5)

        game["guesses"] = {}
        game["round"] += 1
        next_announce = DiceDuelRoundAnnounceView(game)
        game["announce_view"] = next_announce
        next_embed = build_round_embed(
            game,
            "Waiting for both players to lock in a guess.",
            "waiting",
            lines,
        )
        await game["message"].edit(embed=next_embed, view=next_announce)

    @discord.ui.button(label="Lower (1-2)", style=ButtonStyle.primary, emoji="⬇️")
    async def lower(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.lock_in(interaction, "lower")

    @discord.ui.button(label="Three", style=ButtonStyle.success, emoji="3️⃣")
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.lock_in(interaction, "three")

    @discord.ui.button(label="Higher (4-6)", style=ButtonStyle.primary, emoji="⬆️")
    async def higher(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.lock_in(interaction, "higher")


class DiceDuelRoundAnnounceView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=180)
        self.game = game

    @discord.ui.button(label="Make Your Guess", style=ButtonStyle.primary, emoji="🎯")
    async def guess(self, interaction: discord.Interaction, button: discord.ui.Button):
        game = self.game
        if interaction.user.id not in (game["p1"].id, game["p2"].id):
            await interaction.response.send_message("This isn't your game.", ephemeral=True)
            return
        if interaction.user.id in game["guesses"]:
            await interaction.response.send_message("You already locked in a guess this round.", ephemeral=True)
            return
        await interaction.response.send_message(
            "Choose your guess:", view=PersonalGuessView(game, interaction.user), ephemeral=True
        )


class DiceDuelChallengeView(discord.ui.View):
    def __init__(self, challenger: discord.Member, opponent: discord.Member):
        super().__init__(timeout=60)
        self.challenger = challenger
        self.opponent = opponent

    @discord.ui.button(label="Accept Duel", style=ButtonStyle.success, emoji="🎲")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.opponent.id:
            await interaction.response.send_message("This challenge isn't yours to accept.", ephemeral=True)
            return

        game = {
            "p1": self.challenger,
            "p2": self.opponent,
            "scores": {self.challenger.id: 0, self.opponent.id: 0},
            "guesses": {},
            "round": 1,
        }
        announce_view = DiceDuelRoundAnnounceView(game)
        game["announce_view"] = announce_view

        embed = build_round_embed(game, "Waiting for both players to lock in a guess.", "waiting")
        await interaction.response.edit_message(embed=embed, view=announce_view)
        game["message"] = await interaction.original_response()

    @discord.ui.button(label="Decline", style=ButtonStyle.secondary, emoji="✖️")
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.opponent.id:
            await interaction.response.send_message("get out.", ephemeral=True)
            return
        await interaction.response.edit_message(
            content=f"{self.opponent.display_name} declined the duel.", embed=None, view=None
        )

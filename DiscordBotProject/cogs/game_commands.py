import random
import time
from collections import Counter
import asyncio

from discord import app_commands
from discord import ButtonStyle
import discord

from game.player import players, create_player, save_players, kill_player
from game.movement import move_player
from game.items import ITEMS
from utils.constants import ADMIN_ROLE_ID
from utils.constants import GAME_ROLE_ID
from utils.constants import DEAD_ROLE_ID
from utils.helpers import check_player_status
from utils.helpers import format_time
from game.map import ROOMS
from game.room_items import room_items, save_room_items
from game.game_state import GAME, register_kill, time_remaining
from game.room_visibility import set_player_room
from game.sound import notify_sound, notify_global


def setup_commands(bot):

    class LoreFollowUpView(discord.ui.View):
        @discord.ui.button(label="Tell me more...", style=ButtonStyle.secondary)
        async def more_lore(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            follow_up_text = "I uh... don't have anythin' else kid. Ah, come back later after I conspire some more."

            await interaction.followup.send(follow_up_text, ephemeral=True)

    class ShopView(discord.ui.View):
        def __init__(self, user_id: str):
            super().__init__()
            self.user_id = user_id
            user_coins = players[user_id].get("coins", 0)

            # Editable shop offerings: list of tuples (item_id, price)
            SHOP_OFFERINGS = [
                ("knife", 200),
                ("gun", 400),
                ("poisonbottle", 250),
            ]

            for item_id, price in SHOP_OFFERINGS:
                item = ITEMS.get(item_id)
                if not item:
                    continue
                name = item.get("name", item_id)
                emoji = item.get("emoji", "")

                # Determine button style and disabled state
                can_afford = user_coins >= price
                style = ButtonStyle.success if can_afford else ButtonStyle.danger

                button = discord.ui.Button(
                    label=f"{name} ({price})",
                    emoji=emoji,
                    style=style,
                    custom_id=f"shop_buy_{item_id}",
                    disabled=not can_afford
                )
                button.callback = self._make_callback(item_id, price, name)
                self.add_item(button)

            # Lore button
            lore_button = discord.ui.Button(
                label="What's your name?",
                style=ButtonStyle.secondary,
                custom_id="shop_lore"
            )
            lore_button.callback = self._lore_callback
            self.add_item(lore_button)

        async def _lore_callback(self, interaction: discord.Interaction):
            await interaction.response.defer()
            lore_text = "Curious are we now? Well then, can't judge someone for asking. The name's Vincent, I live IN the floor basically.\nI know this may be more than what you asked for but I'm here hoping if I'd get somewhere better by sneaking on the train, was easily able to do it too! Those Sirène guys are a bunch of morons they don't even design their stuff properly.\nAnyways that's all I have for now, buy something and stop wastin' my time."
            await interaction.followup.send(lore_text, view=LoreFollowUpView(), ephemeral=True)

        def _make_callback(self, item_id: str, price: int, name: str):
            async def callback(interaction: discord.Interaction):
                await interaction.response.defer()
                user_id = str(interaction.user.id)
                user_coins = players[user_id].get("coins", 0)

                if user_coins < price:
                    await interaction.followup.send(
                        f"Hey pal, you need {price - user_coins} more of those coins to get that.",
                        ephemeral=True
                    )
                    return

                # Deduct coins and add item
                players[user_id]["coins"] -= price
                players[user_id]["inventory"].append(item_id)
                save_players()

                await interaction.followup.send(
                    f"Here you go bud, a brand new **{name}** for <:Coin:1512937188751446269> {price}. Use it wisely.",
                    ephemeral=True
                )
            return callback

    async def inventory_item_autocomplete(
    interaction,
    current: str
    ):
        user_id = str(interaction.user.id)

        if user_id not in players:
            return []

        return [
            app_commands.Choice(
                name=ITEMS[item]["name"],
                value=item
            )
            for item in players[user_id]["inventory"]
            if current.lower() in item.lower()
        ][:25]

    async def room_item_autocomplete(interaction, current: str):
        user_id = str(interaction.user.id)
        
        if user_id not in players:
            return []

        current_room = players[user_id]["room"]
        room_take_items = ROOMS[current_room]["take_items"]

        floor_items = room_items[current_room]

        choices = []

        for item in room_take_items:
            if current.lower() in ITEMS[item]["name"].lower():
                choices.append(
                    app_commands.Choice(
                        name=f"{ITEMS[item]['name']} (Room)",
                        value=item
                    )
                )

        for item_data in floor_items:
            item_id = item_data["id"]

            if current.lower() in ITEMS[item_id]["name"].lower():
                choices.append(
                    app_commands.Choice(
                        name=f"{ITEMS[item_id]['name']} (Floor)",
                        value=item_id
                    )
                )

        return choices[:25]

    async def room_player_autocomplete(interaction, current: str):
        user_id = str(interaction.user.id)

        if user_id not in players:
            return []

        current_room = players[user_id]["room"]

        choices = []

        if "yourself".startswith(current.lower()) or current == "":
            choices.append(
                app_commands.Choice(
                    name="Yourself",
                    value=user_id
                )
            )

        choices.extend(
            app_commands.Choice(
                name=pdata["nickname"],
                value=pid
            )
            for pid, pdata in players.items()
            if (
                pid != user_id
                and pdata["room"] == current_room
                and current.lower() in pdata["nickname"].lower()
            )
        )

        return choices[:25]
        
    
    @bot.tree.command(
    name="move",
    description="(PLAYER) Move through the train"
    )

    @app_commands.describe(
        direction="Direction to move"
    )

    @app_commands.choices(direction=[
        app_commands.Choice(name="Front", value="front"),
        app_commands.Choice(name="Back", value="back")
    ])

    async def move(
        interaction: discord.Interaction,
        direction: app_commands.Choice[str]
    ):

        user_id = str(interaction.user.id)
        
        error = check_player_status(str(interaction.user.id))
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        # Check move cooldown (10 seconds)
        MOVE_COOLDOWN = 12
        cooldowns = players[user_id].get("cooldowns", {})
        now = time.time()
        
        if "__move__" in cooldowns and cooldowns["__move__"] > now:
            remaining = int(cooldowns["__move__"] - now)
            await interaction.response.send_message(
                f"You're still catching your breath. Try moving again in **{remaining}** second(s).",
                ephemeral=True
            )
            return

        EDGE_WARNINGS = [

            "You stop yourself just before stepping off the train.",

            "The tracks rush beneath you. That would've been a terrible idea.",

            "You nearly lose your footing.",

            "You stare into the blur of the railway below."

        ]

        nickname = players[user_id]["nickname"]
        emoji = players[user_id].get("emoji", "")
        nickname_display = f"{nickname} ({emoji})" if emoji else nickname
        
        current_room = players[user_id]["room"]

        allowed_channel_id = ROOMS[current_room]["command_channel_id"]

        if interaction.channel.id != allowed_channel_id:

            await interaction.response.send_message(
            f"You can only move from the room you're currently in. (Use the command in the {current_room} channel)",
            ephemeral=True
        )

            return

        old_channel_main = interaction.guild.get_channel(
            ROOMS[current_room]["channel_id"]
        )
        if old_channel_main is None:
            old_channel_main = interaction.guild.get_thread(
                ROOMS[current_room]["channel_id"]
            )
        
        result = move_player(
            players[user_id],
            direction.value
        ) # this "checks" the room than actually moving the player

        
        if current_room == "outside_back" and direction.value == "back": # only for this one since its the back of the train and nothing else, where in the front version is the bridge to the cockpit

            players[user_id]["edge_warnings"] += 1

            save_players()

            if players[user_id]["edge_warnings"] < 3:

                await interaction.response.send_message(
                    random.choice(EDGE_WARNINGS),
                    ephemeral=True
                )

                return

            elif players[user_id]["edge_warnings"] >= 3:

                await interaction.response.defer(ephemeral=True)

                await kill_player(
                    interaction.guild,
                    interaction.user,
                    user_id
                ) # this already does the permission things so dw

                await interaction.edit_original_response(
                    content="You took one step too many."
                )

                await old_channel_main.send(
                    f"{nickname_display} lost their balance and disappeared beneath the train."
                )

                await interaction.user.send(
                    f"## You lose your footing on the platform, and fall to the tracks.\n\n*You are dead. You may act out your final moments, or roleplay as a corpse, but you can no longer use game commands.*\nYou killed yourself by jumping off the train.\nYou become forgotten from the history books."
                )

                players[user_id]["room"] = "1"
                players[user_id]["edge_warnings"] = 0
                save_players()

                await register_kill(interaction.guild)

                return

        elif result is None:

            await interaction.response.send_message(
                f"*{nickname} confidently walks into a wall*.",
            )

            return

        new_channel = interaction.guild.get_channel(
            ROOMS[result]["command_channel_id"]

        )

        if new_channel is None:

            new_channel = interaction.guild.get_thread(
                ROOMS[result]["command_channel_id"]
            )
        
        players[user_id]["edge_warnings"] = 0
        players[user_id]["cooldowns"]["__move__"] = now + MOVE_COOLDOWN
        save_players()

        await interaction.response.send_message(
            f"*{nickname_display} moved to the {direction.value} of the train.*",
        )

        if direction.value == "back":
            arrival_direction = "front"
        else:
            arrival_direction = "back"

        # announce leaving in old room
        try:
            if old_channel_main:
                await old_channel_main.send(f"*{nickname_display} leaves towards the {direction.value} of the train.*")
        except Exception:
            pass

        await new_channel.send(
            f"*{nickname_display} arrives from the {arrival_direction} of the train.*"
        )

        # Notify nearby players via DM about the arrival
        try:
            await notify_sound(
                interaction.guild,
                result,
                event="arrival",
                full_message=f"{nickname_display} arrives from the {arrival_direction} of the train.",
                radius=1,
                exclude_ids=[user_id],
            )
        except Exception:
            pass

        await set_player_room(interaction.guild, interaction.user, result)

    
    @bot.tree.command(
    name="horn",
    description="(PLAYER) Ring the horn (cockpit only)"
    )
    
    async def horn(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        error = check_player_status(user_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        current_room = players[user_id]["room"]
        if current_room != "cockpit":
            await interaction.response.send_message(
                "You must be in the cockpit to ring the horn.",
                ephemeral=True
            )
            return

        # simple cooldown (60s)
        now = time.time()
        cooldowns = players[user_id].setdefault("cooldowns", {})
        if cooldowns.get("__horn__", 0) > now:
            remaining = int(cooldowns["__horn__"] - now)
            await interaction.response.send_message(
                f"The horn is still recharging. Try again in {remaining} second(s).",
                ephemeral=True
            )
            return

        # trigger horn
        cooldowns["__horn__"] = now + 120
        save_players()

        await interaction.response.send_message("You pull the horn. A deafening blast rings across the train.", ephemeral=True)

        # DM all players and send a short room announcement
        try:
            await notify_global(interaction.guild, "A loud horn blares from the cockpit, echoing through the train.")
        except Exception:
            pass

        # broadcast a short message to each room's command channel (best-effort)
        for room_id, rdata in ROOMS.items():
            try:
                chan = interaction.guild.get_channel(rdata["command_channel_id"]) or interaction.guild.get_thread(rdata["command_channel_id"]) 
                if chan:
                    await chan.send("A loud horn blares from the cockpit, reverberating through the cars.")
            except Exception:
                pass

    @bot.tree.command(
    name="shop",
    description="(MURDERER) See various killing items to buy."
    )
    async def shop(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        error = check_player_status(user_id)

        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        if players[user_id]["role"] != "Murderer":
            await interaction.response.send_message(
                "no.",
                ephemeral=True
            )
            return

        # Editable shop offerings: list of tuples (item_id, price)
        SHOP_OFFERINGS = [
            ("knife", 200),
            ("gun", 400),
            ("poisonbottle", 250),
        ]

        user_coins = players[user_id].get("coins", 0)
        lines = ["# Black Market", "-.-.-.-.-.-.-.-.-.",'"Hey there, welcome to the shop for all weapons and stuff. Tell me if you would like to buy anything here for any porpuse."']
        lines.append(f"**Your coins:** <:Coin:1512937188751446269> {user_coins}")
        lines.append("")
        
        for item_id, price in SHOP_OFFERINGS:
            item = ITEMS.get(item_id)
            if not item:
                continue
            name = item.get("name", item_id)
            emoji = item.get("emoji", "")
            desc = item.get("description", "")
            affordable = "✅" if user_coins >= price else "❌"
            lines.append(f"{affordable} {emoji} **{name}** - <:Coin:1512937188751446269> {price}")
            if desc:
                lines.append(f"--- {desc}")

        message = "\n".join(lines)
        view = ShopView(user_id)
        await interaction.response.send_message(message, view=view, ephemeral=True)

    @bot.tree.command(
    name="look",
    description="(PLAYER) 👀"
    )
    
    async def look(interaction: discord.Interaction):

        user_id = str(interaction.user.id)
        
        error = check_player_status(str(interaction.user.id))
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)

        current_room = players[user_id]["room"]
        room_data = ROOMS[current_room]

        description = random.choice(
            ROOMS[current_room]["look_descriptions"]
        )
        
        front_room = room_data["front"]
        back_room = room_data["back"]
        
        people_in_room = []
        corpses_in_room = []

        items_in_room = room_items[current_room]

        for player_id, player_data in players.items():

            if player_id == user_id:
                continue
            
            if player_data["room"] != current_room:
                continue

            player_emoji = player_data.get("emoji", "")
            nickname_with_emoji = f"{player_data['nickname']} ({player_emoji})" if player_emoji else player_data["nickname"]

            if player_data["alive"]:

                people_in_room.append(
                    nickname_with_emoji
                )

            else:

                corpses_in_room.append(
                    nickname_with_emoji
                )

        if not people_in_room:
            people_text = "- Nobody"
        else:
            people_text = "\n".join(
                f"- {person}"
                for person in people_in_room
            )

        if corpses_in_room:
            corpses_text = "\n".join(
                f"- {corpse}"
                for corpse in corpses_in_room
            )
            corpse_section = (
                f"### Corpses here:\n"
                f"*{corpses_text}*\n\n"
            )
        else:
            corpse_section = ""

        if items_in_room:

            item_counts = Counter(item["id"] for item in items_in_room)
            
            items_text = "\n".join(
                f"- {ITEMS[item]['name']} ({ITEMS[item]['emoji']})"
                + (f" x{count}" if count > 1 else "")
                for item, count in item_counts.items()
            )

            items_section = (
                f"### Items here:\n"
                f"{items_text}\n\n"
            )
            
        else:
            items_section = ""
        
        exits = []

        if room_data["front"] is not None:
            exits.append(f"{front_room} (Front)")

        if room_data["back"] is not None:
            exits.append(f"{back_room} (Back)")

        if not exits:
            exits_text = "- None"
        else:
            exits_text = "\n".join(
               f"- {exit}"
               for exit in exits
        )

        look_messages = [
            f"You see yourself standing in the {current_room} cabin.",
            f"You take a look around cabin {current_room}.",
            f"The train rattles softly as you stand in cabin {current_room}.",
            f"You find yourself in cabin {current_room}.",
            f"You glance around cabin {current_room}.",
            f"The dimly lit cabin {current_room} stretches around you.",
            f"You survey your surroundings in cabin {current_room}.",
            f"Lo, thou standest within Cabin {current_room}, borne ever onward by the great locomotive. Around thee lie the furnishings of the carriage, whilst beyond its walls the thunderous song of wheel and rail proclaimeth the train's relentless advance."
        ]

        look_message = random.choice(look_messages)
        
        await interaction.edit_original_response(
            content=f"## {look_message}\n"
            "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-\n"
            f"{description}\n-.-.-.-.-.-.-.-.-.-.-\n\n"
            f"People here:\n{people_text}\n\n"
            f"{corpse_section}"
            f"{items_section}"
            f"Exits:\n{exits_text}"
        )

    @bot.tree.command(name="inventory",description="Check your inventory.")
    async def inventory(interaction: discord.Interaction):

        user_id = str(interaction.user.id)

        error = check_player_status(user_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        player_inventory = players[user_id]["inventory"]
        
        if player_inventory:
            item_counts = Counter(player_inventory)
            cooldowns = players[user_id]["cooldowns"]
            now = time.time()

            inventory_text = "\n".join(
                f"- {ITEMS[item]['name']} ({ITEMS[item]['emoji']})"
                + (f" x{count}" if count > 1 else "")
                + (
                    f" — cooldown: {format_time(int(cooldowns[item] - now))}"
                    if cooldowns.get(item, 0) > now
                    else ""
                )
                for item, count in item_counts.items()
            )
        else:
            inventory_text = "- Nothing (So much for a high-profile character, smh)"

        await interaction.response.send_message(
            "You scramble through your pockets, and you find:\n\n"
            f"{inventory_text}",
            ephemeral=True
        )

    @bot.tree.command(name="use",description="(PLAYER) Use an item from your inventory.")

    @app_commands.autocomplete(
        item=inventory_item_autocomplete,
        target=room_player_autocomplete
    )

    async def use(
        interaction: discord.Interaction,
        item: str,
        target: str = None
    ):

        user_id = str(interaction.user.id)

        error = check_player_status(user_id)

        if error:

            await interaction.response.send_message(
                error,
                ephemeral=True
            )

            return

        current_room = players[user_id]["room"]
        
        allowed_channel_id = ROOMS[current_room]["command_channel_id"]

        if interaction.channel.id != allowed_channel_id:

            await interaction.response.send_message(
            f"You can only do that from the room you're currently in. (Use the command in the {current_room} channel)",
            ephemeral=True
            )

            return
        
        if item not in players[user_id]["inventory"]:

            await interaction.response.send_message(
                "You don't have that item.",
                ephemeral=True
            )

            return

        if item not in ITEMS:

            await interaction.response.send_message(
                "That item no longer exists.",
                ephemeral=True
            )

            return

        item_data = ITEMS[item]
        target_type = item_data["target_type"]

        
        if not item_data["usable"]:

            await interaction.response.send_message(
                "You can't really seem to find a use for this item.",
                ephemeral=True
            )

            return
            
        if "cooldown" in item_data:
        
            cooldowns = players[user_id]["cooldowns"]

            now = time.time()

            if item in cooldowns:

                if cooldowns[item] > now:
    
                    remaining = int(cooldowns[item] - now)

                    await interaction.response.send_message(
                        f"That item is on cooldown for another **{format_time(remaining)}**.",
                        ephemeral=True
                    )
                    
                    return
        
        if target_type == "none" and target is not None:

            await interaction.response.send_message(
                "That item doesn't require a target.",
                ephemeral=True
            )

            return
        
        if target_type == "player":

            if target is None:

                await interaction.response.send_message(
                    "That item requires a target. (go find someone)",
                    ephemeral=True
                )

                return

            target_id = target

            if target_id not in players:

                await interaction.response.send_message(
                    "That player is not in the game.",
                    ephemeral=True
                )

                return

            if players[target_id]["room"] != current_room:
                await interaction.response.send_message(
                    "That player is not in this room.",
                    ephemeral=True
                )
                return

            target_member = interaction.guild.get_member(int(target_id))

            if target_member is None:
                await interaction.response.send_message(
                    "That Discord member couldn't be found.",
                    ephemeral=True
                )
                return

            target_nickname = players[target_id]["nickname"]
            target_emoji = players[target_id].get("emoji", "")
            target_display = f"{target_nickname} ({target_emoji})" if target_emoji else target_nickname
            
            user_nickname = players[user_id]["nickname"]
            user_emoji = players[user_id].get("emoji", "")
            user_display = f"{user_nickname} ({user_emoji})" if user_emoji else user_nickname
            
            user_role = players[user_id]["role"]
            target_role = players[target_id]["role"]

            if not players[target_id]["alive"]:

                await interaction.response.send_message(
                    "That player is dead.",
                    ephemeral=True
                )

                return

            action = item_data["action"]
            
            if action == "kill":

                if user_role == "passenger" or (
                    user_role == "vigilante" and item == "knife" and target_id != user_id
                ):

                    await interaction.response.send_message(
                        f"You can't bring yourself to kill {target_display}.",
                        ephemeral=True
                    )

                    return

                if user_role == "murderer" and target_role == "murderer":

                    await interaction.response.send_message(
                        f"You can't kill {target_display}, your murderer co-hort.",
                        ephemeral=True
                    )

                    return

                await interaction.response.defer(ephemeral=True)

                await kill_player(
                    interaction.guild,
                    target_member,
                    target_id
                )

                if user_role == "murderer":
                    players[user_id]["coins"] += 100

                save_players()

                await register_kill(interaction.guild)

                if user_role == "murderer" and target_id != user_id:
                    await interaction.edit_original_response(
                        content="Player killed.\n### You got 100 coins for that!"
                    )
                else:
                    await interaction.edit_original_response(
                        content="Player killed."
                    )

                if target_id == user_id:
                    message = random.choice(item_data["self_kill_messages"])
                else:
                    message = random.choice(item_data["kill_messages"])

                allowed_channel_id = ROOMS[current_room]["command_channel_id"]

                # Get the channel and send the message if it exists
                allowed_channel = interaction.guild.get_channel(allowed_channel_id)

                if allowed_channel is None:
                    allowed_channel = interaction.guild.get_thread(allowed_channel_id)

                if allowed_channel:
                    await allowed_channel.send(
                        message.format(
                            user=user_display,
                            target=target_display
                        )
                    )
                    # notify nearby players via DM about the event
                    try:
                        full_msg = message.format(user=user_display, target=target_display)
                        if item == "gun":
                            # larger radius for gunshots; directional hints for distant players
                            await notify_sound(
                                interaction.guild,
                                current_room,
                                event="gunshot",
                                full_message=full_msg,
                                shooter=user_display,
                                target=target_display,
                                radius=2,
                                exclude_ids=[],
                            )
                        else:
                            await notify_sound(
                                interaction.guild,
                                current_room,
                                event="arrival",
                                full_message=full_msg,
                                radius=1,
                                exclude_ids=[],
                            )
                    except Exception:
                        pass

                if target_id != user_id and target_role != "murderer" and item == "gun":
                    players[user_id]["picked_up_gun"] = True
                    save_players()
                    
                    # Drop the gun to the floor
                    if item in players[user_id]["inventory"]:
                        players[user_id]["inventory"].remove(item)
                        save_players()
                    
                    room_items[current_room].append({"id": item})
                    save_room_items()
                    
                    await asyncio.sleep(5)
                    if allowed_channel:
                        await allowed_channel.send(f"But {target_display} didn't look like a murderer...\nMaking {user_display} drop their gun, for whatever reason.")
                        try:
                            await notify_sound(
                                interaction.guild,
                                current_room,
                                event="clatter",
                                full_message=None,
                                radius=2,
                                exclude_ids=[],
                            )
                        except Exception:
                            pass

                death_message = random.choice(item_data["death_messages"])
                
                # Get the Discord member and send them a DM if they exist
                target_member = interaction.guild.get_member(int(target_id))
                if target_member:
                    await target_member.send(
                        f"## {death_message}\n\n*You are dead. You may act out your final moments, or roleplay as a corpse, but you can no longer use game commands.*\nThe one that brought your demise was {user_display} the {user_role}, whom killed you with the {item_data["name"]}.\n## You become forgotten from the history books."
                    )
        
        if target_type == "none":
        
            await interaction.response.send_message(
                item_data["text"],
                ephemeral=True
            )
        
        if item_data["consumable"]:

            players[user_id]["inventory"].remove(item)

            await interaction.followup.send(
                "The item withers away from your very own eyes.",
                ephemeral=True
            )
            
            save_players()

        if "cooldown" in item_data:

            players[user_id]["cooldowns"][item] = (
                time.time() + item_data["cooldown"]
            )

            save_players()
       
    @bot.tree.command(
    name="take", 
    description="(PLAYER) Pick up an item from the room you are in."
    )

    @app_commands.autocomplete(
        item=room_item_autocomplete
    )

    async def take(
        interaction: discord.Interaction,
        item: str,
    ):

        user_id = str(interaction.user.id)

        error = check_player_status(user_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        current_room = players[user_id]["room"]

        allowed_channel_id = ROOMS[current_room]["command_channel_id"]

        allowed_channel = interaction.guild.get_channel(allowed_channel_id)

        if allowed_channel is None:
            allowed_channel = interaction.guild.get_thread(allowed_channel_id)

        if interaction.channel.id != allowed_channel_id:

            await interaction.response.send_message(
                f"You can only do that from room {current_room}.",
                ephemeral=True
            )

            return
        
        if item not in ITEMS:
            await interaction.response.send_message(
                "That doesn't exist.",
                ephemeral=True
            )
            return

        item_on_floor = any(i["id"] == item for i in room_items[current_room])
        item_from_room = item in ROOMS[current_room]["take_items"]

        if not item_on_floor and not item_from_room:
            await interaction.response.send_message(
                "That item isn't here.",
                ephemeral=True
            )
            return

        if item == "gun" and players[user_id]["picked_up_gun"]:
            await interaction.response.send_message(
                "You can't pick up Revolvers.",
                ephemeral=True
            )
            return

        user_nickname = players[user_id]["nickname"]
        user_emoji = players[user_id].get("emoji", "")
        user_display = f"{user_nickname} ({user_emoji})" if user_emoji else user_nickname

        await interaction.response.send_message(
            f"You picked up **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})**.",
            ephemeral=True
        )

        if item_on_floor:

            for i, room_item in enumerate(room_items[current_room]):
                if room_item["id"] == item:
                    room_items[current_room].pop(i)
                    break

            save_room_items()

            players[user_id]["inventory"].append(item)

            if allowed_channel:
                await allowed_channel.send(
                    f"{user_display} picked up a **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})** from the ground."
                )
                try:
                    await notify_sound(
                        interaction.guild,
                        current_room,
                        event="pickup",
                        full_message=f"{user_display} picked up {ITEMS[item]['name']}.",
                        radius=1,
                        exclude_ids=[user_id],
                    )
                except Exception:
                    pass

        else:

            players[user_id]["inventory"].append(item)

            if allowed_channel:
                await allowed_channel.send(
                    f"{user_display} grabbed a **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})** from the room."
                )

        save_players()

    @bot.tree.command(
    name="give",
    description="(PLAYER) Give an item from your inventory to another player."
    )

    @app_commands.autocomplete(
        item=inventory_item_autocomplete,
        target=room_player_autocomplete
    )

    async def give(
        interaction: discord.Interaction,
        item: str,
        target: str
    ):

        user_id = str(interaction.user.id)

        error = check_player_status(user_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        current_room = players[user_id]["room"]

        allowed_channel_id = ROOMS[current_room]["command_channel_id"]
        
        if interaction.channel.id != allowed_channel_id:
            await interaction.response.send_message(
                f"You can only do that from room {current_room}.",
                ephemeral=True
            )
            return
        
        if item not in players[user_id]["inventory"]:


            await interaction.response.send_message(
                "You don't have that item.",
                ephemeral=True
            )
            return

        if item not in ITEMS:
            await interaction.response.send_message(
                "That item no longer exists.",
                ephemeral=True
            )
            return

        target_id = target
        
        if target_id not in players:
            await interaction.response.send_message(
                "That player is not in the game.",
                ephemeral=True
            )
            return

        if not players[target_id]["alive"]:
            await interaction.response.send_message(
                "That player is dead.",
                ephemeral=True
            )
            return

        if players[target_id]["room"] != current_room:
            await interaction.response.send_message(
                "That player is not in this room.",
                ephemeral=True
            )
            return

        players[user_id]["inventory"].remove(item)
        players[target_id]["inventory"].append(item)
        save_players()

        user_nickname = players[user_id]["nickname"]
        target_nickname = players[target_id]["nickname"]
        target_emoji = players[target_id].get("emoji", "")
        target_display = f"{target_nickname} ({target_emoji})" if target_emoji else target_nickname
        
        item_name = ITEMS[item]["name"]
        
        await interaction.response.send_message(
            f"You gave **{item_name} ({ITEMS[item]['emoji']})** to {target_display}.",
            ephemeral=True
        )

    @bot.tree.command(
    name="inspect",
    description="(PLAYER) Read the description of an item in your inventory."
    )

    @app_commands.autocomplete(
        item=inventory_item_autocomplete,
    )

    async def inspect(
        interaction: discord.Interaction,
        item: str,
    ):

        user_id = str(interaction.user.id)

        error = check_player_status(user_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        if item not in ITEMS:
            await interaction.response.send_message(
                "That item doesn't exist.",
                ephemeral=True
            )
            return
        
        if item not in players[user_id]["inventory"]:
            await interaction.response.send_message(
                "You don't have that item.",
                ephemeral=True
            )
            return

        message = (
            f"## {ITEMS[item]['name']} ({ITEMS[item]['emoji']})\n\n"
            f"{ITEMS[item]['description']}"
        )

        if "text" in ITEMS[item]:
            message += f"\n\n---\n{ITEMS[item]['text']}"

        await interaction.response.send_message(message, ephemeral=True)

    @bot.tree.command(
        name="me",
        description="(PLAYER) Get general information about you."
    )

    async def me(
            interaction: discord.Interaction
    ):

        user_id = str(interaction.user.id)

        error = check_player_status(user_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        player = players[user_id]

        #statuses = (
        #    ", ".join(player["status"])
        #    if player["status"]
        #    else "None"
        #)

        # keeping this in the code till i have status effects

        role = (player["role"] or "none").lower()

        role_hint = {
            "murderer":
                "eliminate every innocent passenger.",
            "vigilante":
                "protect the train and stop the murderers.",
            "passenger":
                "survive until the journey ends.",
        }

        coin_text = (
            f"Since you are the murderer, you have <:Coin:1512937188751446269> {player['coins']} in your stash."
            if role == "murderer"
            else ""
        )
        
        player_emoji = player.get("emoji", "")
        nickname_display = f"{player['nickname']} ({player_emoji})" if player_emoji else player["nickname"]

        await interaction.response.send_message(
            f"""# Information

        You are {nickname_display}, the {role}.
        You are also currently staying in the {player["room"]}.
        {coin_text}

        Your objective is to {role_hint.get(role, "wait for the game to assign your role.")}

        Good luck aboard the Harpy Express.""",
            ephemeral=True
        )

    @bot.tree.command(
        name="timer",
        description="(MURDERER) See the time remaining."
    )
    async def timer(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        error = check_player_status(user_id)

        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        if not GAME["running"]:
            await interaction.response.send_message(
                "There isn't a game running right now.",
                ephemeral=True
            )
            return

        if players[user_id]["role"] != "murderer":
            await interaction.response.send_message(
                "Only the murderers know how long the train has left.",
                ephemeral=True
            )
            return

        remaining = time_remaining()
        days, remaining = divmod(remaining, 86400)
        hours, minutes = divmod(remaining, 3600)
        minutes //= 60

        await interaction.response.send_message(
            f"## {days} day(s), {hours} hour(s), and {minutes} minute(s) remain.",
            ephemeral=True
        )

    # ---- DEBBUGING COMMANdS ----
    @bot.tree.command(name="myroom")
    async def myroom(interaction: discord.Interaction):

        user_id = str(interaction.user.id)

        error = check_player_status(user_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return
    
        await interaction.response.send_message(
            players[user_id]["room"],
            ephemeral=True
        )

# h




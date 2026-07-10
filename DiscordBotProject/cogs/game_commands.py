import random
import time
from collections import Counter

from discord import app_commands
import discord

from game.player import players, create_player, save_players
from game.movement import move_player
from game.items import ITEMS
from utils.constants import ADMIN_ROLE_ID
from utils.constants import GAME_ROLE_ID
from utils.constants import DEAD_ROLE_ID
from utils.helpers import check_player_status
from utils.helpers import format_time
from game.map import ROOMS
from game.room_items import room_items


def setup_commands(bot):

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

        for item in floor_items:
            if current.lower() in ITEMS[item]["name"].lower():
                choices.append(
                    app_commands.Choice(
                        name=f"{ITEMS[item]['name']} (Floor)",
                        value=item
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
    description="Move through the train"
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

        nickname = players[user_id]["nickname"]
        
        current_room = players[user_id]["room"]

        allowed_channel_id = ROOMS[current_room]["command_channel_id"]

        if interaction.channel.id != allowed_channel_id:

            await interaction.response.send_message(
            f"You can only move from the room you're currently in. (Use the command in the {current_room} channel)",
            ephemeral=True
        )

            return

        old_channel = interaction.guild.get_channel(
            ROOMS[current_room]["command_channel_id"]
        )

            
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
        )

        
        if result is None:

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
        
        new_channel_main = interaction.guild.get_channel(
            ROOMS[result]["channel_id"]         
        )
        
        await interaction.response.send_message(
            f"*{nickname} moved to the {direction.value} of the train.*",
        )

        if direction.value == "back":
            arrival_direction = "front"
        else:
            arrival_direction = "back"

        await new_channel.send(
            f"*{nickname} arrives from the {arrival_direction} of the train.*"
        )
        
        await old_channel_main.set_permissions(
            interaction.user,
            view_channel=False
        )

        await new_channel_main.set_permissions(
            interaction.user,
            view_channel=True
        )

    
    @bot.tree.command(
    name="look",
    description="👀"
    )
    
    async def look(interaction: discord.Interaction):

        user_id = str(interaction.user.id)
        
        error = check_player_status(str(interaction.user.id))
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

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

            if player_data["alive"]:

                people_in_room.append(
                    player_data["nickname"]
                )

            else:

                corpses_in_room.append(
                    player_data["nickname"]
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
        
        await interaction.response.send_message(
            f"## {look_message}\n"
            "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-\n"
            f"{description}\n-.-.-.-.-.-.-.-.-.-.-\n\n"
            f"People here:\n{people_text}\n\n"
            f"{corpse_section}"
            f"{items_section}"
            f"Exits:\n{exits_text}",
            ephemeral=True
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

            inventory_text = "\n".join(
                f"- {ITEMS[item]['name']} ({ITEMS[item]['emoji']})"
                + (f" x{count}" if count > 1 else "")
                for item, count in item_counts.items()
            )
        else:
            inventory_text = "- Nothing (So much for a high-profile character, smh)"

        await interaction.response.send_message(
            "You scramble through your pockets, and you find:\n\n"
            f"{inventory_text}",
            ephemeral=True
        )

    @bot.tree.command(name="use",description="Use an item from your inventory.")

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

            target_nickname = players[target_id]["nickname"]
            user_nickname = players[user_id]["nickname"]

            if not players[target_id]["alive"]:

                await interaction.response.send_message(
                    "That player is dead.",
                    ephemeral=True
                )

                return

            action = item_data["action"]
            
            if action == "kill":

                players[target_id]["alive"] = False

                dead_role = interaction.guild.get_role(DEAD_ROLE_ID)
                game_role = interaction.guild.get_role(GAME_ROLE_ID)

                # Get the Discord member to update roles
                target_member = interaction.guild.get_member(int(target_id))
                if target_member:
                    await target_member.remove_roles(game_role)
                    await target_member.add_roles(dead_role)
                
                save_players()

                await interaction.response.send_message(
                    "Action made successfully.",
                    ephemeral=True
                )

                if target_id == user_id:
                    message = random.choice(item_data["self_kill_messages"])
                else:
                    message = random.choice(item_data["kill_messages"])

                # Get the channel and send the message if it exists
                allowed_channel = interaction.guild.get_channel(allowed_channel_id)
                if allowed_channel:
                    await allowed_channel.send(
                        message.format(
                            user=user_nickname,
                            target=target_nickname
                        )
                    )

                death_message = random.choice(item_data["death_messages"])
                
                # Get the Discord member and send them a DM if they exist
                target_member = interaction.guild.get_member(int(target_id))
                if target_member:
                    await target_member.send(
                        f"## {death_message}\n\n*You are dead. You may act out your final moments, or roleplay as a corpse, but you can no longer use game commands.*\nThe one that brought your demise was {user_nickname}, whom killed you with the {item_data["name"]}.\nThe last voyage of the Harpy Express has 1 survivor less."
                    )
        
        if target_type == "none":
        
            await interaction.response.send_message(
                item_data["text"],
                ephemeral=True
            )
        
        if item_data["consumable"]:

            players[user_id]["inventory"].remove(item)

            await interaction.response.send_message(
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
    description="Pick up an item from the room you are in."
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
        
        allowed_channel = interaction.guild.get_channel(
                allowed_channel_id
        )
        
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

        item_in_room = any(i["id"] == item for i in room_items[current_room])
        if not item_in_room:
            await interaction.response.send_message(
                "That item isn't here.",
                ephemeral=True
            )
            return

        user_nickname = players[user_id]["nickname"]

        await interaction.response.send_message(
            f"You picked up **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})**.",
            ephemeral=True
        )
        
        if item in room_items[current_room]:
        
            room_items[current_room] = [i for i in room_items[current_room] if i["id"] != item]
            players[user_id]["inventory"].append(item)

            if allowed_channel:
                await allowed_channel.send(
                    f"{user_nickname} picked up a **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})** from the ground."
                )
        
        elif item in ROOMS[current_room]["take_items"]:

            players[user_id]["inventory"].append(item)
            if allowed_channel:
                await allowed_channel.send(
                    f"{user_nickname} grabbed a **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})** from the room."
                )

    @bot.tree.command(
    name="give",
    description="Give an item from your inventory to another player."
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

        players[user_id]["inventory"].remove(item)
        players[target_id]["inventory"].append(item)
        save_players()

        user_nickname = players[user_id]["nickname"]
        target_nickname = players[target_id]["nickname"]
        item_name = ITEMS[item]["name"]
        
        await interaction.response.send_message(
            f"You gave **{item_name} ({ITEMS[item]['emoji']})** to {target_nickname}.",
            ephemeral=True
        )

    @bot.tree.command(
    name="inspect",
    description="Read the description of an item in your inventory."
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




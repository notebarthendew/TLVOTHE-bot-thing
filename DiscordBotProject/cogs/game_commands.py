import random

from discord import app_commands
import discord

from game.player import players, create_player, save_players
from game.movement import move_player
from game.items import ITEMS
from utils.constants import ADMIN_ROLE_ID
from utils.constants import GAME_ROLE_ID
from utils.constants import DEAD_ROLE_ID
from utils.helpers import check_player_status
from game.map import ROOMS


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
                f"Corpses here:\n"
                f"{corpses_text}\n\n"
            )
        else:
            corpse_section = ""
        
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
            f"{look_message}\n"
            f"{description}\n\n"
            f"People here:\n{people_text}\n\n"
            f"{corpse_section}"
            f"Exits:\n{exits_text}",
            ephemeral=True
        )
        

    @bot.tree.command(
        name="kill",
        description="Kill a player"
    )
    @app_commands.describe(target="The player to kill")
    async def kill(
        interaction: discord.Interaction,
        target: discord.Member
    ):
        user_id = str(interaction.user.id)
        target_id = str(target.id)

        error = check_player_status(user_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        error = check_player_status(target_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        allowed_channel_id = ROOMS[current_room]["command_channel_id"]

        if interaction.channel.id != allowed_channel_id:

            await interaction.response.send_message(
            f"You can only do that from the room you're currently in. (Use the command in the {current_room} channel)",
            ephemeral=True
        )
        
        if players[user_id]["room"] != players[target_id]["room"]:
            await interaction.response.send_message(
                 "That player is not in the same room as you.",
                ephemeral=True
            )
            return

        players[target_id]["alive"] = False
        save_players()

        dead_role = interaction.guild.get_role(DEAD_ROLE_ID)
        game_role = interaction.guild.get_role(GAME_ROLE_ID)

        await target.remove_roles(game_role)
        await target.add_roles(dead_role)

        target_nickname = players[target_id]["nickname"]
        killer_nickname = players[user_id]["nickname"]

        current_room = players[user_id]["room"]
        room_channel = interaction.guild.get_channel(ROOMS[current_room]["channel_id"])

        await interaction.response.send_message(
            f"*{killer_nickname} lunges out to {target_nickname}, they fight against them, but suddenly; {target_nickname} collapses to the floor.*"
        )
        await room_channel.send(
            f"*{target_nickname} has died.*"
        )

    @bot.tree.command(name="inventory")
    async def inventory(interaction: discord.Interaction):

        user_id = str(interaction.user.id)

        error = check_player_status(user_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        player_inventory = players[user_id]["inventory"]
        
        if player_inventory:
            inventory_text = "\n".join(
                f"- {ITEMS[item]['name']}"
                for item in player_inventory
            )
        else:
            inventory_text = "- Nothing (So much for a high-profile character, smh)"

        await interaction.response.send_message(
            "You scramble through your pockets, and you find:\n\n"
            f"{inventory_text}",
            ephemeral=True
        )

    @bot.tree.command(name="use")

    @app_commands.autocomplete(
        item=inventory_item_autocomplete
    )

    async def use(
        interaction: discord.Interaction,
        item: str,
        target: discord.Member = None
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

        item_data = ITEMS[item]

        if item not in ITEMS:

            await interaction.response.send_message(
                "That item no longer exists.",
                ephemeral=True
            )

            return
        
        target_type = item_data["target_type"]
        
        if not item_data["usable"]:

            await interaction.response.send_message(
                "That item cannot be used.",
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

            target_id = str(target.id)
            
            if target_id not in players:

                await interaction.response.send_message(
                    "That player is not in the game.",
                    ephemeral=True
                )

                return

            target_nickname = players[target_id]["nickname"]
            user_nickname = players[user_id]["nickname"]
            
            if players[target_id]["room"] != players[user_id]["room"]:

                await interaction.response.send_message(
                    "They are not in this room.",
                    ephemeral=True
                )

                return

            if not players[target_id]["alive"]:

                await interaction.response.send_message(
                    "That player is already dead.",
                    ephemeral=True
                )

                return
            
            if item == "knife":

                players[target_id]["alive"] = False

                save_players()

                if target_id == user_id:
                    await interaction.response.send_message(
                        f"{user_nickname} stabbed themselves. (what a way to go out vro)"
                    )
                    return
                
                else:
                    await interaction.response.send_message(
                        f"{target_nickname} got fuckign stabbed to death by {user_nickname}. (l bozo vro got killed)"
                    )
                    return
        
        if target_type == "none":
        
            await interaction.response.send_message(
                item_data["text"],
                ephemeral=True
            )
        
        if item_data["consumable"]:

            players[user_id]["inventory"].remove(item)

            save_players()
    
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

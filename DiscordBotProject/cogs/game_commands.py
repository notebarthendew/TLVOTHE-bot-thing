import random

from discord import app_commands
import discord

from game.player import players, create_player
from game.movement import move_player
from utils.constants import ADMIN_ROLE_ID
from utils.constants import GAME_ROLE_ID
from game.map import ROOMS


def setup_commands(bot):

    # --- PLAYER STUFF ----
    
    @bot.tree.command(
        name="add",
        description="Add a player to the game"
    )

    @app_commands.describe(
        member="The player to add"
    )

    async def add(
        interaction: discord.Interaction,
        member: discord.Member,
        nickname: str
    ):

        # Check admin role
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:

            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return

        user_id = str(member.id)

        # Already in game
        if user_id in players:

            await interaction.response.send_message(
                f"{member.mention} is already in the game.",
                ephemeral=True
            )

            return

        # Create player
        print("ADD COMMAND REACHED")
        create_player(user_id, nickname)

        # Give game role
        game_role = interaction.guild.get_role(
            GAME_ROLE_ID
        )

        await member.add_roles(game_role)

        await interaction.response.send_message(
            f"{member.mention} joined the game.",
            ephemeral=True
        )

    # --- PLAYER ACTIONS ---

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

        nickname = players[user_id]["nickname"]
        
        if user_id not in players:

            await interaction.response.send_message(
                "*You are not in a train vrotato.*",
                ephemeral=True
            )

            return

        current_room = players[user_id]["room"]

        allowed_channel_id = ROOMS[current_room]["command_channel_id"]

        if interaction.channel.id != allowed_channel_id:

            await interaction.response.send_message(
            f"You can only move from the room you're currently in. (Use the command in the {current_room} channel)",
            ephemeral=True
        )

            return
        
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
    
    
    @bot.tree.command(
    name="look",
    description="👀"
    )
    
    async def look(interaction: discord.Interaction):

        user_id = str(interaction.user.id)
        
        if user_id not in players:

            await interaction.response.send_message(
                "*You look around to see that you are not in a train*. **(Not in game)**",
                ephemeral=True
            )

            return

        current_room = players[user_id]["room"]
        room_data = ROOMS[current_room]

        front_room = room_data["front"]
        back_room = room_data["back"]
        
        people_in_room = []

        for player_id, player_data in players.items():

            if player_id == user_id:
                continue
            
            if player_data["room"] == current_room:

                people_in_room.append(
                    player_data["nickname"]
                )

        if not people_in_room:
            people_text = "- Nobody"
        else:
            people_text = "\n".join(
                f"- {person}"
                for person in people_in_room
            )

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
            f"You survey your surroundings in cabin {current_room}."
        ]

        look_message = random.choice(look_messages)
        
        await interaction.response.send_message(
            f"{look_message}\n\n"
            f"People here:\n{people_text}\n\n"
            f"Exits:\n{exits_text}",
            ephemeral=True
        )
        
    
    # ---- DEBBUGING COMMANdS ----
    @bot.tree.command(name="myroom")
    async def myroom(interaction: discord.Interaction):

        user_id = str(interaction.user.id)

        if user_id not in players:

            await interaction.response.send_message(
                "*You don't have a room*. **(Not in game)**",
                ephemeral=True
            )

            return
    
        await interaction.response.send_message(
            players[user_id]["room"],
            ephemeral=True
    )

    @bot.tree.command(name="checkplayers")
    async def checkplayers(interaction: discord.Interaction):

        has_admin_role = any(
                role.id == ADMIN_ROLE_ID
                for role in interaction.user.roles
            )

        if not has_admin_role:

            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return
        
        await interaction.response.send_message(
            f"```py\n{players}\n```",
            ephemeral=True
        )

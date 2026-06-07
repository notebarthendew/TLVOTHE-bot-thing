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

        if user_id not in players:

            await interaction.response.send_message(
                "*You are not in a train vrotato.*",
                ephemeral=True
            )

            return

        result = move_player(
            players[user_id],
            direction.value
        )

        if result is None:

            await interaction.response.send_message(
                "*You confidently walk into a wall*.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            f"*You moved to {result}.*",
            ephemeral=True
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
        
        await interaction.response.send_message(
            f"You see yourself standing in the {players[user_id]['room']} cabin.\n\n"
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

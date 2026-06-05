from discord import app_commands
import discord

from game.player import players, create_player
from game.movement import move_player
from utils.constants import ADMIN_ROLE_ID
from utils.constants import GAME_ROLE_ID


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
        member: discord.Member
        nickname: str
    ):

        # Check admin role
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:

            await interaction.response.send_message(
                "You can't do that.",
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
        create_player(user_id)

        # Give game role
        game_role = interaction.guild.get_role(
            GAME_ROLE_ID
        )

        await member.add_roles(game_role)

        await interaction.response.send_message(
            f"{member.mention} joined the game.",
            ephemeral=True
        )

    # --- MOVEMENT STUFF ---

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
                "*You are unable to move that way... crud...*.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            f"*You moved to {result}.*",
            ephemeral=True
        )

    # ---- DEBBUGING COMMANdS ----
    @bot.tree.command(name="myroom")
    async def myroom(interaction: discord.Interaction):

        user_id = str(interaction.user.id)

        if user_id not in players:

            await interaction.response.send_message(
                "Not in game.",
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
                    "You can't do that.",
                    ephemeral=True
                )
        
        await interaction.response.send_message(
            f"```py\n{players}\n```",
            ephemeral=True
        )

from discord import app_commands
import discord

from game.player import players, create_player

ADMIN_ROLE_ID = 1443308083475386370 # "Announcer" role
GAME_ROLE_ID = 1441798643576471773 # "Passenger" role


def setup_commands(bot):

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

    @bot.tree.command(name="checkplayers")
    async def checkplayers(interaction: discord.Interaction):

        await interaction.response.send_message(
            str(players),
            ephemeral=True
        )

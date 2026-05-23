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

    @bot.command()
    async def add(ctx, user_id=None):

        ADMIN_ROLE_ID = 1443308083475386370
        GAME_ROLE_ID = 1441798643576471773

        # Check admin role
        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in ctx.author.roles
        )

        if not has_admin_role:

            await ctx.send(
                "You can't do that."
            )

            return

        # No ID provided
        if user_id is None:

            await ctx.send(
                "You need to provide a user ID."
            )

            return

        # Invalid ID
        try:
            user_id = int(user_id)

        except ValueError:

            await ctx.send(
            "That is not a valid user ID."
            )

            return

        # Try to find member
        member = ctx.guild.get_member(user_id)

        if member is None:

            await ctx.send(
                "Could not find that user."
            )

            return

        # Get game role
        game_role = ctx.guild.get_role(
            GAME_ROLE_ID
        )

        if game_role is None:

            await ctx.send(
                "Game role not found."
        )

            return

        # Give role
        await member.add_roles(game_role)

        await ctx.send(
            f"{member.mention} was added to the game."
        )

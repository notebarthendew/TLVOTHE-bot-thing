# FEAR ME
from discord import app_commands
import discord

from game.player import players, create_player
from utils.constants import ADMIN_ROLE_ID
from utils.constants import GAME_ROLE_ID
from game.map import ROOMS


def setup_commands(bot):

    # --- PLAYER STUFF ----

    async def room_autocomplete(
        interaction,
        current: str
    ):
        return [
            app_commands.Choice(
                name=f"Room {room_id}",
                value=room_id
            )
            for room_id in ROOMS.keys()
            if current.lower() in room_id.lower()
        ][:25]

    
    @bot.tree.command(
        name="add",
        description="Add a player to the game"
    )

    @app_commands.describe(
        member="The player to add"
    )

    @app_commands.autocomplete(
        spawn_room=room_autocomplete
    )

    async def add(
        interaction: discord.Interaction,
        member: discord.Member,
        nickname: str,
        spawn_room: str
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

        if spawn_room not in ROOMS:

            await interaction.response.send_message(
                "That room does not exist.",
                ephemeral=True
            )

            return
        
        # Create player
        print("ADD COMMAND REACHED")
        create_player(user_id, nickname, spawn_room)

        # Give game role
        game_role = interaction.guild.get_role(
            GAME_ROLE_ID
        )

        await member.add_roles(game_role)

        spawn_channel = interaction.guild.get_channel(
            ROOMS[spawn_room]["channel_id"]
        )

        await spawn_channel.set_permissions(
            member,
            view_channel=True
        )

        await interaction.response.send_message(
            f"{member.mention} joined the game in room {spawn_room}.",
            ephemeral=True
        )
    

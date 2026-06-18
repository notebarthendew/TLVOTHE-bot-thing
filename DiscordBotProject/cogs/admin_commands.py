# FEAR ME
from discord import app_commands
import discord

from game.player import players, create_player, remove_player
from game.items import ITEMS
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

    async def item_autocomplete(
        interaction,
        current: str
    ):
        return [
            app_commands.Choice(
                name=data["name"],
                value=item_id
            )
            for item_id, data in ITEMS.items()
            if (
                current.lower() in item_id.lower() 
                or
                current.lower() in data["name"].lower()
            )
            
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

    @bot.tree.command(
        name="remove",
        description="Remove a player from the game (aka admin /kill)"
    )

    @app_commands.describe(
        member="The player to remove"
    )

    async def remove(
        interaction: discord.Interaction,
        member: discord.Member,
    ):

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

        if user_id not in players:

            await interaction.response.send_message(
                "That player is not in the game.",
                ephemeral=True
            )

            return

        for room_data in ROOMS.values():

            channel = interaction.guild.get_channel(
                room_data["channel_id"]
            )

            if channel is not None:

                await channel.set_permissions(
                    member,
                    overwrite=None
                )

        game_role = interaction.guild.get_role(
            GAME_ROLE_ID
        )

        if game_role is not None:
            await member.remove_roles(game_role)

        remove_player(user_id)
        
        await interaction.response.send_message(
            f"{member.mention} was removed from the game.",
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

    @bot.tree.command(name="itemgive")

    @app_commands.describe(
        member="(ADMIN) Give a player an item."
    )

    @app_commands.autocomplete(
        item=item_autocomplete
    )
    
    async def itemgive(
        interaction: discord.Interaction,
        member: discord.Member,
        item: str
    ):

        
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

        if user_id not in players:

            await interaction.response.send_message(
                f"{member.mention} is not in the game..",
                ephemeral=True
            )

            return

        if item not in ITEMS:

            await interaction.response.send_message(
                "That item does not exist.",
                ephemeral=True
            )

            return

        players[user_id]["inventory"].append(item)

        save_players()

        await interaction.response.send_message(
            f"Gave **{ITEMS[item]['name']}** to {member.mention}.",
            ephemeral=True
        )
        

# FEAR ME
from discord import app_commands
import discord

import random
import asyncio

from game.player import players, create_player, remove_player, save_players
from game.items import ITEMS
from utils.constants import ADMIN_ROLE_ID
from utils.constants import GAME_ROLE_ID
from utils.constants import DEAD_ROLE_ID
from utils.helpers import check_player_status
from game.map import ROOMS
from game.room_items import room_items


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

    async def role_autocomplete(
        interaction,
        current: str
    ):
        return [
            app_commands.Choice(
                name=f"Passenger",
                value="passenger"
            ),

            app_commands.Choice(
                name=f"Vigilante",
                value="vigilante"
            ),

            app_commands.Choice(
                name=f"Murderer",
                value="murderer"
            ),

            app_commands.Choice(
                name=f"None",
                value="none"
            )

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

    async def player_nickname_autocomplete(
        interaction,
        current: str
    ):
        return [
            app_commands.Choice(
                name=pdata["nickname"],
                value=pid
            )
            for pid, pdata in players.items()
            if current.lower() in pdata["nickname"].lower()
        ][:25]

    async def room_player_autocomplete(interaction, current: str):
        user_id = str(interaction.user.id)
        
        if user_id not in players:
            return []

        current_room = players[user_id]["room"]
        
        return [
            app_commands.Choice(
                name=players[pid]["nickname"],
                value=pid
            )
            for pid, pdata in players.items()
            if pid != user_id and pdata["room"] == current_room
            and current.lower() in pdata["nickname"].lower()
        ][:25]

    @bot.tree.command(
        name="startgame",
        description="(ADMIN) Starts a game of TLVOTHE."
    )

    async def startgame(interaction: discord.Interaction):

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

        await interaction.response.defer(ephemeral=True)

        alive_players = [
            pid for pid in players
            if players[pid]["alive"]
        ]

        role_pool = alive_players.copy()

        if len(alive_players) < 5:
            await interaction.edit_original_response(
                content="You need at least 5 players."
            )
            return

        random.shuffle(role_pool)

        murderers = [
            role_pool.pop(),
            role_pool.pop()
        ]

        vigilantes = [
            role_pool.pop(),
            role_pool.pop(),
            role_pool.pop()
        ]

        for pid in role_pool:
            players[pid]["role"] = "passenger"

        for pid in murderers:
            players[pid]["role"] = "murderer"

        for pid in vigilantes:
            players[pid]["role"] = "vigilante"

        for pid in alive_players:

            role = players[pid]["role"]

            if role == "murderer":
                players[pid]["inventory"] = ["keys"]

            elif role == "vigilante":
                players[pid]["inventory"] = ["keys", "gun"]

            else:
                players[pid]["inventory"] = ["keys"]


        SPAWN_ROOMS = [
            "front",
            "cafeteria",
            "library",
            "infirmary",
            "front_dorm",
            "mid_dorm",
            "back_dorm",
        ]

        for pid in alive_players:

            spawn_room = random.choice(SPAWN_ROOMS)

            role = players[pid]["role"]

            players[pid]["room"] = spawn_room

            member = interaction.guild.get_member(int(pid))

            lobby_channel = interaction.guild.get_channel(
                ROOMS["train_dock"]["channel_id"]
            )

            if lobby_channel is None:
                lobby_channel = interaction.guild.get_thread(
                    ROOMS["train_dock"]["channel_id"]
                )

            spawn_channel = interaction.guild.get_channel(
                ROOMS[spawn_room]["channel_id"]
            )

            if spawn_channel is None:
                spawn_channel = interaction.guild.get_thread(
                    ROOMS[spawn_room]["channel_id"]
                )

            if lobby_channel is not None:
                await lobby_channel.set_permissions(
                    member,
                    view_channel=False
                )

            # Show their spawn room
            if spawn_channel is not None:
                await spawn_channel.set_permissions(
                    member,
                    view_channel=True
                )

            save_players()

            ROLE_OBJECTIVES = {

                "murderer":
                    "Eliminate all passengers along your with Co-hort before time runs out.",

                "vigilante":
                    "Eliminate any murderers and protect the passengers.",

                "passenger":
                    "Stay safe and survive till the end of the ride.",

                "bodyguard":
                    "Protect your assigned passenger at all costs.",

                "detective":
                    "Use your clues to uncover the murderer's identity."

            }

            print(f"Sending DM to {member} ({pid})")
            print(member)
            print(member.guild.name)


            try:
                await member.send(
                    f"""# Welcome aboard, **{role.upper()}!**

            -.-.-.-.-.-.-.-.-.-

            There are 2 killers aboard the train.

            {ROLE_OBJECTIVES[role]}
            """
                )
                print(f"DM sent to {member}")

            except Exception as e:
                print(f"Couldn't DM {member}: {e}")

        await interaction.edit_original_response(
            content="Game started!"
        )

    @bot.tree.command(
        name="info",
        description="(ADMIN) View all player information."
    )
    async def info(interaction: discord.Interaction):

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

        pages = []
        current = "# Player Information\n\n"

        for pid, pdata in players.items():

            member = interaction.guild.get_member(int(pid))

            username = member.name if member else "Unknown"

            line = (
                f"**{pdata['nickname']}** "
                f"({username})\n"
                f"ID: `{pid}` | "
                f"{'🟢' if pdata['alive'] else '🔴'} | "
                f"**{pdata['role'] or 'None'}** | "
                f"📍 {pdata['room']} | "
                f"🎒 {', '.join(pdata['inventory']) if pdata['inventory'] else 'Empty'}\n\n"
            )

            if len(current) + len(line) > 1900:
                pages.append(current)
                current = ""

            current += line

        if current:
            pages.append(current)

        await interaction.response.send_message(
            pages[0],
            ephemeral=True
        )

        for page in pages[1:]:
            await interaction.followup.send(
                page,
                ephemeral=True
            )

    @bot.tree.command(
        name="say",
        description="(snowy dodo only hah) Make the bot say something."
    )

    async def say(
            interaction: discord.Interaction,
            message: str
    ):

        if interaction.user.id != 1087129816416919613:
            await interaction.response.send_message(
                "You can't do that, silly.",
                ephemeral=True
            )

            return

        await interaction.response.defer(ephemeral=True)

        typing_time = min(
            random.uniform(0.5, 1.2) + len(message) * random.uniform(0.02, 0.05),
            8
        )

        async with interaction.channel.typing():
            await asyncio.sleep(typing_time)

        await interaction.channel.send(message)

        await interaction.followup.send(
            "Sent.",
            ephemeral=True
        )

    @bot.tree.command(
        name="add",
        description="(ADMIN) Add a player to the game"
    )

    @app_commands.describe(
        member="The player to add"
    )

    @app_commands.autocomplete(
        role=role_autocomplete,
        spawn_room=room_autocomplete
    )

    async def add(
        interaction: discord.Interaction,
        member: discord.Member,
        nickname: str,
        role: str,
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
        create_player(user_id, nickname, role, spawn_room)

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
        description="(ADMIN) Remove a player from the game"
    )

    @app_commands.describe(
        member="The player to remove"
    )

    async def remove(
        interaction: discord.Interaction,
        member: discord.Member,
    ):

        await interaction.response.defer(ephemeral=True)

        has_admin_role = any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )

        if not has_admin_role:
            await interaction.edit_original_response(
                content="You cant do that silly."
            )

            return
            
        user_id = str(member.id)

        if user_id not in players:
            await interaction.edit_original_response(
                content="That player isn't in the game."
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

        await interaction.edit_original_response(
            content=f"{member.mention} was removed from the game."
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
        target="The player to give the item to"
    )

    @app_commands.autocomplete(
        item=item_autocomplete,
        target=player_nickname_autocomplete
    )
    
    async def itemgive(
        interaction: discord.Interaction,
        target: str,
        item: str
    ):

        print("ITEMGIVE REACHED")
        
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

        user_id = target

        if user_id not in players:

            await interaction.response.send_message(
                f"That player is not in the game.",
                ephemeral=True
            )

            return

        print(item)
        
        if item not in ITEMS:

            await interaction.response.send_message(
                "That item does not exist.",
                ephemeral=True
            )

            return

        players[user_id]["inventory"].append(item)

        target_nickname = players[user_id]["nickname"]
        await interaction.response.send_message(
            f"Gave **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})** to {target_nickname}.",
            ephemeral=True
        )

    @bot.tree.command(
    name="kill",
    description="(ADMIN) Kill a player"
    )
    @app_commands.describe(target="The player to kill")
    @app_commands.autocomplete(
        target=player_nickname_autocomplete
    )
    async def kill(
        interaction: discord.Interaction,
        target: str
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
        
        target_id = target

        if target_id not in players:

            await interaction.response.send_message(
                "That player is not in the game.",
                ephemeral=True
            )

            return

        players[target_id]["alive"] = False
        save_players()

        dead_role = interaction.guild.get_role(DEAD_ROLE_ID)
        game_role = interaction.guild.get_role(GAME_ROLE_ID)

        # Get the Discord member to update roles
        target_member = interaction.guild.get_member(int(target_id))
        if target_member:
            await target_member.remove_roles(game_role)
            await target_member.add_roles(dead_role)

        target_nickname = players[target_id]["nickname"]

        current_room = players[target_id]["room"]
        room_channel = interaction.guild.get_channel(ROOMS[current_room]["channel_id"])

        await interaction.response.send_message(
            f"*{target_nickname} has been killed.*",
            ephemeral=True
        )
        await room_channel.send(
            f"*{target_nickname} has died.*"
        )

    @bot.tree.command(name="itemspawn")

    @app_commands.describe(
        item="(ADMIN) Spawn an item on a room."
    )

    @app_commands.autocomplete(
        item=item_autocomplete,
        room=room_autocomplete
    )
    
    async def itemspawn(
        interaction: discord.Interaction,
        item: str,
        room: str
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
        
        if room not in ROOMS:

            await interaction.response.send_message(
                "That room does not exist.",
                ephemeral=True
            )

            return

        if item not in ITEMS:

            await interaction.response.send_message(
                "That item does not exist.",
                ephemeral=True
            )

            return
        
        room_items[room].append({
            "id": item
        })

        await interaction.response.send_message(
            f"Spawned **{ITEMS[item]['name']} ({ITEMS[item]['emoji']})** in room {room}.",
            ephemeral=True
        )

        return


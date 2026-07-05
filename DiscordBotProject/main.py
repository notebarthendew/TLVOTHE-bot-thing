# yall, i know this may look like crap, but this is my first bot so please

import random

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import tasks
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)

from game.player import load_players
from cogs.commands import setup_commands as setup_slash_commands
from cogs.prefix_commands import setup_commands as setup_prefix_commands
from cogs.game_commands import setup_commands as setup_game_commands
from cogs.message_commands import setup_commands as setup_message_events
from cogs.admin_commands import setup_commands as setup_admin_commands

setup_slash_commands(bot)
setup_prefix_commands(bot)
setup_game_commands(bot)
setup_message_events(bot)
setup_admin_commands(bot)

STATUSES = [
    # Normal
    "Boarding passengers...",
    "Punching tickets...",
    "Waiting at the station...",
    "Polishing the silverware...",
    "Brewing coffee...",
    "Watching the scenery...",
    "Preparing dinner...",
    "Looking for clues...",

    # Murderer-ish
    "Hiding a knife...",
    "Cleaning blood off the floor...",
    "Staging an accident...",
    "Buying poison...",
    "Following someone...",
    "Hearing footsteps...",
    "Waiting for the lights to go out...",
    "Counting coins...",
    "Making up an alibi...",

    # Funny
    "Definitely not the murderer.",
    "Pretending to be innocent.",
    "Gaslighting the passengers.",
    "Making the evidence disappear.",
    "Bribing the conductor.",
    "Doing totally legal activities.",
    "Absolutely nothing suspicious.",
    "Ignoring the screaming.",
    "everyones dead.",
    "ALIENS ARE REAL!...",
    "AND THEY LIKE TO KILL!", 
    "Why is there blood outside of medbay?" # the 3 of these are amongus show refs
    "Don't trust Cabin 6.",

    # Meta
    "Testing the train brakes...",
    "Syncing slash commands...",
    "Waiting for someone to type /look...",
    "Reading the documentation...",
    "Being hosted on Railway.",
    "Wondering where Fork went.",
    "Debugging another murder."
    "Conducting the Harpy Express...",
    "Keeping the train on the tracks...",
    "Please mind the gap.",
    "Next stop: Nowhere.",
    "Enjoy your stay aboard.",
    "Serving suspiciously good soup...",
    "Today's forecast: Murder.",
]

@tasks.loop(minutes=3)
async def rotate_status():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(random.choice(STATUSES))
    )

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}, {bot.user.id}')
    print("im so fukig evil muehehehe")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Poisoning the food...")
    )

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(random.choice(STATUSES))
    )

    if not rotate_status.is_running():
        rotate_status.start()

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        try:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(
                    "Hello! Thank you for inviting me to your server!.\n"
                    "...Although I should be somewhere else...."
                )
                break

        except discord.Forbidden:
            pass

        except discord.HTTPException as e:
            print(f"Failed to send join message: {e}")

load_players()

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    import traceback

    print("\n--- APP COMMAND ERROR ---")

    traceback.print_exception(
        type(error),
        error,
        error.__traceback__
    )

    print("-------------------------\n")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

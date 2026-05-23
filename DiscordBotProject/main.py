import discord
from discord.ext import commands
from discord import app_commands
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

from cogs.commands import setup_commands as setup_slash_commands
from cogs.prefix_commands import setup_commands as setup_prefix_commands
from cogs.game_commands import setup_commands as setup_game_commands

setup_slash_commands(bot)
setup_prefix_commands(bot)
setup_game_commands(bot)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("haha pepee popoo whoah hehehe")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Poisoning the food...")
    )

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                "Hello! Thank you for inviting me to your server!.\n"
                "...Although I should be somewhere else...."
            )
            break

@bot.event
async def on_member_join(member):
    await member.send("hello hi welcome how are you this is a test but yeah")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "hello gm" in message.content.lower():
        await message.channel.send(f"yo whatup {message.author.mention}")

    if "gm sucks" in message.content.lower():
        await message.channel.send(f"you aint getting in blud")

    if "fuck" in message.content.lower():
        await message.channel.send("https://tenor.com/view/ui-mama-anime-bozo-settle-down-bozo-ui-bozo-anime-gif-16754421357059991258")

    if "omg gm is so handsome" in message.content.lower():
        await message.channel.send("https://tenor.com/view/at-ease-ladies-dr-umar-calm-down-relax-chill-take-it-easy-gif-15917197958281975855")

    if "help" in message.content.lower():
        await message.channel.send("-# *NO ONE IS AROUND TO HELP YOU.*")

    await bot.process_commands(message)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)

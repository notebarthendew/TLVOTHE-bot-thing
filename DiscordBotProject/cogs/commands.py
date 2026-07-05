from discord import app_commands
import discord

import random
import asyncio

def setup_commands(bot):

  @bot.tree.command(name="ping")
  async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

  @bot.tree.command(name="d20roll")
  async def d20roll(interaction: discord.Interaction):
    roll = random.randint(1, 20)
    await interaction.response.send_message("You rolled...")
    await asyncio.sleep(3)
    await interaction.followup.send(f"{roll}.")
  
  @bot.tree.command(name="commands")
  async def commands(interaction: discord.Interaction):
    await interaction.response.send_message(" # TVLOTHE BOT COMMANDS\n"
                                            "## Slash Commands\n"
                                            "* '/ping' Send pong.\n"
                                            "* '/d20roll' Roll a dice of 20 sides.\n"
                                            "## Prefix Commands\n"
                                            "* '?hello' Say hi and ping the caller\n"
                                            "* '?reply' Send a discord reply to the caller\n"
                                            "* '?cheese' Send a cheese gif (not random)\n"
                                            "* '?revolver' Send a Revolver (<:Revolver:1505709394057494659>) emoji",
                                            ephemeral=True
                                            )

  @bot.tree.command(name="game_commands")
  async def game_commands(interaction: discord.Interaction):
    await interaction.response.send_message(" # TVLOTHE BOT *GAME* COMMANDS\n"
                                            "*You are able to use these commands if you are in the game.*"
                                            "## Actions\n"
                                            "* '/move' Move around the train, only able to move linearly (Front or Back)\n"
                                            "* '/look' Get information about the room you are currently in.\n"
                                            "* '/inventory' Look into the items you have in your inventory.\n"
                                            "* '/inspect' Look into the items you have in your inventory.\n"
                                            "* '/use' Use any item inside of your inventory.\n"
                                            "* '/give' Silently give an item to another person.\n"
                                            "* '/take' Take an item from the current room.\n"
                                            "*This will be regularly updated until all planned actions are implemented.*",
                                            ephemeral=True
                                            )
    


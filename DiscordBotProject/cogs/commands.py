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
                                            "## Prefix Commands\n"
                                            "* '?hello' Say hi and ping the caller\n",
                                            "* '?reply' Send a discord reply to the caller\n"
                                            "* '?cheese' Send a cheese gif (not random)\n"
                                            "* '?revolver' Send a Revolver (<:Revolver:1505709394057494659>) emoji",
                                            ephimeral=True
                                            )

  @bot.tree.command(name="game_commands")
  async def game_commands(interaction: discord.Interaction):
    await interaction.response.send_message(" # TVLOTHE BOT *GAME* COMMANDS\n"
                                            "*You are able to use these commands if you are in the game.*"
                                            "## Actions\n"
                                            "* '/move' Move around the train, only able to move linearly (Front or Back)\n"
                                            "* '/look' Get information about the room you are currently in.\n"
                                            "* '/kill' Kill a player. This is a debug command to test the dead people system.\n"
                                            "*This will be regularly updated until all planned actions are implemented.*",
                                            ephimeral=True
                                            )
    


from discord import app_commands
import discord

def setup_commands(bot):

  @bot.tree.command(name="ping")
  async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

  @bot.tree.command(name="commands")
  async def commands(interaction: discord.Interaction):
    await interaction.response.send_message(" # TVLOTHE BOT COMMANDS\n"
                                            "## Slash Commands\n"
                                            "* '/ping' Send pong.\n"
                                            "## Prefix Commands\n"
                                            "* '?hello' Say hi and ping the caller\n"
                                            "* '?reply' Send a discord reply to the caller\n"
                                            "* '?cheese' Send a cheese gif (not random)\n"
                                            "* '?revolver' Send a Revolver (<:Revolver:1505709394057494659>) emoji"
                                            )
    print("Sent 'commands' slash command")

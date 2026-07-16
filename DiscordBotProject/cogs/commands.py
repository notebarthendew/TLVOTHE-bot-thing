from discord import app_commands
import discord

import time
import random
import asyncio

def setup_commands(bot):

  START_TIME = time.time()

  @bot.tree.command(name="ping")
  async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

  @bot.tree.command(name="d20roll")
  async def d20roll(interaction: discord.Interaction):
    roll = random.randint(1, 20)
    await interaction.response.send_message(f"{interaction.user} throws a die on the floor...")
    await asyncio.sleep(3)
    await interaction.followup.send(f"And rolls a {roll}.")

  @bot.tree.command(name="trainfact")
  async def trainfact(interaction: discord.Interaction):
      FACTS = [
          "The first underground railway opened in London in 1863.",
          "High-speed rail lines are built with gentle curves because trains cannot turn sharply at high speeds.",
          "Some modern locomotives can produce over 6,000 horsepower.",
          "Air brakes, invented by George Westinghouse, made trains much safer in the late 1800s.",
          "Most railroad crossings use lights, bells, or gates to warn drivers of approaching trains.",
          "Passenger trains often have 'dead man's switches' or vigilance systems that stop the train if the operator becomes unresponsive.",
          "Steel railroad rails are slightly tilted inward to reduce wear on train wheels.",
          "The longest railway tunnel in the world is the Gotthard Base Tunnel in Switzerland, stretching over 57 kilometers.",
          "Many railways use crushed stone called ballast beneath the tracks to keep them stable and improve drainage.",
          "Trains are one of the most energy-efficient ways to transport large numbers of passengers and cargo.",
          "The standard railway gauge used by most of the world is 1,435 mm (4 ft 8½ in).",
          "Japan's Shinkansen bullet trains have operated since 1964.",
          "Maglev trains float above the track using magnetic levitation instead of wheels.",
          "The world's fastest maglev train has exceeded 600 km/h (373 mph) during testing.",
          "Steam locomotives burn fuel to heat water, creating steam that drives pistons.",
          "Train wheels are made of steel because steel-on-steel creates very little rolling resistance.",
          "Railway signals were originally operated entirely by hand before becoming automated.",
          "Many modern passenger trains use electric motors instead of diesel engines.",
          "Freight trains are generally much longer and heavier than passenger trains.",
          "Railroad tracks expand in hot weather, which is why engineers leave small expansion gaps.",
          "The first public railway opened in 1825.",
          "Steam locomotives can weigh over 100 tons.",
          "Some freight trains are over 3 kilometers long.",
          "A train horn can exceed 110 dB.",
          "Steam locomotives run by boiling water into high-pressure steam.",
          "Railroad tracks are slightly wider than most people think: 1,435 mm apart.",
          "The world's longest railway is the Trans-Siberian Railway.",
          "Train wheels are slightly conical, helping trains stay centered on the rails.",
          "Early railways were originally built to transport coal.",
          "Modern locomotives can produce over 4,000 horsepower.",
          "The Harpy Express definitely has no murderers aboard.",
          "Every Harpy Express ticket comes with complimentary paranoia.",
          "The conductor has never once blinked. This is perfectly normal.",
          "Nobody has ever successfully outrun a train. Don't try it.",
          "The dining carriage's soup has been rated 'acceptable' three years in a row.",
          "If you hear screaming, it is probably unrelated to your journey.",
          "Passengers are reminded that murder is discouraged.",
          "The Harpy Express has never been delayed by ghosts. Officially.",
          "One passenger once tried to pay for a ticket using potatoes.",
          "Someone forgot where they parked the train once.",
          "The luggage compartment has won three hide-and-seek championships.",
          "Not every mysterious stain is blood.",
          "Most mysterious stains are probably tea.",
          "The train is legally considered faster than walking.",
          "The engineer insists every weird noise is intentional.",
          "Steam whistles were originally used to warn people near the tracks.",
          "The Harpy Express whistle scares away at least two birds every morning.",
          "The average passenger asks where the bathroom is within 17 minutes.",
          "Railway workers used pocket watches to keep schedules synchronized.",
          "Coal dust gets everywhere.",
          "Nobody actually knows who cleans the windows.",
          "The train contains at least one spider. Good luck finding it.",
          "One wheel squeaks slightly more than the others.",
          "A surprising amount of engineering goes into making trains stop.",
          "Trains can't swerve around obstacles.",
          "The Harpy Express can. It just chooses not to.",
          "Every ticket has exactly one ticket number.",
          "Some stations once had separate waiting rooms for different ticket classes.",
          "The Harpy Express gift shop sells absolutely nothing.",
          "Some passengers wave at cows. The cows rarely wave back.",
          "The station clock is almost always correct.",
          "Someone once tried to race the train on horseback. They lost.",
          "Every carriage has heard at least one terrible joke.",
          "The train's brass is polished more often than some passengers bathe.",
          "If you can smell coal, you're probably near the locomotive.",
          "Not all smoke means something is on fire.",
          "Unless it does.",
          "The Harpy Herald has never printed fake news. Probably.",
          "Every newspaper is printed fresh before departure.",
          "Some newspapers mysteriously disappear before anyone reads them.",
          "The Harpy Express employs at least one editor with terrible handwriting.",
          "Conductors carry hole punches for tickets.",
          "No one knows why ticket punches are so satisfying.",
          "Railway lanterns often used colored lenses to communicate signals.",
          "The Harpy Express occasionally runs exactly on schedule.",
          "Steam engines require regular maintenance to stay operational.",
          "The train's horn has frightened more sheep than passengers.",
          "Never lick the rails.",
          "Someone had to be told that rule.",
          "The average train ride contains at least one person looking dramatically out the window.",
          "Looking suspicious does not make you suspicious. Usually.",
          "Some people snore louder than the locomotive.",
          "The Harpy Express is powered by steam, steel, and questionable decisions.",
          "A good detective notices details.",
          "A great detective notices the soup.",
          "There is no treasure hidden beneath carriage 7.",
          "Ignore anyone who tells you otherwise.",
          "A train can take over a kilometer to stop at full speed.",
          "The Harpy Express insurance policy is surprisingly short.",
          "Someone once tried opening a door labeled 'Do Not Open.' It did not go well.",
          "The train has exactly the correct number of wheels.",
          "Nobody counted twice.",
          "The luggage knows where it's going. The passengers don't.",
          "Every mystery starts somewhere.",
          "Sometimes it starts in the dining carriage.",
          "If the lights flicker, remain calm.",
          "If they flicker twice... maybe don't.",
          "Some railway workers believed whistling at night brought bad luck.",
          "The Harpy Express has absolutely never derailed in the last five minutes.",
          "The safest place on the train is wherever the murderer isn't.",
          "There is a 97% chance this fact was completely made up.",
          "You have now spent several seconds reading train facts instead of surviving.",
          "The train appreciates your continued patronage."
      ]

      await interaction.response.send_message(
          f"## **Train Fact**\n-.-.-.-.-.-.-.-.-.-.-\n{random.choice(FACTS)}"
      )

  @bot.tree.command(name="coinflip")
  async def d20roll(interaction: discord.Interaction):
      options = ["Heads", "Tails", "on its edge"]
      result = random.choice(options)
      await interaction.response.send_message(f"{interaction.user} throws the coin in the air.")
      await asyncio.sleep(2)
      await interaction.followup.send("...")
      await asyncio.sleep(2)
      await interaction.followup.send(f"It landed {result}.")

  @bot.tree.command(name="sus")
  async def sus(interaction: discord.Interaction):
      await interaction.response.send_message(":face_with_raised_eyebrow:")

  @bot.tree.command(name="uptime")
  async def uptime(interaction: discord.Interaction):
      seconds = int(time.time() - START_TIME)

      days, seconds = divmod(seconds, 86400)
      hours, seconds = divmod(seconds, 3600)
      minutes, seconds = divmod(seconds, 60)

      await interaction.response.send_message(
          f"<:Keys:1453900262698651749> The Harpy Express has been running for:\n"
          f"**{days}d {hours}h {minutes}m {seconds}s**"
      )

  @bot.tree.command(name="commands")
  async def commands(interaction: discord.Interaction):
    await interaction.response.send_message(" # TVLOTHE BOT COMMANDS\n"
                                            "## Slash Commands\n"
                                            "* '/ping' Send pong.\n"
                                            "* '/d20roll' Roll a dice of 20 sides.\n"
                                            "* '/trainfact' Sends a random fact about trains.\n"
                                            "* '/coinflip' Simple and useful coinflip.\n"
                                            "* '/uptime' Show for how long the bot has been running.\n"
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
                                            "*You are able to use these commands if you are in the game.*\n"
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
    


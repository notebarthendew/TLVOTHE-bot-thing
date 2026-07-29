from discord import app_commands
import discord

import time
import random
import asyncio

def setup_commands(bot):

  START_TIME = time.time()

  async def roulette_number_autocomplete(interaction, current: str):
      return [
          app_commands.Choice(name=str(i), value=i)
          for i in range(37)
          if current in str(i)
      ][:25]

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

  @bot.tree.command(name="gamble", description="LET IT RIDE!")
  @app_commands.choices(color=[
      app_commands.Choice(name="Red", value="red"),
      app_commands.Choice(name="Black", value="black"),
      app_commands.Choice(name="Green", value="green")
  ])
  @app_commands.autocomplete(
      number=roulette_number_autocomplete
  )

  async def gamble(
          interaction: discord.Interaction,
          money: int,
          number: int | None = None,
          color: app_commands.Choice[str] | None = None,
          ):

      RED = {
          1, 3, 5, 7, 9,
          12, 14, 16, 18,
          19, 21, 23, 25, 27,
          30, 32, 34, 36
      }

      BLACK = {
          2, 4, 6, 8, 10,
          11, 13, 15, 17,
          20, 22, 24, 26, 28,
          29, 31, 33, 35
      }

      if number is None and color is None:
          await interaction.response.send_message(
              "You have to bet on either a number or a color.",
              ephemeral=True
          )
          return

      if number is not None:

          if number < 0 or number > 36:
              await interaction.response.send_message(
                  "That isn't a valid roulette number, choose between 0 and 36.",
                  ephemeral=True
              )
              return

          if color is not None:

              if number == 0 and color.value != "green":
                  await interaction.response.send_message(
                      "0 is always green.",
                      ephemeral=True
                  )
                  return

              if number in RED and color.value != "red":
                  await interaction.response.send_message(
                      f"{number} is red, not {color.value}.",
                      ephemeral=True
                  )
                  return

              if number in BLACK and color.value != "black":
                  await interaction.response.send_message(
                      f"{number} is black, not {color.value}.",
                      ephemeral=True
                  )
                  return

              if number is None and color is None:
                  await interaction.response.send_message(
                      "You have to bet on something.",
                      ephemeral=True
                  )
                  return

      if number is not None and color is not None:
          bet = f"{number} {color.value}"

      elif number is not None:
          bet = f"{number}"

      elif color is not None:
          bet = color.value

      if number == 17:

          await interaction.response.send_message(
              f"{interaction.user.mention}, **17 Black**!\n*The roulette starts to spin.*",
          )

          if random.random() < 0.80:
              result = 17
          else:
              result = random.choice(
                  [n for n in range(37) if n != 17]
              )

          await asyncio.sleep(1.5)

          await interaction.followup.send("LET IT RIDE!")

      else:
          result = random.randint(0, 36)
          await interaction.response.send_message(
              f"*{interaction.user.mention} bet {money}$ on **{bet}** and the roulette starts to spin.*",
          )

      if result == 0:
          result_color = "green"
      elif result in RED:
          result_color = "red"
      else:
          result_color = "black"

      won = False

      if number is not None:
          if result == number:
              won = True

      elif color is not None:
          if result_color == color.value:
              won = True

      await asyncio.sleep(4)

      if won:

          if number is not None:
              winnings = money * 36

          elif color is not None and color.value == "green":
              winnings = money * 36

          else:
              winnings = money * 2

          EXCUSES = [

              "Your mother insisted on holding onto your winnings for 'safe keeping.' Nobody has seen the money since.",

              "The conductor congratulates you before quietly pocketing the money.",

              "The cashier remembers they left the prize money in another carriage.",

              "Unfortunately, the railway's budget was spent replacing windows after... an incident.",

              "A seagull swooped in and stole your winnings. The staff applauds its precision.",

              "The accountant looked at the numbers, sighed, and walked out.",

              "The Harpy Express Gambling Commission has declared your victory 'financially inconvenient.'",

              "Your winnings were taxed at 100% for existing.",

              "The casino claims your chips were 'commemorative' and hold sentimental value instead.",

              "The dealer says you definitely won, but asks you to imagine receiving the money.",

              "The money was accidentally loaded onto another train.",

              "Your prize was converted into company shares. The company went bankrupt five seconds later.",

              "A passenger loudly claimed the winnings belonged to them. Nobody questioned it.",

              "The conductor spent your prize on more coal. The train thanks you for your contribution.",

              "The railway apologizes, but the vault is currently out of money.",

              "The wheel landed on your number, but the dealer insists everyone saw something else.",

              "A very official-looking gentleman stamped your winnings with 'DENIED.'",

              "Your prize has been donated to the 'Definitely Not Funding Murder' foundation.",

              "Someone replaced the cash with Monopoly money overnight.",

              "The train's financial department has been temporarily eaten by paperwork.",

              "The dealer flips the table over before anyone can pay you.",

              "You receive your winnings in exposure.",

              "The cashier says they'll pay you 'next round.'",

              "Your winnings have been successfully mailed to an unknown address.",

              "The railway invested your money into a revolutionary invisible locomotive.",

              "Your money was last seen rolling down the tracks.",

              "The conductor gives you a thumbs up instead of cash.",

              "The casino's wallet is currently on cooldown. You will get it later I'm sure!",

              "The dealer gives you a mysterious note simply reads: 'Nuh uh.'",

              "The dealer congratulates you, then immediately forgets who you are."

          ]

          await interaction.followup.send(
              f"*The wheel finally stopped spinning, and out came **{result} {result_color}**.*\n"
              f"## {interaction.user.mention} won {winnings}$!!!!!!!"
          )

          print(f"{interaction.user} won {winnings}")

          await asyncio.sleep(5)

          await interaction.followup.send(f"{random.choice(EXCUSES)}")



      else:
          await interaction.followup.send(
              f"*The wheel finally stopped spinning, and out came **{result} {result_color}**.*\n"
              f"## {interaction.user.mention} lost the only {money}$ on their bank account."
          )
          print(f"{interaction.user} lost {money}")

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
    


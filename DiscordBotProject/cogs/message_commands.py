from discord.ext import commands
import discord

class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
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

def setup_commands(bot):
    bot.add_cog(MessageEvents(bot))

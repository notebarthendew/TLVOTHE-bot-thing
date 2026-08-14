from discord.ext import commands

class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        print(f"{message.author}: {message.content}")


def setup_commands(bot):
    bot.add_listener(MessageCommands(bot).on_message)

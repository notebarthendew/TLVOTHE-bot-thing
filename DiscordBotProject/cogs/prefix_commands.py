from discord.ext import commands
import discord
from utils.constants import ADMIN_ROLE_ID

def setup_commands(bot):
    
    @bot.command()
    async def hello(ctx):
        await ctx.send(f"hi {ctx.author.mention}")
        print("Sent hello prefix command")

    @bot.command()
    async def reply(ctx):
        await ctx.reply("This is a reply. (wow)")
        print("Sent reply prefix command")
    
    @bot.command()
    async def cheese(ctx):
        await ctx.send("https://tenor.com/view/crowpunk-cheese-challenge-repost-to-cheese-cat-cheese-cat-gif-4123783956472567463")
        print("Sent cheese prefix command")

    @bot.command()
    async def revolver(ctx):
        await ctx.reply(f"Heres a gun\n"
                       "# <:Revolver:1505709394057494659>")
        print("Sent revolver prefix command")

    @bot.command()
    async def commands(ctx):
        await ctx.reply(" # TVLOTHE BOT COMMANDS\n"
                        "## Slash Commands\n"
                        "* '/ping' Send pong.\n"
                        "## Prefix Commands\n"
                        "* '?hello' Say hi and ping the caller\n"
                        "* '?reply' Send a discord reply to the caller\n"
                        "* '?cheese' Send a cheese gif (not random)\n"
                        "* '?revolver' Send a Revolver (<:Revolver:1505709394057494659>) emoji"
                       )
        print("Sent 'commands' prefix command")

    @bot.command(name="say")
    async def say(ctx, channel_id: int, *, message: str):
        if not any(role.id == ADMIN_ROLE_ID for role in ctx.author.roles):
            return

            try:
                channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)

            if message.startswith('"') and message.endswith('"'):
                message = message[1:-1]

                await channel.send(message)
                await ctx.send("Message sent successfully.")

            except Exception as e:
            await ctx.send(f"Failed to send message: {e}")

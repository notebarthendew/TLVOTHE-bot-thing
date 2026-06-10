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

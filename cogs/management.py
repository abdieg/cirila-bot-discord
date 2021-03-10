import discord
import asyncio
from discord.ext import commands
from cogs.libs import Settings
from cogs.libs import Utils

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def ping(self, ctx):
        await ctx.send(":ping_pong: Pong!")

def setup(bot):
    bot.add_cog(Management(bot))
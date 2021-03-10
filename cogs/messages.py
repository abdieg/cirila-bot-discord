import discord
import os
import asyncio
from discord.ext import commands
from random import randint
from cogs.libs import Settings
from cogs.libs import Utils

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel

        if isinstance(channel, discord.TextChannel):
            content_of_message = message.content
            content_of_message = content_of_message.lower()
            
            author_id = str(message.author.id)
            author_name = message.author.name
            # message_mentions = message.mentions

            if author_id != str(Settings.CIRILABOTID):
                print("\nAlguien escribio un mensaje")
                print(author_name)
                await channel.send("Hola")

def setup(bot):
    bot.add_cog(Messages(bot))
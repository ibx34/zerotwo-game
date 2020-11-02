import os
import random
import sys

import aiohttp
import aioredis
import asyncpg
import config
import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self,ctx):

        embed = discord.Embed(color=config.COLOR,title="A wild zerotwo has appaered!")
        embed.set_image(url=self.bot.user.avatar_url)

        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))

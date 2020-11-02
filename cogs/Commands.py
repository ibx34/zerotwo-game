import os
import random
import sys

import aiohttp
import aioredis
import asyncpg
import config
import discord
from discord.ext import commands
import images


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="claim")
    async def _claim(self,ctx):

        if ctx.channel.id not in self.bot.cards:
            return await ctx.channel.send(f"**{ctx.author.name}**, there is no cards to collect! B-baka >:(")

        card = None
        for x in images.cards:
            if x.name == self.bot.cards[ctx.channel.id]:
                card = x

        await ctx.channel.send(f"**{ctx.author.name}**, WooHoo~! You collected a **{card.type.value}** **{card.name}**")       
        del self.bot.cards[ctx.channel.id]

def setup(bot):
    bot.add_cog(Commands(bot))

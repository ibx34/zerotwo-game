import collections
import os
import random
import sys
from textwrap import dedent

import aiohttp
import aioredis
import asyncpg
import config
import discord
import images
from discord.ext import commands


def leftpad(string: str, amount: int) -> str:
  return ' ' * (amount - len(string)) + string

class CardSender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_count = collections.defaultdict(lambda: 0)

    @commands.Cog.listener()
    async def on_message(self,message):

        if message.author.bot:
            return

        self.message_count[message.channel.id] += 1

        #if self.message_count[message.channel.id] > random.randint(44,71) and random.random() < 0.65:
        if self.message_count[message.channel.id] > 5:
            card = random.choice(images.cards)
            amount_of_space = len('{:_}'.format(max(card.stats.price, card.stats.damage, card.stats.health)))
            embed = discord.Embed(color=config.COLOR,description=dedent(f"""
            ```md
            # {card.name}
            < {card.series} >
            [ Damage ]( {leftpad('{:_}'.format(card.stats.damage), amount_of_space)} )
            [ Health ]( {leftpad('{:_}'.format(card.stats.health), amount_of_space)} )
            [  Cost  ]( {leftpad('{:_}'.format(card.stats.price), amount_of_space)} )
            ```
            """))
            embed.set_image(url=card.url)
            await message.channel.send(embed=embed)
            self.message_count[message.channel.id] = 0
            self.bot.cards[message.channel.id] = card.name

def setup(bot):
    bot.add_cog(CardSender(bot))

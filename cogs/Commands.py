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

from cogs.Error import is_dev, on_cooldown
from cogs.utils import Pagintation, Resonder


def leftpad(string: str, amount: int) -> str:
  return ' ' * (amount - len(string)) + string


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="oni-chan")
    async def _onichan(self,ctx):

        await ctx.channel.send("https://youtu.be/XLj9QtidiTo")

    @commands.command(name="start")
    async def _start(self,ctx):
        async with self.bot.pool.acquire() as conn:
            user = await conn.fetchrow("SELECT * FROM zt_user WHERE id = $1 AND guild = $2",ctx.author.id,ctx.channel.guild.id)

            if user:
                return await ctx.channel.send(f"**{ctx.author.name}**, You... you've already started **REEEEEEE :(")
            try:
                await conn.execute("INSERT INTO zt_user(id,guild) VALUES($1,$2)",ctx.author.id,ctx.channel.guild.id)
            except:
                return await ctx.channel.send(f"Owno something went wrong~! Sowwy :(")
            
            await ctx.channel.send(f"**{ctx.author.name}**, **Congwats~!** you can now start collecting them sick anime babes :sunglasses:")

    @commands.command(name="my")
    async def _my(self,ctx):
        async with self.bot.pool.acquire() as conn:
            user = await conn.fetchrow("SELECT * FROM zt_user WHERE id = $1 AND guild = $2",ctx.author.id,ctx.channel.guild.id)

            if user['other_characters'] == "{}":
                return await ctx.channel.send(f"**{ctx.author.name}**, b-baka you have no cwards... >:(")

            pages = []
            for x in user['other_characters']:
                item = x
                for x in images.cards:
                    if x.id == item:
                        amount_of_space = len('{:_}'.format(max(x.stats.price, x.stats.damage, x.stats.health)))
                        embed = discord.Embed(color=config.COLOR,description=dedent(f"""
                        ```md
                        # {x.name}
                        < {x.series} >
                        [ Damage ]( {leftpad('{:_}'.format(x.stats.damage), amount_of_space)} )
                        [ Health ]( {leftpad('{:_}'.format(x.stats.health), amount_of_space)} )
                        [  Cost  ]( {leftpad('{:_}'.format(x.stats.price), amount_of_space)} )
                        ```
                        """))
                        embed.set_image(url=x.url)  
                        pages.append(embed)

            paginator = Pagintation.BotEmbedPaginator(ctx,pages)
            return await paginator.run()       

    @commands.command(name="claim")
    async def _claim(self,ctx):
        async with self.bot.pool.acquire() as conn:
            user = await conn.fetchrow("SELECT * FROM zt_user WHERE id = $1 AND guild = $2",ctx.author.id,ctx.channel.guild.id)

            if not user:
                return await ctx.channel.send(f"**{ctx.author.name}**, it doesn't seem you like you even exist... run `zt!start` to get started, b-baka~!")

            if ctx.channel.id not in self.bot.cards:
                # del self.bot.cards[ctx.channel.id]
                return await ctx.channel.send(f"**{ctx.author.name}**, there is no cards to collect! B-baka >:(")

            card = self.bot.cards[ctx.channel.id]
            if card.id in user['other_characters'] or card.id == user['main_characters']:
                del self.bot.cards[ctx.channel.id]
                return await ctx.channel.send(f"**{ctx.author.name}**, you already own that card, b-baka ~~!")
            
            try:
                list = [x for x in user['other_characters']]
                list.append(card.id)
                await conn.execute("UPDATE zt_user SET other_characters = $1 WHERE id = $2 AND guild = $3",list,ctx.author.id,ctx.channel.guild.id)
            except Exception as err:
                print(err)
                return await ctx.channel.send(f"Owno something went wrong~! Sowwy :(")
            
            await ctx.channel.send(Resonder.respond(message=random.choice(Resonder.responses['claim']['success']),user=ctx.author,channel=ctx.channel,card=card))
            #await ctx.channel.send(f"**{ctx.author.name}**, WooHoo~! You collected a **{card.type.value}** **{card.name}**")       

def setup(bot):
    bot.add_cog(Commands(bot))

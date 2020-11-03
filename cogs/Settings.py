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


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prefix")
    @commands.has_permissions(manage_guild=True)
    async def _prefix(self,ctx,*,new_prefix):
        if len(new_prefix) > 520:
            return await ctx.channel.send(f"OwO... Your prefwix may not be over 500 characters.")

        async with self.bot.pool.acquire() as conn:
            try:
                await conn.execute("UPDATE zt_guild SET prefix = $1 WHERE id = $2",new_prefix,ctx.channel.guild.id)
                self.bot.prefixes[ctx.channel.guild.id] = new_prefix
            except Exception as err:
                print(err)
                return await ctx.channel.send(f"Owno something went wrong~! Sowwy :(")        

            await ctx.channel.send(f"Great news! Your servers prefix has been set to `{new_prefix}`")
            
    @commands.command(name="disable")
    @commands.has_permissions(manage_guild=True)
    async def _disable(self,ctx,channel:discord.TextChannel):
        async with self.bot.pool.acquire() as conn:
            guild = await conn.fetchrow("SELECT * FROM zt_guild WHERE id = $1",ctx.channel.guild.id)

            try:
                list = [x for x in guild['disabled']]
                list.append(channel.id)
                await conn.execute("UPDATE zt_guild SET disabled = $1 WHERE id = $2",list,ctx.channel.guild.id)
            except Exception as err:
                print(err)
                return await ctx.channel.send(f"Owno something went wrong~! Sowwy :(")            

            await ctx.channel.send(f"**{ctx.author.name}**, OwO character cards will no longer be sent in <#{channel.id}>")

    @commands.command(name="enable")
    @commands.has_permissions(manage_guild=True)
    async def _enable(self,ctx,channel:discord.TextChannel):
        async with self.bot.pool.acquire() as conn:
            guild = await conn.fetchrow("SELECT * FROM zt_guild WHERE id = $1",ctx.channel.guild.id)

            try:
                list = [x for x in guild['disabled']]
                list.remove(channel.id)
                await conn.execute("UPDATE zt_guild SET disabled = $1 WHERE id = $2",list,ctx.channel.guild.id)
            except Exception as err:
                print(err)
                return await ctx.channel.send(f"Owno something went wrong~! Sowwy :(")            

            await ctx.channel.send(f"**{ctx.author.name}**, OwO character cards will now be sent in <#{channel.id}>")

def setup(bot):
    bot.add_cog(Settings(bot))

import collections
import os
import random
import sys

import aiohttp
import aioredis
import asyncpg
import discord
from discord.ext import commands

import config


class ZeroTwo(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.get_pre,
            case_insensitive=True,
            reconnect=True,
            status=discord.Status.idle,
            intents=discord.Intents(
                messages=True,
                guilds=True,
                members=True,
                guild_messages=True,
                dm_messages=True,
                reactions=True,
                guild_reactions=True,
                dm_reactions=True,
            ),
        )
        self.config = config
        self.session = None
        self.pool = None
        self.redis = None
        self.used = 0
        self.cards = {}
        self.prefixes = {}

    async def get_pre(self, bot, message):
        if not message.guild:
            return commands.when_mentioned_or(config.PREFIX)(bot, message)
        try:
            guild_prefix = bot.prefixes[message.guild.id]
            if guild_prefix:
                return commands.when_mentioned_or(guild_prefix)(bot, message)
        except KeyError:
            return commands.when_mentioned_or(config.PREFIX)(bot, message)

    async def start(self):
        self.session = aiohttp.ClientSession(loop=self.loop)
        for ext in config.EXTENSIONS:
            try:
                self.load_extension(f"{ext}")
            except Exception as e:
                print(f"Failed to load {ext}, {e}")

        await super().start(config.TOKEN)

    async def on_ready(self):
        self.pool = await asyncpg.create_pool(**config.DB, max_size=150)
        self.redis = await aioredis.create_redis_pool("redis://localhost", loop=self.loop)

        try:
            with open("schema.sql") as f:
                await self.pool.execute(f.read())
        except Exception as e:
            print(e)

        for i in await self.pool.fetch("SELECT * FROM zt_guild"):
            self.prefixes[i["id"]] = i["prefix"]

        await self.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.listening, name='The Kiss of Death'))
        print(f"Bot started. Guilds: {len(self.guilds)} Users: {len(self.users)}")

    async def on_message(self, message):

        if message.author.bot:
            return

        ctx = await self.get_context(message)

        if ctx.command:
            await self.process_commands(message, ctx)

    async def process_commands(self, message, ctx):

        # ctx = await self.get_context(message)

        if ctx.command is None:
            return

        self.used += 1
        await self.invoke(ctx)
    
   async def on_guild_join(self, guild):

        try:
            await self.pool.execute("INSERT INTO zt_guild(id,prefix) VALUES($1,$2)", guild.id, config.PREFIX)
            self.prefixes[guild.id] = config.PREFIX
        except Exception as err:
            print(err)

if __name__ == "__main__":
    ZeroTwo().run()

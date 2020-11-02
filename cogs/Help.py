import asyncio
import random
import config

import discord
from discord.ext import commands
from cogs import Error
from discord.ext import commands

from cogs import Error


class HelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={"hidden": True})

    def get_command_signature(self, command):
        return "{0.clean_prefix}{1.qualified_name} {1.signature}".format(self, command)

    """
    def command_formatter(self, embed, command):
        embed.title = self.get_command_signature(command)
        if command.description:
            embed.description = f"{command.description}\n\n{command.help}"
        else:
            embed.description = command.help or "No help found..."
    
    """

    async def send_bot_help(self, mapping):

        ctx = self.context
        bot = self.context.bot
        # prefix = bot.prefixes[ctx.guild.id]

        embed = discord.Embed(color=config.COLOR)
        for x in bot.cogs:
            if x in ['CardSender','Error','Help','Jishaku']:
                continue

            cog = bot.get_cog(x)
            filtered = await self.filter_commands(cog.get_commands())

            commandlist = [f"`{x.name}`" for x in filtered] #""
            embed.add_field(name=x, value=', '.join(commandlist), inline=False)
            commandlist = []

        await ctx.send(embed=embed)

    async def send_cog_help(self, cog):

        ctx = self.context
        #bot = self.context.bot
        # prefix = config.PREFIX #bot.prefixes[ctx.guild.id]
        filtered = await self.filter_commands(cog.get_commands())
        commandlist = [f"`{x.name}`" for x in filtered] #""

        embed = discord.Embed(color=config.COLOR)
        embed.add_field(name=cog.qualified_name, value=', '.join(commandlist), inline=False)

        await ctx.send(embed=embed)

    async def send_command_help(self, command):

        # ctx = self.context
        prefix = config.PREFIX # bot.prefixes[ctx.guild.id]
        
        embed = discord.Embed(title=f"{command.name}", description=f"Aliases: {', '.join(command.aliases)}", color=config.COLOR)
        embed.add_field(name="Usage", value=f"`{prefix}{command.usage}`" or "No usage", inline=False)
        embed.add_field(name="Description",value=command.description or "No description",inline=False)

        await self.context.send(embed=embed)

    async def send_group_help(self, group):

        # ctx = self.context
        bot = self.context.bot
        prefix = config.PREFIX # bot.prefixes[ctx.guild.id]
        command = bot.get_command(group.name)

        embed = discord.Embed(title=f"{command.name}", description=f"Aliases: {', '.join(command.aliases)}", color=config.COLOR)
        embed.add_field(name="Usage", value=f"`{prefix}{command.usage}`" or "No usage", inline=False)

        if group.commands:
            embed.add_field(name="Commands", value=', '.join(group.commands), inline=False)
        await self.context.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self


def cog_unload(self):
    self.bot.help_command = self.old_help_command


def setup(bot):
    bot.add_cog(Help(bot))

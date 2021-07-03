## Initialization
from common import config, log, embedMessage
import discord
from discord.ext import commands, tasks

class help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.description = f"Display help about {self.bot.user.name}'s commands"
        self.usage = f"""
        {self.bot.command_prefix}help
        {self.bot.command_prefix}help <command>
        """
        self.hidden = False

    @commands.command()
    async def help(self, ctx, *args):
        embed=False
        prefix = self.bot.command_prefix
        if (args) :
            command = self.bot.get_cog(args[0])
            if not (command):
                pass
            elif (not command.hidden):
                embed=embedMessage.embed(
                    title=command.qualified_name,
                    description=command.description,
                    sections=[("Usage",command.usage)]
                )
        else:
            cogs = []
            for cog in self.bot.cogs:
                cog = self.bot.get_cog(cog)
                if (not cog.hidden):
                    cogs.append((cog.qualified_name,cog.description))
            embed=embedMessage.embed(
                title="List of commands:",
                sections=cogs,
                footer=f"Use {self.bot.command_prefix}help <command> to get more specific usage information."
            )
        if not (embed):   
            embed=embedMessage.embed(
                title="This command does not exist",
                description=f"Try {self.bot.command_prefix}help to see a list of available commands."
            )       
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(help(bot))
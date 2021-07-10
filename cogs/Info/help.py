## Initialization
from common import config, log, embedMessage, category
import discord
from discord.ext import commands, tasks

class help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = f"Displays help about {self.bot.user.name}'s commands"
        self.usage = f"""
        {self.bot.command_prefix}help
        {self.bot.command_prefix}help <command>
        """

    @commands.command(aliases=['commands', '?'])
    async def help(self, ctx, *args):
        embed=False
        prefix = self.bot.command_prefix
        if (args) :
            cog = self.bot.get_cog(args[0])
            command = self.bot.get_command(args[0])
            if not (cog):
                pass
            elif (not cog.hidden):
                embed=embedMessage.embed(
                    title=cog.qualified_name,
                    description=cog.description,
                    sections=[("Usage",cog.usage), ("Category",cog.category)],
                    footer=f'Aliases: {", ".join(command.aliases)}'
                )
        else:
            cogs = {}
            for cog in self.bot.cogs:
                cog = self.bot.get_cog(cog)
                if (not cog.hidden):
                    if not (cog.category in cogs.keys()):
                        cogs[cog.category] = []
                    cogs[cog.category].append(f"`{cog.qualified_name}`\n> {cog.description}")
            ## Display list of commands and descriptions
            embed=embedMessage.embed(
                title="List of commands:",
                footer=f"Use {self.bot.command_prefix}help <command> to get more specific usage information."
            )
            for category in cogs.keys():
                embed.add_field(name=category,value="\n".join(cogs[category]))

        if not (embed):   
            embed=embedMessage.embed(
                title="This command does not exist",
                description=f"Try {self.bot.command_prefix}help to see a list of available commands."
            )       
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(help(bot))
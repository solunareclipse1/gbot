## Initialization
import discord
from discord.ext import commands
from common import config, log, embedMessage, category

## Class setup
class about(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = f'Shows some information about this bot'
        self.usage = f"""
        {config.cfg['options']['prefix']}about
        """

    ## Command defining
    @commands.command()
    async def about(self, ctx):
        embed = embedMessage.embed(
            title = f'About {self.bot.user.name}',
            description = f'{self.bot.user.name} is a Discord bot, written in python, designed to be very modular and configurable.',
            url = 'https://github.com/solunareclipse1/gbot',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(about(bot))
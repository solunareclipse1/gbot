## Initialization
import discord
from discord.ext import commands
from common import config, embedMessage, category

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
    @commands.command(aliases=['info'])
    async def about(self, ctx):
        embed = embedMessage.embed(
            title = f'About {self.bot.user.name}',
            description = f'{self.bot.user.name} is a Discord bot, written in python, designed to be very modular and configurable. Github link above.',
            url = 'https://github.com/solunareclipse1/gbot',
            color = embedMessage.defaultColor,
            thumbnail = 'https://cdn.discordapp.com/attachments/863527179479416852/863527222085419029/gbot.png'
        )
        await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(about(bot))
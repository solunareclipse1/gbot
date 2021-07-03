## Initialization
import discord
from common import config, log
from discord.ext import commands

## Example cog
class exampleCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.description = "Adds numbers together but is overly finnicky about it."
        self.usage = f"""
        {config.cfg['options']['prefix']}add <first number> <second number>
        """
        self.hidden = False

        ## Config stuff
        self.firstNumber = config.cfg['settings']['exampleCommand']['firstNumber']
        self.favNumber = config.cfg['settings']['exampleCommand']['favNumber']

    ## Command defining
    @commands.command()
    @commands.has_guild_permissions(embed_links=True, attach_files=True)
    async def add(self, ctx, arg1: int, arg2: int):
        if arg1 == 9 and arg2 == 10:
            await ctx.send('twenny-wan')
            return
        if arg1 != self.firstNumber:
            await ctx.send(f'Sorry, but the first number must be {self.firstNumber}!')
            return
        ans = arg1 + arg2
        if ans == self.favNumber:
            await ctx.send(f'Wow, the answer is {self.favNumber}, my favorite number!')
            return
        await ctx.send(f'The answer is {ans}')

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(exampleCommandCog(bot))
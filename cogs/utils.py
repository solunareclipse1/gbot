## Initialization
import discord
from common import config, log
from discord.ext import commands, tasks

## General utility commands
class utilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ## Test latency
    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx):
        await ctx.send(f'Ping! Took ~{round (self.bot.latency * 1000)}ms')

    ## Retreive user information
    @commands.command()
    @commands.is_owner()
    async def info(self, ctx):
        await ctx.send(f'{self.bot.user}')

    ## Relay errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        log.log(error)
        await ctx.send(f'Something broke: \n{error}')

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(utilsCog(bot))
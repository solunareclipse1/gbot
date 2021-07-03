## Initialization
import discord
from common import config, log
from discord.ext import commands, tasks

## General utility commands
class debugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = True

    ## Test latency
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Ping! Took ~{round (self.bot.latency * 1000)}ms')

    ## Retreive user information
    @commands.command()
    async def info(self, ctx):
        await ctx.send(f'{self.bot.user}')

    ## Relay errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        log.log(error)
        await ctx.send(f'Something broke: \n{error}')

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(debugCog(bot))
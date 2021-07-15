## Initialization
import discord
from common import config, log, embedMessage
from discord.ext import commands, tasks

## General utility commands
class debugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = True

    ## Debug Command
    @commands.command()
    @commands.is_owner()
    async def debug(self, ctx):
        embed = embedMessage.embed(
            title = 'Bot Debug Information',
            description = f"""
            **Bot Account:** {self.bot.user.mention} \n
            **Bot Latency:** {round (self.bot.latency * 1000)}ms
            """,
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

    ## Relay errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.message.content.startswith(self.bot.command_prefix * 2) and ctx.message.content.endswith(self.bot.command_prefix):
            log.log(f'Detected prefix spam, not sending output through discord. Error logged: \n{error}')
            return
        log.log(error)
        embed = embedMessage.embed(
            title = 'ERROR',
            description = f'An error occured whilst trying to run the command: \n**{error}**',
            color = embedMessage.errorColor
        )
        await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(debugCog(bot))
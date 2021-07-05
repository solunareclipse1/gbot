## Initialization
import discord
from common import config, log, embedMessage
from discord.ext import commands

## Class setup
class join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.description = "Makes the bot join the voice channel you are currently connected to."
        self.usage = f"""
        {config.cfg['options']['prefix']}join
        """

    ## Command defining
    @commands.command()
    @commands.has_guild_permissions(connect=True)
    async def join(self, ctx):
        if ctx.author.voice == None:
            embed = embedMessage.embed(
            title = 'ERROR',
            description = 'You are not connected to a voice channel.',
            color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        joinTarget = ctx.author.voice.channel
        await ctx.guild.change_voice_state(channel=joinTarget, self_deaf=True)
        embed = embedMessage.embed(
            title = 'SUCCESS',
            description = f'Connected to {joinTarget}.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(join(bot))
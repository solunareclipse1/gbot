## Initialization
import discord
from common import config, log, embedMessage
from discord.ext import commands

## Class setup
class leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.description = "Makes the bot disconnect from the voice channel it is connected to."
        self.usage = f"""
        {config.cfg['options']['prefix']}leave
        """

    ## Command defining
    @commands.command()
    @commands.has_guild_permissions(connect=True)
    async def leave(self, ctx):
        if ctx.guild.me.voice == None:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'I am not connected to a voice channel!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        currentChannel = ctx.guild.me.voice.channel
        if ctx.author.voice.channel != currentChannel:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You must be connected to the same voice channel as the bot to disconnect it.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        await ctx.voice_client.disconnect()
        embed = embedMessage.embed(
            title = 'SUCCESS',
            description = f'Left {currentChannel}.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(leave(bot))
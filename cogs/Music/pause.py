## Initialization
import discord
from discord.ext import commands
from common import config, embedMessage, category

## Class setup
class pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = 'Pauses playback.'
        self.usage = f"""
        {config.cfg['options']['prefix']}pause
        """

    ## Command defining
    @commands.command()
    async def pause(self, ctx):
        if not ctx.me.voice:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'I am not currently in a voice channel.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You must be connected to the same voice channel as the bot to stop playback.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        elif ctx.voice_client.is_paused() == True:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'Playback is already paused!\nUse ?play to resume.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        ctx.voice_client.pause()
        embed = embedMessage.embed(
                title = 'SUCCESS',
                description = 'Playback has been paused.'
            )
        await ctx.send(embed=embed)
        
## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(pause(bot))
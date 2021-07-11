## Initialization
import discord
from discord.ext import commands
from common import config, log, embedMessage, category

## Class setup
class skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = 'Skips this song.'
        self.usage = f"""
        {config.cfg['options']['prefix']}skip
        """

    ## Command defining
    @commands.command()
    async def skip(self, ctx):
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
                description = 'You must be connected to the same voice channel as the bot to skip.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        ctx.voice_client.stop()
        
        
## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(skip(bot))
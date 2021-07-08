## Initialization
import discord
import youtube_dl
from discord.ext import commands
from common import config, log, embedMessage, ytdlSrc, category

## Class setup
class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = 'Plays the specified media in voice chat.'
        self.usage = f"""
        {config.cfg['options']['prefix']}play <link>
        {config.cfg['options']['prefix']}play <search>
        {config.cfg['options']['prefix']}play <"search terms">
        """

    ## Command defining
    @commands.command()
    async def play(self, ctx, media):
        if not ctx.author.voice.channel:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You must be in a voice channel to play media.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        elif not ctx.guild.me.voice.channel:
            return
        elif ctx.author.voice.channel != ctx.guild.me.voice.channel:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You must be connected to the same voice channel as the bot to play media.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        if not ctx.guild.me.voice:
            self.connectedChannel = await ctx.author.voice.channel.connect()
        ytdl_src = await ytdlSrc.ytdlSrc.from_url(media, loop=self.bot.loop, stream=True)
        try:
            self.connectedChannel.play(ytdl_src, after=lambda e: print('Player error: %s' % e) if e else None)
        except discord.ClientException as er:
            if er.args[0] == 'Already playing audio.':
                await ctx.send('queued')
        else:
            embed = embedMessage.embed(
                title = 'Now playing:',
                description = ytdl_src.title
            )
            await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(play(bot))
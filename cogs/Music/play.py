## Initialization
import asyncio
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
    async def play(self, ctx, *args):
        if not ctx.author.voice.channel:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You must be in a voice channel to play media.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        elif not ctx.guild.me.voice:
            self.bot.player.connectedChannel = await ctx.author.voice.channel.connect()
        elif ctx.author.voice.channel != ctx.guild.me.voice.channel:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You must be connected to the same voice channel as the bot to play media.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
            
        ## If more thqn one word is passed, collapse args into one string
        if len(args) > 1:
            media = " ".join(args)
        else:
            media = args[0]

        if not self.bot.player.nowPlaying:
            embed = embedMessage.embed(
                title = "Now loading..."
            )
            self.bot.player.nowPlaying = await ctx.send(embed=embed)
        await self.playAudio(media)

    async def playAudio(self,media):
        channel = self.bot.player.nowPlaying.channel
        ytdl_src = await ytdlSrc.ytdlSrc.from_url(media, loop=self.bot.loop, stream=True)
        try:
            self.bot.player.connectedChannel.play(ytdl_src, after=self.onFinish)
        except discord.ClientException as er:
            if er.args[0] == 'Already playing audio.':
                self.bot.player.queue.append(media)
                embed = embedMessage.embed(
                    title = "Queued:",
                    description = ytdl_src.title
                )
                await self.bot.player.nowPlaying.delete()
                self.bot.player.nowPlaying = await channel.send(embed=embed)
                
        else:
            embed = embedMessage.embed(
                    title = "Now Playing:",
                    description = ytdl_src.title
            )
            await self.bot.player.nowPlaying.delete()
            self.bot.player.nowPlaying = await channel.send(embed=embed)
        

    def onFinish(self, err):
        if len(self.bot.player.queue) > 0:
            coroutine = self.playAudio(self.bot.player.queue.pop(0))
        else:
            coroutine = self.bot.player.connectedChannel.disconnect()
        future = asyncio.run_coroutine_threadsafe(coroutine,self.bot.loop)
        try:
            future.result()
        except:
            pass
        



## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(play(bot))
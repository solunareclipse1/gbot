## Initialization
import asyncio
import discord
import youtube_dl
from discord.ext import commands
from common import config, log, embedMessage, ytdlSrc, category, player

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
        """

    ## Command defining
    @commands.command()
    async def play(self, ctx, *args):
        if len(args) == 0:
            if ctx.voice_client != None:
                if ctx.voice_client.is_paused():
                    ctx.voice_client.resume()
                    embed = embedMessage.embed(
                        title = 'SUCCESS',
                        description = 'Playback has been resumed.',
                        color = embedMessage.defaultColor
                    )
                    await ctx.send(embed=embed)
                    return
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You did not specify what I should play!',
                color = embedMessage.errorColor
            )
            return
        elif not ctx.author.voice.channel:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You must be in a voice channel to play media.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        elif not ctx.me.voice:
            voiceClient = await ctx.author.voice.channel.connect()
            self.bot.player.connectedChannel[ctx.guild.id] = voiceClient
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You must be connected to the same voice channel as the bot to play media.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return

        ## If more than one word is passed, collapse args into one string
        if len(args) > 1:
            media = " ".join(args)
        else:
            media = args[0]

       
        if not ctx.guild.id in self.bot.player.nowPlaying.keys():
            embed = embedMessage.embed(
                title = "Now loading..."
            )
            reply = await ctx.send(embed=embed)
            self.bot.player.nowPlaying[ctx.guild.id] = reply
            
        await self.playAudio(media,ctx.guild)

    async def playAudio(self,media,guild):
        if guild.id in self.bot.player.nowPlaying.keys():
            channel = self.bot.player.nowPlaying[guild.id].channel
        ytdl_src = await ytdlSrc.ytdlSrc.from_url(media, loop=self.bot.loop, stream=True)
        try:
            self.bot.player.connectedChannel[guild.id].play(ytdl_src, after=lambda e: self.onFinish(guild))
        except discord.ClientException as er:
            if er.args[0] == 'Already playing audio.':
                if not channel.guild.id in self.bot.player.queue.keys():
                    self.bot.player.queue[channel.guild.id] = []
                self.bot.player.queue[channel.guild.id].append({
                    "name":media,
                    "title":ytdl_src.title
                    })
                embed = embedMessage.embed(
                    title = "Queued:",
                    description = ytdl_src.title
                )
                await self.bot.player.nowPlaying[guild.id].delete()
                self.bot.player.nowPlaying[guild.id] = await channel.send(embed=embed)
        else:
            embed = embedMessage.embed(
                    title = "Now Playing:",
                    description = ytdl_src.title
            )
            await self.bot.player.nowPlaying[guild.id].delete()
            self.bot.player.nowPlaying[guild.id] = await channel.send(embed=embed)

    def onFinish(self, guild):
        if len(self.bot.player.queue[guild.id]) > 0:
            coroutine = self.playAudio(self.bot.player.queue[guild.id].pop(0)["name"],guild)
        else:
            coroutine = self.bot.player.connectedChannel[guild.id].disconnect()
        future = asyncio.run_coroutine_threadsafe(coroutine,self.bot.loop)
        try:
            future.result()
        except:
            pass
        



## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(play(bot))
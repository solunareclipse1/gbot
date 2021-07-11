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

        self.mustJoin = False
        self.joinTarget = None

    ## Command defining
    @commands.command(aliases=['p'])
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
            self.mustJoin = True
            self.joinTarget = ctx.author.voice.channel
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
            self.bot.player.nowPlaying[ctx.guild.id] = {
                "message":reply,
                "song":None
                }
            
        await self.playAudio(media,ctx.guild)

    async def playAudio(self,media,guild):
        if guild.id in self.bot.player.nowPlaying.keys():
            channel = self.bot.player.nowPlaying[guild.id]["message"].channel

        title = None
        if type(media) == dict:
            title = media["title"]
            media = media["name"]
        ytdl_src = await ytdlSrc.ytdlSrc.from_url(media, self.bot, guild, loop=self.bot.loop, stream=True)
        if not title:
            title = ytdl_src.title

        try:
            voiceClient = await self.joinTarget.connect()
            self.bot.player.connectedChannel[guild.id] = voiceClient
        except discord.ClientException as er:
            if er.args[0] == 'Already connected to a voice channel.':
                pass
        except AttributeError:
            pass

        try:
            self.bot.player.connectedChannel[guild.id].play(ytdl_src, after=lambda e: self.onFinish(guild))
        except discord.ClientException as er:
            if er.args[0] == 'Already playing audio.':
                if not guild.id in self.bot.player.queue.keys():
                    self.bot.player.queue[guild.id] = []
                self.bot.player.queue[guild.id].append({
                    "name":media,
                    "title":title
                    })
                embed = embedMessage.embed(
                    title = "Queued:",
                    description = title
                )
                await self.bot.player.nowPlaying[guild.id]["message"].delete()
                self.bot.player.nowPlaying[guild.id]["message"] = await channel.send(embed=embed)
        else:
            embed = embedMessage.embed(
                    title = "Now Playing:",
                    description = title
            )
            await self.bot.player.nowPlaying[guild.id]["message"].delete()
            self.bot.player.nowPlaying[guild.id] = {
                "message":await channel.send(embed=embed),
                "song":title
            }

        if ytdl_src.toQueue:
            if not guild.id in self.bot.player.queue.keys():
                    self.bot.player.queue[guild.id] = []
            for song in ytdl_src.toQueue:
                self.bot.player.queue[guild.id].append({
                    "name":song['url'],
                    "title":song['title']
                })
            embed = embedMessage.embed(
                title = "Queued:",
                description = f"**{len(ytdl_src.toQueue) + 1}** songs from **{ytdl_src.data['title']}**"
            )
            ytdl_src.toQueue = None
            await self.bot.player.nowPlaying[guild.id]["message"].delete()
            self.bot.player.nowPlaying[guild.id]["message"] = await channel.send(embed=embed)

    def onFinish(self, guild):
        if len(self.bot.player.queue[guild.id]) > 0:
            coroutine = self.playAudio(self.bot.player.queue[guild.id].pop(0),guild)
        else:
            coroutine = self.bot.player.connectedChannel[guild.id].disconnect()
        future = asyncio.run_coroutine_threadsafe(coroutine,self.bot.loop)
        try:
            future.result()
        except Exception as er:
            print(er)
            pass
        



## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(play(bot))
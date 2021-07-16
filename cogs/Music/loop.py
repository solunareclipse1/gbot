## Initialization
import discord
from discord.ext import commands
from common import config, embedMessage, category

## Class setup
class loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = 'Loops the queue.'
        self.usage = f"""
        {config.cfg['options']['prefix']}loop
        """

    ## Command defining
    @commands.command(aliases=['repeat'])
    async def loop(self, ctx):
        if not ctx.voice_client:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'I am not in a voice channel.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You must be in the same voice channel as me to enable queue looping!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        if not ctx.guild.id in self.bot.player.loopQueue.keys():
            self.bot.player.loopQueue[ctx.guild.id] = False
        if self.bot.player.loopQueue[ctx.guild.id]:
            self.bot.player.loopQueue[ctx.guild.id] = False
            if not ctx.guild.id in self.bot.player.queue.keys():
                self.bot.player.queue[ctx.guild.id] = []
            if len(self.bot.player.queue[ctx.guild.id]) > 0:
                if self.bot.player.queue[ctx.guild.id][-1]['title'] == self.bot.player.nowPlaying[ctx.guild.id]['song']:
                    self.bot.player.queue[ctx.guild.id].pop()
            embed = embedMessage.embed(
                title = 'SUCCESS',
                description = 'Queue loop **disabled**.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        else:
            self.bot.player.loopQueue[ctx.guild.id] = True
            if not ctx.guild.id in self.bot.player.queue.keys():
                self.bot.player.queue[ctx.guild.id] = []
            if len(self.bot.player.queue[ctx.guild.id]) > 0:
                if self.bot.player.queue[ctx.guild.id][-1]['title'] != self.bot.player.nowPlaying[ctx.guild.id]['song']:
                    self.bot.player.queue[ctx.guild.id].append({
                            "name":self.bot.player.nowPlaying[ctx.guild.id]['url'],
                            "title":self.bot.player.nowPlaying[ctx.guild.id]['song']
                        })
            else:
                self.bot.player.queue[ctx.guild.id].append({
                            "name":self.bot.player.nowPlaying[ctx.guild.id]['url'],
                            "title":self.bot.player.nowPlaying[ctx.guild.id]['song']
                        })
            embed = embedMessage.embed(
                title = 'SUCCESS',
                description = 'Queue loop **enabled**.'
            )
            await ctx.send(embed=embed)
            return

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(loop(bot))
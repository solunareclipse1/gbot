## Initialization
import discord
from discord.ext import commands
from common import config, log, embedMessage, category

## Class setup
class loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = 'Command description'
        self.usage = f"""
        {config.cfg['options']['prefix']}loop <song/queue>
        """

    ## Command defining
    @commands.command(aliases=['repeat'])
    async def loop(self, ctx):
        if self.bot.player.loopQueue:
            self.bot.player.loopQueue = False
            embed = embedMessage.embed(
                title = 'SUCCESS',
                description = 'Queue loop disabled.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        else:
            self.bot.player.loopQueue = True
            if not ctx.guild.id in self.bot.player.queue.keys():
                self.bot.player.queue[ctx.guild.id] = []
            if self.bot.player.queue[ctx.guild.id][-1]['title'] != self.bot.player.nowPlaying[ctx.guild.id]['song']:
                self.bot.player.queue[ctx.guild.id].append({
                        "name":self.bot.player.nowPlaying[ctx.guild.id]['url'],
                        "title":self.bot.player.nowPlaying[ctx.guild.id]['song']
                    })
            embed = embedMessage.embed(
                title = 'SUCCESS',
                description = 'Queue loop enabled.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(loop(bot))
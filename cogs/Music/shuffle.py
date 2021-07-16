## Initialization
import discord, random
from discord.ext import commands
from common import config, embedMessage, category

## Class setup
class shuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = 'Shuffles the queue.'
        self.usage = f"""
        {config.cfg['options']['prefix']}shuffle
        """

    ## Command defining
    @commands.command(aliases=['mix'])
    async def shuffle(self, ctx):
        guildQueue = self.bot.player.queue[ctx.guild.id]
        if guildQueue == []:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'The queue is empty!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        else:
            random.shuffle(guildQueue)
            embed = embedMessage.embed(
                title = 'SUCCESS',
                description = 'Queue has been shuffled.'
            )
            await ctx.send(embed=embed)
            return

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(shuffle(bot))
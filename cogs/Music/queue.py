## Initialization
import discord
from discord.ext import commands
from common import config, log, embedMessage, category, misc

## Class setup
class queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = 'Displays the queue, 10 items per page.'
        self.usage = f"""
        {config.cfg['options']['prefix']}queue <page>
        """

    ## Command defining
    @commands.command(aliases=['q'])
    async def queue(self, ctx, page=1):
        if self.bot.player.queue == []:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'There is nothing in the queue!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        qLength = len(self.bot.player.queue)
        qLower = ((page - 1) * 10) + 1
        qUpper = page * 10
        if page > 1 and qLower < qLength:
            q = "\n⁍ ".join(self.bot.player.queue[qLower:qUpper])
        elif page == 1:
            q = "\n⁍ ".join(self.bot.player.queue[:qUpper])
        elif qLower > qLength:
            qUpper = int(misc.round_up(qLength, -1))
            qLower = int(qUpper - 9)
            page = int(qUpper / 10)
            q = "\n⁍ ".join(self.bot.player.queue[qLower:qLength])
        elif page < 1:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'Invalid page number!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        embed = embedMessage.embed(
            title = 'Queue',
            description = f'⁍ {q}',
            color = embedMessage.defaultColor,
            footer = f'Page {page} of {int((misc.round_up(qLength, -1)) / 10)}'
        )
        await ctx.send(embed=embed)
        return

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(queue(bot))
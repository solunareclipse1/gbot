## Initialization
import discord
from discord.ext import commands
from common import config, embedMessage, category, misc

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
        if not ctx.guild.id in self.bot.player.queue.keys():
            self.bot.player.queue[ctx.guild.id] = []
        if self.bot.player.queue[ctx.guild.id] == []:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'There is nothing in the queue!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        qLength = len(self.bot.player.queue[ctx.guild.id])
        qLower = ((page - 1) * 10) + 1
        qUpper = page * 10
        pageless = qLength < 11
        if page > 1 and qLower <= qLength:
            q = ""
            for song in self.bot.player.queue[ctx.guild.id][qLower-1:qUpper]:
                q += "{}\n".format(f'⁍ {song["title"]}')
        elif page == 1 or qLength < 11:
            q = ""
            for song in self.bot.player.queue[ctx.guild.id][:qUpper]:                
                q += "{}\n".format(f'⁍ {song["title"]}')
        elif qLower > qLength:
            qUpper = int(misc.round_up(qLength, -1))
            qLower = int(qUpper - 9)
            page = int(qUpper / 10)
            q = ""
            for song in self.bot.player.queue[ctx.guild.id][qLower-1:qUpper]:
                q += "{}\n".format(f'⁍ {song["title"]}')
        elif page < 1:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'Invalid page number!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        if "" == q:
            q = "Nothing Queued."
        embed = embedMessage.embed(
            title = 'Queue',
            description = f'{q}'
        )
        if not pageless:
            embed.set_footer(text=f'Page {page} of {int((misc.round_up(qLength, -1)) / 10)}')
        await ctx.send(embed=embed)
        return

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(queue(bot))
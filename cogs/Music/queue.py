## Initialization
import discord
from discord.ext import commands
from common import config, log, embedMessage, category

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
    @commands.command()
    async def queue(self, ctx):
        if self.bot.player.queue == []:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'There is nothing in the queue!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        q = "\n⁍ ".join(self.bot.player.queue[:10])
        embed = embedMessage.embed(
            title = 'Queue',
            description = f'⁍ {q}',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)
        return

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(queue(bot))
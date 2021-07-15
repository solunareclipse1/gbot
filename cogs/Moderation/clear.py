## Initialization
import discord
from discord.ext import commands
from common import config, log, embedMessage, category

## Class setup
class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = 'Deletes the specified number of previous messages. Defaults to 1.'
        self.usage = f"""
        {config.cfg['options']['prefix']}clear <number of messages>
        """

    ## Command defining
    @commands.command(aliases=['clean', 'delete', 'del', 'cls', 'remove', 'rem', 'd'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        if amount > 0:
            await ctx.message.delete()
            delCount = await ctx.channel.purge(limit=amount)
            embed = embedMessage.embed(
                title = 'SUCCESS',
                description = f'Deleted **{len(delCount)}** message(s).',
                color = embedMessage.defaultColor
            )
            await ctx.send(embed=embed, delete_after=3.0)
        else:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'Delete amount must be more than zero!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)


        

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(clear(bot))
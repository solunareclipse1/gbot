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
        self.description = 'Deletes the specified number of previous messages. Defaults to 1. Can be a little slow because of Discords rate limiting.'
        self.usage = f"""
        {config.cfg['options']['prefix']}clear <number of messages>
        """

    ## Command defining
    @commands.command(aliases=['clean', 'delete', 'del', 'cls', 'remove', 'rem', 'd'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        delCount = -1
        async for message in ctx.channel.history(limit=amount + 1):
            await message.delete()
            delCount = delCount + 1
        embed = embedMessage.embed(
            title = 'SUCCESS',
            description = f'Deleted **{delCount}** messages.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed, delete_after=3.0)
        

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(clear(bot))
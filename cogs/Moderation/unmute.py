## Initialization
import discord
from discord.ext import commands, tasks
from common import config, embedMessage, category, modFunc

## Class setup
class unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = "Unmutes the specified user"
        self.usage = f"""
        {config.cfg['options']['prefix']}unmute <@user> <reason>
        """

    ## Unmutes target
    @commands.command(aliases=['ungag'])
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, target: discord.Member, *args):
        if len(args) > 1:
            reason = " ".join(args)
        elif len(args) == 1:
            reason = args[0]
        else:
            reason = f'Unmuted by {ctx.author}'
        await modFunc.unmute(target, reason)
        embed = embedMessage.embed(
            title = 'SUCCESS',
            description = f'{target.mention} has been unmuted.'
        )
        await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(unmute(bot))
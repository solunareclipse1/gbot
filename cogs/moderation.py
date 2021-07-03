## Initialization
import discord
from common import config, log
from discord.ext import commands, tasks
from discord.utils import get

## Server moderation commands
class moderationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ## Mutes target
    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, target: discord.Member):
        muteOverwrite = discord.PermissionOverwrite()
        muteOverwrite.add_reactions = False
        muteOverwrite.send_messages = False
        muteOverwrite.speak = False
        muteOverwrite.stream = False
        if target == ctx.author:
            await ctx.send('You cannot mute yourself!')
            return
        for channel in ctx.guild.channels:
            await channel.set_permissions(target, overwrite=muteOverwrite, reason=f'{target} was muted by {ctx.author}')
        await ctx.send(f'{target} has been muted.')

    ## Unmutes target
    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, target: discord.Member):
        for channel in ctx.guild.channels:
            await channel.set_permissions(target, overwrite=None, reason=f'{target} was unmuted by {ctx.author}')
        await ctx.send(f'{target} has been unmuted.')

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(moderationCog(bot))
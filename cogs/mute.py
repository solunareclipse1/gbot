## Initialization
import discord
from common import config, log
from discord.ext import commands, tasks
from discord.utils import get

## Server moderation commands
class muteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.description = "Mutes the specified user"
        self.usage = f"""
        {config.cfg['options']['prefix']}mute <@user>
        """

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
        if target == self.bot.user:
            await ctx.send(f'> ***I\'ve come to make an announcement: {ctx.author.mention}\'s a bitch-ass motherfucker. He pissed on my fucking wife. That\'s right, he took his hedgehog fuckin\' quilly dick out and he pissed on my fucking wife, and he said his dick was \"THIS BIG\", and I said \"That\'s disgusting!\" So I\'m making a callout post on my Twitter dot com. {ctx.author.mention}, you got a small dick! It\'s the size of this walnut except WAY smaller! And guess what? Here\'s what my dong looks like! That\'s right, baby! All points, no quills, no pillows, look at that, it looks like two balls and a bong! He fucked my wife, so guess what, I\'m gonna fuck the Earth! That\'s right, this is what you get, my SUPER LASER PISS! Except I\'m not gonna piss on the Earth, I\'m gonna go higher. I\'m pissing on the MOON! HOW DO YOU LIKE THAT, OBAMA? I PISSED ON THE MOON, YOU IDIOT!  You have 23 hours before the piss DRRRROPLLLETS hit the fucking Earth! Now get out of my fucking sight, before I piss on you too!***')
            return
        for channel in ctx.guild.channels:
            await channel.set_permissions(target, overwrite=muteOverwrite, reason=f'{target} was muted by {ctx.author}')
        await ctx.send(f'{target} has been muted.')

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(muteCog(bot))
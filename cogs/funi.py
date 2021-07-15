## Initialization
import discord
from discord.ext import commands
from common import config, log, embedMessage, category

## Class setup
class funi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = True

    ## Command defining
    @commands.command(aliases=['announcement', 'tweet', 'callout'])
    async def robotnik(self, ctx, target = None):
        await ctx.message.delete()
        if not target:
            calloutPoster = '@Eggfucker1'
            calledOut = '@xX_ShadoW_ThE_EdgehoG_Xx'
        elif target == ctx.me.mention:
            calloutPoster = f'@{self.bot.user.display_name}'
            calledOut = ctx.author.mention
        else:
            calloutPoster = f'@{ctx.author.display_name}'
            calledOut = target
        embed = embedMessage.embed(
            title = f'twitter.com: {calloutPoster} updated their status',
            description = f'***I\'ve come to make an announcement: {calledOut}\'s a bitch-ass motherfucker. He pissed on my fucking wife. That\'s right, he took his hedgehog fuckin\' quilly dick out and he pissed on my fucking wife, and he said his dick was \"THIS BIG\", and I said \"That\'s disgusting!\" So I\'m making a callout post on my Twitter dot com. {calledOut}, you got a small dick! It\'s the size of this walnut except WAY smaller! And guess what? Here\'s what my dong looks like! That\'s right, baby! All points, no quills, no pillows, look at that, it looks like two balls and a bong! He fucked my wife, so guess what, I\'m gonna fuck the Earth! That\'s right, this is what you get, my SUPER LASER PISS! Except I\'m not gonna piss on the Earth, I\'m gonna go higher. I\'m pissing on the MOON! HOW DO YOU LIKE THAT, OBAMA? I PISSED ON THE MOON, YOU IDIOT!  You have 23 hours before the piss DRRRROPLLLETS hit the fucking Earth! Now get out of my fucking sight, before I piss on you too!***',
            color = discord.Color.from_rgb(42, 169, 224)
        )
        await ctx.send(embed=embed)
        return

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(funi(bot))
## Initialization
import discord, asyncio
from discord.ext import commands
from common import config, embedMessage, category, modFunc

## Class setup
class funny(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = True

    ## This is where I put my joke features / features I made for fun. 
    ## Uploaded to github because aspects of them might be useful outside of this stupidity. 
    ## Recommend you remove this file when using the bot yourself.
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
            color = discord.Color.from_rgb(42, 169, 224),
            thumbnail = 'https://cdn.discordapp.com/attachments/863527179479416852/865673772560416768/small-twitter-bird-icon_151340.png'
        )
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['hellodiscordbotpleasegivemeamdinpermissionpls'])
    async def helloserverpluginpleasetogglethirdpresononmepls(self, ctx):
        await ctx.message.delete()
        await modFunc.mute(ctx.author)
        await ctx.send(f'{ctx.author.mention} ***no***')
        await asyncio.sleep(10)
        await modFunc.unmute(ctx.author)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild.me.id != msg.author.id and (msg.content.startswith('*you') or msg.content.startswith('*yro')):
                embed = embedMessage.embed(
                    title = 'Um, actually...',
                    color = discord.Color.from_rgb(128, 0, 128),
                    image = 'https://cdn.discordapp.com/attachments/724979907259662426/859813674465886228/56ggshcgw7571.jpg'
                )
                await msg.reply(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(funny(bot))
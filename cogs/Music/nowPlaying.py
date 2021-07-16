## Initialization
import discord
from discord.ext import commands
from common import config, embedMessage, category

## Class setup
class nowPlaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = 'Displays the currently playing track.'
        self.usage = f"""
        {config.cfg['options']['prefix']}nowPlaying
        """

    ## Command defining
    @commands.command(aliases=['np'])
    async def nowPlaying(self, ctx):
        embed = embedMessage.embed(
            title="Nothing currently playing",
            description=f"Use {config.cfg['options']['prefix']}play to play something!",
            colour=embedMessage.errorColor
        )
        if not ctx.guild.id in self.bot.player.nowPlaying.keys():
            self.bot.player.nowPlaying[ctx.guild.id] = {
                "message":await ctx.send(embed=embed),
                "song":None
            }
            return
        elif not self.bot.player.nowPlaying[ctx.guild.id]["song"]:
            self.bot.player.nowPlaying[ctx.guild.id] = {
                "message":await ctx.send(embed=embed),
                "song":None
            }
            return
        embed = embedMessage.embed(
            title = "Now Playing:",
            description = self.bot.player.nowPlaying[ctx.guild.id]["song"]
        )
        try:
            await self.bot.player.nowPlaying[ctx.guild.id]["message"].delete()
        except discord.NotFound:
            pass
        self.bot.player.nowPlaying[ctx.guild.id]["message"] = await ctx.send(embed=embed)
        return

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(nowPlaying(bot))
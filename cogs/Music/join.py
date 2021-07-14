## Initialization
import discord
from common import config, log, embedMessage, category
from discord.ext import commands

## Class setup
class join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.description = "Makes the bot join the voice channel you are currently connected to."
        self.usage = f"""
        {config.cfg['options']['prefix']}join
        """

    ## Command defining
    @commands.command(aliases=['connect'])
    @commands.has_guild_permissions(connect=True)
    async def join(self, ctx):
        if ctx.author.voice == None:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = 'You are not connected to a voice channel.',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        joinTarget = ctx.author.voice.channel
        if ctx.voice_client != None:
            if ctx.author.guild_permissions.move_members == False:
                embed = embedMessage.embed(
                    title = 'ERROR',
                    description = 'You need the Move Members permission to change the bot\'s connected channel.',
                    color = embedMessage.errorColor
                )
                await ctx.send(embed=embed)
                return
            await ctx.voice_client.move_to(joinTarget)
            embed = embedMessage.embed(
                title = 'SUCCESS',
                description = f'Moved to **{joinTarget}**.',
                color = embedMessage.defaultColor
            )
            await ctx.send(embed=embed)
            return
        self.bot.player.connectedChannel[ctx.guild.id] = await joinTarget.connect()
        embed = embedMessage.embed(
            title = 'SUCCESS',
            description = f'Connected to **{joinTarget}**.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(join(bot))
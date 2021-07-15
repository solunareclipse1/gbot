## Initialization
import discord
from common import config, log, embedMessage, category
from discord.ext import commands

## Class setup
class exampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = False
        self.category = category.getCategory(self.__module__)
        self.qualified_name = 'exampleCommand'
        self.description = "Adds numbers together but is overly finnicky about it."
        self.usage = f"""
        {config.cfg['options']['prefix']}add <first number> <second number>
        """

        ## Config stuff
        self.firstNumber = config.cfg['settings']['exampleCommand']['firstNumber']
        self.favNumber = config.cfg['settings']['exampleCommand']['favNumber']
        self.listenFor = config.cfg['settings']['exampleCommand']['listenFor']
        self.replyWith = config.cfg['settings']['exampleCommand']['replyWith']

    ## Command defining
    @commands.command(aliases=['add','badd'])
    @commands.has_guild_permissions(embed_links=True, attach_files=True)
    async def exampleCommand(self, ctx, arg1: int, arg2: int):
        if arg1 == 9 and arg2 == 10:
            embed = embedMessage.embed(
                title = 'whas nahn plus tehn?',
                description = 'twenny wan',
                color = embedMessage.defaultColor
            )
            await ctx.send(embed=embed)
            return
        if arg1 != self.firstNumber:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = f'Sorry, the first number must be {self.firstNumber}!',
                color = embedMessage.errorColor
            )
            await ctx.send(embed=embed)
            return
        ans = arg1 + arg2
        if ans == self.favNumber:
            embed = embedMessage.embed(
                title = 'WOW!',
                description = f'The answer is {self.favNumber}, my favorite number!',
                color = discord.Color.from_rgb(255, 215, 0)
            )
            await ctx.send(embed=embed)
            return
        embed = embedMessage.embed(
            title = 'SUCCESS',
            description = f'The answer is {ans}.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

    ## Listener defining
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild.me.id != msg.author.id:
            if msg.content.startswith(self.listenFor):
                await msg.reply(self.replyWith)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(exampleCog(bot))
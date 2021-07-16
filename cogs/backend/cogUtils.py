## Initialization
import discord
from common import embedMessage
from discord.ext import commands

## Cog utility commands
class cogUtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = True
    
    ## Reload a cog
    @commands.command(aliases=['r', 'reloadCog', 'reloadCommand'])
    @commands.is_owner()
    async def reload(self, ctx, *, name: str):
        try:
            self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = f'**{name}** could not be reloaded: \n```{e}```',
                color = embedMessage.errorColor
            )
            return await ctx.send(embed=embed)
        embed = embedMessage.embed(
            title = 'SUCCESS',
            description = f'**{name}** was reloaded.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

    ## Unload a cog
    @commands.command(aliases=['u', 'unloadCog', 'unloadCommand'])
    @commands.is_owner()
    async def unload(self, ctx, *, name: str):
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = f'**{name}** could not be unloaded: \n```{e}```',
                color = embedMessage.errorColor
            )
            return await ctx.send(embed=embed)
        embed = embedMessage.embed(
            title = 'SUCCESS',
            description = f'**{name}** was unloaded.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

    ## Load a new cog
    @commands.command(aliases=['l', 'loadCog', 'loadCommand'])
    @commands.is_owner()
    async def load(self, ctx, *, name: str):
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            embed = embedMessage.embed(
                title = 'ERROR',
                description = f'**{name}** could not be loaded: \n```{e}```',
                color = embedMessage.errorColor
            )
            return await ctx.send(embed=embed)
        embed = embedMessage.embed(
            title = 'Load complete!',
            description = f'Cog **{name}** was loaded.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(cogUtilsCog(bot))

## Initialization
import discord
from discord.ext import commands, tasks
from common import embedMessage

## Cog utility commands
class cogUtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.hidden = True
    
    ## Reload a cog
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, name: str):
        try:
            self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        embed = embedMessage.embed(
            title = 'Reload complete!',
            description = f'Cog **{name}** was reloaded.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

    ## Unload a cog
    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, name: str):
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        embed = embedMessage.embed(
            title = 'Unload complete!',
            description = f'Cog **{name}** was unloaded.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

    ## Load a new cog
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, name: str):
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        embed = embedMessage.embed(
            title = 'Load complete!',
            description = f'Cog **{name}** was loaded.',
            color = embedMessage.defaultColor
        )
        await ctx.send(embed=embed)

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(cogUtilsCog(bot))

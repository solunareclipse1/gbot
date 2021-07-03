## Initialization
import os
import discord
from common import config, log
from discord.ext import commands

## Constants and Config
intents = discord.Intents.default()

## Define gBot
class gBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_command('help')

        ## Load Cogs - Modules in ./cogs directory
        for file in os.listdir("./cogs"):                                     # List contents of ./cogs
            if file.endswith(".py") and not file=="help.py":                  # Find ".py" files
                name = file[:-3]                                              # Trim ".py" from string
                self.load_extension(f"cogs.{name}")                           # Load Cog

    ## Log to console when ready
    async def on_ready(self):
        self.load_extension(f"cogs.help")
        log.log('--------------------------------')
        log.log('Bot Ready.')
        log.log(f'Logged in as {self.user.name}')
        log.log(f'User ID: {self.user.id}')
        log.log('--------------------------------')


## Create instance of gBot using config.cfg['discord']['token']
client = gBot(command_prefix = config.cfg['options']['prefix'], intents=intents)
client.run(config.cfg['discord']['token'])
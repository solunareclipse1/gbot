## Initialization
import os
import re
import discord
from common import config, log, player
from discord.ext import commands

## Constants and Config
intents = discord.Intents.default()

## Define gBot
class gBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_command('help')

        ## Load Cogs - Modules in ./cogs directory
        for root, subdirs, files in os.walk("./cogs"):
            if not ("__pycache__" in root):
                for file in files:
                    if file.endswith(".py") and not (file == "help.py"):
                        name = file[:-3]
                        parent = ".".join(re.findall(r"\w+",root))
                        self.load_extension(f"{parent}.{name}")

        self.player = player.player()

    ## Log to console when ready
    async def on_ready(self):
        self.load_extension(f"cogs.Info.help")
        log.log('--------------------------------')
        log.log('Bot Ready.')
        log.log(f'Logged in as {self.user.name}')
        log.log(f'User ID: {self.user.id}')
        log.log('--------------------------------')



## Create instance of gBot using config.cfg['discord']['token']
client = gBot(command_prefix = config.cfg['options']['prefix'], intents=intents)
client.run(config.cfg['discord']['token'])
import discord

async def mute(target: discord.Member, reason = 'None given.'):
    muteOverwrite = discord.PermissionOverwrite()
    muteOverwrite.add_reactions = False
    muteOverwrite.send_messages = False
    muteOverwrite.speak = False
    muteOverwrite.stream = False
    for channel in target.guild.channels:
        await channel.set_permissions(target, overwrite=muteOverwrite, reason=reason)

async def unmute(target: discord.Member, reason = 'None given.'):
    for channel in target.guild.channels:
        await channel.set_permissions(target, overwrite=None, reason=reason)
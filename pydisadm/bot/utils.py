import discord

def check_allowed_channel(channel, allowed_channel):
    if allowed_channel == None:
        return True
    if isinstance(channel, discord.channel.PartialMessageable):
        return True
    if channel.name == allowed_channel:
        return True
    return 


def text_channels_with_send_permission(bot):
    for guild in bot.guilds:
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(channel.guild.me).send_messages:
                yield channel

"""Bot utility functions"""
import discord

def check_allowed_channel(channel, allowed_channel):
    """Check if bot is allowed to respond in channel"""
    if allowed_channel is None:
        return True
    if isinstance(channel, discord.channel.PartialMessageable):
        return True
    if channel.name == allowed_channel:
        return True
    return False

def text_channels_with_send_permission(bot):
    """List of channels with send message permissions"""
    for guild in bot.guilds:
        for channel in guild.channels:
            if (isinstance(channel, discord.TextChannel) and
                channel.permissions_for(channel.guild.me).send_messages):
                yield channel

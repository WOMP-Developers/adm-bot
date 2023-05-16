import os

class Configuration:
    """App configuration variables"""

    def __init__(self):
        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.discord_channel = os.getenv('DISCORD_CHANNEL')
        self.discord_app_id = os.getenv('DISCORD_APP_ID')

        alliance_id = os.getenv('ALLIANCE_ID')
        if alliance_id != None:
            self.alliance_id = int(alliance_id)

    def __str__(self):
        return '{}(discord_token={}, discord_channel={}, discord_app_id={}, alliance_id={})'.format(
            self.__class__.__name__, self.discord_token, self.discord_channel, self.discord_app_id, self.alliance_id
        )

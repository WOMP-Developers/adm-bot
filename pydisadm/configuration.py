"""Application configuration"""

import os

class Configuration:
    """App configuration variables"""

    DB_SERVICES = ['sqlite', 'mysql']

    def __init__(self):

        self.discord = {
            'token': os.getenv('DISCORD_TOKEN'),
            'channel': os.getenv('DISCORD_CHANNEL'),
            'app_id': os.getenv('DISCORD_APP_ID'),
            'guild_id': os.getenv('DISCORD_GUILD_ID')
        }

        self.database = {
            'service': os.getenv('DB_SERVICE', 'sqlite'),
            'connection_string': os.getenv('DB_CONNECTION_STRING'),
            'keep_adm_days': os.getenv('DB_KEEP_ADM_DAYS', '7')
        }

        if self.database['service'] not in Configuration.DB_SERVICES:
            raise ValueError(
                f'[configuration] unsupported `DB_SERVICE`: {self.database["service"]}'
            )

        self.alliance = {
            'id': os.getenv('ALLIANCE_ID'),
            'ignore_tcu': os.getenv('ALLIANCE_IGNORE_TCU')
        }

        keep_adm_days = self.database['keep_adm_days']
        if keep_adm_days is not None:
            try:
                keep_adm_days = int(keep_adm_days)
            except ValueError as error:
                raise ValueError(
                    '[configuration] invalid `DB_KEEP_ADM_DAYS` value',
                    keep_adm_days) from error

        self.database['keep_adm_days'] = keep_adm_days

        alliance_id = self.alliance['id']
        if alliance_id is not None:
            try:
                alliance_id = int(alliance_id)
            except ValueError as error:
                raise ValueError(
                    '[configuration] invalid `ALLIANCE_ID` value',
                    alliance_id) from error

        self.alliance['id'] = alliance_id

    def pretty_print(self):
        """Create printable string from configuration"""
        return (f'{self.__class__.__name__}' +
            f'(discord_token={self.discord["token"]}, ' +
            f'discord_channel={self.discord["channel"]}, ' +
            f'discord_app_id={self.discord["app_id"]}, ' +
            f'discord_guild_id={self.discord["guild_id"]}, ' +
            f'alliance_id={self.alliance["id"]}, ' +
            f'alliance_ignore_tcu={self.alliance["ignore_tcu"]}, ' +
            f'db_keep_adm_days={self.database["keep_adm_days"]}, ' +
            f'db_service={self.database["service"]}, ' +
            f'db_connection_string={self.database["connection_string"]})')

    def __str__(self):
        return self.pretty_print()

import os

class Configuration:
    """App configuration variables"""

    def __init__(self):
        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.discord_channel = os.getenv('DISCORD_CHANNEL')
        self.discord_app_id = os.getenv('DISCORD_APP_ID')
        self.discord_guild_id = os.getenv('DISCORD_GUILD_ID')

        alliance_id = os.getenv('ALLIANCE_ID')

        db_keep_adm_days = os.getenv('DB_KEEP_ADM_DAYS', '7')
        if db_keep_adm_days is not None:
            try:
                db_keep_adm_days = int(db_keep_adm_days)
            except ValueError as error:
                raise ValueError(
                    '[configuration] invalid `DB_KEEP_ADM_DAYS` value',
                    db_keep_adm_days) from error

        self.db_keep_adm_days = db_keep_adm_days

        if alliance_id is not None:
            try:
                alliance_id = int(alliance_id)
            except ValueError as error:
                raise ValueError(
                    '[configuration] invalid `ALLIANCE_ID` value',
                    alliance_id) from error

        self.alliance_id = alliance_id

    def __str__(self):
        return (f'{self.__class__.__name__}' +
            f'(discord_token={self.discord_token}, ' +
            f'discord_channel={self.discord_channel}, ' +
            f'discord_app_id={self.discord_app_id}, ' +
            f'discord_guild_id={self.discord_guild_id}, ' +
            f'alliance_id={self.alliance_id} ' +
            f'db_keep_adm_days={self.db_keep_adm_days})')

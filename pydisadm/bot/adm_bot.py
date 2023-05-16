import asyncio
import discord
from discord.ext import commands

from pydisadm.bot.adm_cog import Adm
from pydisadm.configuration import Configuration
from pydisadm.controller.adm_controller import AdmController

def create_intents():
    intents = discord.Intents.default()
    intents.message_content = True
    return intents

class AdmBot:
    def __init__(self, configuration: Configuration, controller: AdmController):
        self.configuration = configuration
        self.controller = controller

        intents = create_intents()
        self.bot = commands.Bot(application_id=configuration.discord_app_id, command_prefix=None, intents=intents, help_command=None)
    
    async def setup_cogs_async(self):
        await self.bot.add_cog(Adm(self.bot, self.configuration, self.controller))

    def setup_cogs(self):
        return asyncio.run(self.setup_cogs_async())
    
    async def sync_commands_async(self):
        await self.bot.tree.sync()

    def sync_commands(self):
        return asyncio.run(self.sync_commands_async())

    def run(self):
        self.bot.run(self.configuration.discord_token)

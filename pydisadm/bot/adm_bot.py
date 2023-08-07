"""Discord bot collecting and posting ADM summaries."""

import asyncio
import discord
from discord.ext import commands

from pydisadm.bot.adm_cog import Adm
from pydisadm.configuration import Configuration
from pydisadm.controller.adm_controller import AdmController

def create_intents():
    """Create discord intents for bot."""
    intents = discord.Intents.default()
    intents.message_content = True
    return intents

class AdmBot:
    """Discord bot collecting and posting ADM summaries."""

    def __init__(self, configuration: Configuration, controller: AdmController):
        self.configuration = configuration
        self.controller = controller

        intents = create_intents()
        self.bot = commands.Bot(
            application_id=configuration.discord['app_id'],
            command_prefix='!',
            intents=intents,
            help_command=None
        )

    async def setup_cogs_async(self):
        """Asynchronously setup cogs"""
        await self.bot.add_cog(Adm(self.bot, self.configuration, self.controller))

    def setup_cogs(self):
        """Setup cogs"""
        return asyncio.run(self.setup_cogs_async())

    async def sync_commands_async(self):
        """Asynchronously synchronize command tree"""
        await self.bot.tree.sync()

    def sync_commands(self):
        """Synchronize command tree"""
        return asyncio.run(self.sync_commands_async())

    def run(self):
        """Run the bot, this function is blocking"""
        self.bot.run(self.configuration.discord['token'])

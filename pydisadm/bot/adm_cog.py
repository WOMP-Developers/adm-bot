"""Cog providing ADM related commands"""

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
import pydisadm
from pydisadm.bot.update_adm_modal import UpdateAdmModal

from pydisadm.bot.utils import check_allowed_channel, text_channels_with_send_permission
from pydisadm.configuration import Configuration
from pydisadm.controller.adm_controller import AdmController
from pydisadm.utils.datetime_utils import convert_to_local_timestamp

class Adm(commands.GroupCog):
    """Cog providing ADM related commands"""
    def __init__(self, bot, configuration: Configuration, controller: AdmController):
        self.bot = bot
        self.configuration = configuration
        self.controller = controller

    async def send_tier_list_summary(self, interaction: discord.Interaction):
        """Send a summary of ADMs organized as a tier list"""
        await interaction.response.defer(thinking=True)

        (tier_list, generated_at) = self.controller.generate_tier_list()
        if generated_at is None:
            await interaction.followup.send('😥 No ADM data...')
            return

        timestamp = convert_to_local_timestamp(generated_at)

        file_name = "adm_tier_list.txt"

        with open(file_name, 'w', encoding='UTF-8') as file:
            file.write(tier_list)

        if self.controller.write_file(file_name, tier_list):
            await interaction.followup.send(
                file=discord.File(file_name),
                content=f'ADM @ <t:{timestamp}:F>'
            )
            self.controller.delete_file(file_name)

    async def send_system_graph(self, interaction: discord.Interaction, what: str):
        """Send a graph of ADMs matching name"""
        await interaction.response.defer(thinking=True)

        file_name = 'adm_history.png'
        if self.controller.create_history_graph(what, file_name):
            await interaction.followup.send(
                file=discord.File(file_name),
                content=f"ADM History of {what}"
            )
            self.controller.delete_file(file_name)
        else:
            await interaction.followup.send('😥 No ADM data...')

    async def update_adm(self, interaction: discord.Interaction, system_name: str, adm: float):
        """Update ADM for system"""
        await interaction.response.defer(thinking=True)

        if adm <= 0.0 or adm > 6.0:
            await interaction.followup.send(f"Invalid ADM: {adm} (1.0-6.0 valid)")
            return

        if not self.controller.update_system_adm(system_name, adm):
            await interaction.followup.send(f"Couldn't update ADM for {system_name} to {adm}")
        else:
            await interaction.followup.send(f"Manually updated {system_name} ADM to {adm}")

    @app_commands.command(description='Recommend where to raise ADM')
    async def recommend(self, interaction: discord.Interaction):
        """Command recommending which system to raise ADMs"""
        if not check_allowed_channel(interaction.channel, self.configuration.discord['channel']):
            await interaction.response.send_message('Not allowed in this channel.', ephemeral=True)
            return

        await interaction.response.defer()

        recommended_system = self.controller.get_recommended_system()
        if recommended_system is None:
            await interaction.followup.send('😥 No ADM data...')
            return

        system = recommended_system['solarSystemName']
        region = recommended_system['regionName']

        await interaction.followup.send(f'🦀 `{system} in {region}`', tts=True)

    @app_commands.command(description='Posts a summary of all system ADM levels')
    async def summary(self, interaction: discord.Interaction):
        """Command posting a summary of ADMs"""
        if not check_allowed_channel(interaction.channel, self.configuration.discord['channel']):
            await interaction.response.send_message('Not allowed in this channel.', ephemeral=True)
            return

        await self.send_tier_list_summary(interaction)

    @app_commands.command(description='Posts a CSV file of all system ADM levels')
    async def csv(self, interaction: discord.Interaction):
        """Command posting a CSV file of ADMs"""
        if not check_allowed_channel(interaction.channel, self.configuration.discord['channel']):
            await interaction.response.send_message('Not allowed in this channel.', ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        file_name = "adm_summary.csv"
        if self.controller.create_spreadsheet(file_name):
            await interaction.followup.send(file=discord.File(file_name), content='ADM Spreadsheet')
            self.controller.delete_file(file_name)

    @app_commands.command(description='Post a graph of system ADM.')
    @app_commands.describe(where='The system, constellation, or region to graph.')
    async def history(self, interaction: discord.Interaction, where: str):
        """Command posting a graph of ADM history"""
        if not check_allowed_channel(interaction.channel, self.configuration.discord['channel']):
            await interaction.response.send_message('Not allowed in this channel.', ephemeral=True)
            return

        await self.send_system_graph(interaction, where)

    @app_commands.command(description='Manually refresh all ADM data.')
    async def refresh(self, interaction: discord.Interaction):
        """Command to manually refresh ADM data"""
        if not check_allowed_channel(interaction.channel, self.configuration.discord['channel']):
            await interaction.response.send_message('Not allowed in this channel.', ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        self.controller.update_adm_data()
        await interaction.followup.send("ADM data manually refreshed 🦀")

    @app_commands.command(description='Manually update ADM of system.')
    @app_commands.describe(system_name='Which system to update ADM')
    async def update(self, interaction: discord.Interaction, system_name: str):
        """Command to manually update ADM for system"""
        if not check_allowed_channel(interaction.channel, self.configuration.discord['channel']):
            await interaction.response.send_message('Not allowed in this channel.', ephemeral=True)
            return

        await interaction.response.send_modal(UpdateAdmModal(system_name, self.controller))

    @commands.Cog.listener()
    async def on_ready(self):
        """cog on_ready event callback"""
        channels = text_channels_with_send_permission(self.bot)

        valid_channels = [
            channel for channel in channels if channel.name == self.configuration.discord['channel']
        ]

        embed = discord.Embed(title=f'🦀 ADM Bot v{pydisadm.__version__}')
        embed.add_field(name='Summary', value='/adm summary')
        embed.add_field(name='CSV', value='/adm csv')
        embed.add_field(name='History', value='/adm history <name>')
        embed.add_field(name='Update', value='/adm update <system>')
        embed.add_field(name='Recommend', value='/adm recommend')
        embed.add_field(name='Refresh', value='/adm refresh')
        embed.add_field(name='Source', value='[github](https://github.com/agelito/adm-bot)')

        for channel in valid_channels:
            await channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def adm_sync_commands(self, ctx: Context):
        """synchronize slash commands"""

        if self.configuration.discord['guild_id']:
            guild = discord.Object(id=self.configuration.discord['guild_id'])
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)
        else:
            await self.bot.tree.sync()

        await ctx.send('Synchronized bot commands.')

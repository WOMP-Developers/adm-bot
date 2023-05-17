"""Modal dialog for updating ADM"""
import discord
from discord import ui

from pydisadm.controller.adm_controller import AdmController

class UpdateAdmModal(ui.Modal):
    """Modal dialog for updating ADM"""
    def __init__(self, system_name: str, controller: AdmController):
        super().__init__(title=f"Update {system_name} ADM")
        self.system_name = system_name
        self.controller = controller

    strategic_index = ui.TextInput(label='Strategic Index')
    military_index = ui.TextInput(label='Military Index')
    industry_index = ui.TextInput(label='Industry Index')

    # pylint: disable=arguments-differ
    async def on_submit(self, interaction: discord.Interaction):
        """on_submit callback"""

        try:
            strategic = int(self.strategic_index.value)
        except ValueError:
            await interaction.response.send_message(
                f'Strategic index not a number: {self.strategic_index}',
                ephemeral=True)
            return

        try:
            military = int(self.military_index.value)
        except ValueError:
            await interaction.response.send_message(
                f'Military index not a number: {self.military_index}',
                ephemeral=True)
            return

        try:
            industrial = int(self.industry_index.value)
        except ValueError:
            await interaction.response.send_message(
                f'Industrial index not a number: {self.industry_index}',
                ephemeral=True)
            return

        if not 0 <= strategic <= 5:
            await interaction.response.send_message(
                f'Strategic intex out of range: {self.strategic_index}',
                ephemeral=True)
            return

        if not 0 <= military <= 5:
            await interaction.response.send_message(
                f'Military index out of range: {self.military_index}',
                ephemeral=True)
            return

        if not 0 <= industrial <= 5:
            await interaction.response.send_message(
                f'Industrial index out of range: {self.industry_index}',
                ephemeral=True)
            return

        await interaction.response.defer()

        (result, adm) = self.controller.update_system_adm_from_index(
            self.system_name, military, industrial, strategic)

        if not result:
            await interaction.followup.send(
                f'Unable to update ADM for system: {self.system_name}',
                ephemeral=True)
        else:
            await interaction.followup.send(f'Updated ADM: **{self.system_name}** -> **{adm}**')

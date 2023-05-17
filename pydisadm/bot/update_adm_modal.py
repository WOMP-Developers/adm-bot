"""Modal dialog for updating ADM"""
import discord
from discord import ui

class UpdateAdmModal(ui.Modal):
    """Modal dialog for updating ADM"""
    def __init__(self, system_name: str):
        super().__init__(title=f"Update {system_name} ADM")
        self.system_name = system_name

    strategic_index = ui.TextInput(label='Strategic Index')
    military_index = ui.TextInput(label='Military Index')
    industry_index = ui.TextInput(label='Industry Index')

    # pylint: disable=arguments-differ
    async def on_submit(self, interaction: discord.Interaction):
        """on_submit callback"""
        await interaction.response.send_message(
            f'Update {self.system_name} with s:{self.strategic_index}\
            m:{self.military_index} i:{self.industry_index}'
        )

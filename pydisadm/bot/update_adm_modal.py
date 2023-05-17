import discord
from discord import ui

class UpdateAdmModal(ui.Modal, title="Update ADM"):
    system = ui.TextInput(label='System')
    strategic_index = ui.TextInput(label='Strategic Index')
    military_index = ui.TextInput(label='Military Index')
    industry_index = ui.TextInput(label='Industry Index')

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Update {self.system} with s:{self.strategic_index} m:{self.military_index} i:{self.industry_index}')
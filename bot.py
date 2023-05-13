#!/usr/bin/env python

import discord
import os
import threading
import signal
import sys
from discord.ext import commands
from adm.commands import create_spreadsheet, create_summary, create_system_graph, update_adm_data
from adm.configuration import Configuration
from adm.database import Database
from adm.dateutils import convert_to_local_timestamp
from adm.service import create_system_adm
from adm.static_data import update_static_data
from auto_refresh import threaded_auto_refresh 
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

configuration = Configuration()
database = Database()

interrupt_event = threading.Event()

async def send_system_graph(ctx, system_name):
    file_path = create_system_graph(database, system_name)
    if file_path:
        await ctx.send(file=discord.File(file_path), content=f"{system_name}: Historic Data")
        os.remove(file_path)

    else:
        await ctx.send(f"{system_name}: No data (╯°□°）╯︵ ┻━┻")

async def send_summary(ctx):
    file_name = "adm_summary.txt"
    generated_at = create_summary(database, file_name)
    timestamp = convert_to_local_timestamp(generated_at)

    if os.path.isfile(file_name):
        await ctx.send(file=discord.File(file_name), content=f'ADM @ <t:{timestamp}:F>')
        os.remove(file_name)

async def send_csv(user):
    file_name = "adm_summary.csv"
    generated_at = create_spreadsheet(database, file_name)
    timestamp = convert_to_local_timestamp(generated_at)

    if os.path.isfile(file_name):
        await user.send(file=discord.File(file_name), content=f'ADM @ <t:{timestamp}:F>')
        os.remove(file_name)

async def refresh(ctx):
    await ctx.send("Refreshing ADM data... 🚧")
    update_adm_data(configuration, database)
    await ctx.send("ADM data manually refreshed 🦀")

async def update_adm(ctx, system_name, adm: float):
    system = database.select_system_with_name(system_name)
    if system.empty:
        await ctx.send(f"No system with name: {system_name}")
        return

    adm = float(adm)

    if adm <= 0.0 or adm > 6.0:
        await ctx.send(f"Invalid ADM: {adm} (1.0-6.0 valid)")
        return
    
    insert_systems = create_system_adm(system, adm)

    database.insert_systems(insert_systems)

    await ctx.send(f"Manually updated {system_name} ADM to {adm}")

help_text = """
Summary:
  ADM bot collects ADM values daily from the EVE API.
  Users can send commands to show ADM data.

Usage:
  `!adm` - post summary of all systems
  `!adm csv` - post CSV file of all systems
  `!adm <system>` - post graph of system ADM
  `!adm update <system> <adm>` - manually set adm for system
  `!adm refresh` - manually refresh all adm data
  `!adm help` - display this message
"""

@bot.event
async def on_ready():
    for guild in bot.guilds:
        for channel in guild.channels:
            if (isinstance(channel, discord.TextChannel) and
                channel.permissions_for(guild.me).send_messages and
                channel.name == configuration.discord_channel
            ):
                await channel.send(f"=== ADM Bot is started 🦀 ===\n{help_text}")

@bot.command(name='adm')
async def command_adm(ctx, *args):
    if (not isinstance(ctx.channel, discord.channel.DMChannel) and
        configuration.discord_channel and
        ctx.channel.name != configuration.discord_channel
    ): return

    if len(args) == 0:
        await send_summary(ctx)
        return
    
    if args[0] == 'help':
        await ctx.send(help_text)
        return
    
    if len(args) == 3 and args[0] == 'update':
        await update_adm(ctx, args[1], args[2])
        return
    
    for arg in args:
        if arg == 'refresh':
            await refresh(ctx)
        elif arg == 'csv':
            await send_csv(ctx)
        else:
            await send_system_graph(ctx, arg)

def signal_handler(sig, frame):
    interrupt_event.set()
    print('Interrupted by CTRL+C')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

update_static_data(database)
update_adm_data(configuration, database)
threaded_auto_refresh(interrupt_event)

bot.run(configuration.discord_token)

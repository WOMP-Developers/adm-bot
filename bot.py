#!/usr/bin/env python

from zoneinfo import ZoneInfo
import discord
import os
import threading
import signal
import sys
import time
from discord.ext import commands
from adm.commands import create_spreadsheet, create_summary, create_system_graph, update_adm_data
from adm.configuration import Configuration
from adm.database import Database
from adm.static_data import update_static_data
from auto_refresh import threaded_auto_refresh 
from dotenv import load_dotenv
from datetime import datetime
from dateutil.tz import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

configuration = Configuration()
database = Database()

interrupt_event = threading.Event()

def convert_to_local_timestamp(date):
    generated_utc_date = datetime.fromisoformat(date)
    generated_utc_date = generated_utc_date.replace(tzinfo=tzutc())

    generated_local_date = generated_utc_date.astimezone(tzlocal())

    return int(time.mktime(generated_local_date.timetuple()))


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

async def send_csv(ctx):
    file_name = "adm_summary.csv"
    generated_at = create_spreadsheet(database, file_name)
    timestamp = convert_to_local_timestamp(generated_at)

    if os.path.isfile(file_name):
        await ctx.send(file=discord.File(file_name), content=f'ADM @ <t:{timestamp}:F>')
        os.remove(file_name)

async def refresh(ctx):
    await ctx.send("Refreshing ADM data... 🚧")
    update_adm_data(configuration, database)
    await ctx.send("ADM data manually refreshed 🚀")

@bot.command(name='adm')
async def command_adm(ctx, *args):
    if len(args) == 0:
        await send_summary(ctx)
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

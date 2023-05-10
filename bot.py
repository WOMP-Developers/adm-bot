import discord
import os
import threading
import signal
import sys
from discord.ext import commands
from adm.commands import create_summary, create_system_graph, refresh_data
from adm.configuration import Configuration
from adm.database import Database
from auto_refresh import threaded_auto_refresh 

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
    title = create_summary(database, file_name)

    if os.path.isfile(file_name):
        await ctx.send(file=discord.File(file_name), content=title)
        os.remove(file_name)

async def refresh(ctx):
    refresh_data(configuration, database)
    await ctx.send("ADM data manually refreshed 🚀")

@bot.command(name='adm')
async def command_adm(ctx, *args):
    if len(args) == 0:
        await send_summary(ctx)
        return
    
    for arg in args:
        if arg == 'refresh':
            await refresh(ctx)
        else:
            await send_system_graph(ctx, arg)

def signal_handler(sig, frame):
    interrupt_event.set()
    print('Interrupted by CTRL+C')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

refresh_data(configuration, database)
threaded_auto_refresh(interrupt_event, configuration, database)

bot.run(configuration.discord_token)

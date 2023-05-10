from operator import index
import os
import requests
from tokenize import Token
import discord
from dotenv import load_dotenv
from discord.ext import commands 
import pandas as pd
from tabulate import tabulate
import datetime

load_dotenv()
token = os.getenv('TOKEN') # get discord token in .env file
channel = os.getenv('DISCORD_CHANNEL')
sigmaid = 99011223  # Hard coded, do not change

ints = discord.Intents.default()
ints.message_content = True
client = discord.Client(intents=ints)
bot = commands.Bot(command_prefix='!', intents=ints)

def get_esi_adm(alliance_id):
    list_ids = [alliance_id]

    try:
        name_url = "https://esi.evetech.net/latest/universe/names/?datasource=tranquility"          # Get Alliance Name
        struc_url = "https://esi.evetech.net/latest/sovereignty/structures/?datasource=tranquility" # Get All Structures in game

        struc_resp = requests.get(struc_url)
        struc_json = struc_resp.json()
    except:
        print('Error connecting to EVE ESI')

    try:
        # Get list of solar system ids and its adm maching alliance_id
        adms = {}
        for s in struc_json:
            if s['alliance_id'] == alliance_id:
                if 'vulnerability_occupancy_level' in s:
                    adms[s['solar_system_id']] = s['vulnerability_occupancy_level']

        sysid = []
        for x, y in adms.items():
            sysid.append(x)

        sysnames_response = requests.post(name_url, json=sysid)
        sys_json = sysnames_response.json()

        name_ids = {}
        for name in sys_json:
            name_ids[name['id']] = name['name']

        dfADM = pd.DataFrame(adms.items())
        dfNameID = pd.DataFrame(name_ids.items())
        dfADM_ID = dfADM.merge(dfNameID, left_on=0, right_on=0, how='inner', sort=True)
        df_final = dfADM_ID[['1_x','1_y']].sort_values(['1_x','1_y'])
        df_final.rename(columns={'1_x':'ADM', '1_y':'SYSTEM'}, inplace=True)
        return (df_final, datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
    except:
        print('Error creating dataframes')

@bot.command(name='adm')
async def command_adm(ctx):
    try:
        (df_final, date) = get_esi_adm(sigmaid)
        response = "```" + tabulate(df_final, showindex=False, headers='keys',tablefmt='pipe',numalign='left',stralign='center') + '\n\nGenerated at: ' + date + "```"
        await ctx.send(response)
    except KeyError:
        await ctx.send('Error getting ADM data')

async def on_ready(ctx):
    await ctx.send('ADM Bot is ready!')

try:
    bot.run(token)
except:
    print('Error running bot program')
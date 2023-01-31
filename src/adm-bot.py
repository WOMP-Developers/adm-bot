from operator import index
import os
import requests
from tokenize import Token
import discord
from dotenv import load_dotenv
from discord.ext import commands 
from numpy import true_divide
import pandas as pd
from tabulate import tabulate

load_dotenv()
token = os.getenv('TOKEN') # get discord token in .env file
channel = os.getenv('DISCORD_CHANNEL')

ints = discord.Intents.default()
ints.message_content = True
client = discord.Client(intents=ints)
bot = commands.Bot(command_prefix='!', intents=ints)

sigmaid = 99011223  # Hard coded, do not change
list_ids = [sigmaid]

try:
    name_url = "https://esi.evetech.net/latest/universe/names/?datasource=tranquility"          # Get Alliance Name
    struc_url = "https://esi.evetech.net/latest/sovereignty/structures/?datasource=tranquility" # Get All Structures in game

    name_response = requests.post(name_url, json=list_ids)
    struc_resp = requests.get(struc_url)
    names = name_response.json()
    struc_json = struc_resp.json()
except:
    print('Error connecting to EVE ESI')

try:
    # Get list of SIGMA solar system ids and its adm
    adms = {}
    for s in struc_json:
        if s['alliance_id'] == sigmaid:
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
except:
    print('Error creating dataframes')

# print(df_final)

@bot.command(name='adm')
async def on_ready(ctx):
    try:
        response = "```" + tabulate(df_final, showindex=False, headers='keys',tablefmt='pipe',numalign='left',stralign='center') + "```"
        await ctx.send(response)
    except KeyError as exception:
        await ctx.send('Error getting ADM data')

try:
    bot.run(token)
except:
    print('Error running bot program')

from adm.graphs import plot_save, plot_system_adm
from adm.service import get_system_adms
from tabulate import tabulate
import pandas as pd

def update_adm_data(configuration, database):
    system_adms = get_system_adms(configuration.alliance_id)

    database.insert_systems(system_adms)

def create_system_graph(database, system_name):
    system_history = database.select_system_history(system_name, 10)

    if plot_system_adm(system_history):
        return plot_save(system_name)
    
    return None

def create_summary(database, file_name):
    system_adms = database.select_systems()
    
    system_adms.sort_values(by='adm', inplace=True, ascending=True)
    
    s_tier = system_adms.loc[system_adms['tier'] == 's_tier']
    a_tier = system_adms.loc[system_adms['tier'] == 'a_tier']
    b_tier = system_adms.loc[system_adms['tier'] == 'b_tier']
    c_tier = system_adms.loc[system_adms['tier'] == 'c_tier']
    d_tier = system_adms.loc[system_adms['tier'] == 'd_tier']

    sorted_summary = [
        {'Tier': 'D', 'Systems': '\n'.join(d_tier['solarSystemName']), 'ADM': '\n'.join(d_tier['adm'].map(lambda v: str(v))), 'Constellation': '\n'.join(d_tier['constellationName']), 'Region': '\n'.join(d_tier['regionName'])},
        {'Tier': 'C', 'Systems': '\n'.join(c_tier['solarSystemName']), 'ADM': '\n'.join(c_tier['adm'].map(lambda v: str(v))), 'Constellation': '\n'.join(c_tier['constellationName']), 'Region': '\n'.join(c_tier['regionName'])},
        {'Tier': 'B', 'Systems': '\n'.join(b_tier['solarSystemName']), 'ADM': '\n'.join(b_tier['adm'].map(lambda v: str(v))), 'Constellation': '\n'.join(b_tier['constellationName']), 'Region': '\n'.join(b_tier['regionName'])},
        {'Tier': 'A', 'Systems': '\n'.join(a_tier['solarSystemName']), 'ADM': '\n'.join(a_tier['adm'].map(lambda v: str(v))), 'Constellation': '\n'.join(a_tier['constellationName']), 'Region': '\n'.join(a_tier['regionName'])},
        {'Tier': 'S', 'Systems': '\n'.join(s_tier['solarSystemName']), 'ADM': '\n'.join(s_tier['adm'].map(lambda v: str(v))), 'Constellation': '\n'.join(s_tier['constellationName']), 'Region': '\n'.join(s_tier['regionName'])}
    ]

    table = tabulate(sorted_summary, showindex=False, headers='keys', tablefmt='fancy_grid',numalign='left',stralign='center')

    generated_at = database.select_most_recent_row()

    with open(file_name, 'w', encoding='UTF-8') as f:
        f.write(table)

    return generated_at['created_at'][0]

def create_spreadsheet(database, filename):
    system_adms = database.select_systems()
    system_adms.sort_values(by='adm', inplace=True, ascending=False)

    system_adms.to_csv(filename, index=False, columns=['system_id','adm','tier','created_at','solarSystemName','constellationName','regionName'])

    generated_at = database.select_most_recent_row()

    return generated_at['created_at'][0]

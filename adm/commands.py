
from adm.graphs import plot_save, plot_system_adm
from adm.service import get_system_adms
from tabulate import tabulate
import pandas as pd

def refresh_data(configuration, database):
    system_adms = get_system_adms(configuration.alliance_id)

    database.insert_systems(system_adms)

def create_system_graph(database, system_name):
    o4t = database.select_system_history(system_name, 5)

    if plot_system_adm(o4t):
        plot_save(system_name)

def print_summary(database):
    system_adms = database.select_systems()
    

    system_adms.sort_values(by='adm', inplace=True, ascending=False)
    
    s_tier = system_adms.loc[system_adms['tier'] == 's_tier']
    a_tier = system_adms.loc[system_adms['tier'] == 'a_tier']
    b_tier = system_adms.loc[system_adms['tier'] == 'b_tier']
    c_tier = system_adms.loc[system_adms['tier'] == 'c_tier']
    d_tier = system_adms.loc[system_adms['tier'] == 'd_tier']

    sorted_summary = [
        {'Tier': 'S', 'Systems': '\n'.join(s_tier['name']), 'ADM': '\n'.join(s_tier['adm'].map(lambda v: str(v)))},
        {'Tier': 'A', 'Systems': '\n'.join(a_tier['name']), 'ADM': '\n'.join(a_tier['adm'].map(lambda v: str(v)))},
        {'Tier': 'B', 'Systems': '\n'.join(b_tier['name']), 'ADM': '\n'.join(b_tier['adm'].map(lambda v: str(v)))},
        {'Tier': 'C', 'Systems': '\n'.join(c_tier['name']), 'ADM': '\n'.join(c_tier['adm'].map(lambda v: str(v)))},
        {'Tier': 'D', 'Systems': '\n'.join(d_tier['name']), 'ADM': '\n'.join(d_tier['adm'].map(lambda v: str(v)))}
    ]

    table = tabulate(sorted_summary, showindex=False, headers='keys', tablefmt='fancy_grid',numalign='left',stralign='center')

    generated_at = database.select_most_recent_row()


    summary = f"""
    ```
    {table}
    ```

    Generated at: {generated_at['created_at'][0]}
    """

    print(summary)

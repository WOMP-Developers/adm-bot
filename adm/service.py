import pandas as pd
import numpy as np
from adm.esi import sovereignty_structures, universe_names

def get_alliance_structures(structures, alliance_id):
    df = pd.DataFrame.from_dict(structures)

    drop_columns = [
        'structure_id',
        'structure_type_id',
        'vulnerable_end_time',
        'vulnerable_start_time',
    ]

    df.drop(columns=drop_columns, inplace=True)

    return df[df['alliance_id'] == alliance_id]

def create_system_adm(system, adm):
    system_adm = pd.DataFrame(columns=['system_id', 'adm'])
    system_adm['system_id'] = system['solarSystemID']
    system_adm['adm'] = [ adm ]

    tier_list(system_adm)

    return system_adm

def get_system_adms(alliance_id):
    structures = sovereignty_structures()
    system_adms = get_alliance_structures(structures, alliance_id)

    system_adms.drop_duplicates(inplace=True)

    drop_columns = ['alliance_id']
    system_adms.drop(columns=drop_columns, inplace=True)

    rename_columns = {'solar_system_id':'system_id', 'vulnerability_occupancy_level':'adm'}
    system_adms.rename(columns=rename_columns, inplace=True)

    tier_list(system_adms)

    return system_adms

def tier_list(systems):
    conditions = [
        (systems['adm'] >= 6.0),
        (systems['adm'] >= 5.0) & (systems['adm'] < 6.0),
        (systems['adm'] >= 4.0) & (systems['adm'] < 5.0),
        (systems['adm'] >= 3.5) & (systems['adm'] < 4.0),
        (systems['adm'] < 3.5)
    ]

    values = [
        's_tier',
        'a_tier',
        'b_tier',
        'c_tier',
        'd_tier'
    ]

    systems['tier'] = np.select(conditions, values)

    return systems


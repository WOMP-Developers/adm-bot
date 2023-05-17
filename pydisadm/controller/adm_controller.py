"""Controller implementation for ADM operations"""
import os
import numpy as np
import pandas as pd
from tabulate import tabulate

from pydisadm.configuration import Configuration
from pydisadm.services.database import Database
from pydisadm.services.esi import sovereignty_structures
from pydisadm.utils.plot_utils import plot_adm_history_of_systems, plot_save_to_file


class AdmController:
    """Controller implementation for ADM operations"""

    def __init__(self, configuration: Configuration, database: Database):
        self.configuration = configuration
        self.database = database

    def generate_tier_list(self):
        """Generate a system tier list based on tier values"""
        system_adms = self.database.select_systems()

        system_adms.sort_values(by='adm', inplace=True, ascending=True)

        s_tier = system_adms.loc[system_adms['tier'] == 's_tier']
        a_tier = system_adms.loc[system_adms['tier'] == 'a_tier']
        b_tier = system_adms.loc[system_adms['tier'] == 'b_tier']
        c_tier = system_adms.loc[system_adms['tier'] == 'c_tier']
        d_tier = system_adms.loc[system_adms['tier'] == 'd_tier']

        sorted_summary = [
            {'Tier': 'D', 'Systems': '\n'.join(d_tier['solarSystemName']),
             'ADM': '\n'.join(d_tier['adm'].map(str)),
             'Constellation': '\n'.join(d_tier['constellationName']),
             'Region': '\n'.join(d_tier['regionName'])},
            {'Tier': 'C', 'Systems': '\n'.join(c_tier['solarSystemName']),
             'ADM': '\n'.join(c_tier['adm'].map(str)),
             'Constellation': '\n'.join(c_tier['constellationName']),
             'Region': '\n'.join(c_tier['regionName'])},
            {'Tier': 'B', 'Systems': '\n'.join(b_tier['solarSystemName']),
             'ADM': '\n'.join(b_tier['adm'].map(str)),
             'Constellation': '\n'.join(b_tier['constellationName']),
             'Region': '\n'.join(b_tier['regionName'])},
            {'Tier': 'A', 'Systems': '\n'.join(a_tier['solarSystemName']),
             'ADM': '\n'.join(a_tier['adm'].map(str)),
             'Constellation': '\n'.join(a_tier['constellationName']),
             'Region': '\n'.join(a_tier['regionName'])},
            {'Tier': 'S', 'Systems': '\n'.join(s_tier['solarSystemName']),
             'ADM': '\n'.join(s_tier['adm'].map(str)),
             'Constellation': '\n'.join(s_tier['constellationName']),
             'Region': '\n'.join(s_tier['regionName'])}
        ]

        table = tabulate(sorted_summary, showindex=False, headers='keys',
                         tablefmt='fancy_grid', numalign='left', stralign='center')

        generated_at = self.database.select_most_recent_row()

        return (table, generated_at['created_at'][0])

    def create_history_graph(self, name, file_name):
        """Generate an ADM history graph and save to file"""
        systems_by_name = self.database.select_system_by_name(name)

        if plot_adm_history_of_systems(systems_by_name):
            plot_save_to_file('ADM History', file_name)

        return os.path.isfile(file_name)

    def create_spreadsheet(self, file_name):
        """Generate a spreadsheet of ADM data and save to file"""
        system_adms = self.database.select_systems()
        system_adms.sort_values(by='adm', inplace=True, ascending=False)

        csv_columns = [
            'system_id',
            'adm',
            'tier',
            'created_at',
            'solarSystemName',
            'constellationName',
            'regionName'
        ]

        system_adms.to_csv(file_name, index=False, columns=csv_columns)

        return os.path.isfile(file_name)

    def tier_list(self, systems):
        """Assign tier column based on system ADM"""
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

    def create_system_adm(self, system, adm):
        """Create a DataFrame for system ADM data"""
        system_adm = pd.DataFrame(columns=['system_id', 'adm'])
        system_adm['system_id'] = system['solarSystemID']
        system_adm['adm'] = [adm]

        self.tier_list(system_adm)

        return system_adm

    def get_alliance_structures(self, structures, alliance_id):
        """Retrieve a list of alliance sovreignty structures"""
        structure_data = pd.DataFrame.from_dict(structures)

        drop_columns = [
            'structure_id',
            'structure_type_id',
            'vulnerable_end_time',
            'vulnerable_start_time',
        ]

        structure_data.drop(columns=drop_columns, inplace=True)

        return structure_data[structure_data['alliance_id'] == alliance_id]

    def update_system_adm(self, system_name: str, adm: float) -> bool:
        """Update ADM for system with name"""
        system = self.database.select_system_with_name(system_name)

        if system.empty:
            return False

        insert_systems = self.create_system_adm(system, adm)

        self.database.insert_systems(insert_systems)

        return True

    def get_system_adms(self, alliance_id):
        """Retrieve ADM for systems controlled by alliance"""
        structures = sovereignty_structures()
        system_adms = self.get_alliance_structures(structures, alliance_id)

        system_adms.drop_duplicates(inplace=True)

        drop_columns = ['alliance_id']
        system_adms.drop(columns=drop_columns, inplace=True)

        rename_columns = {'solar_system_id': 'system_id',
                          'vulnerability_occupancy_level': 'adm'}
        system_adms.rename(columns=rename_columns, inplace=True)

        self.tier_list(system_adms)

        return system_adms

    def get_recommended_system(self):
        """Retrieve recommended system to raise ADM"""
        systems = self.database.select_systems()
        systems.sort_values(by='adm', inplace=True, ascending=True)

        return systems.iloc[0]

    def update_adm_data(self):
        """Update ADM data"""
        alliance_id = self.configuration.alliance_id
        system_adms = self.get_system_adms(alliance_id)

        self.database.insert_systems(system_adms)

    def write_file(self, file_name, content) -> bool:
        """Write content to file"""
        with open(file_name, 'w', encoding='UTF-8') as file:
            file.write(content)

        return os.path.isfile(file_name)

    def delete_file(self, file_name):
        """Delete file"""
        os.remove(file_name)

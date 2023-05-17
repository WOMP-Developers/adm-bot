"""Utilities for loading static data"""
import pandas as pd

from pydisadm.loader.datasets import get_constellations, get_regions, get_solar_systems

def load_solar_systems() -> pd.DataFrame:
    """Load solar systems data"""
    solar_systems = pd.read_csv(get_solar_systems(), usecols=[
        'regionID','constellationID','solarSystemID','solarSystemName'])
    solar_systems.set_index('solarSystemID', inplace=True)

    constellations = pd.read_csv(get_constellations(), usecols=[
        'constellationID','constellationName'])
    constellations.set_index('constellationID', inplace=True)

    regions = pd.read_csv(get_regions(), usecols=['regionID','regionName'])
    regions.set_index('regionID', inplace=True)

    solar_systems = solar_systems.join(constellations, on='constellationID', how='left')
    solar_systems = solar_systems.join(regions, on='regionID', how='left')

    return solar_systems

def update_static_data(database):
    """Populate database with solar systems data"""
    solar_systems = load_solar_systems()
    database.insert_map_data(solar_systems)

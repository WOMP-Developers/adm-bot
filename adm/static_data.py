import pandas as pd

def update_static_data(database):
    solar_systems = pd.read_csv('data/mapSolarSystems.csv', usecols=['regionID','constellationID','solarSystemID','solarSystemName'])
    solar_systems.set_index('solarSystemID', inplace=True)

    constellations = pd.read_csv('data/mapConstellations.csv', usecols=['constellationID','constellationName'])
    constellations.set_index('constellationID', inplace=True)

    regions = pd.read_csv('data/mapRegions.csv', usecols=['regionID','regionName'])
    regions.set_index('regionID', inplace=True)

    solar_systems = solar_systems.join(constellations, on='constellationID', how='left')
    solar_systems = solar_systems.join(regions, on='regionID', how='left')

    database.insert_map_data(solar_systems)
from importlib import resources

def get_solar_systems():
    with resources.path('pydisadm.data', 'mapSolarSystems.csv') as f:
        file_path = f
    return file_path

def get_constellations():
    with resources.path('pydisadm.data', 'mapConstellations.csv') as f:
        file_path = f
    return file_path

def get_regions():
    with resources.path('pydisadm.data', 'mapRegions.csv') as f:
        file_path = f
    return file_path

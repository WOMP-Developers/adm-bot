"""Datasets"""
from importlib import resources

def get_solar_systems():
    """Retrieve solar systems dataset path"""
    with resources.path('pydisadm.data', 'mapSolarSystems.csv') as path:
        file_path = path
    return file_path

def get_constellations():
    """Retrieve constellations dataset path"""
    with resources.path('pydisadm.data', 'mapConstellations.csv') as path:
        file_path = path
    return file_path

def get_regions():
    """Retrieve regions dataset path"""
    with resources.path('pydisadm.data', 'mapRegions.csv') as path:
        file_path = path
    return file_path

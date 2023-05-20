from os.path import isfile

from pydisadm.loader.datasets import get_constellations, get_regions, get_solar_systems

def test_get_solar_systems():
    assert isfile(get_solar_systems()) is True

def test_get_constellations():
    assert isfile(get_constellations()) is True

def test_get_regions():
    assert isfile(get_regions()) is True

from pydisadm.loader.static_data import load_solar_systems

def test_load_solar_systems():
    solar_systems = load_solar_systems()

    assert len(solar_systems) > 0, 'no solar systems'
    assert 'solarSystemName' in solar_systems.columns, 'solarSystemName missing'
    assert 'constellationName' in solar_systems.columns, 'constellationName missing'
    assert 'regionName' in solar_systems.columns, 'regionName missing'

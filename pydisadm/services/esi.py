import requests
import logging

logger = logging.getLogger('esi_api')

def safe_get(url):
    try:
        response = requests.get(url)
    except Exception as err:
        logger.error(err)
        return None

    return response

def safe_post(url, json):
    try:
        response = requests.post(url, json=json)
    except Exception as err:
        logger.error(err)
        return None

    return response

def universe_names(ids):
    url = "https://esi.evetech.net/latest/universe/names/?datasource=tranquility"
    return safe_post(url, ids).json()

def universe_system(id):
    url = f"http://esi.evetech.net/latest/universe/systems/{id}?datasource=tranquility"
    return safe_get(url).json()

def universe_constellation(id):
    url = f"http://esi.evetech.net/latest/universe/constellations/{id}?datasource=tranquility"
    return safe_get(url).json()

def universe_region(id):
    url = f"http://esi.evetech.net/latest/universe/regions/{id}?datasource=tranquility"
    return safe_get(url).json()

def sovereignty_structures():
    url = "https://esi.evetech.net/latest/sovereignty/structures/?datasource=tranquility"
    return safe_get(url).json()

"""ESI API"""
import logging
import requests

logger = logging.getLogger('esi_api')

BASE_ENDPOINT="https://esi.evetech.net/latest"

def safe_get(url):
    """Safe get request"""
    try:
        response = requests.get(url, timeout=5000)
    except requests.RequestException as request_exception:
        logger.error(request_exception)
        return None

    return response


def safe_post(url, json):
    """Safe post request"""
    try:
        response = requests.post(url, json=json, timeout=5000)
    except requests.RequestException as request_exception:
        logger.error(request_exception)
        return None

    return response


def universe_names(ids):
    """Get names from IDs"""
    url = f"{BASE_ENDPOINT}/universe/names/?datasource=tranquility"
    return safe_post(url, ids).json()


def universe_system(system_id):
    """Get system by ID"""
    url = f"{BASE_ENDPOINT}/universe/systems/{system_id}?datasource=tranquility"
    return safe_get(url).json()


def universe_constellation(constellation_id):
    """Get constellation by ID"""
    url = f"{BASE_ENDPOINT}/universe/constellations/{constellation_id}?datasource=tranquility"
    return safe_get(url).json()


def universe_region(region_id):
    """Get region by ID"""
    url = f"{BASE_ENDPOINT}/universe/regions/{region_id}?datasource=tranquility"
    return safe_get(url).json()


def sovereignty_structures():
    """Get sovereignty structures"""
    url = f"{BASE_ENDPOINT}/sovereignty/structures/?datasource=tranquility"
    return safe_get(url).json()

import requests

def safe_get(url):
    try:
        response = requests.get(url)
        return response
    except Exception as err:
        print(err)

    return None

def safe_post(url, json):
    try:
        response = requests.post(url, json=json)
        return response
    except Exception as err:
        print(err)

    return None

def universe_names(ids):
    url = "https://esi.evetech.net/latest/universe/names/?datasource=tranquility"
    return safe_post(url, ids).json()

def sovereignty_structures():
    url = "https://esi.evetech.net/latest/sovereignty/structures/?datasource=tranquility"
    return safe_get(url).json()

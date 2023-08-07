"""Common database queries"""

CREATE_TABLE_ADM = """
    CREATE TABLE IF NOT EXISTS adm (
        id INTEGER PRIMARY KEY AUTO_INCREMENT, 
        system_id INTEGER NOT NULL, 
        adm REAL NOT NULL, 
        tier TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

CREATE_TABLE_ADM_HISTORY = """
    CREATE TABLE IF NOT EXISTS adm_history (
        id INTEGER PRIMARY KEY AUTO_INCREMENT, 
        system_id INTEGER NOT NULL, 
        adm REAL NOT NULL, 
        tier TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

CREATE_TABLE_MAP = """
    CREATE TABLE IF NOT EXISTS map (
        solarSystemID INTEGER PRIMARY KEY NOT NULL, 
        constellationID INTEGER NOT NULL, 
        regionID INTEGER NOT NULL, 
        solarSystemName TEXT NOT NULL,
        constellationName TEXT NOT NULL,
        regionName TEXT NOT NULL
    )
"""

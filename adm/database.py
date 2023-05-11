import sqlite3
import pandas as pd

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('adm-data.sqlite')
        self.setup()

    def setup(self):
        cur = self.conn.cursor()
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS systems (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            system_id INTEGER NOT NULL, 
                            adm REAL NOT NULL, 
                            tier TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
        
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS map (
                            solarSystemID INTEGER PRIMARY KEY NOT NULL, 
                            constellationID INTEGER NOT NULL, 
                            regionID INTEGER NOT NULL, 
                            solarSystemName TEXT NOT NULL,
                            constellationName TEXT NOT NULL,
                            regionName TEXT NOT NULL
                        )
                    """)
        self.conn.commit()

    def insert_systems(self, systems):
        systems.to_sql('systems', self.conn, index=False, if_exists='append')

        self.conn.commit()

    def insert_map_data(self, map):
        map.to_sql('map', self.conn, index=True, if_exists='replace')

        self.conn.commit()

    def select_most_recent_row(self):
        return pd.read_sql_query("SELECT created_at FROM systems ORDER BY created_at DESC LIMIT 1", self.conn)

    def select_systems(self):
        return pd.read_sql_query("""
            SELECT t1.*, t2.solarSystemName, t2.constellationName, t2.regionName FROM systems t1 
            LEFT JOIN map t2 ON t1.system_id = t2.solarSystemID 
            WHERE t1.created_at = (SELECT MAX(t3.created_at) FROM systems t3 WHERE t3.system_id = t1.system_id);
        """, self.conn)
    
    def select_system_history(self, system, limit):
        return pd.read_sql_query("SELECT adm, tier, created_at FROM systems INNER JOIN map ON map.solarSystemID = systems.system_id WHERE map.solarSystemName=? ORDER BY created_at DESC LIMIT ?", self.conn, params=[system, limit])

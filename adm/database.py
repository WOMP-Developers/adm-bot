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
                            name TEXT NOT NULL,
                            tier TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
        self.conn.commit()

    def insert_systems(self, systems):
        systems.to_sql('systems', self.conn, index=False, if_exists='append')

        self.conn.commit()

    def select_most_recent_row(self):
        return pd.read_sql_query("SELECT created_at FROM systems ORDER BY created_at DESC LIMIT 1", self.conn)

    def select_systems(self):
        return pd.read_sql_query("SELECT t1.* FROM systems t1 WHERE t1.created_at = (SELECT MAX(t2.created_at) FROM systems t2 WHERE t2.system_id = t1.system_id)", self.conn)
    
    def select_system_history(self, system, limit):
        return pd.read_sql_query("SELECT name, adm, tier, created_at FROM systems WHERE name=? ORDER BY created_at DESC LIMIT ?", self.conn, params=[system, limit])

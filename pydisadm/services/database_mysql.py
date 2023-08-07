"""Mysql database service"""
from sqlalchemy import create_engine, text
import pandas as pd

from pydisadm.services.database import Database

class DatabaseMysql(Database):
    """Mysql database service implementation"""

    def __init__(self, conn_string):
        self.engine = create_engine(f'mysql+mysqldb://{conn_string}')
        self.setup()

    def setup(self):
        """Setup database schema"""
        with self.engine.connect() as conn:
            conn.execute(text("""
                            CREATE TABLE IF NOT EXISTS adm (
                                id INTEGER PRIMARY KEY AUTO_INCREMENT, 
                                system_id INTEGER NOT NULL, 
                                adm REAL NOT NULL, 
                                tier TEXT NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """))
            
            conn.execute(text("""
                            CREATE TABLE IF NOT EXISTS adm_history (
                                id INTEGER PRIMARY KEY AUTO_INCREMENT, 
                                system_id INTEGER NOT NULL, 
                                adm REAL NOT NULL, 
                                tier TEXT NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """))

            conn.execute(text("""
                            CREATE TABLE IF NOT EXISTS map (
                                solarSystemID INTEGER PRIMARY KEY NOT NULL, 
                                constellationID INTEGER NOT NULL, 
                                regionID INTEGER NOT NULL, 
                                solarSystemName TEXT NOT NULL,
                                constellationName TEXT NOT NULL,
                                regionName TEXT NOT NULL
                            )
                        """))
            conn.commit()

    def insert_systems(self, systems):
        """Insert system ADM records"""
        systems.to_sql('adm', self.engine, index=False, if_exists='append')
        systems.to_sql('adm_history', self.engine, index=False, if_exists='append')

    def insert_map_data(self, map_data):
        """Insert map data"""
        map_data.to_sql('map', self.engine, index=True, if_exists='replace')

    def select_system_with_name(self, system_name) -> pd.DataFrame:
        """Select system matching name"""
        return pd.read_sql_query(text("SELECT * FROM map WHERE solarSystemName = :system_name"),
                                 self.engine, params={ 'system_name': system_name })

    def select_most_recent_row(self) -> pd.DataFrame:
        """Select the most recent ADM record"""
        return pd.read_sql_query(text("""
            SELECT created_at FROM adm ORDER BY created_at DESC LIMIT 1
        """), self.engine)

    def select_systems(self) -> pd.DataFrame:
        """Select most recent record of all systems"""
        return pd.read_sql_query(text("""
            SELECT t1.*, t2.solarSystemName, t2.constellationName, t2.regionName FROM adm t1 
            LEFT JOIN map t2 ON t1.system_id = t2.solarSystemID 
            WHERE t1.created_at = (SELECT MAX(t3.created_at) FROM adm t3 WHERE t3.system_id = t1.system_id);
        """), self.engine)

    def select_system_by_name(self, name) -> pd.DataFrame:
        """Select systems by name"""
        sql = text("""
            SELECT map.solarSystemName system_name, adm, tier, created_at FROM adm
            INNER JOIN map ON map.solarSystemID = adm.system_id
            WHERE map.solarSystemName=:system_name OR
                map.constellationName=:constellation_name OR
                map.regionName=:region_name ORDER BY created_at
        """)
        return pd.read_sql_query(sql, self.engine, params={ 'system_name': name,
                                 'constellation_name': name, 'region_name': name })

    def select_system_history(self, system, limit) -> pd.DataFrame:
        """Select history of a single system"""
        return pd.read_sql_query(text("""
            SELECT system_id, adm, tier, created_at FROM adm
            INNER JOIN map ON map.solarSystemID = systems.system_id
            WHERE map.solarSystemName=:system_name ORDER BY created_at DESC LIMIT :limit
        """), self.engine, params={'system_name': system, 'limit': limit })

    def delete_system_rows(self, days_old):
        """Delete system rows older than days_old"""

        with self.engine.connect() as conn:
            conn.execute(text("""
                DELETE FROM adm WHERE created_at < DATE(NOW()-INTERVAL :days DAY)
            """), parameters={ 'days': days_old })

            conn.commit()

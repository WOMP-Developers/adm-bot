"""Disk database service"""
import sqlite3
import pandas as pd
from pydisadm.services.common import CREATE_TABLE_ADM, CREATE_TABLE_MAP

from pydisadm.services.database import Database

class DatabaseSqlite(Database):
    """Disk database service implementation"""

    def __init__(self, conn_string):
        if conn_string is None:
            conn_string = 'adm-data.sqlite'

        self.conn = sqlite3.connect(conn_string)
        self.setup()

    def setup(self):
        """Setup database schema"""
        cur = self.conn.cursor()
        cur.execute(CREATE_TABLE_ADM.replace('AUTO_INCREMENT', 'AUTOINCREMENT'))
        cur.execute(CREATE_TABLE_MAP.replace('AUTO_INCREMENT', 'AUTOINCREMENT'))
        self.conn.commit()

    def insert_systems(self, systems):
        """Insert system ADM records"""
        systems.to_sql('adm', self.conn, index=False, if_exists='append')

        self.conn.commit()

    def insert_map_data(self, map_data):
        """Insert map data"""
        map_data.to_sql('map', self.conn, index=True, if_exists='replace')

        self.conn.commit()

    def select_system_with_name(self, system_name) -> pd.DataFrame:
        """Select system matching name"""
        return pd.read_sql_query("SELECT * FROM map WHERE solarSystemName = ?",
                                 self.conn, params=[system_name])

    def select_most_recent_row(self) -> pd.DataFrame:
        """Select the most recent ADM record"""
        return pd.read_sql_query("SELECT created_at FROM adm ORDER BY created_at DESC LIMIT 1",
                                 self.conn)

    def select_systems(self) -> pd.DataFrame:
        """Select most recent record of all systems"""
        return pd.read_sql_query("""
            SELECT t1.*, t2.solarSystemName, t2.constellationName, t2.regionName FROM adm t1 
            LEFT JOIN map t2 ON t1.system_id = t2.solarSystemID 
            WHERE t1.created_at = (SELECT MAX(t3.created_at) FROM adm t3 WHERE t3.system_id = t1.system_id);
        """, self.conn)

    def select_system_by_name(self, name) -> pd.DataFrame:
        """Select systems by name"""
        sql = """
            SELECT map.solarSystemName system_name, adm, tier, created_at FROM adm
            INNER JOIN map ON map.solarSystemID = adm.system_id
            WHERE map.solarSystemName=? OR map.constellationName=? OR map.regionName=? ORDER BY created_at
        """
        return pd.read_sql_query(sql, self.conn, params=[name, name, name])

    def select_system_history(self, system, limit) -> pd.DataFrame:
        """Select history of a single system"""
        return pd.read_sql_query("""
            SELECT system_id, adm, tier, created_at FROM adm
            INNER JOIN map ON map.solarSystemID = adm.system_id
            WHERE map.solarSystemName=? ORDER BY created_at DESC LIMIT ?
        """, self.conn, params=[system, limit])

    def delete_system_rows(self, days_old):
        """Delete system rows older than days_old"""
        cur = self.conn.cursor()
        cur.execute(f"""
            DELETE FROM adm 
            WHERE id IN (
                SELECT id FROM adm WHERE created_at < (select datetime('now', '-{days_old} day'))
            )
        """)

        self.conn.commit()

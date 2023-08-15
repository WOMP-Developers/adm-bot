"""Mysql database service"""
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import pandas as pd

from pydisadm.services.common import (
    CREATE_TABLE_ADM, CREATE_TABLE_ADM_HISTORY, CREATE_TABLE_MAP
)
from pydisadm.services.database import Database

logger = logging.getLogger('database_mysql')

class DatabaseMysql(Database):
    """Mysql database service implementation"""

    def __init__(self, conn_string):
        self.engine = create_engine(f'mysql+mysqldb://{conn_string}', pool_size=5, echo_pool=True)
        self.setup()

    def setup(self):
        """Setup database schema"""
        with self.engine.connect() as conn:
            conn.execute(text(CREATE_TABLE_ADM))
            conn.execute(text(CREATE_TABLE_ADM_HISTORY))
            conn.execute(text(CREATE_TABLE_MAP))
            conn.commit()

    def insert_systems(self, systems):
        """Insert system ADM records"""
        with self.engine.connect() as conn:
            try:
                systems.to_sql('adm', conn, index=False, if_exists='append')
                systems.to_sql('adm_history', conn, index=False, if_exists='append')
            except OperationalError as error:
                logger.error('insert_systems error', exc_info=error)
                conn.rollback()
                raise error

    def insert_map_data(self, map_data):
        """Insert map data"""
        with self.engine.connect() as conn:
            try:
                map_data.to_sql('map', conn, index=True, if_exists='replace')
            except OperationalError as error:
                logger.error('insert_map_data error', exc_info=error)
                conn.rollback()
                raise error

    def select_system_with_name(self, system_name) -> pd.DataFrame:
        """Select system matching name"""
        with self.engine.connect() as conn:
            try:
                system = pd.read_sql_query(
                    text("SELECT * FROM map WHERE solarSystemName = :system_name"),
                    conn, params={ 'system_name': system_name })
            except OperationalError as error:
                logger.error('select_system_with_name error', exc_info=error)
                conn.rollback()
                raise error

        return system

    def select_most_recent_row(self) -> pd.DataFrame:
        """Select the most recent ADM record"""
        with self.engine.connect() as conn:
            try:
                most_recent = pd.read_sql_query(text("""
                    SELECT created_at FROM adm ORDER BY created_at DESC LIMIT 1
                """), conn)
            except OperationalError as error:
                logger.error('select_most_recent_row error', exc_info=error)
                conn.rollback()
                raise error

        return most_recent

    def select_systems(self) -> pd.DataFrame:
        """Select most recent record of all systems"""

        with self.engine.connect() as conn:
            try:
                systems = pd.read_sql_query(text("""
                    SELECT t1.*, t2.solarSystemName, t2.constellationName, t2.regionName FROM adm t1 
                    LEFT JOIN map t2 ON t1.system_id = t2.solarSystemID 
                    WHERE t1.created_at = (SELECT MAX(t3.created_at) FROM adm t3 WHERE t3.system_id = t1.system_id);
                """), conn)
            except OperationalError as error:
                logger.error('select_systems error', exc_info=error)
                conn.rollback()
                raise error

        return systems

    def select_system_by_name(self, name) -> pd.DataFrame:
        """Select systems by name"""
        sql = text("""
            SELECT map.solarSystemName system_name, adm, tier, created_at FROM adm
            INNER JOIN map ON map.solarSystemID = adm.system_id
            WHERE map.solarSystemName=:system_name OR
                map.constellationName=:constellation_name OR
                map.regionName=:region_name ORDER BY created_at
        """)
        with self.engine.connect() as conn:
            try:
                system = pd.read_sql_query(sql, conn, params={ 'system_name': name,
                                        'constellation_name': name, 'region_name': name })
            except OperationalError as error:
                logger.error('select_system_by_name error', exc_info=error)
                conn.rollback()
                raise error

        return system

    def select_system_history(self, system, limit) -> pd.DataFrame:
        """Select history of a single system"""

        with self.engine.connect() as conn:
            try:
                system_history = pd.read_sql_query(text("""
                    SELECT system_id, adm, tier, created_at FROM adm
                    INNER JOIN map ON map.solarSystemID = systems.system_id
                    WHERE map.solarSystemName=:system_name ORDER BY created_at DESC LIMIT :limit
                """), conn, params={'system_name': system, 'limit': limit })
            except OperationalError as error:
                logger.error('select_system_history error', exc_info=error)
                conn.rollback()
                raise error

        return system_history

    def delete_system_rows(self, days_old):
        """Delete system rows older than days_old"""

        with self.engine.connect() as conn:
            try:
                conn.execute(text("""
                    DELETE FROM adm WHERE created_at < DATE(NOW()-INTERVAL :days DAY)
                """), parameters={ 'days': days_old })

                conn.commit()
            except OperationalError as error:
                logger.error('delete_system_rows error', exc_info=error)
                conn.rollback()
                raise error

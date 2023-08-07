"""Factory to create database implementation"""

from pydisadm.services.database_mysql import DatabaseMysql
from pydisadm.services.database_sqlite import DatabaseSqlite

def create_database(configuration):
    """Create database implementation based on configuration."""

    db_service = configuration.database['service']
    connection_string = configuration.database['connection_string']
    if db_service == 'sqlite':
        database = DatabaseSqlite(connection_string)
    elif db_service == 'mysql':
        database = DatabaseMysql(connection_string)

    return database

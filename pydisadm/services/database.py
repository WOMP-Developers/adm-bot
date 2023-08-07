"""Database service"""
from abc import abstractmethod

import pandas as pd

class Database:
    """Database service"""

    @abstractmethod
    def setup(self):
        """Setup database schema"""
        pass

    @abstractmethod
    def insert_systems(self, systems):
        """Insert system ADM records"""
        pass

    @abstractmethod
    def insert_map_data(self, map_data):
        """Insert map data"""
        pass
    
    @abstractmethod
    def select_system_with_name(self, system_name) -> pd.DataFrame:
        """Select system matching name"""
        pass

    @abstractmethod
    def select_most_recent_row(self) -> pd.DataFrame:
        """Select the most recent ADM record"""
        pass

    @abstractmethod
    def select_systems(self) -> pd.DataFrame:
        """Select most recent record of all systems"""
        pass

    @abstractmethod
    def select_system_by_name(self, name) -> pd.DataFrame:
        """Select systems by name"""
        pass

    @abstractmethod
    def select_system_history(self, system, limit) -> pd.DataFrame:
        """Select history of a single system"""
        pass

    @abstractmethod
    def delete_system_rows(self, days_old):
        """Delete system rows older than days_old"""
        pass

import sys
from adm.commands import refresh_data
from adm.configuration import Configuration
from adm.database import Database

def main() -> int:
    configuration = Configuration()
    database = Database()
    
    refresh_data(configuration, database)

    return 0

if __name__ == '__main__':
    sys.exit(main()) 
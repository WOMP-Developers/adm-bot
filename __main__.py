import sys
from adm.commands import print_summary, refresh_data
from adm.configuration import Configuration
from adm.database import Database

def main() -> int:
    configuration = Configuration()
    database = Database()
    
    refresh_data(configuration, database)
    print_summary(database)

    return 0

if __name__ == '__main__':
    sys.exit(main()) 
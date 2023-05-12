#!/usr/bin/env python

import sys
from adm.commands import update_adm_data
from adm.configuration import Configuration
from adm.database import Database
from dotenv import load_dotenv
from adm.service import create_system_adm

from adm.static_data import update_static_data

load_dotenv()

def main() -> int:
    configuration = Configuration()
    database = Database()

    update_static_data(database)
    update_adm_data(configuration, database)

    return 0

if __name__ == '__main__':
    sys.exit(main()) 
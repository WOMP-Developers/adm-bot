#!/usr/bin/env python

import asyncio
import signal
import sys
import threading
from configuration import Configuration
from pydisadm.bot.adm_bot import AdmBot
from pydisadm.controller.adm_controller import AdmController
from runnable.runnable_refresh import run_auto_refresh
from services.database import Database
from dotenv import load_dotenv

from loader.static_data import update_static_data

interrupt_event = threading.Event()

def signal_handler(sig, frame):
    print('Interrupted by CTRL+C')
    interrupt_event.set()
    sys.exit(0)


def main() -> int:
    load_dotenv(verbose=True)

    signal.signal(signal.SIGINT, signal_handler)

    run_auto_refresh(interrupt_event)

    configuration = Configuration()

    database = Database()
    update_static_data(database)

    controller = AdmController(configuration, database)
    controller.update_adm_data()

    bot = AdmBot(configuration, controller)
    bot.setup_cogs()
    bot.run()

    return 0

if __name__ == '__main__':
    sys.exit(main()) 
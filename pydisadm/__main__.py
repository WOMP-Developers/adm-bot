"""pydisadm discord adm bot"""
#!/usr/bin/env python

import signal
import sys
import threading

from dotenv import load_dotenv

from pydisadm.bot.adm_bot import AdmBot
from pydisadm.configuration import Configuration
from pydisadm.controller.adm_controller import AdmController
from pydisadm.loader.static_data import update_static_data
from pydisadm.runnable.runnable_refresh import run_auto_refresh
from pydisadm.services.factory import create_database

interrupt_event = threading.Event()

def _signal_handler(_1, _2):
    print('Interrupted by CTRL+C')
    interrupt_event.set()
    sys.exit(0)


def main() -> int:
    """Application main entrypoint"""
    load_dotenv(verbose=True)

    signal.signal(signal.SIGINT, _signal_handler)

    run_auto_refresh(interrupt_event)

    configuration = Configuration()

    database = create_database(configuration)

    update_static_data(database)

    controller = AdmController(configuration, database)

    controller.update_adm_data()
    controller.purge_adm_records(configuration.database['keep_adm_days'])

    bot = AdmBot(configuration, controller)
    bot.setup_cogs()
    bot.run()

    interrupt_event.set()

    return 0

if __name__ == '__main__':
    sys.exit(main())

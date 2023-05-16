import schedule
import logging

from pydisadm.configuration import Configuration
from pydisadm.controller.adm_controller import AdmController
from pydisadm.services.database import Database
from pydisadm.utils.thread_utils import run_threaded

logger = logging.getLogger('adm_auto_refresh')

def scheduler_loop(interrupt_event):
    configuration = Configuration()
    database = Database()

    controller = AdmController(configuration, database)

    schedule.every().day.at('11:30', tz='UTC').do(refresh_job, controller)

    while True:
        schedule.run_pending()
        if interrupt_event.wait(timeout=1000):
            break

def refresh_job(controller: AdmController):
    logger.info('updating adm data...')
    controller.update_adm_data()
    logger.info('adm data update finished')

def run_auto_refresh(interrupt_event):
    logger.info('starting adm data update thread')
    run_threaded(lambda: scheduler_loop(interrupt_event))
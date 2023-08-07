"""Module for running scheduled refresh"""
import logging
import schedule

from pydisadm.configuration import Configuration
from pydisadm.controller.adm_controller import AdmController
from pydisadm.services.factory import create_database
from pydisadm.utils.thread_utils import run_threaded

logger = logging.getLogger('adm_auto_refresh')

def scheduler_loop(interrupt_event):
    """Scheduler main loop"""
    configuration = Configuration()

    database = create_database(configuration)

    controller = AdmController(configuration, database)

    schedule.every().day.at('11:30', tz='UTC').do(refresh_job, controller, configuration)

    while True:
        schedule.run_pending()
        if interrupt_event.wait(timeout=1000):
            break

def refresh_job(controller: AdmController, configuration: Configuration):
    """Refresh adm data"""
    logger.info('updating adm data...')
    controller.update_adm_data()
    logger.info('adm data update finished')

    logger.info('purge old adm data...')
    controller.purge_adm_records(configuration.database['keep_adm_days'])
    logger.info('purge finished')

def run_auto_refresh(interrupt_event):
    """Run automatic adm data refresh in separate thread"""
    logger.info('starting adm data update thread')
    run_threaded(lambda: scheduler_loop(interrupt_event))

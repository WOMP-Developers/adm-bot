import threading
import schedule

from adm.commands import update_adm_data
from adm.configuration import Configuration
from adm.database import Database

def threaded(function):
    job_thread = threading.Thread(target=function)
    job_thread.start()

def scheduler_loop(interrupt_event):
    configuration = Configuration()
    database = Database()

    schedule.every().day.at('12:00').do(refresh_job, configuration, database)

    while True:
        schedule.run_pending()
        if interrupt_event.wait(timeout=1000):
            break

def refresh_job(configuration, database):
    print('updating adm data...')
    update_adm_data(configuration, database)
    print('adm data update finished')

def threaded_auto_refresh(interrupt_event):
    threaded(lambda: scheduler_loop(interrupt_event))
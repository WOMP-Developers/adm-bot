import threading
import schedule

from adm.commands import refresh_data

def threaded(function):
    job_thread = threading.Thread(target=function)
    job_thread.start()

def run_pending_jobs(interrupt_event):
    while True:
        schedule.run_pending()
        if interrupt_event.wait(timeout=1):
            break

def refresh_job(configuration, database):
    print('Scheduled data refresh')
    refresh_data(configuration, database)

def threaded_auto_refresh(interrupt_event, configuration, database):
    schedule.every().day.at('12:00').do(refresh_job, configuration, database)
    threaded(lambda: run_pending_jobs(interrupt_event))
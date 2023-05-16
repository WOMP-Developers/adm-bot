
import threading

def run_threaded(function):
    job_thread = threading.Thread(target=function)
    job_thread.start()
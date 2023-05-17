"""Thread utility functions"""
import threading

def run_threaded(function):
    """Run function in separate thread"""
    job_thread = threading.Thread(target=function)
    job_thread.start()

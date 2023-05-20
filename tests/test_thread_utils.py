import threading

from pydisadm.utils.thread_utils import run_threaded

def test_run_threaded():
    interrupt_event = threading.Event()
    run_threaded(interrupt_event.set)

    wait_result = interrupt_event.wait(timeout=250)

    assert wait_result is True, 'event was not set'
    
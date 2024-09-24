import logging
import threading
import time


def wait_for_event(event):
    """Ожидание установки события прежде чем что-то сделать."""

    logging.debug('wait_for_event starting')
    event_is_set = event.wait()
    logging.debug('event set: %s', event_is_set)


def wait_for_event_timeout(event, timeout):
    """Подождать timeout секунд и завершиться по тайм-ауту."""

    while not event.is_set():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = event.wait(timeout)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other work')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s'
)

event = threading.Event()
thread_1 = threading.Thread(name='block', target=wait_for_event, args=(event,))
thread_1.start()
thread_2 = threading.Thread(name='nonblock', target=wait_for_event_timeout, args=(event, 2))
thread_2.start()

logging.debug('Waiting before calling Event.set()')
time.sleep(0.3)
event.set()
logging.debug('Event is set')

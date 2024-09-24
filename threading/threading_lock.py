import logging
import random
import threading
import time


class Counter:

    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start
    
    def increment(self):
        logging.debug('Waiting for lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired lock')
            self.value += 1
        finally:
            self.lock.release()


def worker(counter):
    for i in range(2):
        pause = random.random()
        logging.debug('Sleeping %0.02f', pause)
        time.sleep(pause)
        counter.increment()
    logging.debug('Done')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s'
)

counter = Counter()
for i in range(2):
    thread = threading.Thread(target=worker, args=(counter,))
    thread.start()


logging.debug('Waiting for worker threads')
maim_thread = threading.main_thread()
for thread in threading.enumerate():
    if thread is not maim_thread:
        thread.join()
logging.debug('Counter: %d', counter.value)

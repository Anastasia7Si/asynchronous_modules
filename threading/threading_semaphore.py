import logging
import threading
import time


class ActivePool:

    def __init__(self):
        self.active = []
        self.lock = threading.Lock()
    
    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)
    
    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running: %s', self.active)


def worker(semaphore, pool):
    logging.debug('Waiting to join the pool')
    with semaphore:
        name = threading.current_thread().name
        pool.make_active(name)
        time.sleep(0.1)
        pool.make_inactive(name)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s'
)

pool = ActivePool()
semaphore = threading.Semaphore(2)
for i in range(4):
    thread = threading.Thread(target=worker, name=str(i), args=(semaphore, pool))
    thread.start()

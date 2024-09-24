import logging
import threading
import time


def lock_holfer(lock):
    logging.debug('Starting')
    while True:
        lock.acquire()
        try:
            logging.debug('Holding')
            time.sleep(0.5)
        finally:
            logging.debug('Not holding')
            lock.release()
        time.sleep(0.5)


def worker(lock):
    logging.debug('Starting')
    number_tries = 0
    numver_acquires = 0
    while numver_acquires < 3:
        time.sleep(0.5)
        logging.debug('Trying to acquire')
        have_it = lock.acquire(0)
        try:
            number_tries += 1
            if have_it:
                logging.debug('Iteration %d: Acquired', number_tries)
                numver_acquires += 1
            else:
                logging.debug('Iteration %d: Not acquired', number_tries)
        finally:
            if have_it:
                lock.release()
    logging.debug('Done after %d iterations', number_tries)


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s'
)

lock = threading.Lock()
holder = threading.Thread(
    target=lock_holfer, args=(lock,), name='LockHolder', daemon=True
)
holder.start()
worker_1 = threading.Thread(target=worker, args=(lock,), name='Worker')
worker_1.start()

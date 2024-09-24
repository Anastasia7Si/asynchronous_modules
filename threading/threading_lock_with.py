import logging
import threading


def worker(lock):
    with lock:
        logging.debug('Lock acquired via with')


def worker_not_with(lock):
    lock.acquire()
    try:
        logging.debug('Lock acquired directly')
    finally:
        lock.release()


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s'
)

lock = threading.Lock()
worker_with = threading.Thread(target=worker, args=(lock,))
simple_worker = threading.Thread(target=worker_not_with, args=(lock,))

worker_with.start()
simple_worker.start()

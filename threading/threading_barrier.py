import threading
import time


NUMBER_THREADS = 3


def worker(barrier):
    print(threading.current_thread().name,
          f'waiting for barrier with {barrier.n_waiting} others')
    worker_id = barrier.wait()
    print(threading.current_thread().name, 'after barrier', worker_id)


barrier = threading.Barrier(NUMBER_THREADS)

threads = [
    threading.Thread(
        name='worker-%s' % i,
        target=worker,
        args=(barrier,)
    )
    for i in range(NUMBER_THREADS)
]

for thread in threads:
    print(thread.name, 'starting')
    thread.start()
    time.sleep(0.1)

for thread in threads:
    thread.join()

import threading
import time


NUMBER_THREADS = 3


def worker(barrier):
    print(threading.current_thread().name,
          f'waiting for barrier {barrier.n_waiting} others')
    try:
        worcker_id = barrier.wait()
    except threading.BrokenBarrierError:
        print(threading.current_thread().name, 'aborting')
    else:
        print(threading.current_thread().name, 'after barrier', worcker_id)

barrier = threading.Barrier(NUMBER_THREADS + 1)

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

barrier.abort()

for thread in threads:
    thread.join()

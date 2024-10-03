from concurrent import futures
import threading
import time


def task(number):
    print(f'{threading.current_thread().name}: sleeping {number}')
    time.sleep(number / 10)
    print(f'{threading.current_thread().name}: done with {number}')
    return number / 10


executor = futures.ThreadPoolExecutor(max_workers=2)
print('main: starting')
results = executor.map(task, range(5, 0, -1))
print(f'main: unprocessed results {results}')
print('main: waiting for real results')
real_results = list(results)
print(f'main: results: {real_results}')

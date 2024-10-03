from concurrent import futures
import time


def task(number):
    print(f'{number}: sleeping')
    time.sleep(0.5)
    print(f'{number}: done')
    return number / 10


def done(func):
    if func.cancelled():
        print(f'{func.arg}: canceled')
    elif func.done():
        print(f'{func.arg}: not canceled')
    

if __name__ == '__main__':
    executor = futures.ThreadPoolExecutor(max_workers=2)
    print('main: starting')

    tasks = []
    for i in range(10, 0, -1):
        print(f'main: submitting {i}')
        func = executor.submit(task, i)
        func.arg = i
        func.add_done_callback(done)
        tasks.append((i, func))
    
    for i, t in reversed(tasks):
        if not t.cancelled():
            print(f'main: did not cancel {i}')
    executor.shutdown()

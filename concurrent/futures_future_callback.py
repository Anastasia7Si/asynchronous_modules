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
        error = func.exception()
        if error:
            print(f'{func.arg}: error returned: {error}')
        else:
            result = func.result()
            print(f'{func.arg}: value returned: {result}')


if __name__ == '__main__':
    executor = futures.ThreadPoolExecutor(max_workers=2)
    print('main: starting')
    func = executor.submit(task, 5)
    func.arg = 5
    func.add_done_callback(done)
    result = func.result()

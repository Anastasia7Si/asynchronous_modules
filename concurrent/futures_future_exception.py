from concurrent import futures


def task(number):
    print(f'{number}: starting')
    raise ValueError(f'the value {number} is no good')


executer = futures.ThreadPoolExecutor(max_workers=2)
print('main: starting')
func = executer.submit(task, 5)

error = func.exception()
print(f'main: error: {error}')

try:
    result = func.result()
except ValueError as e:
    print(f'main: saw error "{e}" when accessing result')

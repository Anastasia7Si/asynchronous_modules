import multiprocessing
import sys
import time


def exit_error():
    sys.exit(1)


def exit_ok():
    return


def return_value():
    return 1


def raises():
    raise RuntimeError('There was an error!')


def terminated():
    time.sleep(3)


if __name__ == '__main__':
    jobs = []
    funcs = [
        exit_error,
        exit_ok,
        return_value,
        raises,
        terminated
    ]
    for func in funcs:
        print('Sarting process for', func.__name__)
        job = multiprocessing.Process(target=func, name=func.__name__)
        jobs.append(job)
        job.start()
    jobs[-1].terminate()
    for job in jobs:
        job.join()
        print('{:>15}.exitcode = {}'.format(job.name, job.exitcode))

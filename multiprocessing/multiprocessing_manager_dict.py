import multiprocessing


def worker(dict, key, value):
    dict[key] = value


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    dict = manager.dict()
    jobs = [
        multiprocessing.Process(
            target=worker,
            args=(dict, i, i * 2)
        )
        for i in range(10)
    ]
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()
    print('Results: ', dict)

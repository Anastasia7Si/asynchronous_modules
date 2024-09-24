import multiprocessing


def producer(namespace, event):
    namespace.value = 'This is the value'
    event.set()


def consumer(namespace, event):
    try:
        print(f'Before event: {namespace.value}')
    except Exception as err:
        print(f'Before event: {str(err)}')
    event.wait()
    print('After event:', namespace.value)


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    namespace = manager.Namespace()
    event = multiprocessing.Event()
    process = multiprocessing.Process(
        target=producer,
        args=(namespace, event)
    )
    consumer_1 = multiprocessing.Process(
        target=consumer,
        args=(namespace, event)
    )
    consumer_1.start()
    process.start()
    consumer_1.join()
    process.join()
    
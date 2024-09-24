import multiprocessing
import time


def wait_for_event(event):
    """Дождаться события, прежде чем делать что-либо."""

    print('wait_for_event: starting')
    event.wait()
    print('wait_for_event: event.is_set() ->', event.is_set())


def wait_for_event_timeout(event, timeout):
    """Подождать timeout секунд и затем завершиться по тайм-ауту."""

    print('wait_for_event_timeout: starting')
    event.wait(timeout)
    print('wait_for_event_timeout: event.is_set() ->', event.is_set())


if __name__ == '__main__':
    event = multiprocessing.Event()
    worker_1 = multiprocessing.Process(
        name='block',
        target=wait_for_event,
        args=(event,)
    )
    worker_1.start()
    worker_2 = multiprocessing.Process(
        name='nonblock',
        target=wait_for_event_timeout,
        args=(event, 2)
    )
    worker_2.start()
    print('main: waiting before calling Event.set()')
    time.sleep(3)
    event.set()
    print('main: event is set\n')

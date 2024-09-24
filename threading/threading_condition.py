import logging
import threading
import time


def consumer(condition):
    """Дождаться наступления условия и затем использовать ресурс."""

    logging.debug('Starting consumer thread')
    with condition:
        condition.wait()
        logging.debug('Resorce is available to consumer')


def producer(condition):
    """Настроить ресурс для использования потребителем."""

    logging.debug('Starting producer thread')
    with condition:
        logging.debug('Making resource available')
        condition.notify_all()


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s'
)

condition = threading.Condition()
condition_1 = threading.Thread(name='c1', target=consumer, args=(condition,))
condition_2 = threading.Thread(name='c2', target=consumer, args=(condition,))
producer_1 = threading.Thread(name='p', target=producer, args=(condition,))

condition_1.start()
time.sleep(0.2)
condition_2.start()
time.sleep(0.2)
producer_1.start()

import logging
import random
import threading


def show_value(data):
    try:
        value = data.value
    except AttributeError:
        logging.debug('No value yet')
    else:
        logging.debug('value=%s', value)


def worker(data):
    show_value(data)
    data.value = random.randint(1, 100)
    show_value(data)


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s'
)

local_data = threading.local()
show_value(local_data)
local_data.value = 1000
show_value(local_data)

for i in range(2):
    thread = threading.Thread(target=worker, args=(local_data,))
    thread.start()

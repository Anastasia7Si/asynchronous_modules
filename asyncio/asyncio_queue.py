import asyncio


async def consumer(number, queue):
    print(f'consumer {number}: starting')
    while True:
        print(f'consumer {number}: waiting for item')
        item = await queue.get()
        print(f'consumer {number}: has item {item}')
        if item is None:
            queue.task_done()
            break
        else:
            await asyncio.sleep(0.01 * item)
            queue.task_done()
    print(f'consumer {number}: ending')


async def producer(queue, number_workers):
    print('producer: starting')
    for i in range(number_workers * 3):
        await queue.put(i)
        print(f'producer: added task {i} to the queue')
    print('producer: adding stop signals to the queue')
    for i in range(number_workers):
        await queue.put(None)
    print('producer: waiting for queue to empty')
    await queue.join()
    print('producer: ending')


async def main(loop, number_consumers):
    queue = asyncio.Queue(maxsize=number_consumers)
    consumers = [
        loop.create_task(consumer(i, queue))
        for i in range(number_consumers)
    ]
    prod = loop.create_task(producer(queue, number_consumers))
    await asyncio.wait(consumers + [prod])


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop, 2))
finally:
    event_loop.close()

import asyncio


async def consumer(condition, number):
    with await condition:
        print(f'consumer {number} as waiting')
        await condition.wait()
        print(f'consumer {number} triggered')
    print(f'ending consumer {number}')


async def manipulate_condition(condition):
    print('starting manipulate_condition')
    await asyncio.sleep(0.1)
    for i in range(1, 3):
        with await condition:
            print(f'notify {i} cunsumers')
            condition.notify(n=i)
        await asyncio.sleep(0.1)
    with await condition:
        print('notyfying remaining consumers')
        condition.notify_all()
    print('ending manipulate_condition')


async def main(loop):
    condition = asyncio.Condition()
    consumers = [
        consumer(condition, i)
        for i in range(5)
    ]
    loop.create_task(manipulate_condition(condition))
    await asyncio.wait(consumers)


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

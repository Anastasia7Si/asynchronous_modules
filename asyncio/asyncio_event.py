import asyncio
import functools


def sent_event(event):
    print('setting event in callback')
    event.set()


async def coro_1(event):
    print('coro1 waiting for event')
    await event.wait()
    print('coro1 triggered')


async def coro_2(event):
    print('coro2 waiting for event')
    await event.wait()
    print('coro2 triggered')


async def main(loop):
    event = asyncio.Event()
    print(f'event satrt state: {event.is_set()}')
    loop.call_later(0.1, functools.partial(sent_event, event))
    phases = [
        asyncio.create_task(coro_1(event)),
        asyncio.create_task(coro_2(event))
    ]
    await asyncio.wait(phases)
    print(f'event and state: {event.is_set()}')


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

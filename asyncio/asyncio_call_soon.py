import asyncio
import functools


def callback(arg, *, kwargs='default'):
    print(f'callback invokes with {arg} and {kwargs}')


async def main(loop):
    print('registering callbacks')
    loop.call_soon(callback, 1)
    wrapped = functools.partial(callback, kwargs='not default')
    loop.call_soon(wrapped, 2)
    await asyncio.sleep(0.1)


event_loop = asyncio.get_event_loop()
try:
    print('entering event loop')
    event_loop.run_until_complete(main(event_loop))
finally:
    print('closing ebemt loop')
    event_loop.close()

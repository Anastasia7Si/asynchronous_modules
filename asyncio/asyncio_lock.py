import asyncio
import functools


def unlock(lock):
    print('callback releasing lock')
    lock.release()


async def coro_1(lock):
    print('coro1 waiting for the lock')
    await lock.acquire()
    print('coro1 acquired lock')
    lock.release()
    print('coro1 released lock')


async def coro_2(lock):
    print('coro2 waiting for the lock')
    await lock.acquire()
    try:
        print('coro2 acquired lock')
    finally:
        print('coro2 released lock')
        lock.release()


async def main(loop):
    lock = asyncio.Lock()
    print('acquiring the lock before starting coroutines')
    await lock.acquire()
    print(f'lock acquired: {lock.locked()}')
    loop.call_later(0.1, functools.partial(unlock, lock))
    print('waiting for coroutines')
    phases = [
        asyncio.create_task(coro_1(lock)),
        asyncio.create_task(coro_2(lock))
    ]
    await asyncio.wait(phases)


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

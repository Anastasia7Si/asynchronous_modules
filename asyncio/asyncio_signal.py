import asyncio
import functools
import os
import signal


def signal_handler(name):
    print('signal_handler({!r})'.format(name))


event_loop = asyncio.get_event_loop()
event_loop.add_signal_handler(
    signal.SIGHUP,
    functools.partial(signal_handler, name='SIGHUP')
)
event_loop.add_signal_handler(
    signal.SIGUSR1,
    functools.partial(signal_handler, name='SIGUSR1')
)
event_loop.add_signal_handler(
    signal.SIGINT,
    functools.partial(signal_handler, name='SIGINT')
)

async def send_signals():
    pid = os.getpid()
    print(f'starting send_signals for {pid}')

    for name in ['SIGHUP', 'SIGHUP', 'SIGUSR1', 'SIGINT']:
        os.kill(pid, getattr(signal, name))
        print('yielding control')
        await asyncio.sleep(0.01)
    return

try:
    event_loop.run_until_complete(send_signals())
finally:
    event_loop.close()

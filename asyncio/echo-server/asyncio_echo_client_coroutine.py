import asyncio
import logging
import sys
import ssl


MESSAGES = [
    b'This is the massege. ',
    b'It will be sent ',
    b'in parts.'
]
SERVER_ADDRES = ('localhost', 10_000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr
)
log = logging.getLogger('main')
event_loop = asyncio.get_event_loop()


async def echo_client(addres, messages):
    log = logging.getLogger('echo_client')
    log.debug('connecting to {} port {}'.format(*addres))
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations('pymotw.crt')
    reader, writer = await asyncio.open_connection(*addres, ssl=ssl_context)
    for msg in messages:
        writer.write(msg)
        log.debug('sending {!r}'.format(msg))
    writer.write(b'\x00')
    await writer.drain()
    log.debug('waiting for response')
    while True:
        data = await reader.read(128)
        if data:
            log.debug('received {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return


try:
    event_loop.run_until_complete(echo_client(SERVER_ADDRES, MESSAGES))
finally:
    log.debug('closing event loop')
    event_loop.close()

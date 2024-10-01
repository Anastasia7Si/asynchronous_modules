import asyncio
import functools
import logging
import sys


MESSAGE = [
    b'This is the message.' ,
    b'It will be sent ',
    b'in parts.'
]
SERBER_ADDRES = ('localhost', 10_000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


class EchoClient(asyncio.Protocol):

    def __init__(self, messages, future):
        super().__init__()
        self.messages = messages
        self.log = logging.getLogger('EchoClient')
        self.future = future
    
    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug(
            'connecting to {} port {}'.format(*self.address)
        )
        for msg in self.messages:
            transport.write(msg)
            self.log.debug('sending {!r}'.format(msg))
            if transport.can_write_eof():
                transport.write_eof()
    
    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))
    
    def eof_received(self):
        self.log.debug('received EOF')
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)
    
    def connection_lost(self, exc):
        self.log.debug('server closed connetction')
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)
        super().connection_lost(exc)


client_completed = asyncio.Future()

client_factory = functools.partial(
    EchoClient,
    messages=MESSAGE,
    future=client_completed
)
factory_cotoutine = event_loop.create_connection(
    client_factory,
    *SERBER_ADDRES
)

log.debug('waiting for client to complate')
try:
    event_loop.run_until_complete(factory_cotoutine)
    event_loop.run_until_complete(client_completed)
finally:
    log.debug('closing event loop')
    event_loop.close()

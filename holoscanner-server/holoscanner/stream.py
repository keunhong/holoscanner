import asyncio
from asyncio import streams
import struct
from holoscanner import base_logger


logger = base_logger.getChild(__name__)


HEADER_SIZE = 8
HEADER_FMT = 'Q'


@asyncio.coroutine
def start_server(self, host, port, loop):


    def factory():
        reader = HsStreamReader()
        return HsStreamReaderProtocol(reader, self._accept_client)

    logger.info('HsServer starting at tcp://{}:{}', self.host, self.port)
    self.server = yield from loop.create_server(factory, self.host, self.port)


class HsStreamReaderProtocol(streams.StreamReaderProtocol):
    def connection_made(self, transport):
        self._stream_reader.set_transport(transport)
        if self._client_connected_cb is not None:
            self._stream_writer = HsStreamWriter(transport, self,
                                                 self._stream_reader,
                                                 self._loop)
            res = self._client_connected_cb(self._stream_reader,
                                            self._stream_writer)

            if asyncio.coroutines.iscoroutine(res):
                self._loop.create_task(res)


class HsStreamWriter(streams.StreamWriter):
    def write_msg(self, msg):
        # Serialize message into data.
        data = msg
        self.write(data)


class HsStreamReader(streams.StreamReader):
    @asyncio.coroutine
    def read_msg(self):
        header = yield from self.readexactly(HEADER_SIZE)
        header = struct.unpack(HEADER_FMT, header)
        print(header)
        # msg_type, msg_length = unpack header
        data = yield from self.readexactly(msg_length)

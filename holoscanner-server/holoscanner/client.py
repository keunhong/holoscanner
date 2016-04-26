import asyncio
from holoscanner.stream import HsClientProtocol
from holoscanner.proto.holoscanner_pb2 import Message


if __name__=='__main__':
    msg = Message()
    msg.type = Message.MESH
    msg.device_id = 10

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: HsClientProtocol(msg, loop),
                                  '127.0.0.1', 8888)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

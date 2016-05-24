import os
import asyncio
from holoscanner.game_server import HsClientProtocol
from holoscanner.proto.holoscanner_pb2 import Message
from holoscanner import config, base_logger

logger = base_logger.getChild(__name__)

if __name__ == '__main__':
    messages = []
    for filename in os.listdir(config.MESHES_DIR):
        filepath = os.path.join(config.MESHES_DIR, filename)

        msg = Message()
        msg.type = Message.MESH
        msg.device_id = 'fake_client'
        with open(filepath, 'rb') as f:
            msg.mesh.ParseFromString(f.read())

        messages.append(msg)

    messages[-1].mesh.is_last = True

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: HsClientProtocol(messages, loop),
                                  '127.0.0.1', 8888)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

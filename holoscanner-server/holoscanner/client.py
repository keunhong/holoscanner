import os
import asyncio
import argparse
from holoscanner.game_server import HsClientProtocol
from holoscanner.proto.holoscanner_pb2 import Message
from holoscanner import config, base_logger

logger = base_logger.getChild(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--mesh-dir', dest='mesh_dir', type=str, required=True)
args = parser.parse_args()

if __name__ == '__main__':
    messages = []
    for filename in os.listdir(args.mesh_dir):
        filepath = os.path.join(args.mesh_dir, filename)

        msg = Message()
        msg.type = Message.MESH
        msg.device_id = 'fake_client'
        with open(filepath, 'rb') as f:
            msg.mesh.ParseFromString(f.read())
        msg.mesh.is_last = False

        messages.append(msg)

    messages[-1].mesh.is_last = True

    gsr_message = Message()
    gsr_message.type = Message.CLIENT_READY
    messages.append(gsr_message)

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: HsClientProtocol(messages, loop),
                                  '127.0.0.1', 8888)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

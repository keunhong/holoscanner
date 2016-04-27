import asyncio
from holoscanner.stream import HsClientProtocol, model_to_proto
from holoscanner.proto.holoscanner_pb2 import Message
from holoscanner.io import wavefront


if __name__=='__main__':
    model = wavefront.read_obj_file('assets/model.obj')

    msg = Message()
    msg.type = Message.MESH
    msg.device_id = 10

    model_to_proto(model, msg.mesh)

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: HsClientProtocol(msg, loop),
                                  '127.0.0.1', 8888)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

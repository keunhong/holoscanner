import asyncio
from autobahn.asyncio.websocket import (WebSocketServerProtocol,
                                        WebSocketServerFactory)
from holoscanner import config, base_logger
from holoscanner.proto.holoscanner_pb2 import Message
from holoscanner.state import game_state


logger = base_logger.getChild(__name__)


class RelayProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        logger.info("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        logger.info('WebSocket connection established.')

        with game_state.lock:
            for mesh in game_state.meshes:
                msg = Message()
                msg.type = Message.MESH
                msg.device_id = 999
                msg.mesh.MergeFrom(mesh)
                msg_bytes = msg.SerializeToString()
                logger.info('Sending mesh ({} bytes).'.format(len(msg_bytes)))
                self.sendMessage(msg_bytes, isBinary=True)

        # while True:
        #     mesh = yield from game_state.queue.get()
        #     logger.info('Sending mesh.')
        #     self.sendMessage(mesh.SerializeToString(), isBinary=True)

    @asyncio.coroutine
    def onMessage(self, payload, isBinary):
        if not isBinary:
            logger.info(payload.decode('utf8'))

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {0}".format(reason))


def create_server_factory():
    factory = WebSocketServerFactory("ws://{}:{}".format(
        config.WS_LISTEN_ADDR, config.WS_LISTEN_PORT))
    factory.protocol = RelayProtocol
    return factory

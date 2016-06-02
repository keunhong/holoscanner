import asyncio
from autobahn.asyncio.websocket import (WebSocketServerProtocol,
                                        WebSocketServerFactory)
from holoscanner import config, base_logger
from holoscanner import proto
from holoscanner.proto.holoscanner_pb2 import Message
from holoscanner.state import game_state

logger = base_logger.getChild(__name__)


class DashboardProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self.message_queue = asyncio.Queue()
        game_state.new_websocket_client(self.message_queue)

    def onConnect(self, request):
        logger.debug("New WebSocket connection: {0}".format(request.peer))

    def onOpen(self):
        logger.debug('WebSocket connection established.')

        with game_state.gs_lock:
            self.send_message(game_state.create_game_state_message())
            with game_state.clients_lock:
                for client in game_state.clients.values():
                    for mesh in client.meshes:
                        self.send_message(proto.create_mesh_message(
                            client.client_id, mesh.to_proto()))
            self.send_message(game_state.create_game_state_message())

        while True:
            try:
                msg = yield from self.message_queue.get()
                self.send_message(msg)
            except TimeoutError:
                break

    @asyncio.coroutine
    def onMessage(self, payload, isBinary):
        if not isBinary:
            logger.error('Not Binary {}'.format(payload.decode('utf8')))
        message = Message()
        message.ParseFromString(payload)
        if message.type == Message.CLEAR_MESHES:
            logger.info('Dashboard: Clearing meshes.')
            game_state.clear_meshes()
        elif message.type == Message.CLEAR_GAME_STATE:
            logger.info('Dashboard: Clearing game state.')
            game_state.clear_game_state()
        elif message.type == Message.UPDATE_TARGETS:
            logger.info('Dashboard: Force updating targets.')
            game_state.update_targets(
                config.NUM_TARGETS_GEN,
                keep_first=False,
                force=True)
            game_state.send_to_websocket_clients(
                game_state.create_game_state_message())
        elif message.type == Message.TARGET_FOUND:
            logger.info('Dashboard: Target {} manually acquired.'.format(
                message.target_id))
            game_state.target_found('__server__', message.target_id)
            game_state.send_to_websocket_clients(
                game_state.create_game_state_message())
        elif message.type == Message.VERIFIED:
            logger.info('Dashboard: Sending verified message to clients.')
            msg = Message()
            msg.type = Message.VERIFIED
            game_state.send_to_hololens_clients(msg)

    def onClose(self, wasClean, code, reason):
        logger.debug("WebSocket connection closed: {0}".format(reason))
        game_state.listeners.remove(self.message_queue)

    def send_message(self, msg):
        msg_bytes = msg.SerializeToString()
        # logger.info('Sending message ({} bytes).'.format(len(msg_bytes)))
        self.sendMessage(msg_bytes, isBinary=True)


def create_server_factory():
    factory = WebSocketServerFactory("ws://{}:{}".format(
        config.RELAY_LISTEN_ADDR, config.RELAY_LISTEN_PORT))
    factory.protocol = DashboardProtocol
    return factory

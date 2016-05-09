import asyncio
from autobahn.asyncio.websocket import (WebSocketServerProtocol,
                                        WebSocketServerFactory)
from holoscanner import config


class RelayProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    @asyncio.coroutine
    def onMessage(self, payload, isBinary):
        if not isBinary:
            print(payload.decode('utf8'))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


def create_server_factory():
    factory = WebSocketServerFactory("ws://{}:{}".format(
        config.WS_LISTEN_ADDR, config.WS_LISTEN_PORT))
    factory.protocol = RelayProtocol
    return factory


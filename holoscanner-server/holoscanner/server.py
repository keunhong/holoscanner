import asyncio
from holoscanner.game_server import HsServerProtocol
from holoscanner.relay_server import create_server_factory
from holoscanner import config, base_logger


logger = base_logger.getChild(__name__)


if __name__=='__main__':
    logger.info('Starting server.')

    loop = asyncio.get_event_loop()

    game_coro = loop.create_server(HsServerProtocol,
                                   config.LISTEN_ADDR,
                                   config.LISTEN_PORT)
    ws_coro = loop.create_server(create_server_factory(),
                                 config.WS_LISTEN_ADDR,
                                 config.WS_LISTEN_PORT)

    game_server = loop.run_until_complete(game_coro)
    ws_server = loop.run_until_complete(ws_coro)

    # Serve requests until Ctrl+C is pressed
    logger.info('Serving on {}'.format(game_server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    game_server.close()
    ws_server.close()
    loop.run_until_complete(game_server.wait_closed())
    loop.run_until_complete(ws_server.wait_closed())
    loop.close()


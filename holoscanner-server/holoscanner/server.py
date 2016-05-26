import asyncio
from holoscanner.game_server import HsServerProtocol
from holoscanner.dashboard_server import create_server_factory
from holoscanner import config, base_logger

logger = base_logger.getChild(__name__)

if __name__ == '__main__':
    logger.info('Starting server.')

    loop = asyncio.get_event_loop()

    game_coro = loop.create_server(HsServerProtocol,
                                   config.GAME_LISTEN_ADDR,
                                   config.GAME_LISTEN_PORT)
    dashboard_coro = loop.create_server(create_server_factory(),
                                     config.RELAY_LISTEN_ADDR,
                                     config.RELAY_LISTEN_PORT)

    game_server = loop.run_until_complete(game_coro)
    dashboard_server = loop.run_until_complete(dashboard_coro)

    # Serve requests until Ctrl+C is pressed
    logger.info('Running game server on {}'.format(
        game_server.sockets[0].getsockname()))
    logger.info('Running dashboard server on {}'.format(
        dashboard_server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    game_server.close()
    dashboard_server.close()
    loop.run_until_complete(game_server.wait_closed())
    loop.run_until_complete(dashboard_server.wait_closed())
    loop.close()

import asyncio
from holoscanner.stream import HsServerProtocol
from holoscanner import config, base_logger


logger = base_logger.getChild(__name__)


if __name__=='__main__':
    logger.info('Starting server.')

    loop = asyncio.get_event_loop()
    coro = loop.create_server(HsServerProtocol,
                              config.LISTEN_ADDR,
                              config.LISTEN_PORT)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    logger.info('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


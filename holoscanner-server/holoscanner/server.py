import asyncio
from holoscanner.stream import HsServerProtocol


if __name__=='__main__':
    print('Starting server.')

    loop = asyncio.get_event_loop()
    coro = loop.create_server(HsServerProtocol, '127.0.0.1', 8888)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


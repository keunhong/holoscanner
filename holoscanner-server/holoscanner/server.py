import asyncio
from holoscanner.stream import start_server

@asyncio.coroutine
def handle_message(reader, writer):
    data = yield from reader.read(100)
    message = data.decode()
    address = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, address))

    print("Send: %r" % message)
    writer.write(data)
    yield from writer.drain()

    print("Close the client socket")
    writer.close()


if __name__=='__main__':
    print('Hello World!')

    loop = asyncio.get_event_loop()
    coro = start_server(handle_message, '127.0.0.1', 8888, loop=loop)
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


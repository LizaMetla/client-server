import asyncio
import json
from dataclasses import asdict

from models import TouristOrganisation


def get(pk):
    return TouristOrganisation.get(pk)


operators = {'get': get}


async def handle_echo(reader, writer):
    data = await reader.read(500)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")
    request = json.loads(message)
    response = operators.get(request.get('method'))(request.get('pk'))
    print(response)
    data = json.dumps(response).encode()

    print(f"Send: {data!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())

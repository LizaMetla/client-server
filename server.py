import asyncio
import json
from dataclasses import asdict

from models import TouristOrganisation


def get(pk=None):
    return asdict(TouristOrganisation.get(pk))


def add(**kwargs):
    return asdict(TouristOrganisation(**kwargs).save())


def delete(pk=None):
    TouristOrganisation.delete(tour_uuid=pk)
    return {'message': 'success'}


def get_all_tours():
    all_tours = TouristOrganisation.get_all_tours()
    response = [asdict(tour) for tour in all_tours]
    return response


def edit(**kwargs):
    print('edit')
    asdict(TouristOrganisation(**kwargs).save())
    return {'message': 'success'}


def filter_lt(cost=None):
    response = TouristOrganisation.filter_lt(cost=cost)
    response = [asdict(tour) for tour in response]
    return response


operators = {'get': get, 'add': add, 'delete': delete, 'get_all_tours': get_all_tours, 'edit': edit,
             'filter': filter_lt}


async def handle_echo(reader, writer):
    while True:
        data = await reader.read(10000)
        if not data:
            break
        print(data)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")
        request = json.loads(message)
        response = operators.get(request.get('method'))(**request.get('args'))
        print(response)
        data = json.dumps(response).encode()

        print(f"Send: {data!r}")
        writer.write(data)
        await writer.drain()
    print("Close the connection")
    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
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

import asyncio
import json


async def tcp_echo_client():
    # while True:
    # pass
    ui = UserInterface()
    ui.print_common_menu()
    await ui.socket_start()
    await ui.input_point_of_menu()
    print('Close the connection')
    ui.writer.close()
    my_list = [1, 2, 3, 4]


class UserInterface:
    point = None

    def __init__(self):
        self.menu_common = {
            '1': {'desc': 'Просмотр тура', 'func': self.tour_view},
            '2': {'desc': 'Добавление тура'},
            '3': {'desc': 'Удаление тура'},
            '4': {'desc': 'Редактирование тура'},
            '5': {'desc': 'Фильтрация туров по стоимости'},
            '0': {'desc': 'Выход'}
        }

    async def socket_start(self):
        self.reader, self.writer = await asyncio.open_connection(
            '127.0.0.1', 8888)

    async def send_data(self, method, **kwargs):
        message = {'method': method}
        message.update(kwargs)
        message = json.dumps(message)
        print(f'Send: {message!r}')
        self.writer.write(message.encode())

    async def read_data(self):
        data = await self.reader.read(100)
        response = json.loads(data.decode())
        # for key, value in response.items():
        #     print(key + ':', value)
        print(response)
        return response

    def print_common_menu(self):
        for point, settings in self.menu_common.items():
            print(point + '.', settings.get('desc'))

    async def input_point_of_menu(self):
        while True:
            point = input('>> ')
            if point.isdigit() and point in self.menu_common:
                settings = self.menu_common.get(point)
                await settings['func']()
                break
            else:
                print('Неверный ввод! \n')

    async def tour_view(self):
        pk = input('Введите первичный ключ пользователя: ')
        await self.send_data('get', pk=pk)
        await self.read_data()

    def add_tour(self):
        pass

    def delete_tour(self):
        pass

    def edit_tour(self):
        pass

    def filter_tour(self):
        pass

    def exit_from_program(self):
        pass



if __name__ == '__main__':
    asyncio.run(tcp_echo_client())

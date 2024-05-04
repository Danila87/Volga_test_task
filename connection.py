import aiohttp

from typing import Literal


class Connection:

    """
    Класс подключения к какому либо хосту с реализацией различных методов.
    """

    METHODS = Literal['get', 'post', 'put', 'delete']

    def __init__(self, host: str):

        self.host = host

    async def send_request(self, url: str, method: METHODS, data: dict = None) -> dict | list[dict]:

        async with aiohttp.ClientSession() as session:
            if method == 'get':
                async with session.get(self.host + url, params=data, ssl=False) as response:
                    return await response.json()

            if method == 'post':
                async with session.post(self.host + url, json=data, ssl=False) as response:
                    return await response.json()


weather_connection = Connection(host='https://api.open-meteo.com')  # Создаем экземпляр подключения к хосту open-meteo

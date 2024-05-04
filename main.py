import asyncio

from database.cruds import BaseCruds, WeatherCruds
from database import models

from weather import skoltech_weather
from export import ExcelExport


# Задача получения данных о погоде и отправка их в БД
async def scan_weather(time_sleep: int = 60):

    while True:

        current_weather_data = await skoltech_weather.get_weather_data()
        await BaseCruds.insert_data(model=models.WeatherHistory, **current_weather_data)
        await asyncio.sleep(time_sleep)


# Задача экспорта данных в Excel
async def export_weather():

    weather_history_data = await WeatherCruds.get_weather_data_by_limit()
    excel_export = ExcelExport(path_save='reports/', data=weather_history_data)

    if excel_export.export_to_file():
        print(f'Файл сохранен под названием {excel_export.file_name}')
    else:
        print('Возникла ошибка при сохранении файла')


# Пользовательский ввод
async def dialog():
    while True:
        user_input = await asyncio.to_thread(input, 'Введите "Экспорт", чтобы экспортировать данные >> ')
        if user_input.lower() == 'экспорт':
            await export_weather()


async def main():
    await asyncio.gather(scan_weather(), dialog())


asyncio.run(main())

import pandas
from abc import ABC, abstractmethod
from datetime import datetime


class Export(ABC):

    """
    Абстрактный класс для экспорта данных в какой либо формат.
    """

    @abstractmethod
    def export_to_file(self):
        pass


class ExcelExport(Export):

    def __init__(self, path_save: str, data):

        self.path_save = path_save
        self.file_name = f'{datetime.now()}.xlsx'
        self.data = data

    def export_to_file(self) -> bool:

        dataframe = [

            {'Дата': row.date,
             'Направление ветра': row.wind_direction,
             'Сила ветра': f'{row.wind_speed} м/с',
             'Температура': f'{row.temperature} С',
             'Давление': f'{row.surface_pressure} мм',
             'Погода': f'{row.rel_weather_code.description}',
             'Дождевые осадки': f'{row.rain_size_precipitation} мм',
             'Снежные осадки': f'{row.snow_size_precipitation} мм'
             }

            for row in self.data

        ]
        dataframe = sorted(dataframe, key=lambda key: key['Дата'])
        try:

            df = pandas.DataFrame(dataframe)
            df.to_excel(f'{self.path_save}{self.file_name}', index=False)

            return True

        except:
            return False

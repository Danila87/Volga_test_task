from connection import weather_connection
from datetime import datetime


class Weather:

    """
    Класс реализующий получение погоды и ее анализ
    """

    def __init__(self, weather_params):
        self.weather_params = weather_params

    async def get_weather_data(self) -> dict:
        """
        Функция получения словаря weather_data, который содержит в себе все нужные значения для истории погоды
        :return:
        """

        response_data = await weather_connection.send_request(url='/v1/forecast',
                                                              method='get',
                                                              data=self.weather_params)

        wind_direction = self.analyze_wind_direction(wind_direction=response_data['current']['wind_direction_10m'])
        date = datetime.utcfromtimestamp(response_data['current']['time'])

        weather_data = {
            'date': date,
            'temperature': int(response_data['current']['temperature_2m']),
            'wind_direction': wind_direction,
            'wind_speed': int(response_data['current']['wind_speed_10m']),
            'surface_pressure': int(response_data['current']['surface_pressure']),
            'weather_code': response_data['current']['weather_code'],
            'rain_size_precipitation': response_data['current']['rain'],
            'snow_size_precipitation': response_data['current']['snowfall']
        }

        return weather_data

    @staticmethod
    def analyze_wind_direction(wind_direction: int) -> str:
        """
        Функция определения направления ветра по градусу
        :param wind_direction: направление ветра в градусах
        :return: словесное направление ветра
        """

        dirs = ["северный", "северо-восточный", "восточный", "юго-восточный", "южный", "юго-западный", "западный",
                "северо-западный"]
        ix = round(wind_direction / (360. / len(dirs)))
        return dirs[ix % len(dirs)]


# Параметры запроса к апи
skoltech_weather_params = {
    "latitude": 55.6878,
    "longitude": 37.3684,
    "current": ["temperature_2m", "precipitation", "rain", "showers", "snowfall", "weather_code", "surface_pressure",
                "wind_speed_10m", "wind_direction_10m"],
    "wind_speed_unit": "ms",
    "timeformat": "unixtime"
}


# Экземпляр класс, который получает погоду в районе сколтеха
skoltech_weather = Weather(weather_params=skoltech_weather_params)

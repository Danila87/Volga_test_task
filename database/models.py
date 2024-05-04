from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


class Base(DeclarativeBase):
    pass


class WeatherHistory(Base):

    """
    Модель истории погоды
    """

    __tablename__ = 'weather_history'

    id = Column(Integer, primary_key=True)

    date = Column(DateTime)

    temperature = Column(Integer)

    wind_speed = Column(Integer)
    wind_direction = Column(String(50))

    surface_pressure = Column(Integer)

    weather_code = Column(Integer, ForeignKey('weather_code.code'))

    rain_size_precipitation = Column(Integer)
    snow_size_precipitation = Column(Integer)

    rel_weather_code = relationship('WeatherCode', back_populates='rel_weather_history')


class WeatherCode(Base):

    """
    ENUM модель, содержащая расшифровку всех кодов погоды
    """

    __tablename__ = 'weather_code'

    code = Column(Integer, primary_key=True, autoincrement=False)
    description = Column(String(100))

    rel_weather_history = relationship('WeatherHistory', back_populates='rel_weather_code')
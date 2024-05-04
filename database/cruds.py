from . import models

from .connection import db_session

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload


class BaseCruds:

    """
    Класс с универсальными методами запросов к БД.
    """

    @staticmethod
    async def get_all_data(model) -> dict:

        async with db_session() as session:
            query = select(model)
            result = await session.execute(query)

            data = result.scalars().all()

            return data

    @staticmethod
    async def get_data_by_id(model, model_id: int) -> dict | bool:

        async with db_session() as session:

            query = select(model).filter(model.id == model_id)

            result = await session.execute(query)
            data = result.scalar_one_or_none()

            return data

    @staticmethod
    async def delete_data_by_id(model, model_id: int) -> bool:

        async with db_session() as session:
            data = await BaseCruds.get_data_by_id(model=model, model_id=model_id, encode=False)

            await session.delete(data)
            await session.commit()

            return True

    @staticmethod
    async def get_data_by_filter(model, verify: bool = False, **kwargs) -> dict | bool:

        async with db_session() as session:

            query = select(model).filter_by(**kwargs)
            result = await session.execute(query)

            data = result.scalars().all()

            if verify:

                if len(data) == 0:
                    return False

                return True

            return data

    @staticmethod
    async def insert_data(model, **kwargs) -> bool:
        async with db_session() as session:
            data = model(**kwargs)
            session.add(data)

            await session.commit()

            return True


class WeatherCruds:

    """
    Класс для работы с моделью Weather. Содержит более сложные методы, которые пишутся под конкретную модель.
    """

    @staticmethod
    async def get_weather_data_by_limit(limit_row: int = 10):

        async with (db_session() as session):

            query = select(
                models.WeatherHistory
                           ).options(
                selectinload(models.WeatherHistory.rel_weather_code)
            ).limit(
                limit_row
            ).order_by(
                models.WeatherHistory.date
            )

            result = await session.execute(query)
            data = result.scalars().all()

            return data

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import Car


async def get_car_by_url(db: AsyncSession, url: str):
    result = await db.execute(select(Car).where(Car.url == url))
    return result.scalars().first()


async def create_car(db: AsyncSession, car_data: dict):
    db_car = Car(**car_data)
    db.add(car_data)
    await db.commit()
    await db.refresh(car_data)
    return db_car

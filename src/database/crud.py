from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Car


async def get_car_by_url(db: AsyncSession, url: str):
    result = await db.execute(select(Car).where(Car.url == url))
    return result.scalars().first()

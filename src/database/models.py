from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class Car(Base):
    __tablename__ = "cars"
    __table_args__ = (UniqueConstraint("url", name="url_uc"))

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    tittle = Column(String)
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String)
    phone_number = Column(String)  # пример структуры: +38063……..
    image_url = Column(String)
    car_number = Column(String)
    car_vin = Column(String)
    datetime_found = Column(DateTime, default=datetime.utcnow)

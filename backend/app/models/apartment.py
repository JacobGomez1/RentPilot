from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    city = Column(String)

    pool = Column(String)
    gym = Column(String)
    parking = Column(String)
    pet_friendly = Column(String)
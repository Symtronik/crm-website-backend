from ...config.database import DBBase, engine
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

class Parking(DBBase):
    __tablename__: str = 'parking'

    id = Column(Integer, primary_key=True, index=True)
    registation_number = Column(String(20), unique=True, index=True)
    surname = Column(String(50))
    name = Column(String(50))
    email = Column(String(50), unique=True, index=True)


Parking.metadata.create_all(bind=engine)
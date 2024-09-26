from ...config.database import DBBase, engine
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, Time
from sqlalchemy.orm import relationship

STATUS_BOOKED = 0
STATUS_IN_PARKING = 1
STATUS_LEFT = 2
STATUS_CANCEL = 3

class Parking(DBBase):
    __tablename__ = 'parking'

    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String(20))
    surname = Column(String(50), index=True)
    name = Column(String(50))
    email = Column(String(50), index=True)
    phone = Column(String(15))
    departure_date = Column(Date)
    departure_fly_number= Column(String(20), index=True)
    return_date = Column(Date)
    departure_time = Column(Time)
    return_time = Column(Time)
    return_fly_number = Column(String(20), index=True)
    status = Column(Integer, default=STATUS_BOOKED)
    parking_number = Column(String(20))



Parking.metadata.create_all(bind=engine)
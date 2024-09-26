from ...config.database import DBBase, engine
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, Time, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

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
    departure_time = Column(String(6))
    return_time = Column(String(6))
    return_fly_number = Column(String(20), index=True)
    status = Column(Integer, default=STATUS_BOOKED)
    parking_number = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)  # Ustawienie domyślnej wartości
    client_ip = Column(String(45))  # Możesz ustawić na None w schemacie

Parking.metadata.create_all(bind=engine)

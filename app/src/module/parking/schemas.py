from pydantic import BaseModel, EmailStr
from datetime import date

class ParkingCreate(BaseModel):
    registration_number: str
    surname: str
    name: str
    email: EmailStr
    phone: str
    departure_date: date
    departure_fly_number: str
    return_date: date
    departure_time: str
    return_time: str
    return_fly_number: str
    status: int = 0
    parking_number: str



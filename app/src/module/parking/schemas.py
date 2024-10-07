from pydantic import BaseModel, EmailStr
from datetime import date, datetime, time
from typing import Optional

class ParkingCreate(BaseModel):
    registration_number: Optional[str] = None
    surname: str
    name: str
    email: EmailStr
    phone: str
    departure_date: date
    departure_fly_number: Optional[str] = None
    return_date: date
    departure_time: str
    return_time: str
    return_fly_number: Optional[str] = None
    status: int = 0
    parking_number: Optional[str] = None



class ParkingResponse(BaseModel):
    id: Optional[int] = None
    registration_number: Optional[str] = None
    surname: str
    name: str
    email: EmailStr
    phone: str
    departure_date: date
    departure_fly_number: Optional[str] = None
    return_date: date
    departure_time: str
    return_time: str
    return_fly_number: Optional[str] = None
    status: int
    parking_number: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ParkingUpdate(BaseModel):
    name: Optional[str] = None
    # surname: Optional[str] = None
    # departure_date: Optional[date] = None
    # departure_time: Optional[time] = None
    # return_date: Optional[date] = None
    # return_time: Optional[time] = None
    status: Optional[int] = None

    class Config:
        from_attributes = True
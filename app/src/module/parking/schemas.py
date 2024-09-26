from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, time, datetime

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


    @field_validator('departure_time', 'return_time')
    def validate_time(cls, v):
        try:
            h, m = map(int, v.split(':'))
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError('Czas musi być w zakresie 00:00 do 23:59')
            return time(h, m)
        except ValueError:
            raise ValueError('Niewłaściwy format czasu. Użyj HH:MM.')


data = {
    "registration_number": "ABC123",
    "surname": "Kowalski",
    "name": "Jan",
    "email": "jan.kowalski@example.com",
    "phone": "123456789",
    "departure_date": "2024-09-30",
    "departure_fly_number": "FL123",
    "return_date": "2024-10-07",
    "departure_time": "10:30",
    "return_time": "17:04",
    "return_fly_number": "FL456",
    "status": 0,
    "parking_number": "P1",
    "created_at": datetime.now(),
    "client_ip": "192.168.1.1"
}

parking_entry = ParkingCreate(**data)
print(parking_entry)

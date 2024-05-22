from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    username: str
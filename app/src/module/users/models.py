from ...config.database import DBBase, engine
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship


class User(DBBase):
    __tablename__: str = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    surname = Column(String(50))
    name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    permission = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


User.metadata.create_all(bind=engine)

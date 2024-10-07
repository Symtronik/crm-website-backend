from ...config.database import DBBase, engine
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship


class Role(DBBase):
    __tablename__: str = 'role'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class User(DBBase):
    __tablename__: str = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    surname = Column(String(50))
    name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    # permission = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String(255), nullable=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role")
    applications = relationship("UserApplication", back_populates="owner")
class UserApplication(DBBase):
    __tablename__ = 'user_applications'

    id = Column(Integer, primary_key=True, index=True)
    application_name = Column(String(255))
    application_token = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="applications")

User.metadata.create_all(bind=engine)


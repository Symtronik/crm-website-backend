from ...config.database import DBBase
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

# Tabela asocjacyjna łącząca role i uprawnienia
role_permissions = Table(
    'role_permissions',
    DBBase.metadata,
    Column('role_id', ForeignKey('roles.id')),
    Column('permission_id', ForeignKey('permissions.id'))
)

# Model Permission (Uprawnienia)
class Permission(DBBase):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')

# Model Role (Rola)
class Role(DBBase):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')
    users = relationship("User", back_populates="role")

# Model User (Użytkownik)
class User(DBBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    surname = Column(String(50))
    name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String(255), nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")
    applications = relationship("UserApplication", back_populates="owner")

    def has_permission(self, permission_name: str):
        return any(p.name == permission_name for p in self.role.permissions)

# Model Application (Aplikacja użytkownika)
class UserApplication(DBBase):
    __tablename__ = 'user_applications'

    id = Column(Integer, primary_key=True, index=True)
    application_name = Column(String(255))
    application_token = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="applications")

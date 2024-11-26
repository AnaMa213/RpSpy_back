# app/db/models/user.py
import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String

from app.db.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    role = Column(Enum(UserRole), default=UserRole.user)

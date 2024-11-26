import enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[UserRole] = UserRole.user


class UserCreate(UserBase):
    password: str


# Modèle pour la réponse utilisateur
class UserResponse(UserBase):
    id: int
    is_active: bool


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True

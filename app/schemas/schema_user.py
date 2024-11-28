from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.db.models.enums.user_role import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    role: Optional[UserRole] = UserRole.user


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    hashed_password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    role: Optional[UserRole]


class UserResponse(UserBase):
    id: int
    created_campaigns: List[int] = []  # Liste des IDs des campagnes créées
    mj_campaigns: List[int] = []  # Liste des IDs des campagnes où l'utilisateur est MJ
    accessible_campaigns: List[int] = []  # Liste des IDs des campagnes accessibles

    class Config:
        orm_mode = True

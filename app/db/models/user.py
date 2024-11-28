from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.schemas.schema_user import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    role = Column(Enum(UserRole), default=UserRole.user)

    # Relations avec les campagnes
    created_campaigns = relationship(
        "Campaign", foreign_keys="Campaign.created_by", back_populates="created_by_user"
    )
    mj_campaigns = relationship(
        "Campaign", foreign_keys="Campaign.mj_id", back_populates="mj"
    )
    accessible_campaigns = relationship(
        "Campaign", secondary="campaign_users", back_populates="authorized_users"
    )
    players = relationship(
        "Player", back_populates="user", cascade="all, delete-orphan"
    )

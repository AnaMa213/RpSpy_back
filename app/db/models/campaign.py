from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.models.enums.campaign_genre import CampaignGenre
from app.db.models.enums.campaign_status import CampaignStatus


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    genre = Column(Enum(CampaignGenre), nullable=False, default=CampaignGenre.AUTRE)
    description = Column(Text, nullable=True)
    map_url = Column(
        String(2083), nullable=True
    )  # 2083 est la longueur maximale d'une URL
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Créateur
    mj_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Maître du Jeu
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(
        Enum(CampaignStatus), default=CampaignStatus.IN_PROGRESS
    )  # Ex. "en cours", "terminée", "archivée"
    sessions_count = Column(Integer, default=0)
    notes_url = Column(String(2083), nullable=True)

    # Relations
    mj = relationship("User", foreign_keys=[mj_id], back_populates="mj_campaigns")
    created_by_user = relationship(
        "User", foreign_keys=[created_by], back_populates="created_campaigns"
    )
    players = relationship(
        "Player",
        secondary="campaign_players",  # Table d'association
        back_populates="campaigns",
    )
    npcs = relationship(
        "NPC",
        secondary="campaign_npcs",  # Table d'association
        back_populates="campaigns",
    )
    authorized_users = relationship(
        "User", secondary="campaign_users", back_populates="accessible_campaigns"
    )
    sessions = relationship(
        "Session", back_populates="campaign", cascade="all, delete-orphan"
    )

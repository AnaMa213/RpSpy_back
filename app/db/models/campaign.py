from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, event
from sqlalchemy.orm import relationship

from app.db.models.base import Base
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
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
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
        "CampaignSession", back_populates="campaign", cascade="all, delete-orphan"
    )


# Écouteur pour mettre à jour `updated_at`
@event.listens_for(Campaign, "before_update")
def update_timestamp(target):
    target.updated_at = datetime.now(timezone.utc)

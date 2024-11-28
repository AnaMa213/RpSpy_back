from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, event
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class CampaignSession(Base):
    __tablename__ = "sessions"

    # Identité
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # Nom ou titre de la session
    date = Column(
        DateTime(timezone=True), nullable=False
    )  # Date et heure de la session
    description = Column(Text, nullable=True)  # Résumé ou détails de la session

    # Nouveau champ pour le chemin de l'audio
    audio_path = Column(
        String(2083), nullable=True
    )  # 2083 est la longueur maximale d'une URL

    # Relation avec Campaign
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    campaign = relationship("Campaign", back_populates="sessions")

    # Relations many-to-many avec Players et NPCs
    players = relationship(
        "Player",
        secondary="session_players",  # Table d'association
        back_populates="sessions",
    )
    npcs = relationship(
        "NPC",
        secondary="session_npcs",  # Table d'association
        back_populates="sessions",
    )
    dialogs = relationship(
        "Dialog", back_populates="session", cascade="all, delete-orphan"
    )
    # Timestamps
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


# Écouteur pour mettre à jour `updated_at`
@event.listens_for(CampaignSession, "before_update")
def update_timestamp(target):
    target.updated_at = datetime.now(timezone.utc)

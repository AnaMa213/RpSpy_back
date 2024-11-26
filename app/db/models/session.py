from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Session(Base):
    __tablename__ = "sessions"

    # Identité
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # Nom ou titre de la session
    date = Column(
        DateTime(timezone=True), nullable=False
    )  # Date et heure de la session
    description = Column(Text, nullable=True)  # Résumé ou détails de la session

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

    # Relation one-to-many avec Dialogue
    dialogs = relationship(
        "Dialog", back_populates="session", cascade="all, delete-orphan"
    )

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

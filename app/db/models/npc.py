from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class NPC(Base):
    __tablename__ = "npcs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    race = Column(String(100), nullable=False)
    class_name = Column(String(100), nullable=True)
    alignment = Column(String(50), nullable=True)
    level = Column(Integer, default=1)
    strength = Column(Integer, default=10)
    dexterity = Column(Integer, default=10)
    constitution = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    wisdom = Column(Integer, default=10)
    charisma = Column(Integer, default=10)
    description = Column(Text, nullable=True)

    # Relations
    campaigns = relationship(
        "Campaign", secondary="campaign_npcs", back_populates="npcs"
    )
    sessions = relationship(
        "CampaignSession", secondary="session_npcs", back_populates="npcs"
    )

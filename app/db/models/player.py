from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    race = Column(String(100), nullable=False)
    class_name = Column(String(100), nullable=False)  # "class" est réservé en Python
    background = Column(String(100), nullable=True)
    alignment = Column(String(50), nullable=True)
    level = Column(Integer, default=1)
    strength = Column(Integer, default=10)
    dexterity = Column(Integer, default=10)
    constitution = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    wisdom = Column(Integer, default=10)
    charisma = Column(Integer, default=10)
    current_hp = Column(Float, default=10)
    max_hp = Column(Float, default=10)
    skills = Column(Text, nullable=True)  # Liste des compétences (JSON ou texte)
    inventory = Column(Text, nullable=True)  # Liste d'équipement
    description = Column(Text, nullable=True)

    # Relations
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Lien vers User
    user = relationship("User", back_populates="players")
    campaigns = relationship(
        "Campaign", secondary="campaign_players", back_populates="players"
    )
    sessions = relationship(
        "Session", secondary="session_players", back_populates="players"
    )

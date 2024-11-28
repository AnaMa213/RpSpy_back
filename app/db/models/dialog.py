from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Dialog(Base):
    __tablename__ = "dialogs"

    id = Column(Integer, primary_key=True, index=True)
    order = Column(Integer, nullable=False)  # Order of the dialog line
    start = Column(String(8), nullable=False)  # Start time (HH:MM:SS)
    end = Column(String(8), nullable=True)  # End time (HH:MM:SS)
    speaker_id = Column(
        Integer, ForeignKey("players.id")
    )  # ID of the player or GM (Game Master)
    content = Column(Text, nullable=False)  # Text of the dialog line

    session_id = Column(
        Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    session = relationship("CampaignSession", back_populates="dialogs")

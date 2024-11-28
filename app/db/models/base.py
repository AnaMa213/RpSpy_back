from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declarative_base

# Déclarez la base SQLAlchemy
Base = declarative_base()

# Tables d'association
campaign_users = Table(
    "campaign_users",
    Base.metadata,
    Column(
        "campaign_id",
        Integer,
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
)

campaign_players = Table(
    "campaign_players",
    Base.metadata,
    Column(
        "campaign_id",
        Integer,
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "player_id",
        Integer,
        ForeignKey("players.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

campaign_npcs = Table(
    "campaign_npcs",
    Base.metadata,
    Column(
        "campaign_id",
        Integer,
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "npc_id", Integer, ForeignKey("npcs.id", ondelete="CASCADE"), primary_key=True
    ),
)

session_npcs = Table(
    "session_npcs",
    Base.metadata,
    Column(
        "session_id",
        Integer,
        ForeignKey("sessions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "npc_id", Integer, ForeignKey("npcs.id", ondelete="CASCADE"), primary_key=True
    ),
)

session_players = Table(
    "session_players",
    Base.metadata,
    Column(
        "session_id",
        Integer,
        ForeignKey("sessions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "player_id",
        Integer,
        ForeignKey("players.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

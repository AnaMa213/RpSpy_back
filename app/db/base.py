from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Table d'association entre Campaign et User
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


# Fonction pour importer les modèles et garantir leur enregistrement dans Base.metadata
def import_models():
    from app.db.models.campaign import Campaign  # Importez également Campaign ici
    from app.db.models.dialog import Dialog
    from app.db.models.npc import NPC
    from app.db.models.player import Player
    from app.db.models.session import Session
    from app.db.models.user import (
        User,
    )  # Import différé pour éviter les imports circulaires

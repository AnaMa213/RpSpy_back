# Permet d'importer tous les endpoints depuis app.api.routes
# models/__init__.py

from .base import Base
from .campaign import Campaign
from .campaign_session import CampaignSession
from .dialog import Dialog
from .npc import NPC
from .player import Player
from .user import User

__all__ = ["Base", "Campaign", "CampaignSession", "Dialog", "NPC", "Player", "User"]

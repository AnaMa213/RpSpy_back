# Permet d'importer tous les endpoints depuis app.api.routes

from .schema_campaign import CampaignCreate, CampaignResponse, CampaignUpdate
from .schema_dialog import DialogCreate, DialogResponse, DialogUpdate
from .schema_npc import NPCCreate, NPCResponse, NPCUpdate
from .schema_player import PlayerCreate, PlayerResponse, PlayerUpdate
from .schema_session import SessionCreate, SessionResponse, SessionUpdate
from .schema_token import Token
from .schema_user import UserCreate, UserResponse, UserRole, UserUpdate

__all__ = [
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignResponse",
    "DialogCreate",
    "DialogResponse",
    "DialogUpdate",
    "NPCCreate",
    "NPCResponse",
    "NPCUpdate",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserRole",
    "SessionCreate",
    "SessionResponse",
    "SessionUpdate",
    "PlayerCreate",
    "PlayerUpdate",
    "PlayerResponse",
    "Token",
]

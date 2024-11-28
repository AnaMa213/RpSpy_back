import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.db.models.enums.campaign_genre import CampaignGenre
from app.db.models.enums.campaign_status import CampaignStatus


class CampaignBase(BaseModel):
    name: str
    genre: Optional[CampaignGenre] = CampaignGenre.AUTRE
    description: Optional[str] = None
    map_url: Optional[str] = None
    status: Optional[CampaignStatus] = CampaignStatus.IN_PROGRESS
    notes_url: Optional[str] = None
    mj_id: int  # Maître du jeu
    created_by: int  # Créateur de la campagne


class CampaignCreate(CampaignBase):
    pass  # Hérite de CampaignBase sans modification


class CampaignUpdate(BaseModel):
    name: Optional[str]
    genre: Optional[CampaignGenre]
    description: Optional[str]
    map_url: Optional[str]
    status: Optional[CampaignStatus]
    notes_url: Optional[str]
    mj_id: Optional[int]
    players: Optional[List[int]] = None  # Liste des IDs des joueurs
    npcs: Optional[List[int]] = None  # Liste des IDs des PNJs


class CampaignResponse(CampaignBase):
    id: int
    created_at: datetime
    updated_at: datetime
    sessions_count: int
    players: List[int] = []  # Liste des IDs des joueurs
    npcs: List[int] = []  # Liste des IDs des PNJs
    authorized_users: List[int] = []  # Liste des IDs des utilisateurs autorisés

    model_config = {
        "arbitrary_types_allowed": True,  # Permet les types arbitraires comme datetime
    }

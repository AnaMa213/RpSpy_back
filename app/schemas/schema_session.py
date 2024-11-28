from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class SessionBase(BaseModel):
    title: str
    date: datetime
    description: Optional[str] = None
    audio_path: Optional[str] = None
    campaign_id: int


class SessionCreate(SessionBase):
    pass  # Inhérente de SessionBase, aucun champ supplémentaire requis


class SessionUpdate(BaseModel):
    title: Optional[str]
    date: Optional[datetime]
    description: Optional[str]
    audio_path: Optional[str]
    campaign_id: Optional[int]
    players: Optional[List[int]] = None  # Liste des IDs des joueurs
    npcs: Optional[List[int]] = None  # Liste des IDs des PNJs


class SessionResponse(SessionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    players: List[int] = []  # Liste des IDs des joueurs
    npcs: List[int] = []  # Liste des IDs des PNJs

    model_config = {
        "arbitrary_types_allowed": True,  # Permet les types arbitraires comme datetime
    }

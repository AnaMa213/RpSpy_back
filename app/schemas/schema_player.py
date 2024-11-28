from typing import List, Optional

from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str
    race: str
    class_name: str
    background: Optional[str] = None
    alignment: Optional[str] = None
    level: Optional[int] = 1
    strength: Optional[int] = 10
    dexterity: Optional[int] = 10
    constitution: Optional[int] = 10
    intelligence: Optional[int] = 10
    wisdom: Optional[int] = 10
    charisma: Optional[int] = 10
    current_hp: Optional[float] = 10
    max_hp: Optional[float] = 10
    skills: Optional[str] = None  # JSON ou texte
    inventory: Optional[str] = None  # JSON ou texte
    description: Optional[str] = None


class PlayerCreate(PlayerBase):
    user_id: int  # ID de l'utilisateur auquel appartient le joueur


class PlayerUpdate(BaseModel):
    name: Optional[str]
    race: Optional[str]
    class_name: Optional[str]
    background: Optional[str]
    alignment: Optional[str]
    level: Optional[int]
    strength: Optional[int]
    dexterity: Optional[int]
    constitution: Optional[int]
    intelligence: Optional[int]
    wisdom: Optional[int]
    charisma: Optional[int]
    current_hp: Optional[float]
    max_hp: Optional[float]
    skills: Optional[str]
    inventory: Optional[str]
    description: Optional[str]
    campaigns: Optional[List[int]] = None  # Liste des IDs des campagnes
    sessions: Optional[List[int]] = None  # Liste des IDs des sessions


class PlayerResponse(PlayerBase):
    id: int
    user_id: int
    campaigns: List[int] = []  # Liste des IDs des campagnes
    sessions: List[int] = []  # Liste des IDs des sessions

    class Config:
        orm_mode = True

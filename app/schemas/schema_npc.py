from typing import List, Optional

from pydantic import BaseModel


class NPCBase(BaseModel):
    name: str
    race: str
    class_name: Optional[str] = None
    alignment: Optional[str] = None
    level: Optional[int] = 1
    strength: Optional[int] = 10
    dexterity: Optional[int] = 10
    constitution: Optional[int] = 10
    intelligence: Optional[int] = 10
    wisdom: Optional[int] = 10
    charisma: Optional[int] = 10
    description: Optional[str] = None


class NPCCreate(NPCBase):
    pass  # Hérite de NPCBase sans modification


class NPCUpdate(BaseModel):
    name: Optional[str]
    race: Optional[str]
    class_name: Optional[str]
    alignment: Optional[str]
    level: Optional[int]
    strength: Optional[int]
    dexterity: Optional[int]
    constitution: Optional[int]
    intelligence: Optional[int]
    wisdom: Optional[int]
    charisma: Optional[int]
    description: Optional[str]
    campaigns: Optional[List[int]] = None  # Liste des IDs des campagnes
    sessions: Optional[List[int]] = None  # Liste des IDs des sessions


class NPCResponse(NPCBase):
    id: int
    campaigns: List[int] = []  # Liste des IDs des campagnes
    sessions: List[int] = []  # Liste des IDs des sessions

    class Config:
        orm_mode = True

from typing import Optional

from pydantic import BaseModel, Field


class DialogBase(BaseModel):
    order: int = Field(..., description="Order of the dialog line")
    start: str = Field(..., description="Start time of the dialog (HH:MM:SS)")
    end: Optional[str] = Field(None, description="End time of the dialog (HH:MM:SS)")
    speaker_id: Optional[int] = Field(
        None, description="ID of the speaker (player or GM)"
    )
    content: str = Field(..., description="Content of the dialog line")


class DialogCreate(DialogBase):
    session_id: int = Field(..., description="ID of the session this dialog belongs to")


class DialogUpdate(BaseModel):
    order: Optional[int]
    start: Optional[str]
    end: Optional[str]
    speaker_id: Optional[int]
    content: Optional[str]


class DialogResponse(DialogBase):
    id: int
    session_id: int

    class Config:
        orm_mode = True

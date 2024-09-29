from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Optional
    from app.models.participant import Participant
    from app.models.blacklist import Blacklist


class SecretSantaList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    participants: List[Participant] = Relationship(back_populates="list")
    blacklists: List[Blacklist] = Relationship(back_populates="list")

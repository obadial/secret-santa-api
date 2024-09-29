from __future__ import annotations
from sqlmodel import SQLModel, Field
from sqlalchemy.orm import relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.participant import Participant
    from app.models.blacklist import Blacklist


class SecretSantaList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    participants: List[Participant] = relationship("Participant", back_populates="list")
    blacklists: List[Blacklist] = relationship("Blacklist", back_populates="list")

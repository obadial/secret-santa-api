from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field
from typing import List, Optional
import uuid


class SecretSantaList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    participants: List["Participant"] = relationship(back_populates="list")
    blacklists: List["Blacklist"] = relationship(back_populates="list")

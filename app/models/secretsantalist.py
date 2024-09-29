from sqlalchemy.orm import Relationship
from sqlalchemy.orm import Relationship
from sqlmodel import SQLModel, Field
from typing import List, Optional
import uuid


class SecretSantaList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    participants: List["Participant"] = Relationship(back_populates="list")
    blacklists: List["Blacklist"] = Relationship(back_populates="list")

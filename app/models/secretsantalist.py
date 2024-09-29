from sqlmodel import SQLModel, Field, Relationship
from typing import List
from app.models.participant import Participant
from app.models.blacklist import Blacklist


class SecretSantaList(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    participants: List["Participant"] = Relationship(back_populates="list")
    blacklists: List["Blacklist"] = Relationship(back_populates="list")

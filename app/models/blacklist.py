from __future__ import annotations
from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.secretsantalist import SecretSantaList


class Blacklist(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    participant_id: int = Field(default=None, foreign_key="participant.id")
    blacklisted_participant_id: int = Field(default=None, foreign_key="participant.id")
    list_id: int = Field(default=None, foreign_key="secretsantalist.id")
    list: SecretSantaList = Relationship(back_populates="blacklists")

    @validator("participant_id", "blacklisted_participant_id")
    def id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("IDs must be positive integers")
        return value

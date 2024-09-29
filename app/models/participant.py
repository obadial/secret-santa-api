from __future__ import annotations
from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.secretsantalist import SecretSantaList


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    list_id: Optional[int] = Field(default=None, foreign_key="secretsantalist.id")
    list: Optional[SecretSantaList] = Relationship(back_populates="participants")

    @validator("name")
    def name_must_not_be_empty(cls, value):
        if not value or value.strip() == "":
            raise ValueError("Name must not be empty")
        if len(value) > 50:
            raise ValueError("Name must not exceed 50 characters")
        return value

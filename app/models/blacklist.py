from sqlmodel import SQLModel, Field
from sqlalchemy.orm import relationship
from typing import Optional
from pydantic import validator
from app.models.secretsantalist import SecretSantaList


class Blacklist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: Optional[int] = Field(default=None, foreign_key="participant.id")
    blacklisted_participant_id: Optional[int] = Field(
        default=None, foreign_key="participant.id"
    )
    list_id: Optional[int] = Field(default=None, foreign_key="secretsantalist.id")
    list: Optional["SecretSantaList"] = relationship(
        "SecretSantaList", back_populates="blacklists"
    )

    @validator("participant_id", "blacklisted_participant_id")
    def id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("IDs must be positive integers")
        return value

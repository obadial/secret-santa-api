from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import validator


class Blacklist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: int
    blacklisted_participant_id: int

    @validator("participant_id", "blacklisted_participant_id")
    def id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("IDs must be positive integers")
        return value

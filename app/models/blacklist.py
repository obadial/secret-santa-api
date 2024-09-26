from sqlmodel import SQLModel, Field
from typing import Optional


class Blacklist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: int
    blacklisted_participant_id: int

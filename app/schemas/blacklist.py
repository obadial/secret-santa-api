from pydantic import BaseModel, validator


class BlacklistCreate(BaseModel):
    participant_id: int
    blacklisted_participant_id: int

    @validator("participant_id", "blacklisted_participant_id")
    def id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("IDs must be positive integers")
        return value

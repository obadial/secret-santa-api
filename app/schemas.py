from pydantic import BaseModel, validator


class ParticipantCreate(BaseModel):
    name: str

    @validator("name")
    def name_must_not_be_empty(cls, value):
        if not value or value.strip() == "":
            raise ValueError("Name must not be empty")
        if len(value) > 50:
            raise ValueError("Name must not exceed 50 characters")
        return value


class BlacklistCreate(BaseModel):
    participant_id: int
    blacklisted_participant_id: int

    @validator("participant_id", "blacklisted_participant_id")
    def id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("IDs must be positive integers")
        return value

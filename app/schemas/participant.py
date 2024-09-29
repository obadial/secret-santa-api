from pydantic import BaseModel, validator


class ParticipantCreate(BaseModel):
    name: str

    @validator("name", allow_reuse=True)
    def name_not_empty(cls, value):
        if not value or value.strip() == "":
            raise ValueError("Name must not be empty")
        if len(value) > 50:
            raise ValueError("Name must not exceed 50 characters")
        return value

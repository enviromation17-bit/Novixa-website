from pydantic import BaseModel, Field


class ContactStatusUpdate(BaseModel):

    status: str = Field(
        min_length=1,
        max_length=20,
        pattern="^(new|contacted|qualified|closed)$"
    )
from pydantic import BaseModel, Field, EmailStr


class ContactRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100,
        example="Salman Bari"
    )

    company: str = Field(
        min_length=2,
        max_length=100,
        example="Novixa"
    )

    email: EmailStr = Field(
        example="salman@novixa.com"
    )

    project: str = Field(
        min_length=3,
        max_length=150,
        example="AI Customer Support Agent"
    )

    message: str = Field(
        min_length=10,
        max_length=2000,
        example="We need an AI assistant for our business."
    )
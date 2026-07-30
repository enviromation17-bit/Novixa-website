from pydantic import BaseModel, EmailStr


class ContactRequest(BaseModel):

    name: str

    company: str

    email: EmailStr

    project: str

    message: str
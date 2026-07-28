from pydantic import BaseModel, EmailStr


class ContactRequest(BaseModel):

    name: str

    email: EmailStr

    company: str

    message: str
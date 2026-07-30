from fastapi import APIRouter

from app.schemas.contact import ContactRequest
from app.database import SessionLocal
from app.models.contact import Contact
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/contact")
def submit_contact(data: ContactRequest):

    db = SessionLocal()

    try:

        new_contact = Contact(
            name=data.name,
            company=data.company,
            email=data.email,
            project=data.project,
            message=data.message
        )

        db.add(new_contact)

        db.commit()

        db.refresh(new_contact)

        return {
            "success": True,
            "message": f"Thank you {data.name}! We have received your project request.",
            "id": new_contact.id
        }

    finally:

        db.close()
@router.get("/contacts")
def get_contacts():

    db = SessionLocal()

    try:

        contacts = db.query(Contact).all()

        return contacts

    finally:

        db.close()
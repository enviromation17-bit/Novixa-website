from fastapi import APIRouter
from app.schemas.contact import ContactRequest
from app.database import SessionLocal
from app.models.contact import Contact
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import Depends
from app.core.dependencies import verify_token
from app.core.logger import logger
from sqlalchemy.orm import Session
from fastapi import Depends
from app.dependencies import get_db

router = APIRouter()



@router.post(
    "/contact",
    summary="Create New Client Lead",
    description="Stores a new client inquiry into the database.",
    tags=["Client Leads"]
)
def submit_contact(
    data: ContactRequest,
    db: Session = Depends(get_db)
):

    

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
        logger.info(
        f"New contact received from {new_contact.name} ({new_contact.email})"
        )

        return {

            "success": True,

            "message": f"Thank you {data.name}! We have received your project request.",

            "id": new_contact.id

        }

    except Exception:

        db.rollback()

        raise HTTPException(

            status_code=500,

            detail="Unable to save contact request."

        )

    finally:

        db.close()

@router.get("/contacts")
def get_contacts(
    user=Depends(verify_token)
):

    db = SessionLocal()

    try:

        contacts = db.query(Contact).all()

        return contacts

    finally:

        db.close()
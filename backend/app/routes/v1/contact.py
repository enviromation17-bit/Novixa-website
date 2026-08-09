from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.error import ErrorResponse
from app.schemas.contact import ContactRequest
from app.schemas.response import APIResponse
from app.models.contact import Contact
from app.dependencies import get_db
from app.core.dependencies import verify_token
from app.core.logger import logger
from fastapi import Request
from app.core.limiter import limiter


router = APIRouter()



@router.get(
    "/contacts",
    summary="Get Client Leads",
    description="Returns all client inquiries. Authentication required.",
       tags=["Client Leads"]
)
def get_contacts(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    try:

        contacts = db.query(Contact).all()

        return contacts

    except Exception:

        raise HTTPException(

            status_code=500,

            detail="Unable to retrieve contact requests."

        )

    finally:

        db.close()


@router.post(
    "/contacts",
    summary="Create New Client Lead",
    description="Stores a new client inquiry into the database.",
    tags=["Client Leads"],
    response_model=APIResponse,
    responses={
        200: {
            "description": "Lead created successfully"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        }
    }
)
@limiter.limit("5/minute")
def submit_contact(
    request: Request,
    data: ContactRequest,
    db: Session = Depends(get_db)
):
    try:
        new_contact = Contact(
            name=data.name,
            company=data.company,
            email=data.email,
            project=data.project,
            message=data.message,
            status="new"
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        logger.info(
            f"New contact received from {new_contact.name} ({new_contact.email})"
        )
        return APIResponse(
            success=True,
            message=f"Thank you {data.name}! We have received your project request.",
            data={
                "id": new_contact.id
            }
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save contact request."
        )
    finally:
        db.close()


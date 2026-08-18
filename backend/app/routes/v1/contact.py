from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.schemas.error import ErrorResponse
from app.schemas.contact import ContactRequest
from app.schemas.response import APIResponse
from app.schemas.contact_status import ContactStatusUpdate

from app.models.contact import Contact
from app.dependencies import get_db
from app.core.dependencies import verify_token
from app.core.logger import logger
from app.core.limiter import limiter


router = APIRouter()


# ========================================
# GET ALL CLIENT LEADS
# ========================================

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


# ========================================
# CREATE NEW CLIENT LEAD
# ========================================

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
            f"New contact received from "
            f"{new_contact.name} ({new_contact.email})"
        )

        return APIResponse(
            success=True,
            message=(
                f"Thank you {data.name}! "
                "We have received your project request."
            ),
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


# ========================================
# UPDATE CLIENT LEAD STATUS
# ========================================

@router.patch(
    "/contacts/{contact_id}/status",
    summary="Update Client Lead Status",
    description="Updates the status of an authenticated client lead.",
    tags=["Client Leads"]
)
def update_contact_status(
    contact_id: int,
    data: ContactStatusUpdate,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    try:

        contact = db.query(Contact).filter(
            Contact.id == contact_id
        ).first()

        if not contact:

            raise HTTPException(
                status_code=404,
                detail="Contact not found."
            )

        contact.status = data.status

        db.commit()
        db.refresh(contact)

        logger.info(
            f"Contact {contact.id} status changed "
            f"to {contact.status}"
        )

        return APIResponse(
            success=True,
            message="Contact status updated successfully.",
            data={
                "id": contact.id,
                "status": contact.status
            }
        )

    except HTTPException:

        raise

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to update contact status."
        )

    finally:

        db.close()


# ========================================
# DELETE CLIENT LEAD
# ========================================

@router.delete(
    "/contacts/{contact_id}",
    summary="Delete Client Lead",
    description="Permanently deletes an authenticated client lead.",
    tags=["Client Leads"],
    response_model=APIResponse
)
def delete_contact(
    contact_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    try:

        contact = db.query(Contact).filter(
            Contact.id == contact_id
        ).first()

        if not contact:
            raise HTTPException(
                status_code=404,
                detail="Contact not found."
            )

        db.delete(contact)
        db.commit()

        logger.info(
            f"Contact {contact_id} deleted by administrator."
        )

        return APIResponse(
            success=True,
            message="Contact deleted successfully.",
            data={
                "id": contact_id
            }
        )

    except HTTPException:
        raise

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to delete contact."
        )

    finally:
        db.close()
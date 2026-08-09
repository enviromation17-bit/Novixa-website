from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.schemas.contact import ContactRequest
from app.core.logger import logger
from app.repositories.contact_repository import save_contact


def create_contact(
    db: Session,
    data: ContactRequest
):
    new_contact = Contact(
        name=data.name,
        company=data.company,
        email=data.email,
        project=data.project,
        message=data.message,
        status="new",
    )

    new_contact = save_contact(
        db,
        new_contact
    )

    logger.info(
        f"New contact received from {new_contact.name} ({new_contact.email})"
    )

    return new_contact
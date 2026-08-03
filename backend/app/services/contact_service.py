from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.schemas.contact import ContactRequest
from app.core.logger import logger


def create_contact(
    db: Session,
    data: ContactRequest
):
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

    return new_contact
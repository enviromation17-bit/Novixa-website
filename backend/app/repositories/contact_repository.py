from sqlalchemy.orm import Session

from app.models.contact import Contact


def create_contact(
    db: Session,
    contact: Contact
):
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def get_all_contacts(
    db: Session
):
    return db.query(Contact).all()


def get_contact_by_id(
    db: Session,
    contact_id: int
):
    return (
        db.query(Contact)
        .filter(Contact.id == contact_id)
        .first()
    )


def delete_contact(
    db: Session,
    contact: Contact
):
    db.delete(contact)
    db.commit()
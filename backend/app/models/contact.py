from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    company = Column(String)

    email = Column(String, nullable=False)

    project = Column(String)

    message = Column(String, nullable=False)

    status = Column(
        String,
        nullable=False,
        default="new",
        index=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
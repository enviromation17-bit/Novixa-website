from fastapi import APIRouter

from app.schemas.contact import ContactRequest

router = APIRouter()


@router.post("/contact")
def submit_contact(data: ContactRequest):

    return {

        "success": True,

        "message": "Contact request received successfully.",

        "data": data

    }
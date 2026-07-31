from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest

router = APIRouter()


ADMIN_USERNAME = "admin"

ADMIN_PASSWORD = "novixa123"


@router.post(

    "/login",

    summary="Admin Login",

    tags=["Authentication"]

)

def login(data: LoginRequest):

    if (

        data.username == ADMIN_USERNAME

        and

        data.password == ADMIN_PASSWORD

    ):

        return {

            "success": True,

            "message": "Login Successful"

        }

    raise HTTPException(

        status_code=401,

        detail="Invalid Username or Password"

    )
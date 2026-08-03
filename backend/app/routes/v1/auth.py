from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest 
from app.core.security import verify_password, create_access_token

router = APIRouter()

from app.core.config import (
    ADMIN_USERNAME,
    ADMIN_PASSWORD_HASH
)

@router.post(
    "/login",
    summary="Admin Login",
    tags=["Authentication"]
)
def login(data: LoginRequest):

    if (
        data.username == ADMIN_USERNAME
        and verify_password(
            data.password,
            ADMIN_PASSWORD_HASH
        )
    ):
        access_token = create_access_token(
            {"sub": data.username}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    raise HTTPException(
        status_code=401,
        detail="Invalid Username or Password"
    )
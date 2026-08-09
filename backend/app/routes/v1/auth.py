print("AUTH.PY LOADED")
from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest 
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter()



@router.post(
    "/login",
    summary="Administrator Login",
    description="Authenticates an administrator and returns a JWT access token.",
    tags=["Authentication"]
)
def login(data: LoginRequest):

    print("ENV USER:", settings.ADMIN_USERNAME)
    print("INPUT USER:", data.username)
    print("HASH:", settings.ADMIN_PASSWORD_HASH)

    print(
        "PASSWORD MATCH:",
        verify_password(
            data.password,
            settings.ADMIN_PASSWORD_HASH
        )
    )

    if (
        data.username == settings.ADMIN_USERNAME
        and verify_password(
            data.password,
            settings.ADMIN_PASSWORD_HASH
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
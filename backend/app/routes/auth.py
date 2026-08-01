import token

from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest 
from app.core.security import verify_password, create_access_token

router = APIRouter()

ADMIN_USERNAME = "admin"

ADMIN_HASH = "$argon2id$v=19$m=65536,t=3,p=4$VJecy1Qi7DMR3ljrG3zRVw$ObfaplStZMERpb/aU3Jy96qyId4515tqH1doYEOmJco"


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
            ADMIN_HASH
        )
    ):
        token = create_access_token(
    {"sub": data.username}
)

    return {

        "access_token": token,

        "token_type": "bearer"

    }

    raise HTTPException(
        status_code=401,
        detail="Invalid Username or Password"
    )
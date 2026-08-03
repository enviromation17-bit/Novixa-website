from datetime import datetime, timedelta

from jose import jwt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)



def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password: str, hashed: str):
    return password_hash.verify(password, hashed)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
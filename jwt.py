from datetime import datetime, timedelta
from typing import TypedDict

from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr

from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


class JWTPayload(TypedDict):
    user_id: int
    sub: EmailStr
    exp: datetime


def create_access_token(subject: str, user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "user_id": user_id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str) -> JWTPayload:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type: ignore
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Signature verification failed",
        )


async def get_current_user(
        token: str = Depends(oauth2_schema),
) -> int:
    user_id = decode_jwt(token)["user_id"]
    return user_id

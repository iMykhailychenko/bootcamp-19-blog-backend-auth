from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, HttpUrl

from utils import PaginationSchema


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    created_at: datetime
    avatar: Optional[HttpUrl]
    bio: Optional[str]
    email: EmailStr


class UsersList(PaginationSchema):
    data: List[User]


class UserCreateRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserPartialUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[HttpUrl]
    bio: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str

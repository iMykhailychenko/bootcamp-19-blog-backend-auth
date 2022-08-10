from datetime import datetime

from typing import Optional, List
from pydantic import BaseModel, EmailStr, HttpUrl

from utils import PaginationSchema


class Comment(BaseModel):
    id: int
    post_id: int
    content: str
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int


class CommentListItem(Comment):
    first_name: str
    last_name: str
    avatar: Optional[HttpUrl]
    email: EmailStr


class CommentList(PaginationSchema):
    data: List[CommentListItem]


class NewCommentBody(BaseModel):
    content: str


class UpdateCommentBody(BaseModel):
    content: Optional[str]

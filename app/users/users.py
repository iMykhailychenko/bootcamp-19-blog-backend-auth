from typing import Mapping

from fastapi import APIRouter, HTTPException, Response, status, Depends

from app.users import crud
from app.users.crud import get_user_by_email, select_users, count_total_users
from app.users.schemas import UserCreateRequest, User, Token, LoginRequest, UsersList, UserPartialUpdate
from app.users.utils import get_password_hash, verify_password
from jwt import get_current_user, create_access_token
from utils import pagination

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(body: UserCreateRequest) -> Response:
    """ Create new user """
    if await crud.user_exist(email=body.email):
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )

    await crud.create_user(
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        hashed_password=get_password_hash(body.password),
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/login", response_model=Token)
async def login_user(body: LoginRequest) -> dict:
    """ OAuth2 compatible token login, get an access token for future requests """
    user = dict(await get_user_by_email(email=body.email))

    if not user or not verify_password(body.password, user.get("password", "")):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {
        "access_token": create_access_token(
            subject=body.email, user_id=user["id"]
        ),
        "token_type": "Bearer",
    }


@router.get("", response_model=UsersList)
async def get_post_list(limit: int = 10, page: int = 1, search: str = None) -> UsersList:
    """Return users list with pagination"""
    posts = await select_users(limit=limit, page=page, search=search)
    total = await count_total_users(search=search)

    return UsersList(**pagination(data=posts, limit=limit, page=page, total=total))


@router.get("/profile", response_model=User)
async def logged_in_user_details(user_id: int = Depends(get_current_user)) -> Mapping:
    """ Get logged-in user details """
    return await crud.get_user_by_id(user_id)


@router.put("/profile", response_model=User)
async def update_user(
        update_user_data: UserPartialUpdate,
        user_id: int = Depends(get_current_user),
) -> User:
    stored_user_data = await crud.get_user_by_id(user_id)
    await crud.partial_update_user(
        user_id=user_id,
        update_user_data=update_user_data,
        stored_user_data=stored_user_data,
    )

    user = await crud.get_user_by_id(user_id)
    return User(**user)

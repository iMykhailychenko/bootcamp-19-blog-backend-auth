from typing import Mapping, List

from pydantic import EmailStr

from app.users.schemas import UserPartialUpdate
from db import database


async def user_exist(email: EmailStr) -> bool:
    query = "SELECT TRUE FROM users WHERE email = :email"
    return bool(await database.fetch_one(query=query, values={"email": email}))


async def create_user(
        email: str,
        first_name: str,
        last_name: str,
        hashed_password: str,
) -> None:
    query = """
    INSERT INTO users (
        password,
        first_name,
        last_name,
        email
    )
    VALUES (
        :password,
        :first_name,
        :last_name,
        :email
    )
    """
    values = {
        "password": hashed_password,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
    }
    await database.execute(query=query, values=values)


async def get_user_by_id(user_id: int) -> dict:
    query = """
    SELECT bio, created_at, email, first_name, id, last_name, avatar
    FROM users
    WHERE id = :id
    """
    return await database.fetch_one(query=query, values={"id": user_id})


async def get_user_by_email(email: str) -> dict:
    query = """
        SELECT bio, created_at, email, first_name, id, last_name, avatar, password
        FROM users
        WHERE email = :email
        """
    return await database.fetch_one(query=query, values={"email": email})


async def partial_update_user(
        user_id: int,
        update_user_data: UserPartialUpdate,
        stored_user_data: Mapping,
) -> None:
    stored_user_model = UserPartialUpdate(**stored_user_data)
    update_data = update_user_data.dict(exclude_unset=True)
    updated_user = stored_user_model.copy(update=update_data)

    query = """
    UPDATE users
    SET
        bio = :bio,
        first_name = :first_name,
        last_name = :last_name,
        avatar = :avatar
    WHERE id = :user_id
    """
    values = {
        "bio": updated_user.bio,
        "first_name": updated_user.first_name,
        "last_name": updated_user.last_name,
        "avatar": updated_user.avatar,
        "user_id": user_id
    }
    await database.execute(query=query, values=values)


async def select_users(limit: int, page: int, search: str) -> List[dict]:
    offset = (page - 1) * limit

    query = """
    SELECT *
    FROM users
    WHERE (((:search)::varchar IS NULL OR first_name ilike :search)
          OR ((:search)::varchar IS NULL OR last_name ilike :search))
    ORDER BY created_at DESC
    LIMIT :limit
    OFFSET :offset
    """
    return await database.fetch_all(query=query, values={"limit": limit, "offset": offset, "search": f"%{search}%" if search else None})


async def count_total_users(search: str) -> int:
    query = """
    SELECT count(*) 
    FROM users
    WHERE (((:search)::varchar IS NULL OR first_name ilike :search)
          OR ((:search)::varchar IS NULL OR last_name ilike :search))
    """
    count = await database.fetch_one(query=query, values={"search": f"%{search}%" if search else None})
    return int(count["count"]) if count else 0

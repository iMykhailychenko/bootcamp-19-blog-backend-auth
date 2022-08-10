from typing import List

from db import database
from app.posts.schemas import NewPostBody, UpdatePostBody, Post


async def find_post(post_id: int) -> dict:
    return await database.fetch_one(query="SELECT * FROM posts WHERE id = :id", values={"id": post_id})


async def increment_views(post_id: int) -> None:
    return await database.execute(query="UPDATE posts SET views = views + 1 WHERE posts.id = :id",
                                  values={"id": post_id})


async def select_posts(limit: int, page: int, search: str) -> List[dict]:
    offset = (page - 1) * limit

    query = """
    SELECT
        posts.id, 
        posts.title, 
        posts.content, 
        posts.image, 
        posts.views, 
        posts.user_id, 
        posts.preview_image, 
        posts.created_at, 
        posts.updated_at, 
        users.first_name,
        users.last_name,
        users.avatar,
        users.email
    FROM posts
    INNER JOIN users ON posts.user_id = users.id
    WHERE (((:search)::varchar IS NULL OR title ilike :search)
          OR ((:search)::varchar IS NULL OR content ilike :search))
    ORDER BY posts.created_at DESC
    LIMIT :limit
    OFFSET :offset
    """
    return await database.fetch_all(query=query, values={"limit": limit, "offset": offset,
                                                         "search": f"%{search}%" if search else None})


async def count_total_post(search: str) -> int:
    query = """
    SELECT count(*) 
    FROM posts
    WHERE (((:search)::varchar IS NULL OR title ilike :search)
          OR ((:search)::varchar IS NULL OR content ilike :search))
    """
    count = await database.fetch_one(query=query, values={"search": f"%{search}%" if search else None})
    return int(count["count"]) if count else 0


@database.transaction()
async def insert_post(user_id: int, body: NewPostBody) -> dict:
    query = """
    INSERT INTO posts (
        title,
        content,
        image,
        preview_image,
        user_id
    )
    VALUES (
        :title,
        :content,
        :image,
        :preview_image,
        :user_id
    )
    RETURNING id
    """
    values = {
        "title": body.title,
        "content": body.content,
        "image": body.image,
        "preview_image": body.preview_image,
        "user_id": user_id
    }

    post_id = await database.execute(query=query, values=values)
    return await find_post(post_id)


async def delete_post(post_id):
    query = """
    DELETE FROM posts 
    WHERE posts.id = :id
    """
    await database.execute(query=query, values={"id": post_id})


@database.transaction()
async def update_post(post_id: int, old_post_data: dict, new_post_data: UpdatePostBody) -> dict:
    old_post_model = Post(**old_post_data)
    updated_post = old_post_model.copy(update=new_post_data.dict(exclude_none=True))

    query = """
    UPDATE posts
    SET
        title = :title,
        content = :content,
        image = :image,
        preview_image = :preview_image,
        updated_at = CURRENT_TIMESTAMP
    WHERE posts.id = :id    
    """

    values = {
        "id": post_id,
        "title": updated_post.title,
        "content": updated_post.content,
        "image": updated_post.image,
        "preview_image": updated_post.preview_image
    }

    await database.execute(query=query, values=values)
    return await find_post(post_id)

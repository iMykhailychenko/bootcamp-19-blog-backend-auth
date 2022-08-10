from fastapi import APIRouter, HTTPException, Response, Depends

from jwt import get_current_user
from utils import pagination
from app.posts import crud
from app.posts.schemas import Post, PostsList, NewPostBody, UpdatePostBody

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("", response_model=PostsList)
async def get_post_list(limit: int = 10, page: int = 1, search: str = None) -> PostsList:
    """Return post list with pagination"""
    posts = await crud.select_posts(limit=limit, page=page, search=search)
    total = await crud.count_total_post(search=search)

    return PostsList(**pagination(data=posts, limit=limit, page=page, total=total))


@router.post("", response_model=Post)
async def create_post(body: NewPostBody, user_id: int = Depends(get_current_user)) -> Post:
    """Create new post"""
    post = await crud.insert_post(user_id, body)

    if not post:
        raise HTTPException(status_code=400, detail=f"Something went wrong")

    return Post(**post)


@router.get("/{post_id}", response_model=Post)
async def get_single_post(post_id: int) -> Post:
    """Return single post by ID"""
    await crud.increment_views(post_id)

    post = await crud.find_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} does not exist")

    return Post(**post)


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, user_id: int = Depends(get_current_user)) -> Response:
    """Delete post by id"""
    post = await crud.find_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} does not exist")

    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail=f"Forbidden")

    await crud.delete_post(post_id)
    return Response(status_code=204)


@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, body: UpdatePostBody, user_id: int = Depends(get_current_user)) -> Post:
    """Overwrite post information with new data"""
    post = await crud.find_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} does not exist")

    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail=f"Forbidden")

    new_post = await crud.update_post(post_id=post_id, old_post_data=post, new_post_data=body)
    return Post(**new_post)

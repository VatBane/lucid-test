from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.db import get_session
from exceptions.exceptions import ResourceNotFoundError
from routers.posts.controller import PostWebController
from routers.posts.models import Post
from routers.users.models import UserFullData
from security.auth import get_current_active_user
from services.cache import cache_response

posts_router = APIRouter(tags=['Posts'])


@posts_router.get('/')
@cache_response(namespace='get_posts')
async def get_users_posts(session: Annotated[Session, Depends(get_session)],
         user_data: Annotated[UserFullData, Depends(get_current_active_user)],
         ):
    controller = PostWebController(session=session, user_data=user_data)
    posts = controller.get_users_posts()

    return posts


@posts_router.post('/')
def create_post(session: Annotated[Session, Depends(get_session)],
                user_data: Annotated[UserFullData, Depends(get_current_active_user)],
                post: Annotated[Post, Body()],
                ):
    controller = PostWebController(session=session, user_data=user_data)

    post = controller.create_post(post_data=post)

    session.commit()
    return post.id_


@posts_router.delete('/{postID}')
def delete_post(session: Annotated[Session, Depends(get_session)],
                user_data: Annotated[UserFullData, Depends(get_current_active_user)],
                post_id: Annotated[int, Path(alias='postID')],
                ):
    controller = PostWebController(session=session, user_data=user_data)

    try:
        controller.delete_users_post(post_id=post_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(exc))

    session.commit()

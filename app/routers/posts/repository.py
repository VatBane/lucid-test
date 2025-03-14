from sqlalchemy import select
from sqlalchemy.orm import Session

from db.schemas import PostOrm
from exceptions.exceptions import ResourceNotFoundError
from routers.posts.models import Post, PostWithUser, PostFullData


class PostRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_post(self, post_data: PostWithUser) -> PostFullData:
        post = PostOrm(user_id=post_data.user_id,
                       text=post_data.text)

        self.session.add(post)
        self.session.flush()
        self.session.refresh(post)

        return PostFullData.model_validate(post)

    def get_posts_of_user(self, user_id: int) -> list[PostFullData]:
        query = select(PostOrm).where(PostOrm.user_id == user_id)

        posts = self.session.execute(query)
        posts = [PostFullData.model_validate(p) for p in posts.scalars().all()]

        return posts

    def delete_post(self, post_id: int, user_id: int):
        query = select(PostOrm).where(PostOrm.id_ == post_id, PostOrm.user_id == user_id)
        db_post = self.session.execute(query)
        db_post = db_post.scalar()

        if not db_post:
            # there is message says that post was not found
            # even if it belongs to another user to hide this fact for security reasons
            raise ResourceNotFoundError('Post with this ID not found!')

        self.session.delete(db_post)
        self.session.flush()

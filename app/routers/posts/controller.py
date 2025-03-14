from sqlalchemy.orm import Session

from exceptions.exceptions import ResourceNotFoundError
from routers.posts.models import Post, PostWithUser
from routers.posts.repository import PostRepository
from routers.users.models import UserData, UserFullData


class PostWebController:
    def __init__(
            self,
            session: Session,
            user_data: UserFullData,
    ):
        self.posts_repo = PostRepository(session=session)
        self.user_data = user_data

    def create_post(self, post_data: Post):
        post_data = PostWithUser(text=post_data.text,
                                 user_id=self.user_data.id_)

        db_post = self.posts_repo.create_post(post_data=post_data)

        return db_post

    def get_users_posts(self):
        posts = self.posts_repo.get_posts_of_user(user_id=self.user_data.id_)

        return posts

    def delete_users_post(self, post_id: int):
        self.posts_repo.delete_post(post_id=post_id, user_id=self.user_data.id_)

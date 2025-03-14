from sqlalchemy.orm import Session

from exceptions.exceptions import ResourceNotFoundError
from routers.posts.models import Post, PostWithUser, PostFullData
from routers.posts.repository import PostRepository
from routers.users.models import UserData, UserFullData


class PostWebController:
    """
    Class with business logic that coordinates interaction with Post instances
    """
    def __init__(
            self,
            session: Session,
            user_data: UserFullData,
    ):
        self.posts_repo = PostRepository(session=session)
        self.user_data = user_data

    def create_post(self, post_data: Post) -> PostFullData:
        """
        Creates new post
        :param post_data: data of Post instance
        :return: new Post instance with additional data
        """
        post_data = PostWithUser(text=post_data.text,
                                 user_id=self.user_data.id_)

        db_post = self.posts_repo.create_post(post_data=post_data)

        return db_post

    def get_users_posts(self) -> list[PostFullData]:
        """
        Returns list of all posts created by specific user
        :return: list of users' posts
        """
        posts = self.posts_repo.get_posts_of_user(user_id=self.user_data.id_)

        return posts

    def delete_users_post(self, post_id: int) -> None:
        """
        Deletes post if it belongs to user that tries to delete it
        :param post_id: id of post to delete
        :return: None
        """
        self.posts_repo.delete_post(post_id=post_id, user_id=self.user_data.id_)

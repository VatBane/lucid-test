from typing import Annotated

from pydantic import BaseModel, AfterValidator, Field, ConfigDict

from routers.posts.validators import validate_post_size


class Post(BaseModel):
    text: Annotated[str, AfterValidator(validate_post_size)]


class PostWithUser(Post):
    user_id: int = Field(gt=0)


class PostFullData(PostWithUser):
    id_: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)

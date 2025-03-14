from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.schemas import UserOrm
from routers.users.models import UserData, UserFullData
from security.encryptors import encrypt_password


class UserRepository:
    """
    Data Access Object that interacts with database instances of User
    """

    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> UserFullData | None:
        query = select(UserOrm).where(UserOrm.email == email)
        user = self.session.execute(query)
        user = user.scalar()

        if user:
            return UserFullData.model_validate(user)
        else:
            return user

    def create_user(self, user_data: UserData) -> None:
        user = UserOrm(email=user_data.email,
                       password=encrypt_password(user_data.password))

        self.session.add(user)
        self.session.flush()

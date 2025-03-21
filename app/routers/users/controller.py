from datetime import timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.security import ACCESS_TOKEN_EXPIRE_MINUTES
from db.schemas import UserOrm
from exceptions.exceptions import DuplicateError, AuthenticationError
from routers.users.models import UserData, Token
from routers.users.repository import UserRepository
from security.encryptors import encrypt_password, verify_password
from security.token import create_access_token


class UserWebController:
    """
    Controller level class that implements business logic for User instances
    """

    def __init__(self, session: Session):
        self.repo = UserRepository(session=session)
        self.session = session

    def create_user(
            self,
            user_data: UserData,
    ) -> Token:
        """
        Creates user
        :param user_data: user credentials
        :return: user data with id
        """
        try:
            self.repo.create_user(user_data=user_data)
            self.session.commit()
        except IntegrityError:
            raise DuplicateError('User with provided Email already exists!')

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_data.email}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    def login(self, user_data: UserData) -> Token:
        """
        Authenticates use
        :param user_data:
        :return:
        """
        user = self.repo.get_user_by_email(user_data.email)

        if user is None:
            raise AuthenticationError("Incorrect username or password")

        if not verify_password(user_data.password, user.password):
            raise AuthenticationError("Incorrect username or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

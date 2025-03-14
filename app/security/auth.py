from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette import status

from config.security import SECRET_KEY, ALGORITHM
from db.db import get_session
from routers.users.repository import UserRepository
from security.scheme import oauth2_scheme


def get_current_active_user(session: Annotated[Session, Depends(get_session)],
                            token: Annotated[str, Depends(oauth2_scheme)]):
    user_repo = UserRepository(session=session)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = user_repo.get_user_by_email(email=username)
    if user is None:
        raise credentials_exception

    return user

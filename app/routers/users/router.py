from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.db import get_session
from exceptions.exceptions import DuplicateError, AuthenticationError
from routers.users.controller import UserWebController
from routers.users.models import UserData

users_router = APIRouter(tags=['Authentication'])


@users_router.post('/signup')
def signup(session: Annotated[Session, Depends(get_session)],
           user_data: Annotated[UserData, Body()]):
    controller = UserWebController(session=session)

    try:
        token = controller.create_user(user_data=user_data)
    except DuplicateError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    return token


@users_router.post('/login')
def login(session: Annotated[Session, Depends(get_session)],
          form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          ):
    controller = UserWebController(session=session)
    user = UserData(email=form_data.username,
                    password=form_data.password)

    try:
        token = controller.login(user)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token

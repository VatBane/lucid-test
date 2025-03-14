from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.config import DB_URL

engine = create_engine(DB_URL)


def get_session():
    with Session(engine) as session:
        yield session

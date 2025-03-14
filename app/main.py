from fastapi import FastAPI

from config.general import TITLE, PREFIX
from routers.posts.router import posts_router
from routers.users.router import users_router

app = FastAPI(root_path=PREFIX, title=TITLE)

app.include_router(users_router, prefix='/users')
app.include_router(posts_router, prefix='/posts')

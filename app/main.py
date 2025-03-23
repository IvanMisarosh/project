from fastapi import FastAPI
from app.api.endpoints import users, posts

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])

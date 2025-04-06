from fastapi import FastAPI
from app.api.endpoints import users, posts, comments, files

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, tags=["Comments"])
app.include_router(files.router, prefix="/files", tags=["files"])

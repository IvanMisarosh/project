from fastapi import FastAPI
from app.api.endpoints import users, posts, comments, files, archive

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, tags=["Comments"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(archive.router, prefix="/archive", tags=["archive"])


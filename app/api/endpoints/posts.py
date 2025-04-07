from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.post import PostCreate, PostResponse, PostFileCreate, DetailedPostResponse, PostUpdate
from app.crud.post import create_post, get_posts, delete_post, get_post_by_id, update_post
from app.upload_service import save_file
from typing import Optional
from app.db.mongodb import db as mongo_db

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PostResponse)
async def create_new_post(db: Session = Depends(get_db),
                           author_id: int = Form(...),
                           title: str = Form(...),
                           content: str = Form(...),
                           files: Optional[list[UploadFile]] = File(None)):
    
    post = PostCreate(author_id=author_id, title=title, content=content, files=[])
    if files:
        for file in files:
            file_url = await save_file(file)
            post.files.append(PostFileCreate(filename=file.filename, file_url=file_url))

    return create_post(db, post)

@router.get("/", response_model=list[PostResponse])
def list_posts(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_posts(db, skip, limit)

@router.get("/{post_id}", response_model=DetailedPostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        return None
    comments = await mongo_db.comments.find(
        {"post_id": post_id},
        {"_id": 0}).to_list(length=100)
    post.comments = comments
    return post

@router.put("/{post_id}", response_model=PostResponse)
async def modify_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db)):
    post = update_post(db, post_id, post_data)
    if not post:
        return None
    return post

@router.delete("/{post_id}", response_model=bool)
async def remove_post(post_id: int, db: Session = Depends(get_db)):
    return await delete_post(db, post_id)

from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.post import PostCreate, PostResponse, PostFileCreate
from app.crud.post import create_post, get_posts, delete_post
from app.upload_service import save_file
from typing import Optional

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

@router.delete("/{post_id}", response_model=bool)
async def remove_post(post_id: int, db: Session = Depends(get_db)):
    return await delete_post(db, post_id)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.post import PostCreate, PostResponse
from app.crud.post import create_post, get_posts

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PostResponse)
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)

@router.get("/", response_model=list[PostResponse])
def list_posts(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_posts(db, skip, limit)

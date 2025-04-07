from sqlalchemy.orm import Session
from app.models.post import Post, PostFile
from app.schemas.post import PostCreate, PostUpdate
from app.upload_service import delete_file

def create_post(db: Session, post: PostCreate):
    # Створення нового поста
    db_post = Post(author_id=post.author_id, title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # Додавання файлів до поста, якщо вони є
    if post.files:
        for file in post.files:
            db_file = PostFile(
                filename=file.filename,
                file_url=file.file_url,
                post_id=db_post.id
            )
            db.add(db_file)
        db.commit()

    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post_id: int, post_data: PostUpdate):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        if post_data.title:
            post.title = post_data.title
        if post_data.content:
            post.content = post_data.content
        if post_data.is_archived is not None:
            post.is_archived = post_data.is_archived
        if post_data.archive_url:
            post.archive_url = post_data.archive_url
        db.commit()
        db.refresh(post)
        return post
    return None

async def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        for file in post.files:
            await delete_file(file.file_url)
        db.commit()
        return True
    return False

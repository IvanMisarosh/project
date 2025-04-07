from pydantic import BaseModel, Field
from typing import List, Optional

class PostFileCreate(BaseModel):
    filename: str
    file_url: str # URL файлу

    class Config:
        from_attributes = True

class PostFileResponse(BaseModel):
    id: int
    filename: str
    file_url: str # URL файлу

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    author_id: int  
    title: str
    content: str
    files: Optional[List[PostFileCreate]] = []  # Список файлів, який буде передаватися

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_archived: Optional[bool] = False
    archive_url: Optional[str] = None  

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    files: Optional[List[PostFileResponse]]  # Для відповіді додаємо файли
    is_archived: Optional[bool] = False
    archive_url: Optional[str] = None  

    class Config:
        from_attributes = True

class CommentResponse(BaseModel):
    post_id: int
    author_id: int = Field(..., alias="user_id")
    content: str = Field(..., alias="text")

    class Config:
        from_attributes = True
        populate_by_name = True  # enables accessing with `content`, not `text`

class DetailedPostResponse(PostResponse):
    comments: Optional[List[CommentResponse]] = []  
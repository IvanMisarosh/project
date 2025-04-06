from pydantic import BaseModel
from typing import List, Optional

class PostFileCreate(BaseModel):
    filename: str
    file_url: str # URL файлу

    class Config:
        orm_mode = True

class PostFileResponse(BaseModel):
    id: int
    filename: str
    file_url: str # URL файлу

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    author_id: int  
    title: str
    content: str
    files: Optional[List[PostFileCreate]] = []  # Список файлів, який буде передаватися

class PostResponse(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    files: Optional[List[PostFileResponse]]  # Для відповіді додаємо файли

    class Config:
        orm_mode = True

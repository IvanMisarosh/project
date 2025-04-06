from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Comment(BaseModel):
    post_id: int
    user_id: int
    text: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

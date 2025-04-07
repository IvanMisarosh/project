from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.post_file import PostFile


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    content = Column(String)
    is_archived = Column(Boolean, default=0)
    archive_url = Column(String, nullable=True, default=None)

    author = relationship("User")
    files = relationship("PostFile", back_populates="post", cascade="all, delete")

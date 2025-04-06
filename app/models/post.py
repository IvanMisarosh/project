from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.post_file import PostFile


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User")
    files = relationship("PostFile", back_populates="post", cascade="all, delete")

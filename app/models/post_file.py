from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class PostFile(Base):
    __tablename__ = "post_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_url = Column(String)  # локальний шлях або Azure URL
    post_id = Column(Integer, ForeignKey("posts.id"))

    post = relationship("Post", back_populates="files")
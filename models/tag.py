from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

post_tags = Table("post_tags", Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    posts = relationship("Post", secondary=post_tags, back_populates="tags")

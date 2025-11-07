from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Like(Base):
    """点赞模型"""
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
    
    # 唯一约束：一个用户只能给一篇文章点一次赞
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uix_user_post"),
    )

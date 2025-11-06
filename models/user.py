import enum
from sqlalchemy import Boolean, DateTime, Integer, String, func, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column

from database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.READER)
    created_at = Column(DateTime, default=func.now())
    avatar_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="user")



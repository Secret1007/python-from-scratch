# schemas/user.py
from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from schemas.post import PostSimple

# 简化的用户信息
class UserSimple(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str] = None
    role: str = "reader"
    model_config = {"from_attributes": True}

class UserBase(BaseModel):
    username: str
    email: str
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "reader"

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime
    bio: Optional[str] = None
    posts: List["PostSimple"] = []
    model_config = {"from_attributes": True}


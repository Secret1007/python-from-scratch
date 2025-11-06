# schemas/post.py
from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from schemas.user import UserSimple
    from schemas.tag import TagSimple

class PostBase(BaseModel):
    title: str
    content: str
    author_id: int

class PostCreate(BaseModel):
    """创建文章时，不需要传 author_id（从 token 中获取）"""
    title: str
    content: str

class PostSimple(BaseModel):
    """简化的文章信息，用于在用户主页显示文章列表"""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author: Optional["UserSimple"] = None
    tags: List["TagSimple"] = []
    model_config = {"from_attributes": True}


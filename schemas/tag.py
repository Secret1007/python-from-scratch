# schemas/tag.py
from pydantic import BaseModel
from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from schemas.post import PostSimple

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagSimple(BaseModel):
    """简化的标签信息，用于在文章中显示"""
    id: int
    name: str
    model_config = {"from_attributes": True}

class TagResponse(TagBase):
    id: int
    created_at: datetime
    posts: List["PostSimple"] = []
    model_config = {"from_attributes": True}


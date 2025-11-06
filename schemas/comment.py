# schemas/comment.py
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from schemas.user import UserSimple

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: Optional["UserSimple"] = None
    model_config = {"from_attributes": True}
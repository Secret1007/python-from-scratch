from datetime import datetime
from pydantic import BaseModel

from schemas.user import UserSimple
from schemas.post import PostSimple

class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime.datetime
    user: UserSimple
    model_config = {"from_attributes": True}

class LikeCount(BaseModel):
    count: int
    is_liked: bool
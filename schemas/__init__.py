# schemas/__init__.py
from .user import UserSimple, UserBase, UserCreate, UserResponse
from .post import PostBase, PostCreate, PostSimple, PostResponse
from .tag import TagBase, TagCreate, TagSimple, TagResponse
from .comment import CommentBase, CommentCreate, CommentUpdate, CommentResponse
from .like import LikeResponse, LikeStats

# 解析前向引用
UserResponse.model_rebuild()
PostResponse.model_rebuild()
TagResponse.model_rebuild()
CommentResponse.model_rebuild()
LikeResponse.model_rebuild()

__all__ = [
    "UserSimple", "UserBase", "UserCreate", "UserResponse",
    "PostBase", "PostCreate", "PostSimple", "PostResponse",
    "TagBase", "TagCreate", "TagSimple", "TagResponse",
    "CommentBase", "CommentCreate", "CommentUpdate", "CommentResponse",
    "LikeResponse", "LikeStats",
]


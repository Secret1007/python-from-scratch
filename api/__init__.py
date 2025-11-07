# api/__init__.py
from .users import router as users_router
from .posts import router as posts_router
from .auth import router as auth_router
from .tags import router as tags_router
from .comment import router as comment_router
from .likes import router as likes_router

__all__ = ["users_router", "posts_router", "auth_router", "tags_router", "comment_router", "likes_router"]


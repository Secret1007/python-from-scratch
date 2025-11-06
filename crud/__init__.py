# crud/__init__.py
from .user import (
    create_user,
    get_user,
    get_user_by_username,
    get_user_by_email,
    get_users,
    authenticate_user,
)
from .post import (
    create_post,
    get_posts,
    get_post,
    update_post,
    delete_post,
    get_user_posts,
)
from .tag import (
    create_tag,
    get_tag,
    get_tag_by_name,
    get_tags,
    add_tag_to_post,
    remove_tag_from_post,
    delete_tag,
)
from .comment import (
    create_comment,
    get_comments,
    update_comment,
    delete_comment,
    get_comment
)

__all__ = [
    "create_user", "get_user", "get_user_by_username", "get_user_by_email",
    "get_users", "authenticate_user",
    "create_post", "get_posts", "get_post", "update_post", "delete_post",
    "get_user_posts",
    "create_tag", "get_tag", "get_tag_by_name", "get_tags",
    "add_tag_to_post", "remove_tag_from_post", "delete_tag",
    "create_comment", "get_comments", "update_comment", "delete_comment", "get_comment",
]


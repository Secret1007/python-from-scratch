# core/permissions.py
"""
权限控制模块 - 博客系统
"""
from fastapi import HTTPException, status

def check_owner_or_admin(
    resource_owner_id: int,
    current_user,
    resource_name: str = "resource"
) -> None:
    """
    检查用户是否是资源所有者或管理员
    
    Args:
        resource_owner_id: 资源所有者的ID
        current_user: 当前登录用户
        resource_name: 资源名称（用于错误消息）
    
    Raises:
        HTTPException: 403 如果没有权限
        
    Example:
        post = crud.get_post(db, post_id)
        check_owner_or_admin(post.author_id, current_user, "post")
    """
    is_owner = current_user.id == resource_owner_id
    is_admin = current_user.role == "admin"
    
    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to modify this {resource_name}"
        )

def require_role(current_user, required_role: str) -> None:
    """
    检查用户是否有指定角色
    
    Args:
        current_user: 当前用户
        required_role: 需要的角色 (admin, author, reader)
        
    Raises:
        HTTPException: 403 如果角色不足
        
    Example:
        require_role(current_user, "admin")
    """
    # 角色层级：admin > author > reader
    role_hierarchy = {
        "reader": 1,
        "author": 2,
        "admin": 3
    }
    
    user_level = role_hierarchy.get(current_user.role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    if user_level < required_level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied. Required role: {required_role} or higher"
        )

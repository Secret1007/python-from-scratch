from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from api.users import get_current_user
from services import LikeService
import schemas
import models

router = APIRouter(tags=["likes"])


# ============= 依赖注入 =============

def get_like_service(db: Session = Depends(get_db)) -> LikeService:
    """创建 LikeService 实例"""
    return LikeService(db)


# ============= API 路由 =============

@router.post("/posts/{post_id}/like", response_model=schemas.LikeStats)
def like_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    like_service: LikeService = Depends(get_like_service)
):
    """
    点赞文章（需要登录）
    
    返回最新的点赞统计信息
    """
    return like_service.like_post(post_id, current_user.id)


@router.delete("/posts/{post_id}/like", response_model=schemas.LikeStats)
def unlike_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    like_service: LikeService = Depends(get_like_service)
):
    """
    取消点赞（需要登录）
    
    返回最新的点赞统计信息
    """
    return like_service.unlike_post(post_id, current_user.id)


@router.get("/posts/{post_id}/likes", response_model=list[schemas.LikeResponse])
def get_post_likes(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    like_service: LikeService = Depends(get_like_service)
):
    """
    获取文章的点赞列表（公开）
    
    返回点赞用户列表，按点赞时间倒序
    """
    return like_service.get_post_likes(post_id, skip, limit)


@router.get("/posts/{post_id}/likes/stats", response_model=schemas.LikeStats)
def get_like_stats(
    post_id: int,
    like_service: LikeService = Depends(get_like_service)
):
    """
    获取文章的点赞统计（公开，无需登录）
    
    返回：
    - count: 总点赞数
    - is_liked: false（因为未登录）
    
    注意：如果需要获取当前用户是否点赞，请先登录后调用此接口
    """
    return like_service.get_like_stats(post_id, user_id=None)


@router.get("/users/me/likes", response_model=list[schemas.LikeResponse])
def get_my_likes(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    like_service: LikeService = Depends(get_like_service)
):
    """
    获取我点赞的所有文章（需要登录）
    """
    return like_service.get_user_likes(current_user.id, skip, limit)


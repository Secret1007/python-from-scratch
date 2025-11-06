# api/posts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from api.users import get_current_user
from services import PostService
import schemas
import models

router = APIRouter(prefix="/posts", tags=["posts"])


# ============= 依赖注入 =============

def get_post_service(db: Session = Depends(get_db)) -> PostService:
    """创建 PostService 实例"""
    return PostService(db)


# ============= API 路由 =============

@router.post("", response_model=schemas.PostResponse)
async def create_post(
    post: schemas.PostCreate,
    current_user: models.User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service)
):
    """创建文章（需要登录，只有 author 和 admin 可以创建）"""
    return post_service.create_post(post, current_user.id)


@router.get("", response_model=list[schemas.PostResponse])
async def read_posts(
    skip: int = 0, 
    limit: int = 10, 
    post_service: PostService = Depends(get_post_service)
):
    """获取所有文章（公开）"""
    return post_service.get_posts(skip, limit)


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def read_post(
    post_id: int, 
    post_service: PostService = Depends(get_post_service)
):
    """获取单篇文章（公开）"""
    return post_service.get_post(post_id)


@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(
    post_id: int,
    post_data: schemas.PostCreate,
    current_user: models.User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service)
):
    """更新文章（只有作者或管理员可以）"""
    return post_service.update_post(post_id, post_data, current_user)


@router.delete("/{post_id}", response_model=schemas.PostResponse)
async def delete_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service)
):
    """删除文章（只有作者或管理员可以）"""
    return post_service.delete_post(post_id, current_user)

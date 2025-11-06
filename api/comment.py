from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.users import get_current_user
from database import get_db
import models
import schemas
from services import CommentService

router = APIRouter(tags=["comments"])


# ============= 依赖注入 =============

def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    """创建 CommentService 实例"""
    return CommentService(db)


# ============= API 路由 =============

@router.post("/posts/{post_id}/comments", response_model=schemas.CommentResponse)
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    current_user: models.User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    """创建评论（需要登录）"""
    return comment_service.create_comment(post_id, comment, current_user.id)


@router.get("/posts/{post_id}/comments", response_model=list[schemas.CommentResponse])
def get_comments(
    post_id: int,
    comment_service: CommentService = Depends(get_comment_service)
):
    """获取文章的所有评论（公开）"""
    return comment_service.get_post_comments(post_id)


@router.put("/comments/{comment_id}", response_model=schemas.CommentResponse)
def update_comment(
    comment_id: int,
    comment: schemas.CommentUpdate,
    current_user: models.User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    """更新评论（只有评论作者或管理员可以）"""
    return comment_service.update_comment(comment_id, comment, current_user)


@router.delete("/comments/{comment_id}", response_model=dict)
def delete_comment(
    comment_id: int,
    current_user: models.User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    """删除评论（只有评论作者或管理员可以）"""
    return comment_service.delete_comment(comment_id, current_user)

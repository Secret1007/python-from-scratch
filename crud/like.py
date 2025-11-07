from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from typing import List, Optional


def create_like(db: Session, user_id: int, post_id: int) -> models.Like:
    """创建点赞记录"""
    db_like = models.Like(
        user_id=user_id,
        post_id=post_id
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def get_like(db: Session, user_id: int, post_id: int) -> Optional[models.Like]:
    """查询点赞记录（检查是否已点赞）"""
    return db.query(models.Like).filter(
        models.Like.user_id == user_id,
        models.Like.post_id == post_id
    ).first()


def delete_like(db: Session, user_id: int, post_id: int) -> bool:
    """删除点赞记录"""
    db_like = get_like(db, user_id, post_id)
    if db_like:
        db.delete(db_like)
        db.commit()
        return True
    return False


def get_post_likes(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[models.Like]:
    """获取文章的所有点赞记录"""
    return db.query(models.Like).filter(
        models.Like.post_id == post_id
    ).order_by(
        models.Like.created_at.desc()  # 最新的在前
    ).offset(skip).limit(limit).all()


def get_like_count(db: Session, post_id: int) -> int:
    """统计文章的点赞数"""
    return db.query(models.Like).filter(
        models.Like.post_id == post_id
    ).count()


def increment_post_like_count(db: Session, post_id: int):
    """增加文章点赞数（原子操作）"""
    db.query(models.Post).filter(
        models.Post.id == post_id
    ).update({
        models.Post.like_count: models.Post.like_count + 1
    })
    db.commit()


def decrement_post_like_count(db: Session, post_id: int):
    """减少文章点赞数（原子操作）"""
    db.query(models.Post).filter(
        models.Post.id == post_id
    ).update({
        models.Post.like_count: models.Post.like_count - 1
    })
    db.commit()


def get_user_likes(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Like]:
    """获取用户点赞的所有文章"""
    return db.query(models.Like).filter(
        models.Like.user_id == user_id
    ).order_by(
        models.Like.created_at.desc()
    ).offset(skip).limit(limit).all()


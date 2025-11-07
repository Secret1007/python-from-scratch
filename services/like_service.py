from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import models
from services.post_service import PostService


class LikeService:
    """点赞服务层 - 处理点赞相关的业务逻辑"""
    
    def __init__(self, db: Session):
        self.db = db
        self.post_service = PostService(db)
    
    def like_post(self, post_id: int, user_id: int) -> dict:
        """
        点赞文章
        
        业务逻辑：
        1. 检查文章是否存在
        2. 检查是否已经点过赞（防止重复）
        3. 创建点赞记录
        4. 更新文章的 like_count + 1（原子操作）
        5. 返回最新的点赞统计
        """
        # 1. 检查文章是否存在
        self.post_service.get_post_with_validation(post_id)
        
        # 2. 检查是否已经点过赞
        existing_like = crud.get_like(self.db, user_id, post_id)
        if existing_like:
            raise HTTPException(
                status_code=400,
                detail="You have already liked this post"
            )
        
        # 3. 创建点赞记录
        crud.create_like(self.db, user_id, post_id)
        
        # 4. 更新文章点赞数（原子操作，避免并发问题）
        crud.increment_post_like_count(self.db, post_id)
        
        # 5. 返回最新的点赞统计
        return self.get_like_stats(post_id, user_id)
    
    def unlike_post(self, post_id: int, user_id: int) -> dict:
        """
        取消点赞
        
        业务逻辑：
        1. 检查点赞记录是否存在
        2. 删除点赞记录
        3. 更新文章的 like_count - 1
        4. 返回最新的点赞统计
        """
        # 1. 检查点赞记录是否存在
        existing_like = crud.get_like(self.db, user_id, post_id)
        if not existing_like:
            raise HTTPException(
                status_code=400,
                detail="You have not liked this post"
            )
        
        # 2. 删除点赞记录
        crud.delete_like(self.db, user_id, post_id)
        
        # 3. 更新文章点赞数
        crud.decrement_post_like_count(self.db, post_id)
        
        # 4. 返回最新的点赞统计
        return self.get_like_stats(post_id, user_id)
    
    def get_post_likes(self, post_id: int, skip: int = 0, limit: int = 100) -> List[models.Like]:
        """
        获取文章的点赞列表
        
        业务逻辑：
        1. 检查文章是否存在
        2. 获取点赞记录列表
        """
        # 1. 检查文章是否存在
        self.post_service.get_post_with_validation(post_id)
        
        # 2. 获取点赞列表
        return crud.get_post_likes(self.db, post_id, skip, limit)
    
    def get_like_stats(self, post_id: int, user_id: int = None) -> dict:
        """
        获取点赞统计信息
        
        返回：
        - count: 总点赞数
        - is_liked: 当前用户是否点赞（如果提供了 user_id）
        
        业务逻辑：
        1. 统计总点赞数
        2. 检查当前用户是否点赞
        """
        # 1. 统计总点赞数
        count = crud.get_like_count(self.db, post_id)
        
        # 2. 检查当前用户是否点赞
        is_liked = False
        if user_id:
            is_liked = crud.get_like(self.db, user_id, post_id) is not None
        
        return {
            "count": count,
            "is_liked": is_liked
        }
    
    def get_user_likes(self, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Like]:
        """
        获取用户点赞的所有文章
        
        业务逻辑：
        1. 检查用户是否存在（可选）
        2. 获取用户的点赞列表
        """
        return crud.get_user_likes(self.db, user_id, skip, limit)


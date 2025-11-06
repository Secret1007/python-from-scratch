from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
from services.post_service import PostService
from utils import contains_sensitive_words


class CommentService:
    """评论服务层 - 处理评论相关的业务逻辑"""
    
    def __init__(self, db: Session):
        self.db = db
        self.post_service = PostService(db)
    
    def create_comment(
        self, 
        post_id: int, 
        comment_data: schemas.CommentCreate, 
        user_id: int
    ) -> models.Comment:
        """
        创建评论
        
        业务逻辑：
        1. 检查文章是否存在
        2. 敏感词检测
        3. 创建评论
        """
        # 1. 检查文章是否存在（如果不存在会自动抛出 404）
        self.post_service.get_post_with_validation(post_id)
        
        # 2. 敏感词检测
        if contains_sensitive_words(comment_data.content):
            raise HTTPException(
                status_code=400, 
                detail="Comment contains sensitive words"
            )
        
        # 3. 创建评论
        new_comment = crud.create_comment(self.db, comment_data, post_id, user_id)
        return new_comment
    
    def update_comment(
        self, 
        comment_id: int, 
        comment_data: schemas.CommentUpdate, 
        current_user: models.User
    ) -> models.Comment:
        """
        更新评论
        
        业务逻辑：
        1. 检查评论是否存在
        2. 权限检查（只有评论作者或管理员可以修改）
        3. 敏感词检测
        4. 更新评论
        """
        # 1. 检查评论是否存在（如果不存在会自动抛出 404）
        comment = self.get_comment_with_validation(comment_id)
        
        # 2. 权限检查
        if comment.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=403, 
                detail="You don't have permission to update this comment"
            )
        
        # 3. 敏感词检测
        if contains_sensitive_words(comment_data.content):
            raise HTTPException(
                status_code=400, 
                detail="Comment contains sensitive words"
            )
        
        # 4. 更新评论
        updated_comment = crud.update_comment(self.db, comment_id, comment_data)
        return updated_comment
    
    def delete_comment(
        self, 
        comment_id: int, 
        current_user: models.User
    ) -> dict:
        """
        删除评论
        
        业务逻辑：
        1. 检查评论是否存在
        2. 权限检查
        3. 删除评论
        """
        # 1. 检查评论是否存在（如果不存在会自动抛出 404）
        comment = self.get_comment_with_validation(comment_id)
        
        # 2. 权限检查
        if comment.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=403, 
                detail="You don't have permission to delete this comment"
            )
        
        # 3. 删除评论
        return crud.delete_comment(self.db, comment_id)
    
    def get_post_comments(self, post_id: int) -> List[models.Comment]:
        """
        获取文章的所有评论
        
        业务逻辑：
        1. 检查文章是否存在
        2. 获取评论列表
        """
        # 1. 检查文章是否存在
        self.post_service.get_post_with_validation(post_id)
        
        # 2. 获取评论
        return crud.get_comments(self.db, post_id)
    
    # ============= 辅助方法 =============
    
    def get_comment_with_validation(self, comment_id: int) -> models.Comment:
        """
        获取评论并验证是否存在
        
        这是一个可复用的辅助方法，在多个地方都会用到：
        - update_comment 需要先验证评论存在
        - delete_comment 需要先验证评论存在
        """
        comment = crud.get_comment(self.db, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

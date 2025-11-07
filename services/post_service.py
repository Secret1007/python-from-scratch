from sqlalchemy.orm import Session
from typing import List, Optional
import crud
import schemas
import models
from fastapi import HTTPException
from utils import contains_sensitive_words

class PostService:
    """文章服务层 - 处理文章相关的业务逻辑"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_post(self, post_data: schemas.PostCreate, author_id: int) -> models.Post:
        """
        创建文章
        
        业务逻辑：
        1. 检查用户是否存在
        2. 检查用户权限（只有 author 和 admin 可以发文章）
        3. 敏感词检测
        4. 创建文章
        """
        # 1. 检查用户是否存在
        user = crud.get_user(self.db, author_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # 2. 权限检查
        if user.role not in ["admin", "author"]:
            raise HTTPException(
                status_code=403, 
                detail="Only authors and admins can create posts"
            )
        
        # 3. 敏感词检测
        if contains_sensitive_words(post_data.content):
            raise HTTPException(
                status_code=400, 
                detail="Post contains sensitive words"
            )
        
        # 4. 创建文章
        new_post = crud.create_post(self.db, post_data, author_id)
        return new_post
    
    def get_post(self, post_id: int) -> models.Post:
        """
        获取单篇文章（带验证）
        """
        return self.get_post_with_validation(post_id)
    
    def get_posts(
        self, 
        skip: int = 0, 
        limit: int = 10,
        author_id: Optional[int] = None
    ) -> List[models.Post]:
        """
        获取文章列表
        
        参数：
        - skip: 跳过多少条
        - limit: 返回多少条
        - author_id: 可选，按作者筛选
        """
        posts = crud.get_posts(self.db, skip, limit)
        
        # 如果指定了作者，进行筛选
        if author_id:
            posts = [p for p in posts if p.author_id == author_id]
        
        return posts
    
    def update_post(
        self, 
        post_id: int, 
        post_data: schemas.PostCreate, 
        current_user: models.User
    ) -> models.Post:
        """
        更新文章
        
        业务逻辑：
        1. 检查文章是否存在
        2. 检查权限（只有作者本人或管理员可以修改）
        3. 敏感词检测
        4. 更新文章
        """
        # 1. 检查文章是否存在
        post = self.get_post_with_validation(post_id)
        
        # 2. 权限检查
        if post.author_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this post"
            )
        
        # 3. 敏感词检测
        if contains_sensitive_words(post_data.content):
            raise HTTPException(
                status_code=400,
                detail="Post contains sensitive words"
            )
        
        # 4. 更新文章
        updated_post = crud.update_post(self.db, post_id, post_data)
        return updated_post
    
    def delete_post(
        self, 
        post_id: int, 
        current_user: models.User
    ) -> models.Post:
        """
        删除文章
        
        业务逻辑：
        1. 检查文章是否存在
        2. 检查权限（只有作者本人或管理员可以删除）
        3. 删除文章
        """
        # 1. 检查文章是否存在
        post = self.get_post_with_validation(post_id)
        
        # 2. 权限检查
        if post.author_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this post"
            )
        
        # 3. 删除文章
        deleted_post = crud.delete_post(self.db, post_id)
        return deleted_post
    
    def get_user_posts(self, user_id: int) -> List[models.Post]:
        """
        获取某个用户的所有文章
        """
        # 检查用户是否存在
        user = crud.get_user(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return crud.get_user_posts(self.db, user_id)

    def update_post_like_count(self, post_id: int, count: int):
        post = self.get_post_with_validation(post_id)
        post.like_count += count
        self.db.commit()
        return post
    
    # ============= 辅助方法 =============
    
    def get_post_with_validation(self, post_id: int) -> models.Post:
        """
        获取文章并验证是否存在
        
        这是一个可复用的辅助方法，在多个地方都会用到：
        - update_post 需要先验证文章存在
        - delete_post 需要先验证文章存在
        - 给文章添加评论时需要验证文章存在
        """
        post = crud.get_post(self.db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
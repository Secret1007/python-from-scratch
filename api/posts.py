# api/posts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from api.users import get_current_user
from core.permissions import check_owner_or_admin
import schemas
import crud
import models

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=schemas.PostResponse)
async def create_post(
    post: schemas.PostCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建文章（需要登录）"""
    return crud.create_post(db=db, post=post, author_id=current_user.id)

@router.get("", response_model=list[schemas.PostResponse])
async def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """获取所有文章（公开）"""
    posts = crud.get_posts(db=db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=schemas.PostResponse)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    """获取单篇文章（公开）"""
    post = crud.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(
    post_id: int,
    post_data: schemas.PostCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新文章（只有作者或管理员可以）"""
    # 1. 获取文章
    post = crud.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 2. 权限检查
    check_owner_or_admin(post.author_id, current_user, "post")
    
    # 3. 更新文章
    updated_post = crud.update_post(db=db, post_id=post_id, post=post_data)
    return updated_post

@router.delete("/{post_id}", response_model=schemas.PostResponse)
async def delete_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文章（只有作者或管理员可以）"""
    # 1. 获取文章
    post = crud.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 2. 权限检查
    check_owner_or_admin(post.author_id, current_user, "post")
    
    # 3. 删除文章
    deleted_post = crud.delete_post(db=db, post_id=post_id)
    return deleted_post


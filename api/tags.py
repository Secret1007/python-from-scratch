# api/tags.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import crud

router = APIRouter(prefix="/tags", tags=["tags"])

@router.post("", response_model=schemas.TagResponse)
async def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    """创建标签"""
    return crud.create_tag(db=db, tag=tag)

@router.get("", response_model=list[schemas.TagResponse])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取所有标签"""
    tags = crud.get_tags(db=db, skip=skip, limit=limit)
    return tags

@router.get("/{tag_id}", response_model=schemas.TagResponse)
async def read_tag(tag_id: int, db: Session = Depends(get_db)):
    """获取单个标签"""
    tag = crud.get_tag(db=db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.post("/posts/{post_id}/tags/{tag_id}", response_model=schemas.PostResponse)
async def add_tag_to_post(post_id: int, tag_id: int, db: Session = Depends(get_db)):
    """给文章添加标签"""
    post = crud.add_tag_to_post(db=db, post_id=post_id, tag_id=tag_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post or Tag not found")
    return post

@router.delete("/posts/{post_id}/tags/{tag_id}", response_model=schemas.PostResponse)
async def remove_tag_from_post(post_id: int, tag_id: int, db: Session = Depends(get_db)):
    """从文章移除标签"""
    post = crud.remove_tag_from_post(db=db, post_id=post_id, tag_id=tag_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post or Tag not found")
    return post

@router.delete("/{tag_id}")
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """删除标签"""
    tag = crud.delete_tag(db=db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}


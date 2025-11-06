# crud/tag.py
from sqlalchemy.orm import Session
from models import Tag, Post
from schemas import TagCreate

def create_tag(db: Session, tag: TagCreate):
    """创建标签，如果已存在则返回已有标签"""
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        return existing_tag
    
    db_tag = Tag(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_tag(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()

def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tag).offset(skip).limit(limit).all()

def add_tag_to_post(db: Session, post_id: int, tag_id: int):
    """给文章添加标签"""
    post = db.query(Post).filter(Post.id == post_id).first()
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    
    if post and tag:
        if tag not in post.tags:
            post.tags.append(tag)
            db.commit()
            db.refresh(post)
        return post
    return None

def remove_tag_from_post(db: Session, post_id: int, tag_id: int):
    """从文章移除标签"""
    post = db.query(Post).filter(Post.id == post_id).first()
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    
    if post and tag:
        if tag in post.tags:
            post.tags.remove(tag)
            db.commit()
            db.refresh(post)
        return post
    return None

def delete_tag(db: Session, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
        return tag
    return None


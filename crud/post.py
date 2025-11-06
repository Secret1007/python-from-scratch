# crud/post.py
from sqlalchemy.orm import Session
from models import Post
from schemas import PostCreate

def create_post(db: Session, post: PostCreate, author_id: int):
    db_post = Post(**post.model_dump(), author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post_id: int, post: PostCreate):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db_post.title = post.title
        db_post.content = post.content
        db.commit()
        db.refresh(db_post)
        return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return db_post

def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Post).filter(Post.author_id == user_id).offset(skip).limit(limit).all()


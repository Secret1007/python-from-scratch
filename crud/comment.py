from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
from schemas.comment import CommentCreate, CommentUpdate



def create_comment(db:Session,comment:CommentCreate,post_id:int, user_id:int):
    db_comment = models.Comment(content=comment.content,post_id=post_id,user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments(db:Session,post_id:int):
    return db.query(models.Comment).filter(models.Comment.post_id==post_id).all()

def update_comment(db:Session,comment_id:int,comment:CommentUpdate):
    db_comment = db.query(models.Comment).filter(models.Comment.id==comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db_comment.content = comment.content
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db:Session,comment_id:int):
    db_comment = db.query(models.Comment).filter(models.Comment.id==comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(db_comment)
    db.commit()
    return {"message": "Comment deleted successfully"}

def get_comment(db:Session,comment_id:int):
    return db.query(models.Comment).filter(models.Comment.id==comment_id).first()
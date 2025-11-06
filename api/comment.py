from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.users import get_current_user
from core.permissions import check_owner_or_admin
import crud
from database import get_db
import models
from schemas import CommentCreate
import schemas
from schemas.comment import CommentUpdate

router = APIRouter(tags=["comments"])

@router.post("/posts/{post_id}/comments", response_model=schemas.CommentResponse)
def create_comment(post_id:int,comment:CommentCreate,db:Session=Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_comment(db,comment,post_id, current_user.id)

@router.get("/posts/{post_id}/comments", response_model=list[schemas.CommentResponse])
def get_comments(post_id:int,db:Session=Depends(get_db)):
    return crud.get_comments(db,post_id)

@router.put("/comments/{comment_id}", response_model=schemas.CommentResponse)
def update_comment(comment_id:int,comment:CommentUpdate,db:Session=Depends(get_db), current_user: models.User = Depends(get_current_user)):
    comment = crud.get_comment(db,comment_id)
    check_owner_or_admin(comment.user_id, current_user, "comment")
    return crud.update_comment(db,comment_id,comment)

@router.delete("/comments/{comment_id}", response_model=dict)
def delete_comment(comment_id:int,db:Session=Depends(get_db), current_user: models.User = Depends(get_current_user)):
    comment = crud.get_comment(db,comment_id)
    check_owner_or_admin(comment.user_id, current_user, "comment")
    return crud.delete_comment(db,comment_id)

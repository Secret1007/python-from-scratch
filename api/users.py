# api/users.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from auth import create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
import schemas
import crud
import models

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token") 
    user = crud.get_user_by_username(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.post("", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db=db, user=user)

@router.get("", response_model=list[schemas.UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=schemas.UserResponse)
async def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/posts", response_model=list[schemas.PostResponse])
async def read_user_posts(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_user_posts(db=db, user_id=user_id, skip=skip, limit=limit)
    return posts


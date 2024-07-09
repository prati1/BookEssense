from fastapi import APIRouter, Depends
from typing import Any, Union
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.services.user import create_user, get_user
from app.db.session import get_db

router = APIRouter()

@router.post("/create", response_model=UserRead)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(db=db, user_id=user_id)

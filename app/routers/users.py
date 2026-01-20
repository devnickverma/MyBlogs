from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserRead
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud_user.get_user(db=db, user_id=user_id)

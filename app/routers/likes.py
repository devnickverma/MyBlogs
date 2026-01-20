from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from app.crud import like as crud_like
from app.schemas.like import LikeCreate
from app.dependencies import get_db, get_current_user
from app.models.models import User

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(
    like: LikeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud_like.like_post(db=db, post_id=like.post_id, user_id=current_user.id)
    return {"message": "Post liked"}

@router.delete("/", status_code=status.HTTP_200_OK)
def unlike_post(
    like: LikeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud_like.unlike_post(db=db, post_id=like.post_id, user_id=current_user.id)
    return {"message": "Post unliked"}

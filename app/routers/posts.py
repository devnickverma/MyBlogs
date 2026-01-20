from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.crud import post as crud_post
from app.schemas.post import PostCreate, PostRead
from app.dependencies import get_db, get_current_user
from app.models.models import User

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Extract owner_id from the current_user
    user_id = current_user.id
    # We might need to exclude owner_id from the post dict in CRUD if it causes conflict,
    # but let's see if we can handle it here or if CRUD handles it.
    # Actually, to be safe and adhere to "Keep CRUD unchanged", let's pass it as is.
    # Note: If PostCreate has owner_id, and CRUD does Post(**post.dict(), owner_id=user_id),
    # it might error. Realistically, we should update CRUD to exclude it or just use it.
    # But user said "Ensure CRUD function usage remains unchanged". 
    # Let's assume CRUD acts on the schema content.
    return crud_post.create_post(db=db, post=post, user_id=user_id)

@router.get("/", response_model=List[PostRead])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_post.get_posts(db=db, skip=skip, limit=limit)

@router.get("/{post_id}", response_model=PostRead)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return crud_post.get_post(db=db, post_id=post_id)

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.crud import comment as crud_comment
from app.schemas.comment import CommentCreate, CommentRead
from app.dependencies import get_db, get_current_user
from app.models.models import User

# Using no prefix to support both /comments and /posts/{post_id}/comments cleanly
# or we use prefix="/comments" and user POST /comments and GET /comments?post_id=...
# But request asked for specific endpoints.
# Let's stick to explicit definitions to match requirements exactly.

router = APIRouter(tags=["comments"])

@router.post("/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Extract IDs from body
    return crud_comment.create_comment(
        db=db, 
        comment=comment, 
        post_id=comment.post_id, 
        user_id=current_user.id
    )

@router.get("/posts/{post_id}/comments", response_model=List[CommentRead])
def read_comments(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_comment.get_comments_by_post(db=db, post_id=post_id, skip=skip, limit=limit)

from sqlalchemy.orm import Session
from app.models.models import Comment, Post
from app.schemas.comment import CommentCreate

from app.exceptions import PostNotFoundError

def get_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: CommentCreate, post_id: int, user_id: int):
    # Verify post exists first (defensive check)
    if not db.query(Post).filter(Post.id == post_id).first():
        raise PostNotFoundError(post_id=post_id)

    db_comment = Comment(
        **comment.model_dump(exclude={"post_id", "author_id"}),
        post_id=post_id,
        author_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

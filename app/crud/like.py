from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.models import Like, Post
from app.exceptions import AlreadyLikedError, NotLikedError, PostNotFoundError

def like_post(db: Session, post_id: int, user_id: int):
    # Check if post exists
    if not db.query(Post).filter(Post.id == post_id).first():
        raise PostNotFoundError(post_id=post_id)

    try:
        db_like = Like(post_id=post_id, user_id=user_id)
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return db_like
    except IntegrityError:
        db.rollback()
        raise AlreadyLikedError(post_id=post_id, user_id=user_id)

def unlike_post(db: Session, post_id: int, user_id: int):
    db_like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    if db_like:
        db.delete(db_like)
        db.commit()
        return True
    raise NotLikedError(post_id=post_id, user_id=user_id)

def get_like_count(db: Session, post_id: int):
    return db.query(Like).filter(Like.post_id == post_id).count()

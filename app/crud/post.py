from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import Post
from app.schemas.post import PostCreate
from app.exceptions import PostNotFoundError

def get_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise PostNotFoundError(post_id=post_id)
    return post

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).order_by(desc(Post.created_at), desc(Post.id)).offset(skip).limit(limit).all()

def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(**post.model_dump(exclude={"owner_id"}), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

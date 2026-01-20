from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError
from app.models.models import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.exceptions import UserAlreadyExistsError, UserNotFoundError

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError(user_id=user_id)
    return user

def get_user_by_email(db: Session, email: str):
    # Used for checking existence, so returning None is acceptable/expected by caller dependent on logic,
    # but based on strict finding, we keep it returning None to allow external checks.
    # However, create_user handles the duplication check via IntegrityError now.
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise UserAlreadyExistsError(email=user.email)

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.crud import user as crud_user
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that yields a database session.
    Closes the session after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = crud_user.get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user

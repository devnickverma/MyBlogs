from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    PostNotFoundError,
    AlreadyLikedError,
    NotLikedError
)
from app.core.database import engine, Base
# Import models to ensure they are registered with Base
from app.models import models
from app.routers import users, posts, comments, likes, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Blog API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)

@app.exception_handler(UserAlreadyExistsError)
async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

@app.exception_handler(PostNotFoundError)
async def post_not_found_handler(request: Request, exc: PostNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

@app.exception_handler(AlreadyLikedError)
async def already_liked_handler(request: Request, exc: AlreadyLikedError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.exception_handler(NotLikedError)
async def not_liked_handler(request: Request, exc: NotLikedError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

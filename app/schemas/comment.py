from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class CommentBase(BaseModel):
    content: str = Field(min_length=1, max_length=500)

class CommentCreate(CommentBase):
    post_id: int

class CommentRead(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

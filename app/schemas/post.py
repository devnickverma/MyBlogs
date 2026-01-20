from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.comment import CommentRead

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=5000)

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    # Optional: include comments count or list if needed later, but keeping basic for now.
    
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

class UserRead(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

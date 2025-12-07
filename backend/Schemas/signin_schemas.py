from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=20)
    password_confirm: str
    nickname: constr(min_length=2, max_length=10)
    profile_image: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    profile_image: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

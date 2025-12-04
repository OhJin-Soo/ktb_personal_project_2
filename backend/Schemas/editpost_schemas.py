from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    file_name: str
    title: constr(max_length=26)
    content: str
    image_url: Optional[str] = None
    version: str

class PostRead(PostCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

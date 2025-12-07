from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=26)
    content: str
    image_filename: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

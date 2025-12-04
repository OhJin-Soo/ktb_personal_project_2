from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    title: str = Field(max_length=26)
    content: str
    image_url: Optional[str] = None
    version: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

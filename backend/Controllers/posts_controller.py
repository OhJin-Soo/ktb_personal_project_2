from typing import List
from datetime import datetime
from pydantic import BaseModel

# 게시글 모델 정의
class Post(BaseModel):
    id: int
    title: str
    created_at: datetime
    comments_count: int
    views_count: int

# 샘플 데이터
POSTS = [
    Post(id=1, title="첫 번째 게시글", created_at=datetime.now(), comments_count=123, views_count=1500),
    Post(id=2, title="두 번째 게시글", created_at=datetime.now(), comments_count=456, views_count=25000),
    Post(id=3, title="세 번째 게시글", created_at=datetime.now(), comments_count=789, views_count=150000),
]

def format_count(count: int) -> str:
    """1k, 10k, 100k 단위로 표기"""
    if count >= 100_000:
        return f"{count//1000}k"
    elif count >= 10_000:
        return f"{count//1000}k"
    elif count >= 1_000:
        return f"{count//1000}k"
    return str(count)

def get_posts(skip: int = 0, limit: int = 10) -> List[Post]:
    """무한 스크롤용 페이지네이션"""
    posts_slice = POSTS[skip:skip+limit]
    for post in posts_slice:
        post.comments_count = format_count(post.comments_count)
        post.views_count = format_count(post.views_count)
    return posts_slice
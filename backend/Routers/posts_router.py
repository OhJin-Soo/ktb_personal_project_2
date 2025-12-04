from fastapi import APIRouter, Query
from typing import List
from Controllers.posts_controller import get_posts, Post

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[Post])
def read_posts(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    """
    게시글 목록 조회
    - skip: 건너뛸 게시글 수
    - limit: 가져올 게시글 수
    """
    return get_posts(skip=skip, limit=limit)

from fastapi import HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# 데이터 모델 정의
class Comment(BaseModel):
    id: int
    post_id: int
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class Post(BaseModel):
    id: int
    title: str
    content: str
    views: int = 0
    likes: int = 0
    liked: bool = False
    comments: List[Comment] = []

# 임시 DB
posts_db = []
comments_db = []
post_id_seq = 1
comment_id_seq = 1

# 컨트롤러 함수
def get_post(post_id: int) -> Post:
    for post in posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

def create_post(title: str, content: str) -> Post:
    global post_id_seq
    post = Post(id=post_id_seq, title=title, content=content)
    posts_db.append(post)
    post_id_seq += 1
    return post

def update_post(post_id: int, title: str, content: str) -> Post:
    post = get_post(post_id)
    post.title = title
    post.content = content
    return post

def delete_post(post_id: int):
    post = get_post(post_id)
    posts_db.remove(post)
    return {"message": "Post deleted"}

def increment_views(post_id: int):
    post = get_post(post_id)
    post.views += 1
    return post.views

def toggle_like(post_id: int):
    post = get_post(post_id)
    if post.liked:
        post.likes -= 1
    else:
        post.likes += 1
    post.liked = not post.liked
    return post.likes

# 댓글 관련
def add_comment(post_id: int, content: str) -> Comment:
    global comment_id_seq
    post = get_post(post_id)
    comment = Comment(id=comment_id_seq, post_id=post_id, content=content, created_at=datetime.now())
    comments_db.append(comment)
    post.comments.append(comment)
    comment_id_seq += 1
    return comment

def update_comment(comment_id: int, content: str) -> Comment:
    for comment in comments_db:
        if comment.id == comment_id:
            comment.content = content
            comment.updated_at = datetime.now()
            return comment
    raise HTTPException(status_code=404, detail="Comment not found")

def delete_comment(comment_id: int):
    for comment in comments_db:
        if comment.id == comment_id:
            post = get_post(comment.post_id)
            post.comments = [c for c in post.comments if c.id != comment_id]
            comments_db.remove(comment)
            return {"message": "Comment deleted"}
    raise HTTPException(status_code=404, detail="Comment not found")

from fastapi import APIRouter, Form
from typing import List
from Controllers.post_controller import (
    get_post, create_post, update_post, delete_post,
    increment_views, toggle_like, add_comment, update_comment, delete_comment,
    Post, Comment
)

router = APIRouter(prefix="/posts", tags=["posts"])

# 게시글 CRUD
@router.post("/", response_model=Post)
def api_create_post(title: str = Form(...), content: str = Form(...)):
    return create_post(title, content)

@router.get("/{post_id}", response_model=Post)
def api_get_post(post_id: int):
    increment_views(post_id)
    return get_post(post_id)

@router.put("/{post_id}", response_model=Post)
def api_update_post(post_id: int, title: str = Form(...), content: str = Form(...)):
    return update_post(post_id, title, content)

@router.delete("/{post_id}")
def api_delete_post(post_id: int):
    return delete_post(post_id)

# 좋아요
@router.post("/{post_id}/like")
def api_toggle_like(post_id: int):
    return {"likes": toggle_like(post_id)}

# 댓글
@router.post("/{post_id}/comments", response_model=Comment)
def api_add_comment(post_id: int, content: str = Form(...)):
    return add_comment(post_id, content)

@router.put("/comments/{comment_id}", response_model=Comment)
def api_update_comment(comment_id: int, content: str = Form(...)):
    return update_comment(comment_id, content)

@router.delete("/comments/{comment_id}")
def api_delete_comment(comment_id: int):
    return delete_comment(comment_id)

from typing import List
from sqlmodel import select
from Models.makepost_model import Post
from Schemas.makepost_schemas import PostCreate, PostResponse
from Database.database import get_session

def create_post_in_db(post_in: PostCreate) -> Post:
    """
    Inserts a post into DB and returns the DB model (Post).
    """
    with get_session() as session:
        post = Post(
            title=post_in.title,
            content=post_in.content,
            image_filename=post_in.image_filename
        )
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

def list_posts_from_db() -> List[Post]:
    with get_session() as session:
        statement = select(Post).order_by(Post.created_at.desc())
        results = session.exec(statement).all()
        return results

def get_post_from_db(post_id: int) -> Post:
    """
    Get a single post from database by ID
    """
    with get_session() as session:
        post = session.get(Post, post_id)
        if not post:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Post not found")
        return post

def update_post_in_db(post_id: int, title: str, content: str, image_filename: str = None) -> Post:
    """
    Update an existing post in the database
    """
    with get_session() as session:
        post = session.get(Post, post_id)
        if not post:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Post not found")
        
        post.title = title
        post.content = content
        if image_filename:
            post.image_filename = image_filename
        
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

def update_post_in_db(post_id: int, title: str, content: str, image_filename: str = None) -> Post:
    """
    Update an existing post in the database
    """
    with get_session() as session:
        post = session.get(Post, post_id)
        if not post:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Post not found")
        
        post.title = title
        post.content = content
        if image_filename:
            post.image_filename = image_filename
        
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

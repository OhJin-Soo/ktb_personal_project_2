from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from typing import List
from fastapi.responses import JSONResponse
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

@router.get("/{post_id}")
def api_get_post(post_id: int):
    """
    Get a single post - try database first, fallback to in-memory
    """
    from Controllers.makepost_controller import get_post_from_db
    from Schemas.makepost_schemas import PostResponse
    from fastapi.responses import JSONResponse
    from fastapi import HTTPException
    
    try:
        # Try to get from database first
        post = get_post_from_db(post_id)
        # Convert to response schema
        post_response = PostResponse.model_validate(post).model_dump(mode='json')
        # Add default values for views, likes, comments
        post_response['views'] = 0
        post_response['likes'] = 0
        post_response['liked'] = False
        post_response['comments'] = []
        return JSONResponse(status_code=200, content=post_response)
    except HTTPException:
        # If not found in database, try in-memory (for backward compatibility)
        try:
            increment_views(post_id)
            post = get_post(post_id)
            return post
        except:
            raise HTTPException(status_code=404, detail="Post not found")

@router.put("/{post_id}")
async def api_update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None)
):
    """
    Update an existing post in the database
    """
    from Controllers.makepost_controller import update_post_in_db
    from Schemas.makepost_schemas import PostResponse
    from fastapi.responses import JSONResponse
    from Routers.makepost_router import save_upload_file
    from typing import Optional
    
    try:
        # Save new image if provided
        image_filename: Optional[str] = None
        if image:
            image_filename = await save_upload_file(image)
        
        # Update post in database
        post = update_post_in_db(post_id, title, content, image_filename)
        
        # Convert to response schema
        post_response = PostResponse.model_validate(post).model_dump(mode='json')
        return JSONResponse(status_code=200, content=post_response)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error updating post: {error_trace}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"서버 오류가 발생했습니다: {str(e)}"}
        )

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

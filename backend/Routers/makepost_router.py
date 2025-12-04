from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from typing import List, Optional
from pathlib import Path
from uuid import uuid4
from datetime import datetime

from Controllers.makepost_controller import create_post_in_db, list_posts_from_db
from Schemas.makepost_schemas import PostCreate, PostResponse
from Database.database import init_db

UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter(prefix="/posts", tags=["Posts"])

# create DB tables on import/startup (you can move to app startup event if preferred)
init_db()

async def save_upload_file(file: UploadFile) -> Optional[str]:
    if not file:
        return None
    # 허용되는 MIME 타입 검사 (필요시 확장)
    if file.content_type not in ["image/png", "image/jpeg", "image/jpg", "image/gif"]:
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    ext = Path(file.filename).suffix or ""
    filename = f"{uuid4().hex}{ext}"
    dest = UPLOAD_DIR / filename
    # UploadFile.read() is async
    content = await file.read()
    with open(dest, "wb") as f:
        f.write(content)
    return filename  # DB에는 파일명(또는 경로)을 저장

@router.post("/", response_model=PostResponse)
async def add_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None)
):
    # Validation
    if not title or len(title) > 26:
        raise HTTPException(status_code=400, detail="Title must be 1-26 characters.")
    if not content:
        raise HTTPException(status_code=400, detail="Content cannot be empty.")

    # 이미지 저장 (비동기)
    image_filename = await save_upload_file(image) if image else None

    # DB DTO (Pydantic)
    post_in = PostCreate(title=title, content=content, image_filename=image_filename)

    # DB 저장 (동기 controller)
    post = create_post_in_db(post_in)
    return post  # response_model=PostResponse로 자동 직렬화

@router.get("/", response_model=List[PostResponse])
def get_posts():
    posts = list_posts_from_db()
    return posts

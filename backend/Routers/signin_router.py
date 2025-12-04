from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from typing import Optional
from pathlib import Path

from Controllers.signin_controller import edit_profile_db
from Database.database import init_db

router = APIRouter(prefix="/user", tags=["user"])

# DB 테이블 생성 (앱 시작 시)
init_db()

@router.post("/edit")
async def edit_profile_route(
    image: UploadFile = File(None),
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    nickname: str = Form(...),
):
    # 이미지가 업로드 되었다면 파일명과 bytes를 튜플로 넘깁니다.
    image_payload = None
    if image:
        # mime/type 검사: 안전을 위해 라우터에서 검사
        if image.content_type not in ["image/png", "image/jpeg", "image/jpg", "image/gif"]:
            raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
        content = await image.read()  # bytes
        image_payload = (image.filename, content)

    result = edit_profile_db(image_payload, email, password, password_confirm, nickname)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result  # {"success": True, "message": ..., "data": { ... }}

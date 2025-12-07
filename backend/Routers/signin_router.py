from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from pathlib import Path
import traceback

from Controllers.signin_controller import edit_profile_db
from Database.database import init_db

router = APIRouter(prefix="/user", tags=["user"])

# DB 테이블 생성 (앱 시작 시)
init_db()

@router.post("/edit")
async def edit_profile_route(
    image: UploadFile = File(None),
    email: str = Form(...),
    password: str = Form(default=""),
    password_confirm: str = Form(default=""),
    nickname: str = Form(default=""),
):
    try:
        # 이미지가 업로드 되었다면 파일명과 bytes를 튜플로 넘깁니다.
        image_payload = None
        if image and hasattr(image, 'filename') and image.filename and image.filename.strip():
            # mime/type 검사: 안전을 위해 라우터에서 검사
            if image.content_type and image.content_type not in ["image/png", "image/jpeg", "image/jpg", "image/gif"]:
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "message": "이미지 파일만 업로드 가능합니다."}
                )
            try:
                content = await image.read()  # bytes
                if content:
                    image_payload = (image.filename, content)
            except Exception as img_error:
                print(f"Error reading image file: {img_error}")
                # Continue without image if there's an error reading it

        # Handle empty strings or None - convert to None for profile updates
        password_val = password if (password and password.strip()) else None
        password_confirm_val = password_confirm if (password_confirm and password_confirm.strip()) else None
        nickname_val = nickname if (nickname and nickname.strip()) else None
        
        result = edit_profile_db(image_payload, email, password_val, password_confirm_val, nickname_val)
        
        if not result.get("success"):
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": result.get("message", "회원가입에 실패했습니다.")}
            )
        
        return JSONResponse(status_code=200, content=result)
    
    except Exception as e:
        # Log the error for debugging
        error_trace = traceback.format_exc()
        print(f"Error in edit_profile_route: {error_trace}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"서버 오류가 발생했습니다: {str(e)}"}
        )

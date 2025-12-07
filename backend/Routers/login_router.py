from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
from Controllers.login_controller import login_user

router = APIRouter(prefix="/auth", tags=["Login"])

# ==========================
# 로그인 라우트
# ==========================
@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):
    """
    1. 이메일/비밀번호 유효성 검사
    2. 로그인 성공 시 게시글 목록(/posts)로 이동
    """
    try:
        result = login_user(email, password)
        return JSONResponse(status_code=200, content=result)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in login: {error_trace}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"서버 오류가 발생했습니다: {str(e)}"}
        )


# ==========================
# 회원가입 이동 라우트
# ==========================
@router.get("/register")
async def move_to_register():
    """
    3. 회원가입 페이지 이동
    """
    return JSONResponse(status_code=200, content={"redirect_to": "/register"})

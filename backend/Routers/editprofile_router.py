from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
from Controllers.editprofile_controller import delete_user

router = APIRouter(prefix="/user", tags=["user"])

# 회원 탈퇴
@router.post("/delete")
def delete(email: str = Form(...), confirm: bool = Form(...)):
    """
    Delete user account from database
    """
    try:
        if not confirm:
            return JSONResponse(
                status_code=200,
                content={"message": "탈퇴가 취소되었습니다.", "success": False}
            )
        
        result = delete_user(email)
        return JSONResponse(status_code=200, content=result)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"message": e.detail, "success": False}
        )
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in delete user route: {error_trace}")
        return JSONResponse(
            status_code=500,
            content={"message": f"서버 오류가 발생했습니다: {str(e)}", "success": False}
        )

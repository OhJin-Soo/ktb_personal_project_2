from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from Controllers.editpassword_controller import change_password

router = APIRouter(prefix="/user", tags=['user'])

@router.post("/change")
async def change_password_route(
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...)
):
    try:
        result = change_password(email, password, password_confirm)
        if result.get("success"):
            return JSONResponse(status_code=200, content=result)
        else:
            return JSONResponse(status_code=400, content=result)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in change_password_route: {error_trace}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"서버 오류가 발생했습니다: {str(e)}"}
        )

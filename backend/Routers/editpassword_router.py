from fastapi import APIRouter, Form
from Controllers.editpassword_controller import change_password

router = APIRouter(prefix="/user", tags=['user'])

@router.post("/change")
async def change_password_route(
    password: str = Form(...),
    password_confirm: str = Form(...)
):
    return change_password(password, password_confirm)

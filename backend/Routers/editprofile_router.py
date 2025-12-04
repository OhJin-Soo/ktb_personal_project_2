from fastapi import APIRouter, Form
from Controllers.editprofile_controller import change_profile_image, update_nickname, delete_user

router = APIRouter(prefix="/user", tags=["user"])

# 프로필 이미지 변경
@router.post("/profile-image")
def profile_image(username: str = Form(...), image_url: str = Form(...)):
    return change_profile_image(username, image_url)

# 닉네임 수정
@router.post("/nickname")
def nickname(username: str = Form(...), new_nickname: str = Form(...)):
    return update_nickname(username, new_nickname)

# 회원 탈퇴
@router.post("/delete")
def delete(username: str = Form(...), confirm: bool = Form(...)):
    if not confirm:
        return {"message": "탈퇴가 취소되었습니다."}
    return delete_user(username)

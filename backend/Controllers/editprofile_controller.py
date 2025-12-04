from fastapi import HTTPException

# 임시 데이터 저장
fake_users = {
    "existing_user": {"nickname": "existing_user", "profile_image": "default.png"}
}

# 프로필 이미지 변경
def change_profile_image(username: str, image_url: str):
    if username not in fake_users:
        raise HTTPException(status_code=404, detail="User not found")
    fake_users[username]["profile_image"] = image_url
    return {"message": "프로필 이미지가 변경되었습니다.", "profile_image": image_url}

# 닉네임 수정
def update_nickname(username: str, new_nickname: str):
    if not new_nickname:
        raise HTTPException(status_code=400, detail="닉네임을 입력해주세요.")
    if len(new_nickname) > 10:
        raise HTTPException(status_code=400, detail="닉네임은 최대 10자까지 작성 가능합니다.")
    # 중복 확인
    for user in fake_users.values():
        if user["nickname"] == new_nickname:
            raise HTTPException(status_code=400, detail="중복된 닉네임입니다.")
    fake_users[username]["nickname"] = new_nickname
    return {"message": "닉네임이 수정되었습니다.", "nickname": new_nickname}

# 회원 탈퇴
def delete_user(username: str):
    if username not in fake_users:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_users[username]
    return {"message": "회원 탈퇴가 완료되었습니다."}

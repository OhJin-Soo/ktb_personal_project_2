from fastapi import HTTPException
import re

# 임시 사용자 데이터베이스 (예시)
users = {
    "example@example.com": {"password": "Test1234!"}
}

# ==========================
# 이메일 유효성 검사
# ==========================
def validate_email(email: str):
    if not email or len(email) < 5:
        raise HTTPException(status_code=400, detail="이메일을 입력해주세요.")
    
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise HTTPException(status_code=400, detail="올바른 이메일 주소 형식을 입력해주세요.")


# ==========================
# 비밀번호 유효성 검사
# ==========================
def validate_password(password: str):
    if not password or len(password) < 8 or len(password) > 20:
        raise HTTPException(status_code=400, detail="비밀번호는 8자 이상 20자 이하로 입력해주세요.")

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[`~!@#$%^&*(),.?\":{}|<>]).+$"
    if not re.match(pattern, password):
        raise HTTPException(status_code=400, detail="비밀번호 형식을 확인해주세요.")


# ==========================
# 로그인 처리
# ==========================
def login_user(email: str, password: str):
    validate_email(email)
    validate_password(password)

    if email not in users or users[email]["password"] != password:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호를 확인해주세요.")

    # 로그인 성공 시 반환
    return {"message": "로그인 성공", "redirect_to": "/posts"}

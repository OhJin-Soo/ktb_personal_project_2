from fastapi import HTTPException
import re
from passlib.context import CryptContext
from sqlmodel import select

from Database.database import get_session
from Models.signin_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    # Don't validate password format for login - just check if it exists
    if not password:
        raise HTTPException(status_code=400, detail="비밀번호를 입력해주세요.")

    # Check database for user
    with get_session() as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="아이디 또는 비밀번호를 확인해주세요.")
        
        # Verify password using bcrypt
        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="아이디 또는 비밀번호를 확인해주세요.")

    # 로그인 성공 시 반환
    return {
        "message": "로그인 성공",
        "redirect_to": "/posts",
        "user": {
            "id": user.id,
            "email": user.email,
            "nickname": user.nickname,
            "profile_image": user.profile_image
        }
    }

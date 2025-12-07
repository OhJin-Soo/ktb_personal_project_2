import re
from datetime import datetime
from passlib.context import CryptContext
from sqlmodel import select
from Database.database import get_session
from Models.signin_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def validate_password(password: str):
    """비밀번호 유효성 검사"""
    if not password:
        return False, "비밀번호를 입력해주세요"
    if len(password) < 8 or len(password) > 20:
        return False, "비밀번호는 8자 이상 20자 이하로 입력해야 합니다"
    if not re.search(r"[A-Z]", password):
        return False, "비밀번호에 최소 하나의 대문자가 포함되어야 합니다"
    if not re.search(r"[a-z]", password):
        return False, "비밀번호에 최소 하나의 소문자가 포함되어야 합니다"
    if not re.search(r"[0-9]", password):
        return False, "비밀번호에 최소 하나의 숫자가 포함되어야 합니다"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "비밀번호에 최소 하나의 특수문자가 포함되어야 합니다"
    return True, ""

def change_password(email: str, password: str, password_confirm: str):
    """비밀번호 변경 로직 - 실제로 DB를 업데이트합니다"""
    valid, message = validate_password(password)
    if not valid:
        return {"success": False, "message": message}
    
    if not password_confirm:
        return {"success": False, "message": "비밀번호를 한번 더 입력해주세요"}
    
    if password != password_confirm:
        return {"success": False, "message": "비밀번호 확인과 다릅니다"}

    # Find user and update password in database
    try:
        with get_session() as session:
            statement = select(User).where(User.email == email)
            user = session.exec(statement).first()
            
            if not user:
                return {"success": False, "message": "사용자를 찾을 수 없습니다."}
            
            # Update password
            user.hashed_password = hash_password(password)
            user.updated_at = datetime.utcnow()
            session.add(user)
            session.commit()
            
            return {"success": True, "message": "비밀번호가 성공적으로 변경되었습니다."}
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error changing password: {error_trace}")
        return {"success": False, "message": f"비밀번호 변경 중 오류가 발생했습니다: {str(e)}"}

import re

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

def change_password(password: str, password_confirm: str):
    """비밀번호 변경 로직"""
    valid, message = validate_password(password)
    if not valid:
        return {"success": False, "message": message}
    
    if not password_confirm:
        return {"success": False, "message": "비밀번호를 한번 더 입력해주세요"}
    
    if password != password_confirm:
        return {"success": False, "message": "비밀번호 확인과 다릅니다"}

    # DB는 사용하지 않으므로 JSON으로 성공 반환
    return {"success": True, "message": "수정 완료"}

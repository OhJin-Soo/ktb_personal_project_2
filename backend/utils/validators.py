import re
from fastapi import HTTPException

def validate_password(password: str, password_confirm: str):
    if password != password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if len(password) < 8 or len(password) > 20:
        raise HTTPException(status_code=400, detail="Password length must be 8-20 characters")
    
    if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Password must contain letters, numbers, and special characters")

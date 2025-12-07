from fastapi import HTTPException
from sqlmodel import select
from Database.database import get_session
from Models.signin_model import User

# 회원 탈퇴 - Use database instead of fake_users
def delete_user(email: str):
    """
    Delete user from database by email
    """
    try:
        with get_session() as session:
            statement = select(User).where(User.email == email)
            user = session.exec(statement).first()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            session.delete(user)
            session.commit()
            return {"message": "회원 탈퇴가 완료되었습니다.", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error deleting user: {error_trace}")
        raise HTTPException(status_code=500, detail=f"회원 탈퇴 중 오류가 발생했습니다: {str(e)}")

import re
from pathlib import Path
from uuid import uuid4
from datetime import datetime

from passlib.context import CryptContext
from sqlmodel import select

from Database.database import get_session
from Models.signin_model import User
from Schemas.signin_schemas import UserRegister, UserResponse

UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(exist_ok=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- 유틸리티: 비밀번호 해시 ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# --- 파일 저장 (동기) ---
def save_image_file(upload_file) -> str | None:
    if not upload_file:
        return None
    filename_lower = upload_file.filename.lower()
    if not filename_lower.endswith((".png", ".jpg", ".jpeg", ".gif")):
        raise ValueError("이미지 파일만 업로드 가능합니다.")
    ext = Path(upload_file.filename).suffix or ""
    filename = f"{uuid4().hex}{ext}"
    dest = UPLOAD_DIR / filename
    # UploadFile in FastAPI may be SpooledTemporaryFile with .file attribute.
    # We assume caller passes UploadFile (async) but here used in router after await read.
    # We'll accept bytes or file-like object. Expect bytes passed in 'content' param typically.
    if hasattr(upload_file, "read"):  # file-like / UploadFile object
        content = upload_file.read()
    else:
        content = upload_file  # already bytes
    with open(dest, "wb") as f:
        f.write(content)
    return filename

# --- 검증 및 DB 저장 함수 ---
def edit_profile_db(image_bytes_or_upload, email: str, password: str, password_confirm: str, nickname: str) -> dict:
    """
    - image_bytes_or_upload: raw bytes OR an object with .read() returning bytes
    - Returns dict like {"success": bool, "message": str, "data": {...}}
    """
    # 1) 이미지 검사 (optional)
    filename = None
    if image_bytes_or_upload:
        # We cannot check content_type here because router will pass bytes; router checks mime
        # For safety, require router to check filename; here we accept bytes and filename separately.
        # If image_bytes_or_upload is tuple (filename, bytes), handle that.
        if isinstance(image_bytes_or_upload, tuple) and len(image_bytes_or_upload) == 2:
            orig_name, content_bytes = image_bytes_or_upload
            name_low = orig_name.lower()
            if not name_low.endswith((".png", ".jpg", ".jpeg", ".gif")):
                return {"success": False, "message": "이미지 파일만 업로드 가능합니다."}
            # save
            ext = Path(orig_name).suffix or ""
            filename = f"{uuid4().hex}{ext}"
            dest = UPLOAD_DIR / filename
            with open(dest, "wb") as f:
                f.write(content_bytes)
        else:
            # fallback: try to read .read() or treat as bytes
            try:
                content = image_bytes_or_upload.read()
            except Exception:
                content = image_bytes_or_upload
            if not content:
                filename = None
            else:
                # we cannot know original extension; default to .bin (but router sends filename too)
                filename = f"{uuid4().hex}.bin"
                with open(UPLOAD_DIR / filename, "wb") as f:
                    f.write(content)

    # 2) 이메일 형식 검사
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"success": False, "message": "유효하지 않은 이메일 형식입니다."}

    # 3) 비밀번호 검사
    if not password:
        return {"success": False, "message": "비밀번호를 입력해주세요"}
    if len(password) < 8 or len(password) > 20:
        return {"success": False, "message": "비밀번호 형식을 확인해주세요 (8~20자)"}
    if not re.search(r"[A-Z]", password):
        return {"success": False, "message": "비밀번호 형식을 확인해주세요 (대문자 포함)"}
    if not re.search(r"[a-z]", password):
        return {"success": False, "message": "비밀번호 형식을 확인해주세요 (소문자 포함)"}
    if not re.search(r"\d", password):
        return {"success": False, "message": "비밀번호 형식을 확인해주세요 (숫자 포함)"}
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return {"success": False, "message": "비밀번호 형식을 확인해주세요 (특수문자 포함)"}

    # 4) 비밀번호 확인
    if not password_confirm:
        return {"success": False, "message": "비밀번호를 한번 더 입력해주세요"}
    if password != password_confirm:
        return {"success": False, "message": "비밀번호 확인과 다릅니다"}

    # 5) 닉네임 검사
    if len(nickname) < 2 or len(nickname) > 10:
        return {"success": False, "message": "닉네임 형식을 확인해주세요 (2~10자)"}
    if not re.match(r"^[가-힣a-zA-Z0-9]+$", nickname):
        return {"success": False, "message": "닉네임 형식을 확인해주세요 (한글, 영어, 숫자만 가능)"}

    # 6) DB 중복 이메일 검사 및 저장
    with get_session() as session:
        statement = select(User).where(User.email == email)
        existing = session.exec(statement).first()
        if existing:
            return {"success": False, "message": "이미 등록된 이메일입니다."}

        hashed = hash_password(password)
        now = datetime.utcnow()
        user = User(
            email=email,
            hashed_password=hashed,
            nickname=nickname,
            profile_image=filename,
            created_at=now,
            updated_at=now
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Build response data
        user_data = UserResponse.from_orm(user).dict()
        return {"success": True, "message": "회원정보 수정이 완료되었습니다.", "data": user_data}

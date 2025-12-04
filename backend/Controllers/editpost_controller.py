from fastapi import HTTPException, UploadFile
from pathlib import Path
import shutil
from datetime import datetime

from Models.editpost_model import Post
from Schemas.editpost_schemas import PostCreate, PostRead
from Database.database import get_session

UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(exist_ok=True)

class PostController:

    @staticmethod
    def validate_title(title: str):
        if len(title) > 26:
            raise HTTPException(status_code=400, detail="제목은 26자 이하로 작성해야 합니다.")
        return title

    @staticmethod
    async def save_image(file: UploadFile) -> str | None:
        if not file:
            return None
        if file.content_type not in ["image/png", "image/jpeg", "image/jpg", "image/gif"]:
            raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
        # (주의) 파일명 충돌을 피하려면 실제로는 uuid 등으로 파일명 변경 권장
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return str(file_path)

    @staticmethod
    def create_post_in_db(post_in: PostCreate) -> Post:
        """
        DB에 삽입하고 DB 모델(Post 인스턴스)을 반환합니다.
        (FastAPI 라우트에서 response_model=PostRead를 사용하면 JSON 직렬화됩니다.)
        """
        db = get_session()
        try:
            post = Post(
                file_name=post_in.file_name,
                title=post_in.title,
                content=post_in.content,
                image_url=post_in.image_url,
                version=post_in.version,
                created_at=datetime.utcnow()
            )
            db.add(post)
            db.commit()
            db.refresh(post)  # id, created_at 등 DB 값 갱신
            return post
        finally:
            db.close()

    @staticmethod
    def get_post_from_db(post_id: int) -> Post | None:
        db = get_session()
        try:
            post = db.get(Post, post_id)
            return post
        finally:
            db.close()

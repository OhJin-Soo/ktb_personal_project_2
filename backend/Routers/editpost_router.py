from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from Controllers.editpost_controller import PostController
from Schemas.editpost_schemas import PostCreate, PostRead

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/edit", response_model=PostRead)
async def edit_post(
    file_name: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    version: str = Form(...),
    image: UploadFile = File(None),
):
    # 제목 검증
    PostController.validate_title(title)

    # 이미지 저장
    image_url = await PostController.save_image(image) if image else None

    # DB에 저장할 DTO 생성
    post_data = PostCreate(
        file_name=file_name,
        title=title,
        content=content,
        image_url=image_url,
        version=version,
    )

    # DB 저장 실행
    post = PostController.create_post_in_db(post_data)
    if not post:
        raise HTTPException(status_code=500, detail="게시글 저장에 실패했습니다")

    return post  # response_model에 의해 JSON 변환 자동 처리

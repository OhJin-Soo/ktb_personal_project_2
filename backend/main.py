from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from Routers.editpassword_router import router as editpassword_router  # 라우터 import
from Routers.editpost_router import router as editpost_router  # 라우터 import
from Routers.editprofile_router import router as editprofile_router  # 라우터 import
from Routers.login_router import router as login_router  # 라우터 import
from Routers.post_router import router as post_router  # 라우터 import
from Routers.posts_router import router as posts_router  # 라우터 import
from Routers.signin_router import router as signin_router  # 라우터 import
from Routers.community_router import router as community_router  # 라우터 import

app = FastAPI(title="Community Web")

# Serve uploaded images as static files
upload_dir = Path("uploaded_images")
upload_dir.mkdir(exist_ok=True)
app.mount("/uploaded_images", StaticFiles(directory=str(upload_dir)), name="uploaded_images")


routers = [
    editpassword_router,
    editpost_router,
    editprofile_router,
    login_router,
    post_router,
    posts_router,
    signin_router,
    community_router
]

for r in routers:
    app.include_router(r)

@app.get("/")
def read_root():
    return {"message": "Welcome to Community Web"}

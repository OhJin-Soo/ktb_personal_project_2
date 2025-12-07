from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path
from Routers.editpassword_router import router as editpassword_router  # 라우터 import
from Routers.editpost_router import router as editpost_router  # 라우터 import
from Routers.editprofile_router import router as editprofile_router  # 라우터 import
from Routers.login_router import router as login_router  # 라우터 import
from Routers.post_router import router as post_router  # 라우터 import
from Routers.posts_router import router as posts_router  # 라우터 import
from Routers.signin_router import router as signin_router  # 라우터 import
from Routers.makepost_router import router as makepost_router  # 라우터 import

app = FastAPI(title="Community Web")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers to return JSON instead of HTML
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "message": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors, "message": "Validation error", "errors": errors}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    import traceback
    error_trace = traceback.format_exc()
    print(f"Unhandled exception: {error_trace}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)}
    )

# Serve uploaded images as static files
upload_dir = Path("uploaded_images")
upload_dir.mkdir(exist_ok=True)
app.mount("/uploaded_images", StaticFiles(directory=str(upload_dir)), name="uploaded_images")

# Serve frontend as static files
frontend_dir = Path("../frontend")
if not frontend_dir.exists():
    frontend_dir = Path("frontend")
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


routers = [
    editpassword_router,
    editpost_router,
    editprofile_router,
    login_router,
    signin_router,
    # Posts routers - order matters! More specific routes first
    makepost_router,  # GET /posts/ (DB posts) and POST /posts/
    post_router,      # GET /posts/{post_id}, PUT, DELETE (specific post operations)
    # posts_router,    # Conflicts with makepost_router - both have GET /posts/
]

for r in routers:
    app.include_router(r)

@app.get("/")
def read_root():
    frontend_path = Path("../frontend/index.html")
    if not frontend_path.exists():
        frontend_path = Path("frontend/index.html")
    if frontend_path.exists():
        return FileResponse(str(frontend_path))
    return {"message": "Welcome to Community Web"}

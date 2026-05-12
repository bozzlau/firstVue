from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.admin.auth import router as admin_auth_router
from app.routers.admin.categories_tags import router as admin_cat_tag_router
from app.routers.admin.posts import router as admin_posts_router
from app.routers.admin.comments import router as admin_comments_router
from app.routers.public.blog import router as public_router

app = FastAPI(title="Personal Blog API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:6006"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router)
app.include_router(admin_auth_router)
app.include_router(admin_cat_tag_router)
app.include_router(admin_posts_router)
app.include_router(admin_comments_router)


@app.get("/health")
def health():
    return {"status": "ok"}

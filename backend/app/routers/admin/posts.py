from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_admin
from app.schemas.blog import PaginatedPosts, PostCreate, PostOut, PostUpdate
from app.services import blog as svc

router = APIRouter(prefix="/admin", tags=["admin-posts"])


@router.get("/posts", response_model=PaginatedPosts)
def list_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    total, items = svc.get_posts(db, published_only=False, page=page, page_size=page_size)
    return PaginatedPosts(total=total, page=page, page_size=page_size, items=items)


@router.get("/posts/{post_id}", response_model=PostOut)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    obj = svc.get_post(db, post_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Post not found")
    return obj


@router.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if svc.get_post_by_slug(db, data.slug):
        raise HTTPException(status_code=409, detail="Slug already exists")
    return svc.create_post(db, data)


@router.put("/posts/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    obj = svc.update_post(db, post_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Post not found")
    return obj


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if not svc.delete_post(db, post_id):
        raise HTTPException(status_code=404, detail="Post not found")

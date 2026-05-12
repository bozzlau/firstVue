from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_admin
from app.schemas.blog import CategoryCreate, CategoryOut, CategoryUpdate, TagCreate, TagOut, TagUpdate
from app.services import blog as svc

router = APIRouter(prefix="/admin", tags=["admin-categories-tags"])


# ── Categories ────────────────────────────────────────────────────────────────

@router.get("/categories", response_model=list[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    return svc.get_categories(db)


@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if svc.get_category_by_slug(db, data.slug):
        raise HTTPException(status_code=409, detail="Slug already exists")
    return svc.create_category(db, data)


@router.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    obj = svc.update_category(db, category_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return obj


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if not svc.delete_category(db, category_id):
        raise HTTPException(status_code=404, detail="Category not found")


# ── Tags ──────────────────────────────────────────────────────────────────────

@router.get("/tags", response_model=list[TagOut])
def list_tags(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    return svc.get_tags(db)


@router.post("/tags", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    data: TagCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if svc.get_tag_by_slug(db, data.slug):
        raise HTTPException(status_code=409, detail="Slug already exists")
    return svc.create_tag(db, data)


@router.put("/tags/{tag_id}", response_model=TagOut)
def update_tag(
    tag_id: int,
    data: TagUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    obj = svc.update_tag(db, tag_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Tag not found")
    return obj


@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if not svc.delete_tag(db, tag_id):
        raise HTTPException(status_code=404, detail="Tag not found")

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.blog import CategoryOut, CommentCreate, CommentOut, PaginatedPosts, PostOut, TagOut
from app.services import blog as svc

router = APIRouter(prefix="/api", tags=["public"])


# ── Categories & Tags ─────────────────────────────────────────────────────────

@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return svc.get_categories(db)


@router.get("/tags", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db)):
    return svc.get_tags(db)


# ── Posts ─────────────────────────────────────────────────────────────────────

@router.get("/posts", response_model=PaginatedPosts)
def list_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category: str | None = Query(None, description="Filter by category slug"),
    tag: str | None = Query(None, description="Filter by tag slug"),
    db: Session = Depends(get_db),
):
    total, items = svc.get_posts(
        db,
        published_only=True,
        category_slug=category,
        tag_slug=tag,
        page=page,
        page_size=page_size,
    )
    return PaginatedPosts(total=total, page=page, page_size=page_size, items=items)


@router.get("/posts/{slug}", response_model=PostOut)
def get_post(slug: str, db: Session = Depends(get_db)):
    obj = svc.get_post_by_slug(db, slug)
    if not obj or not obj.published:
        raise HTTPException(status_code=404, detail="Post not found")
    svc.increment_views(db, obj)
    return obj


# ── Comments ──────────────────────────────────────────────────────────────────

@router.get("/posts/{slug}/comments", response_model=list[CommentOut])
def list_comments(slug: str, db: Session = Depends(get_db)):
    post = svc.get_post_by_slug(db, slug)
    if not post or not post.published:
        raise HTTPException(status_code=404, detail="Post not found")
    return svc.get_comments(db, post.id, approved_only=True)


@router.post("/posts/{slug}/comments", response_model=CommentOut, status_code=201)
def create_comment(slug: str, data: CommentCreate, db: Session = Depends(get_db)):
    post = svc.get_post_by_slug(db, slug)
    if not post or not post.published:
        raise HTTPException(status_code=404, detail="Post not found")
    return svc.create_comment(db, post.id, data)


# ── Search ────────────────────────────────────────────────────────────────────

@router.get("/search", response_model=PaginatedPosts)
def search(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total, items = svc.search_posts(db, q, published_only=True, page=page, page_size=page_size)
    return PaginatedPosts(total=total, page=page, page_size=page_size, items=items)

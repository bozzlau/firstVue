from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.post import Category, Comment, Post, PostLog, Tag, post_tags
from app.schemas.blog import (
    CategoryCreate, CategoryUpdate,
    CommentCreate, CommentUpdate,
    PostCreate, PostUpdate,
    TagCreate, TagUpdate,
)


def _add_log(db: Session, post_id: int, action: str, note: str | None = None) -> None:
    db.add(PostLog(post_id=post_id, action=action, note=note))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_tags_by_ids(db: Session, tag_ids: list[int]) -> list[Tag]:
    return db.query(Tag).filter(Tag.id.in_(tag_ids)).all()


# ── Category ──────────────────────────────────────────────────────────────────

def get_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name).all()


def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_slug(db: Session, slug: str) -> Category | None:
    return db.query(Category).filter(Category.slug == slug).first()


def create_category(db: Session, data: CategoryCreate) -> Category:
    obj = Category(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_category(db: Session, category_id: int, data: CategoryUpdate) -> Category | None:
    obj = get_category(db, category_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_category(db: Session, category_id: int) -> bool:
    obj = get_category(db, category_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Tag ───────────────────────────────────────────────────────────────────────

def get_tags(db: Session) -> list[Tag]:
    rows = (
        db.query(Tag, func.count(post_tags.c.post_id).label("post_count"))
        .outerjoin(post_tags, Tag.id == post_tags.c.tag_id)
        .group_by(Tag.id)
        .order_by(Tag.name)
        .all()
    )
    for tag, cnt in rows:
        tag.post_count = cnt
    return [tag for tag, _ in rows]


def get_tag(db: Session, tag_id: int) -> Tag | None:
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get_tag_by_slug(db: Session, slug: str) -> Tag | None:
    return db.query(Tag).filter(Tag.slug == slug).first()


def create_tag(db: Session, data: TagCreate) -> Tag:
    obj = Tag(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_tag(db: Session, tag_id: int, data: TagUpdate) -> Tag | None:
    obj = get_tag(db, tag_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_tag(db: Session, tag_id: int) -> bool:
    obj = get_tag(db, tag_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Post ──────────────────────────────────────────────────────────────────────

def get_posts(
    db: Session,
    *,
    published_only: bool = False,
    include_deleted: bool = False,
    category_slug: str | None = None,
    tag_slug: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> tuple[int, list[Post]]:
    q = db.query(Post)
    if not include_deleted:
        q = q.filter(Post.deleted_at.is_(None))
    if published_only:
        q = q.filter(Post.published.is_(True))
    if category_slug:
        q = q.join(Category).filter(Category.slug == category_slug)
    if tag_slug:
        q = q.join(Post.tags).filter(Tag.slug == tag_slug)
    total = q.count()
    items = q.order_by(Post.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return total, items


def get_post(db: Session, post_id: int) -> Post | None:
    return db.query(Post).filter(Post.id == post_id).first()


def get_post_by_slug(db: Session, slug: str) -> Post | None:
    return db.query(Post).filter(Post.slug == slug, Post.deleted_at.is_(None)).first()


def increment_views(db: Session, post: Post) -> None:
    post.views += 1
    db.commit()


def create_post(db: Session, data: PostCreate) -> Post:
    tag_ids = data.tag_ids
    post_data = data.model_dump(exclude={"tag_ids"})
    obj = Post(**post_data)
    if tag_ids:
        obj.tags = _get_tags_by_ids(db, tag_ids)
    db.add(obj)
    db.flush()
    _add_log(db, obj.id, "published" if obj.published else "draft")
    db.commit()
    db.refresh(obj)
    return obj


def update_post(db: Session, post_id: int, data: PostUpdate) -> Post | None:
    obj = get_post(db, post_id)
    if not obj:
        return None
    update_data = data.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)
    old_published = obj.published
    for field, value in update_data.items():
        setattr(obj, field, value)
    if tag_ids is not None:
        obj.tags = _get_tags_by_ids(db, tag_ids)
    if "published" in update_data and update_data["published"] != old_published:
        _add_log(db, obj.id, "published" if obj.published else "draft")
    db.commit()
    db.refresh(obj)
    return obj


def soft_delete_post(db: Session, post_id: int, note: str | None = None) -> Post | None:
    obj = db.query(Post).filter(Post.id == post_id, Post.deleted_at.is_(None)).first()
    if not obj:
        return None
    obj.deleted_at = datetime.now(timezone.utc)
    _add_log(db, obj.id, "deleted", note)
    db.commit()
    db.refresh(obj)
    return obj


def restore_post(db: Session, post_id: int, note: str | None = None) -> Post | None:
    obj = db.query(Post).filter(Post.id == post_id, Post.deleted_at.isnot(None)).first()
    if not obj:
        return None
    obj.deleted_at = None
    _add_log(db, obj.id, "restored", note)
    db.commit()
    db.refresh(obj)
    return obj


def get_post_logs(db: Session, post_id: int) -> list[PostLog]:
    return db.query(PostLog).filter(PostLog.post_id == post_id).order_by(PostLog.operated_at).all()


# ── Comment ───────────────────────────────────────────────────────────────────

def get_comments(db: Session, post_id: int, *, approved_only: bool = False) -> list[Comment]:
    q = db.query(Comment).filter(Comment.post_id == post_id)
    if approved_only:
        q = q.filter(Comment.approved.is_(True))
    return q.order_by(Comment.created_at.asc()).all()


def get_all_comments(db: Session, *, approved_only: bool = False) -> list[Comment]:
    q = db.query(Comment)
    if approved_only:
        q = q.filter(Comment.approved.is_(True))
    return q.order_by(Comment.created_at.desc()).all()


def create_comment(db: Session, post_id: int, data: CommentCreate) -> Comment:
    obj = Comment(post_id=post_id, **data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_comment(db: Session, comment_id: int, data: CommentUpdate) -> Comment | None:
    obj = db.query(Comment).filter(Comment.id == comment_id).first()
    if not obj:
        return None
    obj.approved = data.approved
    db.commit()
    db.refresh(obj)
    return obj


def delete_comment(db: Session, comment_id: int) -> bool:
    obj = db.query(Comment).filter(Comment.id == comment_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def search_posts(
    db: Session,
    q: str,
    *,
    published_only: bool = True,
    page: int = 1,
    page_size: int = 10,
) -> tuple[int, list[Post]]:
    from sqlalchemy import or_
    query = db.query(Post).filter(
        or_(
            Post.title.ilike(f"%{q}%"),
            Post.summary.ilike(f"%{q}%"),
            Post.content.ilike(f"%{q}%"),
        )
    )
    if published_only:
        query = query.filter(Post.published.is_(True))
    total = query.count()
    items = query.order_by(Post.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return total, items

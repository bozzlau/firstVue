from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


# ── Category ──────────────────────────────────────────────────────────────────

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None


class CategoryOut(CategoryBase):
    id: int
    post_count: int = 0

    model_config = {"from_attributes": True}


# ── Tag ───────────────────────────────────────────────────────────────────────

class TagBase(BaseModel):
    name: str
    slug: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None


class TagOut(TagBase):
    id: int
    post_count: int = 0

    model_config = {"from_attributes": True}


# ── Post ──────────────────────────────────────────────────────────────────────

class PostBase(BaseModel):
    title: str
    slug: str
    summary: str | None = None
    content: str
    cover_image: str | None = None
    published: bool = False
    category_id: int | None = None


class PostCreate(PostBase):
    tag_ids: list[int] = []


class PostUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    summary: str | None = None
    content: str | None = None
    cover_image: str | None = None
    published: bool | None = None
    category_id: int | None = None
    tag_ids: list[int] | None = None


class PostOut(PostBase):
    id: int
    views: int
    deleted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    category: CategoryOut | None = None
    tags: list[TagOut] = []

    model_config = {"from_attributes": True}


class PostSummaryOut(BaseModel):
    id: int
    title: str
    slug: str
    summary: str | None = None
    cover_image: str | None = None
    published: bool
    views: int
    deleted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    category: CategoryOut | None = None
    tags: list[TagOut] = []

    model_config = {"from_attributes": True}


class PostLogOut(BaseModel):
    id: int
    post_id: int
    action: str
    operated_at: datetime
    note: str | None = None

    model_config = {"from_attributes": True}


# ── Comment ───────────────────────────────────────────────────────────────────

class CommentCreate(BaseModel):
    author_name: str
    author_email: EmailStr
    content: str

    @field_validator("author_name", "content")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field must not be blank")
        return v.strip()


class CommentUpdate(BaseModel):
    approved: bool


class CommentOut(BaseModel):
    id: int
    author_name: str
    author_email: str
    content: str
    approved: bool
    created_at: datetime
    post_id: int

    model_config = {"from_attributes": True}


# ── Auth ──────────────────────────────────────────────────────────────────────

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Pagination ────────────────────────────────────────────────────────────────

class PaginatedPosts(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[PostSummaryOut]

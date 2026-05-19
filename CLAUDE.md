# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A personal blog with a FastAPI backend and a Vue 3 frontend (both complete). The backend lives in `backend/`, frontend in `frontend/`, learning notes and specs in `docs/`.

## Backend

### Setup

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set SECRET_KEY at minimum
alembic upgrade head
```

Config is loaded from `backend/.env` via Pydantic Settings (`app/config.py`). Required: `SECRET_KEY`. Defaults: SQLite at `./blog.db`, admin credentials `admin` / `changeme123`.

### Dev server

```bash
cd backend
uvicorn app.main:app --reload --port 8001
# API docs: http://localhost:8001/docs
```

### Tests

```bash
cd backend
pytest                        # all tests
pytest tests/test_blog.py::test_name  # single test
```

Tests use an in-memory SQLite database with `StaticPool`. The `autouse` fixture in `conftest.py` creates and drops all tables around each test. No `.env` needed for tests.

`conftest.py` provides three fixtures: `db` (raw session), `client` (TestClient with DB override), and `auth_headers` (pre-authenticated Bearer token for admin routes).

### Migrations

```bash
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

`alembic/env.py` imports `app.models` to register all models on `Base.metadata` before autogenerate runs — keep that import in place.

## Architecture

### Layer structure

```
routers/   — HTTP boundary: parse request, call service, return response
services/  — business logic (all DB operations live here)
models/    — SQLAlchemy ORM models
schemas/   — Pydantic models for request/response shapes
```

Routers never query the DB directly; they call `services/blog.py` functions.

```
routers/
├── public/blog.py      — all /api/* public endpoints
└── admin/
    ├── auth.py         — POST /admin/login
    ├── posts.py        — CRUD + soft-delete + restore + logs
    ├── categories_tags.py
    └── comments.py
```

### API surface

| Prefix | Auth | Purpose |
|--------|------|---------|
| `/api` | none | Public blog (posts, categories, tags, comments, search) |
| `/admin` | Bearer JWT | Admin CRUD for all resources |

Admin auth is a single user (no user table). `POST /admin/login` accepts form data and returns a JWT. All `/admin/*` routes depend on `get_current_admin` from `app/dependencies.py`.

### Key design decisions

- **Soft delete**: Posts are never hard-deleted. `deleted_at` is set on delete; `POST /admin/posts/{id}/restore` clears it. Public endpoints filter out `deleted_at IS NOT NULL` rows automatically.
- **PostLog audit trail**: Every publish, draft, delete, and restore action writes a row to `post_logs`. Valid `action` values: `published`, `draft`, `deleted`, `restored`. Use `GET /admin/posts/{id}/logs` to retrieve history.
- **Comment moderation**: Comments have an `approved` field (default `False`). Public post endpoints only return approved comments; `PATCH /admin/comments/{id}` toggles approval.
- **Model registration**: `app/models/__init__.py` must be imported before `Base.metadata` is used (alembic env and test conftest both do `import app.models`). Add new model files to that `__init__.py`.
- **CORS**: Allowed origins: `http://localhost:5173`, `http://localhost:5174`, `http://localhost:6006`.

### Model relationships

- Post ↔ Tag: many-to-many via `post_tags` join table
- Post → Comment: one-to-many, cascade delete
- Post → PostLog: one-to-many, cascade delete
- Category → Post: one-to-many, `SET NULL` on category delete (posts survive without a category)

### Service layer notes

- `get_posts()` accepts both `category_slug` and `tag_slug` filters simultaneously
- `search_posts()` runs case-insensitive ILIKE across `title`, `summary`, and `content`
- `get_tags()` computes `post_count` via a SQL join — the count is attached to each tag object before returning

## Frontend

### Setup

```bash
cd frontend
npm install
npm run dev   # http://localhost:6006
npm run build # production build
```

### Stack

- Vue 3 + Vite + Vue Router 4 + Pinia
- **Public blog** (`/`): Tailwind CSS v3, plain HTML/CSS components
- **Admin** (`/admin/*`): Element Plus (auto-imported via `unplugin-vue-components`)
- **Markdown editor**: `md-editor-v3` (PostEditView)
- **Markdown rendering**: `marked` (PostView)
- HTTP: axios, all calls in `src/api/`, JWT token auto-attached via request interceptor

### Directory structure

```
src/
├── api/           — one file per resource (client.js, auth.js, posts.js, …)
├── stores/        — auth.js (token + login state), post.js (list/current cache)
├── router/        — index.js, all routes + auth guard
├── components/
│   ├── public/    — PublicLayout.vue (nav + sidebar), PostCard.vue
│   └── admin/     — AdminLayout.vue (resizable sidebar + el-menu, logout at bottom)
└── views/
    ├── public/    — HomeView, PostView, CategoryView, TagView, SearchView, AboutView
    └── admin/     — LoginView, DashboardView, PostsView, PostEditView,
                     CategoriesView, TagsView, CommentsView
```

### Key design decisions

- **Nested routes**: Public pages are children of `PublicLayout` (nav + sidebar rendered once). Admin pages are children of `AdminLayout` (resizable sidebar, no top header bar).
- **Resizable panels**: `AdminLayout` sidebar is draggable (100–400px). `PostEditView` right panel is also draggable (min 128px); main editor fills remaining space.
- **Auth guard**: `router.beforeEach` checks `meta.requiresAuth`; redirects to `/admin/login` if `auth.isLoggedIn` is false.
- **Token storage**: JWT stored in `localStorage`, read on app init by `useAuthStore`. The axios interceptor reads it on every request; a 401 response clears it and redirects to login.
- **Element Plus**: configured for on-demand auto-import — do not add global `import ElementPlus from 'element-plus'` to `main.js`.
- **Admin CSS scoping**: All admin styles live under `.admin-scope` in `style.css` to prevent leaking into the public HUD theme. `AdminLayout` wraps everything in `.admin-scope`; `LoginView` adds it to its own root element since it renders outside `AdminLayout`. All `el-dialog`, `el-popconfirm`, and `el-select` components in admin views must use `:teleported="false"` to stay inside `.admin-scope`.
- **API base URL**: hardcoded to `http://localhost:8001` in `src/api/client.js` — change there if the backend port changes.
- **TOC visibility**: `PublicLayout` owns a `tocVisible` ref and `provide`s it to child views. `PostView` injects it to show/hide the TOC column. The layout shifts from 2-column (article + sidebar) to 3-column (TOC + article + sidebar) when on a post page and the screen is wide enough.
- **Tag cloud**: Sidebar tag cloud cycles through a `TAG_COLORS` array and scales font size by `post_count` — both computed in `PublicLayout`.

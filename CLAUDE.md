# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A personal blog with a FastAPI backend (complete) and a Vue 3 frontend (not yet scaffolded). The backend lives in `backend/`, learning notes and specs in `docs/`.

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
uvicorn app.main:app --reload
# API docs: http://localhost:8000/docs
```

### Tests

```bash
cd backend
pytest                        # all tests
pytest tests/test_blog.py::test_name  # single test
```

Tests use an in-memory SQLite database with `StaticPool`. The `autouse` fixture in `conftest.py` creates and drops all tables around each test. No `.env` needed for tests.

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

### API surface

| Prefix | Auth | Purpose |
|--------|------|---------|
| `/api` | none | Public blog (posts, categories, tags, comments, search) |
| `/admin` | Bearer JWT | Admin CRUD for all resources |

Admin auth is a single user (no user table). `POST /admin/login` accepts form data and returns a JWT. All `/admin/*` routes depend on `get_current_admin` from `app/dependencies.py`.

### Key design decisions

- **Soft delete**: Posts are never hard-deleted. `deleted_at` is set on delete; `POST /admin/posts/{id}/restore` clears it. Public endpoints filter out `deleted_at IS NOT NULL` rows automatically.
- **PostLog audit trail**: Every publish, draft, delete, and restore action writes a row to `post_logs`. Use `GET /admin/posts/{id}/logs` to retrieve history.
- **Model registration**: `app/models/__init__.py` must be imported before `Base.metadata` is used (alembic env and test conftest both do `import app.models`). Add new model files to that `__init__.py`.
- **CORS**: Only `http://localhost:5173` is allowed (Vue dev server default).

## Frontend

### Setup

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
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
│   └── admin/     — AdminLayout.vue (el-aside + el-menu)
└── views/
    ├── public/    — HomeView, PostView, CategoryView, TagView, SearchView, AboutView
    └── admin/     — LoginView, DashboardView, PostsView, PostEditView,
                     CategoriesView, TagsView, CommentsView
```

### Key design decisions

- **Nested routes**: Public pages are children of `PublicLayout` (nav + sidebar rendered once). Admin pages are children of `AdminLayout` (el-aside sidebar).
- **Auth guard**: `router.beforeEach` checks `meta.requiresAuth`; redirects to `/admin/login` if `auth.isLoggedIn` is false.
- **Token storage**: JWT stored in `localStorage`, read on app init by `useAuthStore`. The axios interceptor reads it on every request; a 401 response clears it and redirects to login.
- **Element Plus**: configured for on-demand auto-import — do not add global `import ElementPlus from 'element-plus'` to `main.js`.

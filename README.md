# Personal Blog

A full-stack personal blog built with FastAPI and Vue 3.

## Tech Stack

**Backend**
- FastAPI + SQLAlchemy + Alembic
- SQLite (default) — swappable via `DATABASE_URL`
- JWT authentication (single admin user)
- Soft delete + audit log for posts

**Frontend**
- Vue 3 + Vite + Vue Router 4 + Pinia
- Public UI: Tailwind CSS v3 with HUD-style theming (5 switchable palettes, 3 dark + 2 light)
- Admin UI: Element Plus
- Markdown editor: md-editor-v3 / marked

## Project Structure

```
├── backend/          # FastAPI app
│   ├── app/
│   │   ├── routers/  # HTTP layer
│   │   ├── services/ # Business logic + DB queries
│   │   ├── models/   # SQLAlchemy ORM models
│   │   └── schemas/  # Pydantic request/response shapes
│   ├── alembic/      # DB migrations
│   └── tests/
└── frontend/         # Vue 3 app
    └── src/
        ├── api/       # Axios API clients
        ├── stores/    # Pinia stores (auth, post)
        ├── router/    # Routes + auth guard
        ├── components/
        └── views/
```

## Getting Started

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set SECRET_KEY at minimum
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

API docs available at `http://localhost:8001/docs`.

Default admin credentials: `admin` / `changeme123` (change in `.env`).

### Frontend

```bash
cd frontend
npm install
npm run dev   # http://localhost:6006
```

## API Overview

| Prefix   | Auth       | Purpose                                      |
|----------|------------|----------------------------------------------|
| `/api`   | None       | Public blog (posts, categories, tags, search)|
| `/admin` | Bearer JWT | Admin CRUD for all resources                 |

Admin login: `POST /admin/login` (form data) → returns JWT.

## Running Tests

```bash
cd backend
pytest
```

Tests use an in-memory SQLite database — no `.env` required.

## Key Features

- **Soft delete**: Posts are never hard-deleted; restorable via `POST /admin/posts/{id}/restore`
- **Audit log**: Every publish/draft/delete/restore action is recorded in `post_logs`
- **Resizable panels**: Admin sidebar and post editor panel are draggable
- **Auth guard**: Frontend redirects to `/admin/login` on 401 or missing token
- **HUD theming (v2.0)**: Public site ships with a HUD/dashboard visual language and a runtime theme switcher (5 palettes via CSS variables, persisted in `localStorage`); see [docs/project-summary.md](docs/project-summary.md) for details

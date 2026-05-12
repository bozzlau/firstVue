def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_login_success(client):
    resp = client.post(
        "/admin/login",
        data={"username": "admin", "password": "changeme123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    resp = client.post(
        "/admin/login",
        data={"username": "admin", "password": "wrong"},
    )
    assert resp.status_code == 401


def test_admin_requires_auth(client):
    resp = client.get("/admin/posts")
    assert resp.status_code == 401


# ── Categories ────────────────────────────────────────────────────────────────

def test_create_and_list_category(client, auth_headers):
    resp = client.post(
        "/admin/categories",
        json={"name": "Tech", "slug": "tech", "description": "Technology"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["slug"] == "tech"

    resp = client.get("/api/categories")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_duplicate_category_slug(client, auth_headers):
    payload = {"name": "Tech", "slug": "tech"}
    client.post("/admin/categories", json=payload, headers=auth_headers)
    resp = client.post("/admin/categories", json=payload, headers=auth_headers)
    assert resp.status_code == 409


def test_update_category(client, auth_headers):
    resp = client.post(
        "/admin/categories",
        json={"name": "Tech", "slug": "tech"},
        headers=auth_headers,
    )
    cat_id = resp.json()["id"]
    resp = client.put(
        f"/admin/categories/{cat_id}",
        json={"name": "Technology"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Technology"


def test_delete_category(client, auth_headers):
    resp = client.post(
        "/admin/categories",
        json={"name": "Tech", "slug": "tech"},
        headers=auth_headers,
    )
    cat_id = resp.json()["id"]
    resp = client.delete(f"/admin/categories/{cat_id}", headers=auth_headers)
    assert resp.status_code == 204


# ── Tags ──────────────────────────────────────────────────────────────────────

def test_create_and_list_tag(client, auth_headers):
    resp = client.post(
        "/admin/tags",
        json={"name": "Python", "slug": "python"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    resp = client.get("/api/tags")
    assert len(resp.json()) == 1


# ── Posts ─────────────────────────────────────────────────────────────────────

def test_create_and_get_post(client, auth_headers):
    resp = client.post(
        "/admin/posts",
        json={
            "title": "Hello World",
            "slug": "hello-world",
            "content": "First post content",
            "published": True,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["slug"] == "hello-world"

    resp = client.get("/api/posts/hello-world")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Hello World"


def test_unpublished_post_not_visible_publicly(client, auth_headers):
    client.post(
        "/admin/posts",
        json={"title": "Draft", "slug": "draft", "content": "...", "published": False},
        headers=auth_headers,
    )
    resp = client.get("/api/posts/draft")
    assert resp.status_code == 404


def test_post_list_pagination(client, auth_headers):
    for i in range(3):
        client.post(
            "/admin/posts",
            json={"title": f"Post {i}", "slug": f"post-{i}", "content": "x", "published": True},
            headers=auth_headers,
        )
    resp = client.get("/api/posts?page=1&page_size=2")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2


def test_search_posts(client, auth_headers):
    client.post(
        "/admin/posts",
        json={"title": "FastAPI Guide", "slug": "fastapi-guide", "content": "Learn FastAPI", "published": True},
        headers=auth_headers,
    )
    resp = client.get("/api/search?q=FastAPI")
    assert resp.status_code == 200
    assert resp.json()["total"] == 1


# ── Comments ──────────────────────────────────────────────────────────────────

def test_create_and_approve_comment(client, auth_headers):
    client.post(
        "/admin/posts",
        json={"title": "Post", "slug": "post", "content": "content", "published": True},
        headers=auth_headers,
    )
    resp = client.post(
        "/api/posts/post/comments",
        json={"author_name": "Alice", "author_email": "alice@example.com", "content": "Great post!"},
    )
    assert resp.status_code == 201
    comment_id = resp.json()["id"]
    assert resp.json()["approved"] is False

    # Not visible publicly until approved
    resp = client.get("/api/posts/post/comments")
    assert len(resp.json()) == 0

    # Admin approves
    resp = client.patch(
        f"/admin/comments/{comment_id}",
        json={"approved": True},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["approved"] is True

    # Now visible publicly
    resp = client.get("/api/posts/post/comments")
    assert len(resp.json()) == 1


# ── Soft Delete & Restore ─────────────────────────────────────────────────────

def test_soft_delete_hides_post_publicly(client, auth_headers):
    client.post(
        "/admin/posts",
        json={"title": "To Delete", "slug": "to-delete", "content": "bye", "published": True},
        headers=auth_headers,
    )
    # 公开可见
    assert client.get("/api/posts/to-delete").status_code == 200

    # 软删除
    resp = client.delete("/admin/posts/1", headers=auth_headers)
    assert resp.status_code == 200

    # 公开不可见
    assert client.get("/api/posts/to-delete").status_code == 404


def test_restore_post(client, auth_headers):
    client.post(
        "/admin/posts",
        json={"title": "Restore Me", "slug": "restore-me", "content": "x", "published": True},
        headers=auth_headers,
    )
    post_id = client.get("/admin/posts?include_deleted=true", headers=auth_headers).json()["items"][0]["id"]

    client.delete(f"/admin/posts/{post_id}", headers=auth_headers)
    assert client.get("/api/posts/restore-me").status_code == 404

    resp = client.post(f"/admin/posts/{post_id}/restore", headers=auth_headers)
    assert resp.status_code == 200
    assert client.get("/api/posts/restore-me").status_code == 200


def test_post_logs_recorded(client, auth_headers):
    client.post(
        "/admin/posts",
        json={"title": "Log Test", "slug": "log-test", "content": "x", "published": True},
        headers=auth_headers,
    )
    post_id = client.get("/admin/posts", headers=auth_headers).json()["items"][0]["id"]

    client.delete(f"/admin/posts/{post_id}", headers=auth_headers)
    client.post(f"/admin/posts/{post_id}/restore", headers=auth_headers)

    logs = client.get(f"/admin/posts/{post_id}/logs", headers=auth_headers).json()
    actions = [l["action"] for l in logs]
    assert "published" in actions
    assert "deleted" in actions
    assert "restored" in actions


# ── Views ─────────────────────────────────────────────────────────────────────

def test_views_increment_on_get(client, auth_headers):
    client.post(
        "/admin/posts",
        json={"title": "View Test", "slug": "view-test", "content": "x", "published": True},
        headers=auth_headers,
    )
    client.get("/api/posts/view-test")
    client.get("/api/posts/view-test")
    resp = client.get("/api/posts/view-test")
    assert resp.json()["views"] == 3


# ── Cover Image ───────────────────────────────────────────────────────────────

def test_cover_image_stored(client, auth_headers):
    resp = client.post(
        "/admin/posts",
        json={
            "title": "With Cover",
            "slug": "with-cover",
            "content": "x",
            "published": True,
            "cover_image": "https://example.com/cover.jpg",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["cover_image"] == "https://example.com/cover.jpg"

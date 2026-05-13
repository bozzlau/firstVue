# 25 · pytest 测试

## 💡 为什么要写测试

改了一个功能，怎么确认没有把其他功能搞坏？手动点一遍太慢，而且容易漏。测试就是**用代码来验证代码**，每次改动后跑一遍，几秒钟就能知道有没有问题。

`pytest` 是第三方包，在 `requirements.txt` 里。

---

## 🧩 最简单的测试（test_blog.py 第 1 行）

```python
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
```

pytest 的规则：**函数名以 `test_` 开头，就是一个测试**。

`assert` 是 Python 内置关键字，意思是"断言这个条件为真，否则报错"：

```python
assert 1 + 1 == 2      # 通过
assert resp.status_code == 200   # 如果状态码不是 200，测试失败
```

`client` 是从哪来的？看函数参数——pytest 看到参数名 `client`，会自动去 `conftest.py` 里找同名的 fixture 注入进来。

---

## 🧩 conftest.py：测试的基础设施

`conftest.py` 是 pytest 的特殊文件，里面定义的 **fixture（夹具）** 可以被同目录所有测试文件使用。

### 测试用独立数据库（第 13 行）

```python
engine = create_engine(
    "sqlite://",          # 内存数据库，不写文件，测试结束自动消失
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, # 所有连接共享同一个内存数据库
)
```

测试不能用真实数据库，否则测试数据会污染生产数据。这里用 SQLite 内存数据库，测试结束自动清空。

### autouse fixture：每个测试前后自动执行（第 21 行）

```python
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)   # 测试前：建表
    yield
    Base.metadata.drop_all(bind=engine)     # 测试后：删表
```

`autouse=True` 表示不需要在测试函数里声明，每个测试自动使用它。

`yield` 把执行权交给测试函数，测试跑完后回来执行 `yield` 后面的代码（删表）。这样每个测试都从干净的空数据库开始。

### client fixture：模拟 HTTP 请求（第 37 行）

```python
@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db   # 替换依赖
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

两个关键点：

**`TestClient`** — FastAPI 提供的测试工具，模拟 HTTP 请求，不需要真正启动服务器：

```python
resp = client.get("/health")                            # 模拟 GET 请求
resp = client.post("/admin/login", data={...})          # 模拟 POST 请求
```

**`dependency_overrides`** — FastAPI 的依赖替换机制。正常运行时 `get_db` 连接真实数据库，测试时把它替换成连接内存数据库的版本，接口代码完全不用改：

```python
app.dependency_overrides[get_db] = override_get_db   # 测试时用这个
# 测试结束后：
app.dependency_overrides.clear()   # 恢复原来的
```

### auth_headers fixture：自动登录（第 51 行）

```python
@pytest.fixture
def auth_headers(client):
    resp = client.post(
        "/admin/login",
        data={"username": "admin", "password": "changeme123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

需要登录的测试，在参数里加 `auth_headers`，pytest 自动登录并返回带 token 的请求头：

```python
def test_create_and_list_category(client, auth_headers):
    resp = client.post(
        "/admin/categories",
        json={"name": "Tech", "slug": "tech"},
        headers=auth_headers,   # 自动带上 token
    )
```

---

## 🧩 fixture 的依赖链

pytest 的 fixture 可以互相依赖，自动按顺序创建：

```
setup_db（autouse，每个测试自动执行）
    ↓
db（创建数据库 session）
    ↓
client（依赖 db，创建测试客户端）
    ↓
auth_headers（依赖 client，执行登录）
```

测试函数写 `def test_xxx(client, auth_headers)`，pytest 自动把整条链都准备好。

---

## 🧩 运行测试

```bash
cd backend
pytest                                         # 跑所有测试
pytest tests/test_blog.py::test_health        # 跑单个测试
pytest -v                                      # 显示每个测试的名字和结果
```

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `pytest` | 第三方包 | 测试框架，函数名 `test_` 开头就是测试 |
| `assert` | Python 内置 | 断言条件为真，否则测试失败 |
| `conftest.py` | pytest 约定 | 定义 fixture，自动被同目录测试使用 |
| `@pytest.fixture` | `pytest` | 标记一个函数为 fixture |
| `autouse=True` | `pytest` | 每个测试自动使用，不需要声明 |
| `yield` | Python 语法 | fixture 里的 yield：前面是准备，后面是清理 |
| `TestClient` | `fastapi` | 模拟 HTTP 请求，不需要启动服务器 |
| `dependency_overrides` | `fastapi` | 测试时替换依赖，不改业务代码 |

## 🔗 相关文件

- `backend/tests/conftest.py` — fixture 定义
- `backend/tests/test_blog.py` — 所有测试用例

# 18 · FastAPI 路由：参数、依赖注入、装饰器

## 🧩 路由器和前缀

打开 `backend/app/routers/public/blog.py` 第 8 行：

```python
router = APIRouter(prefix="/api", tags=["public"])
```

`APIRouter` 把一组相关接口打包在一起：
- `prefix="/api"` → 这个路由器里所有接口自动加上 `/api` 前缀
- `tags=["public"]` → 在 API 文档里分组显示

所以写 `@router.get("/posts")`，实际完整路径是 `/api/posts`。

---

## 🧩 Python 类型注解

看函数定义：

```python
def list_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
```

Python 里 `参数名: 类型 = 默认值` 是**类型注解**语法：

```python
page: int = 1           # page 是整数，默认值 1
name: str = "hello"     # name 是字符串，默认值 "hello"
tag: str | None = None  # tag 是字符串或 None，默认 None
```

类型注解在 Python 里**不强制**——写错类型程序不会报错。但 FastAPI 会读取这些注解，自动做**参数验证和转换**。

比如前端发来 `?page=2`，URL 里的 `2` 是字符串，FastAPI 看到 `page: int` 就自动转成整数。

---

## 🧩 Query 参数

```python
page: int = Query(1, ge=1)
page_size: int = Query(10, ge=1, le=100)
```

`Query` 从 `fastapi` 包导入，告诉 FastAPI 这个参数从 **URL 查询字符串**里读取（`?page=1&page_size=10` 这部分）。

括号里的参数：
- 第一个值 → 默认值，前端不传时用这个
- `ge=1` → greater or equal，值必须 ≥ 1
- `le=100` → less or equal，值必须 ≤ 100

如果前端传了 `?page_size=999`，FastAPI 自动返回 422 错误，不需要手动写校验逻辑。

---

## 🧩 依赖注入：Depends(get_db)

```python
db: Session = Depends(get_db)
```

`Depends(get_db)` 的意思：**每次这个接口被调用时，先执行 `get_db` 函数，把返回值作为 `db` 参数传进来**。

打开 `backend/app/database.py` 第 18-23 行：

```python
def get_db():
    db = SessionLocal()   # 创建数据库连接
    try:
        yield db          # 把连接交给接口函数用
    finally:
        db.close()        # 接口函数执行完后，关闭连接
```

`yield` 是 Python 关键字，这里的执行顺序：
1. 创建数据库连接 `db`
2. `yield db` → 把 `db` 交给接口函数
3. 接口函数执行完毕，回到 `finally`，关闭连接

每个请求都有独立的数据库连接，用完自动关闭，不会泄漏。

**为什么叫"依赖注入"：** 接口函数依赖数据库连接才能工作，但它不自己创建，由 FastAPI 框架"注入"进来。测试时可以注入假的数据库连接，不影响真实数据。

---

## 🧩 装饰器

```python
@router.get("/posts", response_model=PaginatedPosts)
def list_posts(...):
    ...
```

`@router.get("/posts")` 是 Python 的**装饰器**语法，`@` 开头。

作用：**给函数附加额外行为**，这里把 `list_posts` 注册为"处理 GET /api/posts 请求的函数"。

`response_model=PaginatedPosts` 告诉 FastAPI：返回的数据按 `PaginatedPosts` 格式序列化成 JSON。

---

## 🧩 完整请求流程

前端发来 `GET /api/posts?page=1&page_size=10`，FastAPI 做了这些事：

```
1. 匹配到 list_posts 函数
2. 从 URL 读取 page=1、page_size=10，转成整数
3. 执行 get_db()，创建数据库连接，注入为 db
4. 调用 list_posts(page=1, page_size=10, db=<连接>)
5. 函数里调用 svc.get_posts(...) 查数据库
6. 把结果包装成 PaginatedPosts 对象
7. FastAPI 序列化成 JSON 返回给前端
```

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `APIRouter` | `fastapi` 包 | 打包一组接口，`prefix` 加统一前缀 |
| 类型注解 `参数: 类型` | Python 语法 | FastAPI 用它做参数验证和转换 |
| `Query(默认值, ge=, le=)` | `fastapi` 包 | 从 URL 查询字符串读参数，自动校验 |
| `Depends(get_db)` | `fastapi` 包 | 依赖注入，每次请求自动执行并注入结果 |
| `yield` | Python 语法 | 交出值后继续执行 finally，用于资源管理 |
| `@router.get(...)` | — | 装饰器，注册路由处理函数 |

## 🔗 相关文件

- `backend/app/routers/public/blog.py` —— 路由定义
- `backend/app/database.py` —— get_db 依赖函数

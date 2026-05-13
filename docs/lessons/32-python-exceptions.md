# 32 · Python 异常处理与 HTTPException

## 💡 Python 的异常处理

Python 用 `try / except` 处理可能出错的代码，和 JavaScript 的 `try / catch` 类似：

```python
# JavaScript
try {
  const data = JSON.parse(text)
} catch (e) {
  console.log('解析失败')
}

# Python
try:
    data = json.loads(text)
except Exception as e:
    print('解析失败')
```

项目里的实际用法（`backend/app/services/auth.py` 第 31 行）：

```python
def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None   # token 无效或过期，返回 None 而不是让程序崩溃
```

`except JWTError` — 只捕获 `JWTError` 这种特定异常，其他异常不拦截，让它继续往上抛。

---

## 🧩 raise：主动抛出异常

`raise` 是 Python 关键字，主动触发一个异常，让程序停在这里：

```python
raise HTTPException(status_code=404, detail="Category not found")
```

类比 JavaScript 的 `throw new Error('...')`。

---

## 🧩 HTTPException：FastAPI 的 HTTP 错误

`HTTPException` 是 FastAPI 提供的特殊异常类，`raise` 它之后 FastAPI 会自动把它转成对应的 HTTP 响应：

```python
raise HTTPException(status_code=404, detail="Category not found")
# → HTTP 404 响应：{"detail": "Category not found"}

raise HTTPException(status_code=409, detail="Slug already exists")
# → HTTP 409 响应：{"detail": "Slug already exists"}
```

**常见状态码：**

| 状态码 | 含义 | 项目里的场景 |
|--------|------|-------------|
| 404 | Not Found | 查不到记录 |
| 409 | Conflict | slug 重复 |
| 401 | Unauthorized | 未登录或 token 无效 |
| 422 | Unprocessable Entity | 参数验证失败（Pydantic 自动返回） |

---

## 🧩 实际用法（categories_tags.py 第 28 行）

```python
@router.post("/categories", response_model=CategoryOut, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), ...):
    if svc.get_category_by_slug(db, data.slug):
        raise HTTPException(status_code=409, detail="Slug already exists")
    return svc.create_category(db, data)
```

流程：
1. 先查数据库，slug 是否已存在
2. 已存在 → `raise HTTPException(409)`，函数立即停止，FastAPI 返回 409 错误
3. 不存在 → 继续执行，创建分类，返回 201

```python
@router.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, data: CategoryUpdate, ...):
    obj = svc.update_category(db, category_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return obj
```

`svc.update_category` 找不到记录时返回 `None`，`if not obj` 检测到 `None` 就抛 404。

---

## 🧩 status_code 参数

路由装饰器上也可以设置成功时的状态码：

```python
@router.post("/categories", status_code=status.HTTP_201_CREATED)   # 创建成功返回 201
@router.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)  # 删除成功返回 204
```

`status.HTTP_201_CREATED` 是 FastAPI 提供的常量，等于整数 `201`，用常量名更易读。

默认不写 `status_code` 时，GET 返回 200，POST 也返回 200（不是 201）。

---

## 🧩 `_` 参数名的含义

```python
def list_categories(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),   # 注意这里用了 _
):
```

`_` 是 Python 约定，表示**这个变量我不打算用**。这里只需要 `get_current_admin` 的副作用（验证登录，失败就 401），不需要它的返回值（用户名），所以用 `_` 接收。

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `try / except` | Python 语法 | 捕获异常，防止程序崩溃 |
| `raise` | Python 语法 | 主动抛出异常，立即停止当前函数 |
| `HTTPException` | `fastapi` | 抛出后自动转成 HTTP 错误响应 |
| `status_code=404` | HTTP 标准 | 资源不存在 |
| `status_code=409` | HTTP 标准 | 冲突（如重复数据） |
| `status.HTTP_201_CREATED` | `fastapi` | 状态码常量，等于 201 |
| `_` 参数名 | Python 约定 | 表示不使用这个变量 |

## 🔗 相关文件

- `backend/app/routers/admin/categories_tags.py` — HTTPException 用法
- `backend/app/routers/admin/posts.py` — HTTPException 用法
- `backend/app/services/auth.py` — try/except 用法

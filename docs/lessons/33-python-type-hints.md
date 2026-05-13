# 33 · Python 类型注解

## 💡 类型注解是什么

Python 是动态类型语言，变量不需要声明类型。但可以**选择性地加上类型注解**，告诉读代码的人（和工具）这个变量或函数应该是什么类型。

```python
# 没有注解
def get_category(db, category_id):
    ...

# 有注解
def get_category(db: Session, category_id: int) -> Category | None:
    ...
```

注解**不强制执行**——写错了 Python 不报错。但 FastAPI 和 Pydantic 会读取这些注解，用来做参数验证和序列化（第 18、20 课）。

---

## 🧩 基本语法

```python
# 变量注解
name: str = "admin"
count: int = 0
flag: bool = True

# 函数参数注解
def greet(name: str, age: int) -> str:
    return f"你好，{name}"

# -> 后面是返回值类型
# -> None 表示没有返回值
def log(msg: str) -> None:
    print(msg)
```

---

## 🧩 项目里的常见写法

### `str | None`（第 115 行）

```python
category_slug: str | None = None
```

`|` 表示"或"，`str | None` 意思是：**这个值可以是字符串，也可以是 None**。

等价的旧写法（Python 3.9 之前）：`Optional[str]`。

项目里大量出现：

```python
def get_category(db: Session, category_id: int) -> Category | None:
    # 找到了返回 Category 对象，找不到返回 None
```

### `list[int]`（第 20 行）

```python
def _get_tags_by_ids(db: Session, tag_ids: list[int]) -> list[Tag]:
```

`list[int]` — 元素全是整数的列表。`list[Tag]` — 元素全是 Tag 对象的列表。

### `tuple[int, list[Post]]`（第 119 行）

```python
def get_posts(...) -> tuple[int, list[Post]]:
    ...
    return total, items
```

`tuple[int, list[Post]]` — 一个元组，第一个元素是整数（total），第二个是 Post 列表（items）。

Python 函数可以同时返回多个值，`return total, items` 实际上是返回一个元组。

### `-> None`（第 14 行）

```python
def _add_log(db: Session, post_id: int, action: str, note: str | None = None) -> None:
```

`-> None` 表示这个函数没有返回值，只做操作（写数据库），不返回数据。

### `-> bool`（第 57 行）

```python
def delete_category(db: Session, category_id: int) -> bool:
    obj = get_category(db, category_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
```

返回 `True` 表示删除成功，`False` 表示记录不存在。路由层根据这个值决定是否抛 404。

---

## 🧩 为什么要写类型注解

**1. 代码即文档** — 看函数签名就知道传什么、返回什么，不用读函数体：

```python
def get_post_by_slug(db: Session, slug: str) -> Post | None:
```

一眼就知道：传 slug 字符串，返回 Post 对象或 None。

**2. IDE 自动补全** — 编辑器知道类型后，能提示可用的属性和方法。

**3. FastAPI 依赖它** — FastAPI 读取参数类型注解来做验证和转换（第 18 课）。Pydantic 读取字段注解来定义 Schema（第 20 课）。

---

## 🎯 小结

| 写法 | 含义 |
|------|------|
| `参数: str` | 参数类型是字符串 |
| `参数: int = 0` | 参数类型是整数，默认值 0 |
| `-> Category` | 返回 Category 对象 |
| `-> None` | 没有返回值 |
| `str \| None` | 字符串或 None |
| `list[int]` | 整数列表 |
| `tuple[int, list[Post]]` | 元组，含整数和 Post 列表 |

## 🔗 相关文件

- `backend/app/services/blog.py` — 所有 Service 函数都有完整注解
- `backend/app/schemas/blog.py` — Pydantic 字段注解
- `backend/app/models/post.py` — SQLAlchemy `Mapped[str]` 注解

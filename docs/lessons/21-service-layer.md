# 21 · Service 层：SQLAlchemy 查询语法

## 💡 Service 层是什么

打开 `backend/app/services/blog.py`。

这一层是**业务逻辑层**，专门负责和数据库打交道。

```
Router（路由层）   → 解析请求参数，调用 Service
Service（服务层）  → 查数据库，处理业务逻辑
Model（模型层）    → 定义表结构
```

Router 不直接查数据库，它只调用 Service 里的函数。这样分层的好处：路由文件只管"接收请求、返回响应"，数据库逻辑集中在一个地方，好维护。

---

## 🧩 查询语法：链式调用

SQLAlchemy 的查询是**链式调用**，一步一步加条件，最后用 `.all()` 或 `.first()` 执行。

### 查所有分类（第 27 行）

```python
def get_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name).all()
```

拆开来看：

```
db.query(Category)          → 告诉 SQLAlchemy：我要查 Category 表
.order_by(Category.name)    → 按 name 字段排序
.all()                      → 执行查询，返回所有结果（列表）
```

翻译成 SQL：`SELECT * FROM categories ORDER BY name`

### 查单条记录（第 31 行）

```python
def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()
```

```
.filter(Category.id == category_id)  → WHERE id = ?
.first()                              → 只取第一条，没有返回 None
```

`.all()` 返回列表，`.first()` 返回单个对象或 `None`。

---

## 🧩 增删改查的标准流程

### 新增（第 38 行）

```python
def create_category(db: Session, data: CategoryCreate) -> Category:
    obj = Category(**data.model_dump())   # 1. 创建对象
    db.add(obj)                           # 2. 加入会话
    db.commit()                           # 3. 写入数据库
    db.refresh(obj)                       # 4. 从数据库重新读取
    return obj
```

**`data.model_dump()`** — Pydantic 提供的方法，把 Schema 对象转成字典：

```python
data = CategoryCreate(name="技术", slug="tech")
data.model_dump()
# → {"name": "技术", "slug": "tech", "description": None}
```

**`Category(**data.model_dump())`** — Python 的 `**` 语法，把字典展开成关键字参数：

```python
# 等价于：
Category(name="技术", slug="tech", description=None)
```

**`db.refresh(obj)`** — 提交后数据库会自动填入 `id`、`created_at` 等字段，`refresh` 把这些值同步回 Python 对象，这样 `return obj` 时对象是完整的。

### 更新（第 46 行）

```python
def update_category(db: Session, category_id: int, data: CategoryUpdate) -> Category | None:
    obj = get_category(db, category_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj
```

两个新东西：

**`exclude_unset=True`** — 前端更新文章时可能只传了 `title`，没传 `slug`。`exclude_unset=True` 只返回前端实际传了的字段，没传的字段不包含在字典里，避免把没传的字段覆盖成 `None`。

**`setattr(obj, field, value)`** — Python 内置函数，动态设置对象属性：

```python
setattr(obj, "name", "新名字")
# 等价于：
obj.name = "新名字"
```

用 `setattr` 是因为字段名是变量（`field`），不能写 `obj.field`（那会找名叫 `field` 的属性）。

### 删除（第 57 行）

```python
def delete_category(db: Session, category_id: int) -> bool:
    obj = get_category(db, category_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
```

`db.delete(obj)` 标记删除，`db.commit()` 真正执行。

---

## 🧩 get_posts：带过滤和分页（第 110 行）

```python
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
```

**`*` 参数** — 函数定义里的 `*` 表示后面的参数必须用关键字传，不能按位置传：

```python
get_posts(db, published_only=True)   # 正确
get_posts(db, True)                  # 报错
```

**条件叠加** — `q` 是查询对象，每次 `.filter()` 返回新的查询对象，条件累积：

```python
q = db.query(Post)
q = q.filter(Post.deleted_at.is_(None))   # 加条件1
q = q.filter(Post.published.is_(True))    # 加条件2
# 最终 SQL：WHERE deleted_at IS NULL AND published = true
```

**分页**：

```python
.offset((page - 1) * page_size)   # 跳过前几条
.limit(page_size)                  # 最多取几条
```

第 1 页：`offset(0).limit(10)` → 取第 1-10 条  
第 2 页：`offset(10).limit(10)` → 取第 11-20 条

**返回 `tuple[int, list[Post]]`** — 同时返回总数和当前页数据，前端用总数计算总页数。

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `db.query(Model)` | SQLAlchemy | 开始一个查询 |
| `.filter(条件)` | SQLAlchemy | 加 WHERE 条件，可以链式叠加 |
| `.all()` / `.first()` | SQLAlchemy | 执行查询，返回列表 / 单个对象 |
| `db.add()` / `db.commit()` / `db.refresh()` | SQLAlchemy | 新增的三步走 |
| `data.model_dump()` | Pydantic | Schema 对象转字典 |
| `exclude_unset=True` | Pydantic | 只包含前端实际传了的字段 |
| `setattr(obj, field, value)` | Python 内置 | 动态设置对象属性 |
| `.offset().limit()` | SQLAlchemy | 分页 |

## 🔗 相关文件

- `backend/app/services/blog.py` — 所有 Service 函数
- `backend/app/routers/public/blog.py` — 调用 Service 的路由

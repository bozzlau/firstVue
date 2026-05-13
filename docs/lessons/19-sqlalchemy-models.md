# 19 · SQLAlchemy 数据模型（ORM）

## 💡 SQLAlchemy 是什么，从哪来

`sqlalchemy` 是一个**第三方 Python 包**，打开 `backend/requirements.txt` 能看到它。

作用：**让你用 Python 类来描述数据库表，用 Python 代码查询数据库**，不需要手写 SQL。这种技术叫 **ORM（对象关系映射）**。

没有 ORM：
```python
cursor.execute("SELECT * FROM posts WHERE published = 1 LIMIT 10")
rows = cursor.fetchall()
```

有了 ORM：
```python
posts = db.query(Post).filter(Post.published == True).limit(10).all()
```

ORM 帮你把 Python 代码翻译成 SQL。

---

## 🧩 一个模型类 = 一张数据库表

打开 `backend/app/models/post.py`，看 `Post` 类（第 54 行）：

```python
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(280), unique=True, nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

| Python 类 | 数据库表 |
|----------|---------|
| `class Post` | 表名 `posts` |
| `id: Mapped[int]` | `id` 列，整数 |
| `title: Mapped[str]` | `title` 列，字符串 |
| `published: Mapped[bool]` | `published` 列，布尔值 |
| `deleted_at: Mapped[datetime \| None]` | `deleted_at` 列，可以为空 |

`Base` 是从 `database.py` 导入的基类，所有模型都要继承它，SQLAlchemy 才能识别。

---

## 🧩 列的配置选项

```python
id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
slug: Mapped[str] = mapped_column(String(280), unique=True, nullable=False, index=True)
```

| 配置 | 含义 |
|------|------|
| `primary_key=True` | 主键，唯一标识每一行 |
| `nullable=False` | 不能为空 |
| `nullable=True` | 可以为空（NULL） |
| `unique=True` | 值在整张表里唯一 |
| `index=True` | 建索引，查询更快 |
| `default=False` | 插入时的默认值 |

---

## 🧩 关联关系（relationship）

### 为什么需要 relationship

没有 `relationship`，想拿文章的分类名需要两次查询：

```python
# 第一次：查文章，拿到 category_id（只是一个数字）
post = db.query(Post).filter(Post.id == 1).first()
print(post.category_id)   # → 3

# 第二次：拿着数字再查分类表
category = db.query(Category).filter(Category.id == post.category_id).first()
print(category.name)      # → "技术"
```

有了 `relationship`，SQLAlchemy 自动做第二次查询：

```python
post = db.query(Post).filter(Post.id == 1).first()
print(post.category.name)   # → "技术"，一行搞定
```

### Post 模型里的两个字段对比

```python
category_id: Mapped[int | None] = mapped_column(...)    # 存数字 3（外键）
category: Mapped["Category | None"] = relationship(...) # 存完整 Category 对象
```

- `post.category_id` → `3`（数字）
- `post.category` → `<Category id=3 name="技术">`（对象）
- `post.category.name` → `"技术"`

### back_populates：双向关联

```python
# Category 类里
posts: Mapped[list["Post"]] = relationship("Post", back_populates="category")

# Post 类里
category: Mapped["Category | None"] = relationship("Category", back_populates="posts")
```

`back_populates` 告诉 SQLAlchemy 这两个关联是同一个关系的两端，互相对应：

```
Post.category  ←→  Category.posts
```

效果：
```python
post.category        # → 这篇文章的分类对象
category.posts       # → 这个分类下所有文章的列表
```

`back_populates` 的值就是**对方那端的属性名**。

### 多对多：文章 ↔ 标签

一篇文章可以有多个标签，一个标签也可以属于多篇文章。需要一张中间表：

```python
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
```

`post_tags` 表只有两列，记录哪篇文章有哪个标签。

```python
# Post 类里
tags: Mapped[list["Tag"]] = relationship("Tag", secondary=post_tags, back_populates="posts")
```

`secondary=post_tags` 告诉 SQLAlchemy 通过中间表关联。之后直接用 `post.tags` 拿到所有标签列表。

---

## 💡 软删除：deleted_at 字段

```python
deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

文章"删除"时不真正从数据库删除，而是把 `deleted_at` 设为当前时间：
- `deleted_at` 是 `None` → 文章正常存在
- `deleted_at` 有值 → 文章已被软删除

公开接口过滤掉 `deleted_at` 不为空的文章，管理后台可以恢复。

---

## 💡 自动时间戳和 lambda

```python
created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
)
updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc),
)
```

- `default=lambda: datetime.now(timezone.utc)` → 插入时自动填入当前时间
- `onupdate=lambda: datetime.now(timezone.utc)` → 更新时自动更新时间

`lambda` 是 Python 的匿名函数，`lambda: 表达式` 等价于：

```python
def get_now():
    return datetime.now(timezone.utc)
```

`default` 需要传**函数**而不是值——传值的话所有记录用同一个时间；传函数，每次插入时才调用，得到当前时间。

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `sqlalchemy` | Python 包 | ORM，用 Python 类操作数据库 |
| `class Post(Base)` | — | 一个类 = 一张表 |
| `mapped_column(...)` | `sqlalchemy` | 定义列的类型和约束 |
| `ForeignKey` | `sqlalchemy` | 外键，关联另一张表 |
| `relationship` | `sqlalchemy` | 关联对象，直接通过属性访问关联数据 |
| `back_populates` | `sqlalchemy` | 声明双向关联，值是对方的属性名 |
| 软删除 | 设计模式 | 不真正删除，用 `deleted_at` 标记 |
| `lambda` | Python 语法 | 匿名函数，`lambda: 表达式` |

## 🔗 相关文件

- `backend/app/models/post.py` —— 所有数据模型
- `backend/app/database.py` —— Base 基类定义

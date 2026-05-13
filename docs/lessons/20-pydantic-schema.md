# 20 · Pydantic Schema：数据验证与序列化

## 💡 Pydantic 是什么，从哪来

`pydantic` 是一个**第三方 Python 包**，打开 `backend/requirements.txt` 能看到它。FastAPI 内部也大量依赖它。

作用：**定义数据的结构，自动做验证和序列化**。

---

## 💡 为什么需要 Schema

数据库里的 `Post` 对象包含所有字段，但不同场景需要不同的数据：

- 前端**创建文章**时发来的数据：`title`、`content`、`tag_ids`...
- 前端**更新文章**时发来的数据：所有字段都是可选的
- 后端**返回给前端**的数据：包含 `id`、`created_at`、嵌套的 `category` 对象...

Schema 就是**定义每种场景下数据长什么样**，同时充当两个方向的过滤器：

```
输入方向：验证前端发来的数据格式是否正确
输出方向：控制返回给前端哪些字段、什么格式
```

---

## 🧩 Schema 在哪一步发挥作用

看路由定义：

```python
@router.post("/posts", response_model=PostOut)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
```

**验证发生在函数执行之前**，是 FastAPI 框架自动做的。

```
前端发来 JSON
    ↓
FastAPI 接收到请求
    ↓
FastAPI 看到参数 data: PostCreate
    ↓
FastAPI 把 JSON 交给 Pydantic，按 PostCreate 的定义验证
    ↓
验证失败 → 直接返回 422 错误，函数不执行
验证成功 → 把 JSON 转成 PostCreate 对象，传给函数
    ↓
你的函数 create_post(data, db) 开始执行
```

**你的函数代码还没开始跑，验证就已经做完了。**

### 具体场景

`PostCreate` 定义：

```python
class PostCreate(PostBase):
    tag_ids: list[int] = []

class PostBase(BaseModel):
    title: str       # 必填，字符串
    slug: str        # 必填，字符串
    content: str     # 必填，字符串
    published: bool = False
    category_id: int | None = None
```

**场景 1：漏传 `title`**

```json
{ "slug": "hello", "content": "..." }
```

FastAPI 进入函数之前发现 `title` 缺失，直接返回 422，函数不执行。

**场景 2：`tag_ids` 传了字符串**

```json
{ "title": "hello", "content": "...", "slug": "hi", "tag_ids": ["abc"] }
```

`tag_ids` 里的值不是整数，直接返回 422，函数不执行。

**场景 3：数据完全正确**

```json
{ "title": "hello", "content": "...", "slug": "hi", "tag_ids": [1, 3] }
```

验证通过，转成 `PostCreate` 对象传给函数：

```python
def create_post(data: PostCreate, ...):
    print(data.title)    # "hello"
    print(data.tag_ids)  # [1, 3]（整数列表，不是字符串）
```

---

## 🧩 输出方向：response_model 过滤字段

`svc.get_posts()` 查数据库返回的 `Post` 对象包含所有字段：

```
Post 对象内部：
  id, title, slug, content（全文）, published, views,
  deleted_at, created_at, updated_at,
  category_id, category, tags, comments, logs ...
```

路由定义了 `response_model=PaginatedPosts`，FastAPI 按 `PostSummaryOut` 的定义过滤：

```python
class PostSummaryOut(BaseModel):
    id: int
    title: str
    slug: str
    summary: str | None = None    # 只要摘要，不要全文 content
    cover_image: str | None = None
    views: int
    created_at: datetime
    category: CategoryOut | None = None
    tags: list[TagOut] = []
    model_config = {"from_attributes": True}
```

前端最终收到：

```json
{
  "id": 5,
  "title": "关于写作",
  "summary": "写作不是为了让别人看...",
  "category": { "id": 3, "name": "随笔", "slug": "essay" },
  "tags": [{ "id": 1, "name": "思考", "slug": "thinking" }]
}
```

`content`（文章全文）、`comments`、`logs` 等字段不在 Schema 里，全部被丢掉。

### 同一数据，不同 Schema，不同结果

文章列表页用 `PostSummaryOut`（没有 `content`），文章详情页用 `PostOut`（有 `content`）：

```python
# 列表页
@router.get("/posts", response_model=PaginatedPosts)      # PostSummaryOut，无全文

# 详情页
@router.get("/posts/{slug}", response_model=PostOut)      # PostOut，有全文
```

同一个数据库对象，不同的 Schema，返回不同的字段。

---

## 🧩 `from_attributes: True` 的作用

```python
class CategoryOut(CategoryBase):
    id: int
    model_config = {"from_attributes": True}
```

SQLAlchemy 查出来的是**对象**，Pydantic 默认只能处理**字典**。

加了 `from_attributes: True` 之后，Pydantic 能直接读取对象的属性，把 `Category` 对象转成 JSON。

---

## 🧩 Schema 的继承结构

```python
class CategoryBase(BaseModel):    # 公共字段，不直接用
    name: str
    slug: str
    description: str | None = None

class CategoryCreate(CategoryBase):  # 创建时用，继承所有字段
    pass                              # pass = 没有额外内容

class CategoryOut(CategoryBase):     # 返回时用，多了 id
    id: int
    model_config = {"from_attributes": True}
```

继承避免重复写字段。`pass` 是 Python 语法，表示"这个类没有额外内容，只继承父类"。

---

## 🧩 不用 Schema 会怎样

### 输入验证：手动写 if 判断

有 Schema 的写法：

```python
@router.post("/posts", response_model=PostOut)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
    # data 已经验证完毕，直接用
    ...
```

没有 Schema，你要自己验证每个字段：

```python
@router.post("/posts")
def create_post(request_body: dict, db: Session = Depends(get_db)):
    if "title" not in request_body:
        raise HTTPException(400, "title 是必填项")
    if not isinstance(request_body["title"], str):
        raise HTTPException(400, "title 必须是字符串")
    if "content" not in request_body:
        raise HTTPException(400, "content 是必填项")
    if "tag_ids" in request_body:
        if not isinstance(request_body["tag_ids"], list):
            raise HTTPException(400, "tag_ids 必须是列表")
        for tag_id in request_body["tag_ids"]:
            if not isinstance(tag_id, int):
                raise HTTPException(400, "tag_id 必须是整数")
    # ... 每个字段都要这样写，还没开始真正的业务逻辑
```

`PostCreate` 有 5 个字段，每个字段都要这样写一遍。

### 输出过滤：手动拼字典

有 Schema 的写法：

```python
@router.get("/posts", response_model=PaginatedPosts)
def list_posts(...):
    items, total = svc.get_posts(...)
    return {"total": total, "items": items}  # FastAPI 自动过滤字段
```

没有 Schema，你要手动把每个字段拼成字典，`datetime` 还要手动转字符串：

```python
@router.get("/posts")
def list_posts(...):
    items, total = svc.get_posts(...)
    result = []
    for post in items:
        result.append({
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "summary": post.summary,
            "cover_image": post.cover_image,
            "views": post.views,
            "created_at": post.created_at.isoformat(),  # datetime 要手动转字符串
            "category": {
                "id": post.category.id,
                "name": post.category.name,
                "slug": post.category.slug,
            } if post.category else None,
            "tags": [
                {"id": t.id, "name": t.name, "slug": t.slug}
                for t in post.tags
            ],
        })
    return {"total": total, "items": result}
```

新增一个字段，两个地方都要改；漏写一个字段，前端就拿不到。

### 对比总结

| | 有 Schema | 没有 Schema |
|--|---------|-----------|
| 输入验证 | 自动，一行声明 | 手动，每个字段写 if 判断 |
| 输出过滤 | 自动，`response_model` | 手动，拼字典，datetime 要手动转字符串 |
| 类型转换 | 自动 | 手动 |
| API 文档 | 自动生成 | 没有 |

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `pydantic` | Python 包 | 数据验证和序列化 |
| `BaseModel` | `pydantic` | 所有 Schema 的基类 |
| 验证时机 | FastAPI 框架 | 函数执行前自动验证，失败直接返回 422 |
| `response_model` | FastAPI | 控制返回哪些字段 |
| `from_attributes: True` | Pydantic 配置 | 允许从 SQLAlchemy 对象读取属性 |
| Schema 继承 | Python 语法 | 子类拥有父类所有字段，避免重复 |

## 🔗 相关文件

- `backend/app/schemas/blog.py` —— 所有 Schema 定义
- `backend/app/routers/public/blog.py` —— response_model 使用示例

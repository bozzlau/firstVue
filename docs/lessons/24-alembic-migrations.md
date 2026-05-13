# 24 · Alembic 数据库迁移

## 💡 为什么需要迁移

数据库表不是手动创建的。开发过程中模型会变化——加字段、改类型、加新表——每次变化都要同步到数据库。

Alembic 是专门做这件事的工具：**把 Python 模型的变化转成 SQL，记录变更历史，可以升级也可以回滚**。

`alembic` 是第三方包，在 `requirements.txt` 里。

---

## 🧩 迁移文件长什么样

打开 `backend/alembic/versions/e78bfa37a2d1_initial_schema.py`（第一次建表）：

```python
def upgrade() -> None:
    op.create_table('categories', ...)
    op.create_table('posts', ...)
    op.create_table('tags', ...)
    # ...

def downgrade() -> None:
    op.drop_table('post_tags')
    op.drop_table('posts')
    # ...
```

每个迁移文件有两个函数：
- `upgrade()` — 向前，执行变更
- `downgrade()` — 向后，撤销变更

文件名里的 `e78bfa37a2d1` 是自动生成的唯一 ID，Alembic 用它追踪当前数据库执行到哪一步了。

---

## 🧩 常用命令

**第一次使用，建表：**

```bash
cd backend
alembic upgrade head   # 执行所有迁移，建好所有表
```

`head` 表示"最新版本"，把所有未执行的迁移按顺序跑完。

**改了模型，生成新迁移：**

```bash
alembic revision --autogenerate -m "add cover_image to posts"
```

Alembic 对比当前数据库和 Python 模型的差异，自动生成迁移文件。`-m` 后面是描述，会出现在文件名里。

**执行新迁移：**

```bash
alembic upgrade head
```

**回滚一步：**

```bash
alembic downgrade -1
```

---

## 🧩 env.py 做了什么

打开 `backend/alembic/env.py`：

```python
from app.config import settings
from app.database import Base
import app.models   # 注册所有模型到 Base.metadata

target_metadata = Base.metadata

# 从 .env 读数据库地址，不用在 alembic.ini 里硬编码
config.set_main_option("sqlalchemy.url", settings.database_url)
```

关键是 `import app.models`——这一行让所有模型类都加载进来，Alembic 才能知道数据库应该长什么样，才能做对比生成迁移。

`CLAUDE.md` 里特别注明：**新增模型文件必须加到 `app/models/__init__.py`**，否则 `import app.models` 不会加载它，autogenerate 就检测不到新表。

---

## 🧩 迁移链

两个迁移文件之间有依赖关系：

```
e78bfa37a2d1_initial_schema.py       ← 第一个，建所有基础表
        ↓
c3302f0d02c3_add_views_cover_image…  ← 第二个，加 views、cover_image 等字段
```

每个文件头部有 `down_revision` 字段指向上一个，形成链条。`alembic upgrade head` 按这个顺序依次执行。

---

## 🎯 小结

| 概念 | 记住 |
|------|------|
| `alembic upgrade head` | 执行所有未跑的迁移，建表/改表 |
| `alembic revision --autogenerate -m "..."` | 对比模型和数据库，自动生成迁移文件 |
| `alembic downgrade -1` | 回滚最近一次迁移 |
| `upgrade()` / `downgrade()` | 每个迁移文件的两个函数，向前/向后 |
| `import app.models` | env.py 里必须有，让 Alembic 能检测到所有模型 |

## 🔗 相关文件

- `backend/alembic/env.py` — Alembic 配置，连接数据库和模型
- `backend/alembic/versions/` — 所有迁移文件

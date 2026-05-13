# 23 · 配置与环境变量

## 💡 为什么需要环境变量

`SECRET_KEY` 是签发 JWT 的密钥，管理员密码是登录凭证——这些不能写死在代码里，否则提交到 Git 就泄露了。

解决方案：把敏感信息放在 `.env` 文件里，`.env` 加入 `.gitignore`，不提交到代码仓库。

---

## 🧩 .env 文件

打开 `backend/.env.example`（示例文件，可以提交）：

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./blog.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme123
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

实际使用时复制成 `.env` 并填入真实值：

```bash
cp backend/.env.example backend/.env
```

`.env` 文件格式：`变量名=值`，每行一个。

---

## 🧩 Pydantic Settings 自动加载（config.py）

打开 `backend/app/config.py`：

```python
from pydantic_settings import BaseSettings   # pydantic-settings 是第三方包

class Settings(BaseSettings):
    secret_key: str                              # 必填，没有会报错
    database_url: str = "sqlite:///./blog.db"   # 有默认值，可以不填
    admin_username: str = "admin"
    admin_password: str = "changeme123"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"   # 告诉它去哪里读配置文件

settings = Settings()   # 模块加载时立即读取，全局单例
```

`pydantic-settings` 是第三方包（在 `requirements.txt` 里），它继承自 Pydantic，加载顺序：

```
1. 先读环境变量（系统级，优先级最高）
2. 再读 .env 文件
3. 最后用字段的默认值
```

`secret_key: str` 没有默认值，如果 `.env` 里没有 `SECRET_KEY`，启动时直接报错，不会悄悄用空值。

---

## 🧩 在其他文件里使用

```python
# backend/app/services/auth.py
from app.config import settings

jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
```

```python
# backend/app/routers/admin/auth.py
from app.config import settings

if form.username != settings.admin_username or ...:
```

`settings` 是模块级别的单例，整个应用共享同一个实例，只读取一次 `.env`。

---

## ⚠️ 常见问题

**启动报错 `secret_key field required`** — `.env` 文件不存在，或者 `SECRET_KEY` 没有填。

**修改了 `.env` 没有生效** — 需要重启 uvicorn，配置只在启动时读取一次。

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `.env` 文件 | 约定 | 存敏感配置，不提交 Git |
| `pydantic-settings` | 第三方包 | 自动读取 `.env`，做类型验证 |
| `BaseSettings` | `pydantic-settings` | 所有配置类的基类 |
| 无默认值的字段 | Pydantic | 缺失时启动报错，不会静默失败 |
| `settings = Settings()` | — | 全局单例，模块加载时执行一次 |

## 🔗 相关文件

- `backend/app/config.py` — 配置定义
- `backend/.env.example` — 配置示例
- `backend/.env` — 实际配置（不在 Git 里）

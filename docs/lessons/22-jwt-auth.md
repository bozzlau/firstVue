# 22 · JWT 认证：管理后台登录是怎么工作的

## 💡 JWT 是什么

JWT（JSON Web Token）是一种**令牌**，登录成功后服务器发给前端，前端之后每次请求都带上它，服务器验证令牌有效就放行。

类比：就像景区的门票，买票（登录）一次，之后进出都刷票，不用每次重新验身份。

---

## 🧩 密码加密：bcrypt（第 8 行）

打开 `backend/app/services/auth.py`：

```python
from passlib.context import CryptContext   # passlib 是第三方包，在 requirements.txt 里

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**为什么不直接存明文密码？** 数据库一旦泄露，所有密码都暴露。bcrypt 是一种**单向哈希算法**，把密码变成一串乱码，无法反推原始密码。

```python
def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)
# "changeme123" → "$2b$12$abc...xyz"（每次结果不同）

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
# 验证时不是比较字符串，而是用算法重新计算
```

`verify_password` 不是把输入的密码再哈希一次然后比较字符串——bcrypt 每次哈希结果不同，它内部有专门的验证逻辑。

---

## 🧩 JWT 的生成和解析（第 21 行）

```python
from jose import JWTError, jwt   # python-jose 是第三方包，在 requirements.txt 里

ALGORITHM = "HS256"   # 签名算法

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
```

JWT 本质是一个**被签名的字典**：

```python
# 传入的 data：
{"sub": "admin"}

# 加上过期时间后：
{"sub": "admin", "exp": 1748000000}

# 用 secret_key 签名，生成一串字符串：
"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.xxx"
```

`secret_key` 是只有服务器知道的密钥（存在 `.env` 里）。有了它才能生成有效的 JWT，也才能验证 JWT 是否被篡改。

解析：

```python
def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload   # → {"sub": "admin", "exp": 1748000000}
    except JWTError:
        return None      # token 无效或已过期
```

---

## 🧩 登录接口（auth.py 第 11 行）

打开 `backend/app/routers/admin/auth.py`：

```python
@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends()):
    if form.username != settings.admin_username or not verify_password(
        form.password, _hashed_admin_password()
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": form.username})
    return TokenOut(access_token=token)
```

`OAuth2PasswordRequestForm` 是 FastAPI 提供的，专门处理表单格式的用户名密码提交（`username` + `password` 字段）。

登录流程：

```
前端发来 username + password
    ↓
对比 username 是否匹配配置
    ↓
用 verify_password 验证密码
    ↓
验证通过 → 生成 JWT → 返回给前端
验证失败 → 返回 401 错误
```

---

## 🧩 Depends：依赖注入

`Depends` 是 FastAPI 提供的，作用是：**在执行这个接口之前，先执行另一个函数，把它的返回值作为参数传进来**。

**例 1：注入数据库连接**
```python
def list_posts(db: Session = Depends(get_db)):
```
FastAPI 先执行 `get_db()`，把返回的数据库连接赋给 `db`，再调用 `list_posts`。

**例 2：验证登录状态**
```python
def list_posts(admin: str = Depends(get_current_admin)):
```
FastAPI 先执行 `get_current_admin()`，验证失败直接抛 401，函数根本不会执行；验证成功返回用户名赋给 `admin`。

**例 3：解析表单**
```python
def login(form: OAuth2PasswordRequestForm = Depends()):
```
`Depends()` 不传参数时，FastAPI 直接把 `OAuth2PasswordRequestForm` 本身当作依赖来执行，解析请求里的表单数据。

本质：把重复的前置工作抽出来复用。不用 `Depends` 的话，每个接口都要自己创建数据库连接、自己验证 token。用了 `Depends`，写一次，到处复用。

---

## 🧩 保护路由：get_current_admin（dependencies.py）

打开 `backend/app/dependencies.py`：

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

def get_current_admin(token: str = Depends(oauth2_scheme)) -> str:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, ...)
    username: str | None = payload.get("sub")
    if username != settings.admin_username:
        raise HTTPException(status_code=401, ...)
    return username
```

`OAuth2PasswordBearer` 是 FastAPI 提供的，自动从请求头里读取 `Authorization: Bearer <token>`，把 token 字符串传给函数。

管理后台的路由都加了这个依赖：

```python
# backend/app/routers/admin/posts.py
@router.get("/admin/posts")
def list_posts(
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),   # 没有有效 token → 直接 401
):
    ...
```

只要在参数里写 `Depends(get_current_admin)`，这个接口就自动受保护了。

---

## 🧩 完整认证流程

```
1. 前端发 POST /admin/login，带 username + password
        ↓
2. 后端验证密码，生成 JWT，返回给前端
        ↓
3. 前端把 JWT 存到 localStorage
        ↓
4. 之后每次请求，axios 拦截器自动加上：
   Authorization: Bearer eyJhbGci...
        ↓
5. 后端 get_current_admin 从请求头读取 token
        ↓
6. decode_access_token 验证签名和过期时间
        ↓
7. 验证通过 → 执行接口逻辑
   验证失败 → 返回 401，前端跳转到登录页
```

前端的 axios 拦截器（`frontend/src/api/client.js`）和 Pinia auth store（`frontend/src/stores/auth.js`）负责第 3、4、7 步。

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `passlib` | 第三方包 | 密码哈希，bcrypt 算法 |
| `python-jose` | 第三方包 | JWT 生成和解析 |
| `jwt.encode()` | `python-jose` | 生成 JWT 字符串 |
| `jwt.decode()` | `python-jose` | 解析并验证 JWT |
| `Depends(fn)` | `fastapi` | 执行接口前先执行 fn，把返回值注入为参数 |
| `OAuth2PasswordRequestForm` | `fastapi` | 处理登录表单 |
| `OAuth2PasswordBearer` | `fastapi` | 从请求头提取 Bearer token |
| `Depends(get_current_admin)` | `fastapi` | 保护路由，未登录直接 401 |

## 🔗 相关文件

- `backend/app/services/auth.py` — 密码和 JWT 工具函数
- `backend/app/routers/admin/auth.py` — 登录接口
- `backend/app/dependencies.py` — get_current_admin 依赖
- `frontend/src/api/client.js` — axios 拦截器，自动带 token
- `frontend/src/stores/auth.js` — 前端存储和管理 token

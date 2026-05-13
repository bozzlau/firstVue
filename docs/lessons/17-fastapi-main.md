# 17 · FastAPI 基础：main.py 与应用入口

## 💡 FastAPI 是什么，从哪来

`fastapi` 是一个**第三方 Python 包**，不是 Python 自带的。打开 `backend/requirements.txt` 能看到它。

作用：**让你用 Python 写 HTTP 接口**，类似前端世界的 Express（Node.js）。

---

## 🧩 main.py 逐行拆解

打开 `backend/app/main.py`。

### Python 的 import 语法

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
```

和 JavaScript 类似，但写法不同：

| JavaScript | Python |
|-----------|--------|
| `import { ref } from 'vue'` | `from fastapi import FastAPI` |
| `import axios from 'axios'` | `import fastapi` |

`from 包名 import 具体的东西` 是 Python 最常用的导入方式。

### 创建应用

```python
app = FastAPI(title="Personal Blog API", version="1.0.0")
```

和前端的 `createApp(App)` 类似，创建一个 FastAPI 应用实例。`title` 和 `version` 会显示在自动生成的 API 文档里（访问 `http://localhost:8001/docs`）。

### CORS 中间件

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:6006"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**CORS 是什么：** 浏览器安全限制，前端页面只能请求和自己同域名的接口。前端在 `localhost:6006`，后端在 `localhost:8001`，端口不同就算跨域，浏览器默认拦截。

CORS 中间件让后端告诉浏览器"我允许这些来源的请求"。`allow_origins` 就是白名单。

**中间件**的概念和前端 axios 拦截器类似——每个请求进来之前都经过它处理。

### 注册路由

```python
app.include_router(public_router)
app.include_router(admin_auth_router)
app.include_router(admin_posts_router)
```

后端把接口按功能拆成多个文件，每个文件定义一组路由，最后在 `main.py` 统一注册。和前端 Vue Router 的思路一样。

### 最简单的接口示例

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

`@app.get("/health")` 是**装饰器**——Python 特有语法，意思是"把下面这个函数注册为处理 GET /health 请求的函数"。

访问 `http://localhost:8001/health` 返回 `{"status": "ok"}`。

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `FastAPI` | `fastapi` 包 | Python Web 框架 |
| `app = FastAPI()` | — | 创建应用实例 |
| CORS 中间件 | `fastapi` 包 | 允许前端跨域请求 |
| `app.include_router` | — | 注册路由模块 |
| `@app.get("/path")` | — | 装饰器，注册路由处理函数 |

## 🔗 相关文件

- `backend/app/main.py` —— 应用入口

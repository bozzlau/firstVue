# 个人博客项目 · 学习笔记

跟着项目一起走的学习文档。按照「用户打开首页 → 文章列表渲染完成」这条完整链路展开，每一步拆出涉及的 JavaScript / Vue / 工程实践知识点。

## 学习路线

入口选择：**用户访问首页 → 文章列表出现在屏幕上**

```
浏览器打开首页
    ↓
Vue Router 匹配路由
    ↓
HomeView.vue 组件挂载
    ↓
onMounted 触发 load()
    ↓
api/posts.js 发请求
    ↓
axios → 后端 FastAPI
    ↓
数据返回前端
    ↓
ref 响应式触发重新渲染
    ↓
PostCard 循环渲染文章卡片
```

## 目录

- [01 学习入口与路线图](01-entry-and-roadmap.md)
- [02 Vue 3 响应式：ref](02-vue-ref.md)
- [03 ES 模块：import 语法](03-es-module-import.md)
- [04 生命周期钩子：onMounted](04-onmounted-lifecycle.md)
- [05 异步基础：async / await / try / finally](05-async-await.md)
- [06 Promise 是什么](06-promise.md)
- [07 .then() vs await：回调地狱的演化史](07-then-vs-await.md)
- [08 axios 和 HTTP 客户端基础](08-axios-basics.md)
- [09 axios 拦截器（上）—— 请求拦截器](09-axios-request-interceptor.md)
- [10 axios 拦截器（下）—— 响应拦截器](10-axios-response-interceptor.md)
- [11 Vue 模板语法：v-if / v-for / :key / :attr / @event](11-vue-template-directives.md)
- [12 组件通信：props](12-vue-props.md)
- [13 Vue Router：路由与导航](13-vue-router.md)
- [14 Pinia 状态管理](14-pinia-store.md)
- [15 script setup / computed / v-model](15-script-setup-computed-vmodel.md)
- [16 Tailwind CSS](16-tailwind-css.md)
- [17 FastAPI 基础：main.py 与应用入口](17-fastapi-main.md)
- [18 FastAPI 路由：参数、依赖注入、装饰器](18-fastapi-router.md)
- [19 SQLAlchemy 数据模型（ORM）](19-sqlalchemy-models.md)
- [20 Pydantic Schema：数据验证与序列化](20-pydantic-schema.md)
- [21 Service 层：SQLAlchemy 查询语法](21-service-layer.md)
- [22 JWT 认证：管理后台登录](22-jwt-auth.md)
- [23 配置与环境变量](23-config-env.md)
- [24 Alembic 数据库迁移](24-alembic-migrations.md)
- [25 pytest 测试](25-pytest.md)
- [26 完整链路串讲](26-full-request-flow.md)
- [27 管理后台链路串讲：登录与发文](27-admin-auth-flow.md)
- [28 Markdown 编辑与渲染](28-markdown.md)
- [29 Element Plus 与按需自动导入](29-element-plus.md)
- [30 JavaScript 常用语法：箭头函数 / 模板字符串 / 可选链 / 解构赋值](30-js-syntax.md)
- [31 懒加载：动态 import](31-lazy-loading.md)
- [32 Python 异常处理与 HTTPException](32-python-exceptions.md)
- [33 Python 类型注解](33-python-type-hints.md)

## 阅读方式

- 按顺序读，每一章都基于前一章的概念
- 每章末尾有小结表，快速回顾
- 代码示例都能在项目中找到对应文件

## 约定

- 🧩 = 代码片段
- 💡 = 概念解释
- ⚠️ = 容易踩坑的点
- 🎯 = 小结

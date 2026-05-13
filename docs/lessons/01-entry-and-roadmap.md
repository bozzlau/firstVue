# 01 · 学习入口与路线图

## 为什么选这条路线

一个 Web 项目的知识点散落在各处：响应式、路由、组件、HTTP、后端 API、数据库……如果按「先学 Vue 再学 FastAPI」这样分开学，会很抽象。

所以我们选一条**完整的真实链路**——用户访问首页、看到文章列表——沿着这条链路走，每一步涉及什么知识点就学什么。

## 完整链路

```
① 浏览器地址栏输入 http://localhost:6006
           ↓
② Vite 返回 index.html，加载 main.js
           ↓
③ main.js 初始化 Vue 应用，挂载到 #app
           ↓
④ Vue Router 匹配 "/" → HomeView.vue
           ↓
⑤ HomeView 组件创建，script setup 执行
           ↓
⑥ onMounted 注册的 load() 被调用
           ↓
⑦ load() 调用 api/posts.js 的 getPosts()
           ↓
⑧ axios 发出 HTTP GET 到 http://localhost:8001/api/posts
           ↓
⑨ FastAPI 路由匹配，调用 service 查数据库
           ↓
⑩ SQLAlchemy 执行 SQL，返回结果
           ↓
⑪ 后端把数据序列化为 JSON 响应
           ↓
⑫ axios 拿到响应，返回给 load()
           ↓
⑬ posts.value = data.items（响应式赋值）
           ↓
⑭ Vue 检测到 ref 变化，重新渲染模板
           ↓
⑮ v-for 循环渲染每个 PostCard 组件
           ↓
⑯ 浏览器看到文章列表
```

## 对应的知识点分布

| 步骤 | 知识点 |
|------|--------|
| ②③ | Vite 构建工具、入口文件 |
| ④ | Vue Router、SPA 路由原理 |
| ⑤ | Vue 组件、`<script setup>` |
| ⑥ | 生命周期钩子、异步函数 |
| ⑦⑧ | HTTP 请求、axios、Promise |
| ⑨⑩ | FastAPI 路由、依赖注入、ORM |
| ⑪ | Pydantic schema、JSON 序列化 |
| ⑬⑭ | Vue 响应式系统、`ref` |
| ⑮ | 指令 `v-for`、组件通信（props） |

## 当前进度

已经讲过：
- ✅ 第 ⑤⑬ 步涉及的 `ref` 响应式
- ✅ 第 ⑤ 步的 `import` 语法
- ✅ 第 ⑥ 步的 `onMounted` 和 `async/await`
- ✅ 第 ⑦⑧ 步的 Promise 基础

下一站：axios 和 HTTP 请求本身。

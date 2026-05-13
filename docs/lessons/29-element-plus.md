# 29 · Element Plus 与按需自动导入

## 💡 Element Plus 是什么

Element Plus 是一个 **Vue 3 UI 组件库**，提供现成的按钮、表单、表格、对话框等组件。管理后台里所有 `<el-*>` 开头的标签都来自它。

`element-plus` 是第三方 npm 包，在 `frontend/package.json` 里。

---

## 🧩 为什么 main.js 里没有 import ElementPlus

普通的组件库用法是在 `main.js` 里全局注册：

```javascript
// 普通用法（这个项目没有这样做）
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
app.use(ElementPlus)
```

这样会把 Element Plus 所有组件（几百个）全部打包进去，即使只用了其中 10 个。

这个项目用的是**按需自动导入**，打开 `frontend/vite.config.js`：

```javascript
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({ resolvers: [ElementPlusResolver()] }),
    Components({ resolvers: [ElementPlusResolver()] }),
  ],
})
```

这两个插件（`unplugin-auto-import`、`unplugin-vue-components`）是 Vite 插件，在构建时自动分析代码，只打包实际用到的组件。

---

## 🧩 两个插件分别做什么

**`Components` 插件** — 自动注册组件。

你在模板里写 `<el-button>`，不需要手动 `import { ElButton } from 'element-plus'`，插件在构建时自动加上这行导入。

**`AutoImport` 插件** — 自动导入 API 函数。

Element Plus 的一些功能（比如弹出消息提示 `ElMessage`）是函数调用，不是组件。这个插件让你直接用 `ElMessage.success('保存成功')`，不需要手动 import。

---

## 🧩 实际使用

在任何 `.vue` 文件里，直接用 `<el-*>` 组件，不需要 import：

```html
<!-- LoginView.vue -->
<el-card shadow="never">
  <el-form :model="form" @submit.prevent="handleLogin">
    <el-form-item label="用户名">
      <el-input v-model="form.username" />
    </el-form-item>
    <el-button type="primary" native-type="submit" :loading="loading">
      登录
    </el-button>
  </el-form>
</el-card>
```

构建时，插件检测到用了 `ElCard`、`ElForm`、`ElFormItem`、`ElInput`、`ElButton`，自动只打包这五个组件的代码和样式。

---

## ⚠️ 注意事项

`CLAUDE.md` 里特别注明：**不要在 `main.js` 里加 `import ElementPlus from 'element-plus'`**。

如果同时有全局注册和按需导入，组件会被重复加载，样式也可能冲突。这个项目只用按需自动导入，不用全局注册。

---

## 🧩 Vite 插件是什么

`vite.config.js` 里的 `plugins` 数组是 Vite 的插件系统。Vite 是这个项目的构建工具（第 3 课提到过 `npm run dev` 启动的就是 Vite）。

插件在**构建阶段**介入，可以转换代码、分析依赖、自动生成 import 语句。`unplugin-auto-import` 和 `unplugin-vue-components` 就是在构建时扫描代码，自动补上缺少的 import。

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `element-plus` | npm 包 | Vue 3 UI 组件库，`<el-*>` 组件 |
| `unplugin-vue-components` | npm 包 | 自动注册组件，不需要手动 import |
| `unplugin-auto-import` | npm 包 | 自动导入 API 函数 |
| `ElementPlusResolver` | `unplugin-vue-components` | 告诉插件去哪里找 Element Plus 的组件 |
| Vite 插件 | Vite | 构建阶段介入，转换和分析代码 |

## 🔗 相关文件

- `frontend/vite.config.js` — Vite 配置，插件注册
- `frontend/src/main.js` — 应用入口，注意没有全局注册 Element Plus

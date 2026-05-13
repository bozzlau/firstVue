# 16 · Tailwind CSS

## 💡 Tailwind 是什么，从哪来

`tailwindcss` 是一个**第三方 npm 包**，不是浏览器自带的，也不是 Vue 自带的。打开 `frontend/package.json`：

```json
"devDependencies": {
  "tailwindcss": "^3.x.x",
  "@tailwindcss/typography": "^0.5.x"
}
```

它在 `devDependencies`（开发依赖）里，只在开发和打包时用，不会打进最终代码里。

---

## 💡 Tailwind 的核心思想

传统 CSS 写法：自己起类名，然后写样式：

```css
.card {
  display: flex;
  align-items: center;
  padding: 16px;
  background-color: white;
}
```

```html
<div class="card">...</div>
```

**Tailwind 的思想完全不同**：它提供几百个**原子类**，每个类只做一件事，直接在 HTML 里组合：

```html
<div class="flex items-center p-4 bg-white">...</div>
```

- `flex` → `display: flex`
- `items-center` → `align-items: center`
- `p-4` → `padding: 16px`（4 × 4px）
- `bg-white` → `background-color: white`

不需要自己起类名，不需要写 CSS 文件，直接在 HTML 里堆类名。

---

## 🧩 项目里的实例

打开 `frontend/src/views/admin/LoginView.vue` 第 28 行：

```html
<div class="min-h-screen bg-gray-50 flex items-center justify-center">
```

| 类名 | 对应 CSS | 效果 |
|------|---------|------|
| `min-h-screen` | `min-height: 100vh` | 最小高度撑满整个屏幕 |
| `bg-gray-50` | `background-color: #f9fafb` | 浅灰色背景 |
| `flex` | `display: flex` | 开启 flex 布局 |
| `items-center` | `align-items: center` | 垂直居中 |
| `justify-center` | `justify-content: center` | 水平居中 |

---

## 🧩 常用类名规律

**间距（数字 × 4px）：**

```
p-4    → padding: 16px（四边）
px-4   → padding 左右
py-2   → padding 上下
mt-4   → margin-top: 16px
gap-4  → flex/grid 子元素间距 16px
```

**颜色（颜色名-深浅，50 最浅，900 最深）：**

```
bg-white        → 白色背景
bg-gray-50      → 极浅灰背景
bg-gray-800     → 深灰背景
text-gray-500   → 中灰文字
text-blue-600   → 蓝色文字
border-gray-200 → 浅灰边框
```

**尺寸：**

```
w-full   → width: 100%
w-64     → width: 256px（64 × 4px）
h-48     → height: 192px
max-w-sm → max-width: 384px
```

**文字：**

```
text-sm       → font-size: 14px
text-xl       → font-size: 20px
font-semibold → font-weight: 600
```

**圆角：**

```
rounded      → border-radius: 4px
rounded-lg   → border-radius: 8px
rounded-full → border-radius: 9999px（圆形）
```

---

## 💡 状态前缀

```html
<button class="hover:bg-gray-50 disabled:opacity-40">
```

- `hover:bg-gray-50` → 鼠标悬停时背景变浅灰
- `disabled:opacity-40` → 按钮禁用时透明度 40%

---

## 💡 响应式前缀

```
sm:   → 640px 以上生效
md:   → 768px 以上生效
lg:   → 1024px 以上生效
```

比如 `md:flex` 表示"768px 以上才用 flex 布局，小屏幕默认 block"。

---

## 💡 为什么公开页面用 Tailwind，管理后台用 Element Plus

| | Tailwind | Element Plus |
|--|---------|-------------|
| 提供什么 | 样式工具类 | 完整 UI 组件（表格、表单、弹窗...） |
| 灵活性 | 高，自定义设计 | 低，风格固定 |
| 开发效率 | 需要自己搭结构 | 开箱即用 |
| 适合场景 | 需要设计感的公开页面 | 不需要设计感的管理后台 |

---

## 🎯 小结

| 点 | 记住 |
|----|------|
| 来源 | npm 包，`devDependencies` |
| 核心思想 | 原子类，每个类只做一件事，HTML 里直接组合 |
| 间距规律 | 数字 × 4px，`p` 是 padding，`m` 是 margin |
| 颜色规律 | `颜色名-深浅`，50 最浅，900 最深 |
| 状态 | `hover:` `disabled:` `focus:` 缀 |
| 响应式 | `sm:` `md:` `lg:` 前缀 |

## 🔗 相关文件

- `frontend/tailwind.config.js` —— Tailwind 配置
- `frontend/src/views/admin/LoginView.vue` —— 典型 Tailwind 用法
- `frontend/src/components/public/PostCard.vue` —— 公开页面 Tailwind 用法

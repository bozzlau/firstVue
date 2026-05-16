import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import { useThemeStore } from './stores/theme'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

useThemeStore().init()

app.mount('#app')

import { defineStore } from 'pinia'
import { ref } from 'vue'

export const THEMES = [
  { key: 'amber-dark',   name: '琉珀控制台', mode: 'dark',  swatch: ['#ffb700', '#121214'] },
  { key: 'cyan-dark',    name: '电子终端',   mode: 'dark',  swatch: ['#22d3ee', '#0c1018'] },
  { key: 'magenta-dark', name: '赛博粉紫',   mode: 'dark',  swatch: ['#ec4899', '#120a18'] },
  { key: 'paper-light',  name: '牛皮蓝图',   mode: 'light', swatch: ['#b87900', '#f4eedf'] },
  { key: 'frost-light',  name: '极地霜白',   mode: 'light', swatch: ['#0d9488', '#eef2f7'] },
]

const VALID_KEYS = THEMES.map((t) => t.key)
const DEFAULT_KEY = 'amber-dark'

function readStored() {
  const v = localStorage.getItem('theme')
  return VALID_KEYS.includes(v) ? v : DEFAULT_KEY
}

export const useThemeStore = defineStore('theme', () => {
  const themes = THEMES
  const current = ref(readStored())

  function setTheme(key) {
    if (!VALID_KEYS.includes(key)) return
    current.value = key
    localStorage.setItem('theme', key)
    document.documentElement.dataset.theme = key
  }

  function init() {
    document.documentElement.dataset.theme = current.value
  }

  return { themes, current, setTheme, init }
})

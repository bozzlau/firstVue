/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        hud: {
          bg: 'rgb(var(--hud-bg) / <alpha-value>)',
          surface: 'rgb(var(--hud-surface) / <alpha-value>)',
          surfaceAlt: 'rgb(var(--hud-surface-alt) / <alpha-value>)',
          border: 'rgb(var(--hud-border) / <alpha-value>)',
          borderDim: 'rgb(var(--hud-border-dim) / <alpha-value>)',
          amber: 'rgb(var(--hud-amber) / <alpha-value>)',
          amberDim: 'rgb(var(--hud-amber-dim) / <alpha-value>)',
          amberSoft: 'rgb(var(--hud-amber-soft) / <alpha-value>)',
          warn: '#ff3344',
          text: 'rgb(var(--hud-text) / <alpha-value>)',
          textDim: 'rgb(var(--hud-text-dim) / <alpha-value>)',
          textMuted: 'rgb(var(--hud-text-muted) / <alpha-value>)',
        },
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', '"PingFang SC"', '"Hiragino Sans GB"', '"Microsoft YaHei"', 'sans-serif'],
      },
      animation: {
        'hud-pulse': 'hud-pulse 1.6s ease-in-out infinite',
        'hud-fade-up': 'hud-fade-up 0.4s ease-out both',
        'hud-blink': 'hud-blink 1s steps(2, start) infinite',
      },
      keyframes: {
        'hud-pulse': {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.4', transform: 'scale(1.4)' },
        },
        'hud-fade-up': {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'hud-blink': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}

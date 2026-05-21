/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        ed: {
          bg:      'rgb(var(--ed-bg) / <alpha-value>)',
          surface: 'rgb(var(--ed-surface) / <alpha-value>)',
          surface2:'rgb(var(--ed-surface2) / <alpha-value>)',
          border:  'rgb(var(--ed-border) / <alpha-value>)',
          fg:      'rgb(var(--ed-fg) / <alpha-value>)',
          muted:   'rgb(var(--ed-muted) / <alpha-value>)',
          accent:  'rgb(var(--ed-accent) / <alpha-value>)',
          accent2: 'rgb(var(--ed-accent2) / <alpha-value>)',
          accent3: 'rgb(var(--ed-accent3) / <alpha-value>)',
        },
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'Inter', 'system-ui', 'sans-serif'],
        serif: ['"Iowan Old Style"', 'Charter', 'Georgia', 'serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', '"PingFang SC"', '"Hiragino Sans GB"', '"Microsoft YaHei"', 'sans-serif'],
      },
      animation: {
        'blob-float': 'blob-float 8s ease-in-out infinite',
        'blob-morph': 'blob-morph 10s ease-in-out infinite',
        'fade-up': 'fade-up 0.5s ease-out both',
      },
      keyframes: {
        'blob-float': {
          '0%, 100%': { transform: 'translate(0, 0) scale(1)' },
          '33%': { transform: 'translate(20px, -20px) scale(1.05)' },
          '66%': { transform: 'translate(-15px, 10px) scale(0.97)' },
        },
        'blob-morph': {
          '0%, 100%': { borderRadius: '60% 40% 30% 70% / 60% 30% 70% 40%' },
          '50%': { borderRadius: '30% 60% 70% 40% / 50% 60% 30% 60%' },
        },
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}

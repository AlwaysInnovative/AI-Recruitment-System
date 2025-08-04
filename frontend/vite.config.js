import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import eslint from 'vite-plugin-eslint'
import svgr from 'vite-plugin-svgr'
import path from 'path'
import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'

export default defineConfig({
  plugins: [
    react({
      jsxImportSource: '@emotion/react',
      babel: {
        plugins: ['@emotion/babel-plugin']
      }
    }),
    eslint({
      cache: false,
      include: ['./src/**/*.ts', './src/**/*.tsx']
    }),
    svgr()
  ],
  css: {
    postcss: {
      plugins: [
        tailwindcss(),
        autoprefixer()
      ]
    },
    modules: {
      localsConvention: 'camelCase'
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@assets': path.resolve(__dirname, './src/assets')
    }
  },
  server: {
    port: 3000,
    open: true,
    host: true
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom'],
          vendor: ['lodash', 'zod', 'date-fns'],
          ui: [
            '@radix-ui/react-*', 
            'class-variance-authority',
            'clsx',
            'lucide-react'
          ]
        }
      }
    }
  },
  optimizeDeps: {
    include: [
      '@emotion/react', 
      '@emotion/styled',
      'tailwindcss',
      'autoprefixer'
    ]
  }
})

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react({
    jsxImportSource: '@emotion/react',
    babel: {
      plugins: ['@emotion/babel-plugin'],
    },
  })],
  resolve: {
    alias: [
      {
        find: '@',
        replacement: path.resolve(__dirname, 'src')
      },
      {
        find: '@components',
        replacement: path.resolve(__dirname, 'src/components')
      },
      {
        find: '@assets',
        replacement: path.resolve(__dirname, 'src/assets')
      }
    ]
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom'],
          vendor: ['lodash', 'date-fns'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
        },
      },
      external: [],
      onwarn(warning, warn) {
        if (warning.code === 'MODULE_LEVEL_DIRECTIVE') return;
        if (warning.code === 'UNUSED_EXTERNAL_IMPORT') return;
        warn(warning);
      }
    }
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'https://0vhlizckd7jk.manussite.space',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      '@radix-ui/react-dialog',
      '@radix-ui/react-dropdown-menu'
    ],
    exclude: ['js-big-decimal']
  }
});

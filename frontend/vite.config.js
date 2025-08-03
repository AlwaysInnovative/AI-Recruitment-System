import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import eslint from 'vite-plugin-eslint';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [
    react({
      jsxImportSource: '@emotion/react',
      babel: {
        plugins: ['@emotion/babel-plugin'],
      },
    }),
    eslint()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'lodash': path.resolve(__dirname, 'node_modules/lodash'),
    }
  },
  build: {
    commonjsOptions: {
      include: [/lodash/, /node_modules/]
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        manualChunks: {
          lodash: ['lodash'],
          radix: [/@radix-ui/],
          vendor: ['react', 'react-dom', 'react-router-dom']
        }
      }
    }
  },
  optimizeDeps: {
    include: ['lodash']
  }
});

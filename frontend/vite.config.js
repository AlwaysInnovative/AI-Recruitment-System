import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // Use '@' to alias the 'src' directory
    },
  },
  build: {
    outDir: 'dist', // Output directory for the build files
  },
});

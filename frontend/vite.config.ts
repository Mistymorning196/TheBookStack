import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  base: mode === 'development' ? '/' : '/', // You can leave this as '/' unless you need a different base for production
  build: {
    emptyOutDir: true,
    outDir: 'dist', // This will be the output folder where Vite builds the app (you move files from here later)
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
}));


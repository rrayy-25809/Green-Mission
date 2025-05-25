import { defineConfig } from 'vite';
import { resolve } from 'path';
import { readdirSync } from 'fs';

const pagesDir = resolve(__dirname, 'client');
const htmlFiles = readdirSync(pagesDir).filter(file => file.endsWith('.html'));

const input = htmlFiles.reduce((acc, file) => {
  const name = file.replace('.html', '');
  acc[name] = resolve(pagesDir, file);
  return acc;
}, {});

export default defineConfig({
  build: {
    rollupOptions: {
      input
    }
  }
});
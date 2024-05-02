import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { templateCompilerOptions } from '@tresjs/core'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue({...templateCompilerOptions})],
  resolve:{
    alias:{
      '@': resolve(__dirname,'./src')
    }
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    open: true
  }
})

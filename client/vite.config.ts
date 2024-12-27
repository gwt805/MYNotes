const os = require("os")
import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { webUpdateNotice } from "@plugin-web-update-notification/vite"

function getNetWorkIp() {
  let needHost = ""
  try {
    let network = os.networkInterfaces()
    for (const dev in network) {
      let iface = network[dev]
      for (let i = 0; i < iface.length; i++) {
        const alias = iface[i]
        if (alias.family === "IPv4" && alias.address !== "127.0.0.1" && !alias.internal && alias.address.indexOf("172") == "-1" && !alias.internal && alias.address.indexOf("220") == "-1") {
          needHost = alias.address
        }
      }
    }
  } catch (error) {
    needHost = "localhost"
  }
  return needHost
}
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    webUpdateNotice({
      versionType: "build_timestamp",
      logVersion: true,
      locale: "zh_CN",
      notificationProps: {
        title: '📢 系统更新',
        description: '系统更新啦, 请刷新页面',
        buttonText: '刷新',
        dismissButtonText: '忽略'
      },
    }),
  ],
  resolve:{
    alias:{
      '@': resolve(__dirname,'src/'),
      'components': resolve(__dirname,'src/components/'),
      'utils': resolve(__dirname,'src/utils/'),
      'api': resolve(__dirname,'src/api/'),
    }
  },
  build: {
    outDir: 'dist'
  },
  server: {
    port: 5173,
    open: true,
    host: '0.0.0.0'
  },
  define: {
    'import.meta.env.BASE_IP': JSON.stringify(getNetWorkIp())
  }
})
import './style.css'
import App from './App.vue'
import Tres from '@tresjs/core'
import { createApp } from 'vue'
import router from "@/routes/index"
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/dark/css-vars.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(ElementPlus, { locale: zhCn })
app.use(router)
app.use(Tres)
app.mount('#app')

// https://aieditor.dev/zh/config/base.html
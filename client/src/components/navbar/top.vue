<template>
    <el-dialog v-model="selfinfomodel" title="个人信息" center :close-on-click-modal="true" :close-on-press-escape="true" append-to="html" style="width: 500px;">
        <el-form label-position="left" label-width="80px" style="max-width: 550px">
            <div class="avatar-div">
                <el-image class="tx" :src="avatar_url" :zoom-rate="1.2" :preview-src-list="[avatar_url]" :max-scale="7" :min-scale="0.2" :initial-index="4" fit="cover" draggable="false"/>
            </div>
            <el-form-item label="用户ID">
                <el-input v-model="user_id" disabled />
            </el-form-item>
            <el-form-item label="用户名">
                <el-input v-model="name" disabled />
            </el-form-item>
            <el-form-item label="邮箱">
                <el-input v-model="email" disabled />
            </el-form-item>
        </el-form>
    </el-dialog>
    <el-menu class="el-menu-demo top" mode="horizontal" :ellipsis="false">
        <img src="/icon.svg" alt="icon" @click="$router.push('/index')">
        <div class="flex-grow" />
        <div class="div-theme">
            <el-button circle @click="toggleDark()" v-if="isDark"><el-icon :size="4 * 4"> <Cloudy /> </el-icon></el-button>
            <el-button circle @click="toggleDark()" v-if="isDark == false"><el-icon :size="4 * 4"> <Sunny /> </el-icon></el-button>
        </div>
        <el-sub-menu index="2" class="slc">
            <template #title><el-avatar class="avatar" size="small" :src="avatar_url" />{{ name }}</template>
            <el-menu-item class="slc" @click="$router.push('/index/article/create')">新增文章</el-menu-item>
            <el-menu-item class="slc" @click="selfinfomodel=true">个人信息</el-menu-item>
            <el-menu-item class="slc" @click="loginout">退出登录</el-menu-item>
        </el-sub-menu>
    </el-menu>
</template>

<script setup lang="ts">
import { useDark } from '@vueuse/core';
import { useToggle } from '@vueuse/shared';
import { miss_token } from '@/utils/session';
import { ref, onMounted, onUnmounted } from "vue";
import { Sunny, Cloudy } from '@element-plus/icons-vue';
import { getSession, clearSession, is_expire, nullSession } from "@/utils/session";
import { ElMessageBox } from 'element-plus'
const isDark = ref(useDark({ storageKey: 'vitepress-theme-appearance' }))
const toggleDark = ref(useToggle(isDark))
const {user_id, name, avatar_url, email} = getSession()
const selfinfomodel = ref(false)
const cron_setintvel = ref()
const cron_token = ref()

const loginout = () => {
    clearSession()
    window.location.href = "/login"
}

const open_token_warning_tooltip = () => {
  ElMessageBox.confirm(
    '如果您正在编辑, 请及时保存; 后面还需要提示嘛?',
    'Token 即将失效',
    {
      confirmButtonText: '提示',
      cancelButtonText: '不提示',
      type: 'warning',
    }
  ).then(() => {}).catch(() => {clearInterval(cron_token.value)})
}

onMounted(()=> {
    cron_token.value = setInterval(()=> {
        if (miss_token()) {
            open_token_warning_tooltip()
        }
    })
    cron_setintvel.value = setInterval(()=> {
        if (nullSession() || is_expire()) {
            loginout()
        }
    }, 1000)
   
})

onUnmounted(()=> {
    clearInterval(cron_setintvel.value)
})
</script>

<style scoped lang="less">
.el-menu {
    width: 100%;
    position: absolute;
    left: 0;
}
.div-theme {
    margin: auto;
}
.avatar {
    margin-right: 10px;
}

.avatar-div {
    height: 100px;
    margin-bottom: 20px;
}

.avatar-div .tx {
    width: 100px;
    height: 100px;
    margin: auto;
    display: block;
    border-radius: 50%;
}

p {
    text-align: center;
    margin-left: 20px;
    line-height: 30px;
}

p:first-child {
    margin-top: -20px;
}

p:last-child {
    text-align: center;
    margin: 20px 0 -30px 0;
}

.flex-grow {
    flex-grow: 1;
}

img {
    margin-top: 5px;
    padding-bottom: 5px;
    -webkit-user-drag: none;
    user-select: none;
}

.slc img::before {
    background-color: transparent;
}

.slc {
    user-select: none !important;
}

.perrmsg {
    color: red;
    margin-bottom: 10px;
}

.btn-updpwd {
    width: 100%;
}
</style>
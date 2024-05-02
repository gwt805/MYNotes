<template>
    <div class="login-box" id="demo" v-loading="loading" element-loading-text="正在登录请稍后...">
    <div class="input-content">
      <div class="login_tit">
        <div>
          <i class="tit-bg left"></i>
          Everyday · 在线笔记
          <i class="tit-bg right"></i>
        </div>
        <p>Notes&nbsp;&nbsp;&nbsp;&nbsp;Everyday</p>
      </div>
      <p class="p user_icon">
        <input type="text" placeholder="用户名/邮箱" autocomplete="off" class="login_txtbx" id="user" v-model="userform.username">
      </p>
      <p class="p pwd_icon">
        <input type="password" placeholder="密码" autocomplete="off" class="login_txtbx" id="pwd" v-model="userform.password">
      </p>
      <div class="signup">
        <a class="gv" href="https://gitee.com/" target="_blank">注&nbsp;&nbsp;册</a>
        <a class="gv" @click="loginbt()">登&nbsp;&nbsp;录</a>
      </div>
    </div>
    <div class="canvaszz"> </div>
    <canvas id="canvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { login } from "@/api/auth";
import '@/assets/js/login_canvas.js';
import { useRouter } from "vue-router";
import { is_expire } from "@/utils/session";
import { setSession } from "@/utils/session/index";
import { public_elmsg_warning, public_elmsg_success } from "@/utils/elmsg";

document.title = "登录"

const loading = ref(false);
const router = useRouter();
const userform = ref({ "username": "", "password": "" })

const loginbt = () => {
  login(userform.value.username.trim(), userform.value.password.trim()).then((res:any) => {
      if (res.code == 0) {
        setSession(res.data.access_token, res.data.refresh_token, res.data.expires_in, res.data.created_at, res.data.user_id, res.data.name, res.data.avatar_url,res.data.email)
        public_elmsg_success(res.msg)
          setTimeout(() => {
              if (router.currentRoute.value.query.redirect) {
                  const redirect: any = router.currentRoute.value.query.redirect;
                  window.location.href = redirect;
              }
              else {
                window.location.href = "/index";
              }
          }, 2000);
      }
      else {
        public_elmsg_warning(res.data)
      }
  })
}

if (!is_expire()) { router.push({name: "index"}); }
</script>

<style scoped>
@import url('@/assets/css/login.css');
</style>
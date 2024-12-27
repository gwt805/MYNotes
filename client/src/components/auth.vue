<template>
    <div class="login-box" id="demo" v-loading="loading" element-loading-text="正在登录请稍后...">
        <div class="input-content">
        <div class="login_tit">
            <div><i class="tit-bg left"></i>Everyday · 博客系统<i class="tit-bg right"></i></div>
            <p>Notes&nbsp;&nbsp;&nbsp;&nbsp;Everyday</p>
        </div>
        <p class="p user_icon">
            <input type="text" placeholder="用户名" autocomplete="off" class="login_txtbx" v-model="loginform.username">
        </p>
        <p class="p pwd_icon">
            <input type="password" placeholder="密码" autocomplete="off" class="login_txtbx" v-model="loginform.password">
        </p>
        <p class="p pwd_icon" v-if="is_resiter">
            <input type="password" placeholder="确认密码" autocomplete="off" class="login_txtbx" v-model="loginform.password1">
        </p>
        <div class="signup">
            <a class="gv" @click="is_resiter=false" v-if="is_resiter">返&nbsp;&nbsp;回</a>
            <a class="gv" @click="registerfn()" v-if="is_resiter">提&nbsp;&nbsp;交</a>
            <a class="gv" @click="is_resiter=true" v-if="!is_resiter">注&nbsp;&nbsp;册</a>
            <a class="gv" @click="loginfn()" v-if="!is_resiter">登&nbsp;&nbsp;录</a>
        </div>
        </div>
        <div class="canvaszz"> </div>
        <canvas id="canvas"></canvas>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import '@/assets/js/login_canvas.js';
import { login, register } from '@/api/auth';
import router from "@/routes/index";
import { public_elmsg_success, public_elmsg_warning } from "@/utils/elmsg/index";

document.title = "登录";

const is_resiter = ref(false);
const loginform = ref({'username': '', 'password': '', 'password1': ''});
const loading = ref(false);

watch(is_resiter, () => {loginform.value = {'username': '', 'password': '', 'password1': ''};});

const registerfn = () => {
    if (loginform.value.username.trim() == "") {
        public_elmsg_warning("用户名不能为空");
        return;
    }
    if (loginform.value.password != loginform.value.password1) {
        public_elmsg_warning("两次密码不一致");
        return;
    }
    if (loginform.value.password.trim() == "") {
        public_elmsg_warning("密码不能为空");
        return;
    }
    loading.value = true;
    register(loginform.value.username.trim(), loginform.value.password.trim()).then((res) => {
        loading.value = false;
        if (res.code == 0) {
            public_elmsg_success("注册成功,请登录");
            is_resiter.value = false;
        }else public_elmsg_warning(res.msg);
    })
}
const loginfn = () => {
    loading.value = true;
    if (loginform.value.username.trim() == "") {
        public_elmsg_warning("用户名不能为空");
        return;
    }
    if (loginform.value.password.trim() == "") {
        public_elmsg_warning("密码不能为空");
        return;
    }
    login(loginform.value.username.trim(), loginform.value.password.trim()).then((res: any) => {
        loading.value = false;
        if (res.code == 0) {
            window.localStorage.setItem("userinfo", JSON.stringify(res.data));
            public_elmsg_success("登录成功");
            setTimeout(() => {
                if (router.currentRoute.value.query.redirect) {
                    const redirect: any = router.currentRoute.value.query.redirect;
                    window.location.href = redirect;
                }
                else {
                    window.location.href = "/index";
                }
            }, 2000);
        } else public_elmsg_warning(res.msg);
    })
};

if (localStorage.getItem("userinfo") != null ) window.location.href = "/index";
</script>

<style scoped>
    @import url('@/assets/css/login.css');
</style>

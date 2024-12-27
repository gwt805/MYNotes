import axios from 'axios';
import { userinfo } from '@/utils/session/index'
import router from "@/routes/index";
import { API_BASE_URL } from "@/utils/config/index";
import { public_elmsg_warning } from "@/utils/elmsg/index";

// 存储发送但未响应的请求
const set = new Set();

// 生成唯一key的方法
function generateUniqueKey(config: any, hash: any) {
    const { method, url, params, data } = config;
    return [method, url, JSON.stringify(params), JSON.stringify(data), hash].join('&');
}

// 创建 axios 实例
const http = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        Authorization: userinfo()?.token ? userinfo()?.token : ""
    },
});

// 添加请求拦截器
http.interceptors.request.use(
    (config: any) => {
        const hash = location.hash;
        const reqKey = generateUniqueKey(config, hash);

        // 如果请求重复，直接拒绝本次请求
        if (set.has(reqKey)) {
            return Promise.reject('Duplicate request');
        } else {
            // 保存请求的唯一标识符
            config.pendKey = reqKey;
            set.add(reqKey); // 将请求的唯一标识符加入 set
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器
http.interceptors.response.use(
    (res: any) => {
        // 请求成功后移除标识符
        set.delete(res.config.pendKey);
        if (res.data.code === -2) {
            window.localStorage.clear();
            window.location.href = `/login?redirect=${router.currentRoute.value.fullPath}`;
        } else {
            return res.data; // 返回接口返回的数据
        }
    },
    (error) => {
        // 如果请求失败，确保从 set 中移除
        if (error.config && error.config.pendKey) {
            set.delete(error.config.pendKey);
            console.log(error);
            if (JSON.parse(error.request.response)?.code == -2) {
                window.localStorage.clear();
                window.location.href = `/login?redirect=${router.currentRoute.value.fullPath}`;
            }
        }
        if (error !== "Duplicate request") {
            // 显示错误信息，或者其他处理
            public_elmsg_warning("请求错误 , 请检查网络/服务状态 !")
        }
        return Promise.reject(error);
    }
);

export default http;

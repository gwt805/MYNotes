import axios from 'axios'
import router from "@/routes/index";

const http = axios.create({
    baseURL: "http://192.168.3.3:8080",
    headers: {
        AUTHORIZATION: window.localStorage.getItem("access_token"),
    }
})

http.interceptors.response.use(
    (res) => {
        if (res.data.code == -2) {
            window.localStorage.clear();
            window.location.href = `/login?redirect=${router.currentRoute.value.fullPath}`;
        }
        else {
            return res.data;
        }
    },
    (error) => {
        return Promise.reject(error);
    }
);

const whttp = axios.create()
whttp.interceptors.response.use(
    (res) => {
        return res.data;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default http; whttp
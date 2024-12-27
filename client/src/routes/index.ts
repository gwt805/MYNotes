import { type RouteRecordRaw, createRouter, createWebHistory } from 'vue-router';
import auth from '@/components/auth.vue'
import index from '@/components/index.vue'
import edsh from '@/components/blog/edsh.vue'
import empy from '@/components/empty.vue'
import create from '@/components/blog/creat.vue'
// import { public_elmsg_warning } from '@/utils/elmsg/index';

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'login',
        component: auth
    },
    {
        path: '/index',
        name: 'index',
        component: index,
    },
    {
        path: '/page/create',
        name: 'blog-create',
        component: create
    },
    {
        path: '/page/:type/:id',
        name: 'page-update-show',
        component: edsh
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: empy },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// router.beforeEach((to, from, next) => {
//     const userRole = window.localStorage.getItem('is_superuser');
//     if (to.meta.roles) {
//         if (to.meta.roles == userRole) { next(); }
//         else {
//             public_elmsg_warning('您没有权限访问该页面 !');
//             // next({name: 'index'});
//             location.href = '/index';
//         }
//     }
//     else { next(); }
// });

export default router;
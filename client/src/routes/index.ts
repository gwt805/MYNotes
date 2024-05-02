import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";
import empty from "@/components/empty/empty.vue";
import login from "@/components/auth/login.vue"
import article_create from "@/components/article/create.vue"
import article_show from "@/components/article/show.vue"
import article_index from "@/components/index.vue"
import article_desc from "@/components/article/decription.vue"
import article_update from "@/components/article/update.vue"

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "login",
    component: login
  },
  {
    path: "/index",
    component: article_index,
    children: [
      {
        path: "",
        name: "index",
        component: article_show
      },
	  {
		  path: "article/:id",
		  name: "article_show",
		  component: article_desc
	  },
      {
        path: "article/create",
        name: "article-create",
        component: article_create
      },
	  {
		  path: "article/update/:id",
		  name: "article_update",
		  component: article_update
	  }
    ]
  },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: empty },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
<template>
    <div class="container">
        <div class="nav">
            <div class="nav-left"><img src="../assets/logo.svg" alt="Logo" srcset="" draggable="false"></div>
            <div class="nav-right">
                <el-input v-model="search_input" placeholder="在此搜索" class="input-with-select" @change="get_data">
                    <template #append><el-button :icon="Search" /></template>
                </el-input>
                <el-tooltip content="写文章" :hide-after="0"><el-icon :size="30" color="gray" @click="goto('create', 0)"><EditPen /></el-icon></el-tooltip>
                <el-avatar size="default" :src="userinfo().avatar" @click="ismodel = true" :with-header="false" append-to-body />
            </div>
        </div>
        <div class="blog">
            <div class="blog-item" v-for="item in pageData">
                <div class="blog-title"><h3 @click="goto('show', 1)">{{ item.title }}</h3></div>
                <div class="blog-content"><p>{{ item.content }}</p></div>
                <div class="blog-footer">
                    posted @ {{ item.created_at }}  updated @ {{ item.updated_at }}
                    <el-button type="primary" text @click="goto('edit', 1)">编辑</el-button>
                    <el-button type="danger" text @click="deletefn(item.id)">删除</el-button>
                </div>
            </div>
        </div>
        <div class="pagenum">
            <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :background="false" layout="total, prev, pager, next, jumper" :total="count" @size-change="handleSizeChange" @current-change="handleCurrentChange"/>
        </div>
        <el-drawer v-model="ismodel" size="100vw">
            <h2>个人信息</h2>
            <div class="div-avatar"><el-image style="width: 100px; height: 100px" :src="form.avatar" :preview-src-list="[form.avatar]" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2"></el-image></div>
            <el-form :model="form" label-width="auto">
                <el-form-item label="ID">
                    <el-input v-model="form.id" disabled />
                </el-form-item>
                <el-form-item label="用户名">
                    <el-input v-model="form.username" disabled />
                </el-form-item>
                <el-form-item label="头像">
                    <el-input v-model="form.avatar" />
                </el-form-item>
                <el-form-item label="创建时间">
                    <el-input v-model="form.created_at" disabled />
                </el-form-item>
                <el-form-item label="更新时间">
                    <el-input v-model="form.updated_at" disabled />
                </el-form-item>
            </el-form>
            <el-button type="primary" @click="closemodelfn">确定</el-button>
        </el-drawer>
    </div>
</template>

<script setup lang="ts">
import { updateuserimg } from '@/api/auth';
import { ElMessageBox } from 'element-plus';
import { ref, type Ref, nextTick } from 'vue';
import { Search } from '@element-plus/icons-vue';
import { get_blog_all, deleteblog } from '@/api/blog';
import { userinfo, setuseravatar } from '@/utils/session';
import { public_elmsg_success, public_elmsg_error } from '@/utils/elmsg';

const ismodel = ref(false);
const form = ref(userinfo())
const search_input = ref("");
const currentPage = ref(1);
const pageSize = ref(5);
const count: Ref<number|any> = ref(0);
const pageData:Ref<Map<string, string>|any> = ref([]);

const handleSizeChange = (val: number) => {
    pageSize.value = val;
    get_data();
};
const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    get_data();
}

const get_data = async () => {
    get_blog_all(currentPage.value, pageSize.value, search_input.value.trim()).then((res)=>{
        if (res.code == 0) {
            count.value = res.data?.count
            pageData.value = res.data?.data
        }else public_elmsg_error(res.msg)
    })
}

const goto = (path: string, id: number) => {
    if (path == "show") window.location.href = `/page/show/${id}`;
    else if (path == "edit") window.location.href = `/page/edit/${id}`;
    else if (path == "create") window.location.href = `/page/create`;
}
const deletefn = (id: number) => {
    ElMessageBox.confirm('Are you sure you want to close this?')
    .then(() => {
        deleteblog(id).then((res)=> {
            if (res.code == 0) {
                public_elmsg_success(res.msg);
                get_data();
            }else public_elmsg_error(res.msg)
        })
    })
}
nextTick(() => {get_data();})
const closemodelfn = () => {
    updateuserimg(form.value.id, form.value.avatar).then((res)=>{
        if (res.code == 0) {
            ismodel.value = false;
            setuseravatar(form.value.avatar);
        }else {
            public_elmsg_error(res.msg);
            ismodel.value = false;
        }
    })
}
</script>

<style scoped lang="less">
.container {
    height: 100%;
    width: 100%;
    .nav {
        height: 40px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        .nav-left {
            width: 90%;
            margin: auto 0;
            padding-left: 50px;
        }
        .nav-right {
            // width: 90%;
            display: flex;
            align-items: center;
            padding-right: 50px;
            .el-input {
                min-width: 150px;
            }
            .el-icon {
                padding: 0 10px;
            }
            .el-icon:hover {
                color: #41ABF1;
            }
        }
    }
    .blog {
        height: calc(100% - 40px);
        width: 100%;
        margin-top: 10px;
        .blog-item {
            height: auto;
            width: 90%;
            margin: 0 auto;
            border-bottom: 1px dashed gray;
            .blog-title {
                height: auto;
                line-height: 40px;
                width: 100%;
                opacity: 0.8;
                h3:hover {
                    color: #41ABF1;
                }
            }
            .blog-content {
                height: auto;
                max-height: 100px;
                width: 100%;
                overflow: hidden;
                line-height: 2rem;
                opacity: 0.7;
            }
            .blog-footer {
                height: auto;
                width: 100%;
                line-height: 35px;
                opacity: 0.4;
                .el-button:hover {
                    font-size: large;
                }
            }
        }
    }
    .pagenum {
        height: auto;
        width: 90%;
        margin: 10px auto 0 auto;
    }
    .el-drawer {
        h2 {
            text-align: center;
        }
        .div-avatar {
            width: 100px;
            height: 100px;
            margin: auto;
            margin-top: 20px;
        }
        .el-form {
            margin-top: 20px;
        }
        .el-button {
            width: 100%;
        }
    }
}
</style>
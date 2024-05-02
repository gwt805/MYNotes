<template>
    <div class="common-layout">
        <el-container>
            <el-header><top /></el-header>
            <el-main><router-view></router-view></el-main>
            <el-footer><span><b>Copyright © gwt805 2024.04</b></span></el-footer>
        </el-container>
    </div>
</template>

<script setup lang="ts">
import top from "@/components/navbar/top.vue"
document.title = "首页"
</script>

<style scoped lang="less">
.common-layout {
    .el-container {
        .el-header {
            width: 100%;
            height: 60px;
            position: fixed;
            top: 0;
        }
        .el-footer {
            width: 100%;
            height: 20px;
            position: fixed;
            bottom: 0;
            text-align: center;
            line-height: 20px;
            user-select: none;
        }
    }
}
</style>
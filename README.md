<div align="center">
    <a href="https://cn.vuejs.org/"><img src="./Demo/vue.svg" width="50px"></a>
    <a href="https://robyn.tech/"><img src="./Demo/robyn.png" style="margin: 0 20px 0 20px;"></a>
    <a href="https://www.wangeditor.com/" style="margin: 0 8px 0 20px;"><img src="./Demo/wangEditor.png" width="50px"></a>
    <a href="https://min.io/open-source/download"><img src="./Demo/minio.svg" width="50px" style="margin: 0 0 0 0;"></a>
    <a href="https://www.mysql.com/"><img src="./Demo/Mysql.svg" width="50px" style="margin: 0 8px 0 20px;"></a>
</div>

### 简介
本项目是一个简单的本地博客系统，前端使用Vue.js，后端使用 Robyn，数据库使用 MySQL，存储使用 MinIO，编辑器使用 wangEditor5， 虽然页面不是很好看，但是够用，哈哈哈

### 功能
- 用户注册、登录
- 文章发布、编辑、删除、预览、搜索

### 部署
    > docker-compose up -d

    > 访问 http://localhost:9000 创建一个名为 blog 的 bucket, 并将该 bucket 的 Access Policy 设置为 public
    
    > 访问 http://localhost:5173 开启笔记之旅

### Demo
|                     首页                 |                     编辑                  |                     预览                 |
|:---------------------------------------- |:-----------------------------------------|:-----------------------------------------|
|<img src="./Demo/index.jpg" width="200px">|<img src="./Demo/edit.jpg" width="200px">|<img src="./Demo/preview.jpg" width="200px">|

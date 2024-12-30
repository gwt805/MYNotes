<template>
    <div class="content">
        <div class="title">
            <el-input type="text" placeholder="请输入标题" v-model="title"/>
            <el-button round size="small" style="width: 10vw;" @click="submit">保存</el-button>
        </div>
        <div class="div-editor">
            <Toolbar id="toolbar" :editor="editorRef" :defaultConfig="defaultConfig" :mode="mode" />
            <Editor id="editor" v-model="content" :defaultConfig="editorConfig" :mode="mode" @onCreated="handleCreated" :style="editorStyle" />
        </div>
    </div>
</template>

<script setup lang="ts">
import "@/assets/js/spidercanvas.js";
import { createblog } from "@/api/blog";
import "@wangeditor/editor/dist/css/style.css";
import { userinfo } from '@/utils/session/index'
import { API_BASE_URL } from '@/utils/config/index'
import { Boot } from '@wangeditor/editor'
import linkCardModule from '@wangeditor/plugin-link-card'
import markdownModule from '@wangeditor/plugin-md'
import attachmentModule from '@wangeditor/plugin-upload-attachment'
import { type IEditorConfig } from '@wangeditor/editor'
import { Editor, Toolbar } from "@wangeditor/editor-for-vue";
import formulaModule from '@wangeditor/plugin-formula'
import { ref, type Ref, reactive, shallowRef, onBeforeUnmount, onBeforeMount} from 'vue'
import { public_elmsg_error, public_elmsg_success, public_elmsg_warning } from "@/utils/elmsg";
import router from "@/routes";


const title:Ref<string|any> = ref('')
const content:Ref<string|any> = ref('');

const editorStyle = reactive({height: '300px'})
const mode = "default"
const defaultConfig = {
    insertKeys: {
        index: 0, // 自定义插入的位置
        keys: ['uploadAttachment', 'insertFormula'], // “上传附件”菜单
    }
}
const editorRef = shallowRef() // 编辑器实例，必须用 shallowRef
const edit_image_list:Ref<Set<string>> = ref(new Set()) 
const edit_video_list:Ref<Set<string>> = ref(new Set())

// 编辑器配置
const editorConfig: Partial<IEditorConfig> = {
    placeholder: '请输入内容...',
    readOnly: false,
    hoverbarKeys: {
        attachment: {
            menuKeys: ['downloadAttachment'], // “下载附件”菜单
        },
        formula: {
            menuKeys: ['editFormula'], // “编辑公式”菜单
        },
    },
    MENU_CONF: {
        viewLink: {
            getLinkCardData(linkUrl: string) {
                console.log(`获取链接卡片数据: ${linkUrl}`)
            }
        },
        uploadImage: {
            server: `${API_BASE_URL}/api/file/uploadimg`, // 上传接口 URL
            fieldName: "file", // 图片字段名称
            withCredentials: true,
            allowedFileTypes: ['image/*'],
            headers: {
                Authorization: userinfo().token
            },
            onSuccess(file: File, res: any) {
                console.log(`${file.name} 上传成功`, res)
            }
        },
        insertImage: {
            onInsertedImage(imageNode){
                if (imageNode == null) return
                const { src, alt, url, href} = imageNode
                edit_image_list.value.add(src)
                console.log(`插入图片`, src, alt, url, href)
            }
        },
        editImage: {
            onUpdatedImage(imageNode){
                if (imageNode == null) return
                const { src, alt, url, href} = imageNode
                console.log(`更新图片`, src, alt, url, href)
            }
        },
        uploadVideo: {
            server: `${API_BASE_URL}/api/file/uploadfile`, // 上传接口 URL
            fieldName: "file", // 视频字段名称
            withCredentials: true,
            allowedFileTypes: ['video/*'],
            headers: {
                Authorization: userinfo().token
            },
            onSuccess(file: File, res: any) {
                console.log(`${file.name} 上传成功`, res);
                const { url } = res.data || {}
                edit_video_list.value.add(url.split("/")[JSON.parse(res.data).url.split("/").length - 1]);
            },
            customInsert(res: any, insertFn: any) {
                const { url } = res.data || {}
                insertFn(url, "")
            }
        },
        uploadAttachment: {
            server: `${API_BASE_URL}/api/file/uploadfile`,
            fieldName: "file",
            withCredentials: true,
            allowedFileTypes: ['*'],
            maxFileSize: 500 * 1024 * 1024, // 10M
            headers: {
                Authorization: userinfo().token
            },
            onSuccess(file: File, res: any) {
                public_elmsg_success(`${file.name} 上传成功`)
                console.log(`${file.name} 上传成功`, file, res);
            },
            onFailed(file: File, res: any) {
                public_elmsg_error(res.message)
                console.log('onFailed', file, res)
            },
            onError(file: File, err: Error, res: any) {
                public_elmsg_error(err.message)
                console.error('onError', file, err, res)
            },
            customInsert(res: any, file: File, insertFn: Function) {
                console.log('customInsert', res)
                const { url } = res.data || {}
                if (!url) throw new Error(`url is empty`)
                insertFn(`customInsert-${file.name}`, url)
            },
        }
    }
}

onBeforeMount(()=> {
    Boot.registerModule(linkCardModule)
    Boot.registerModule(attachmentModule)
    Boot.registerModule(markdownModule)
    Boot.registerModule(formulaModule)
})

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
    const editor = editorRef.value
    if (editor == null) return
    editor.destroy()
})

const handleCreated = (editor) => {editorRef.value = editor}
const submit = () => {
    createblog(title.value.trim(), content.value).then((res)=>{
        if (res.code == 0) {
            public_elmsg_success(res.msg);
            router.push("/index")
        } else public_elmsg_warning(res.msg)
    })
}

window.addEventListener('load', () => {
    const toolbar:any = document.getElementById("toolbar")
    const windowHeight = window.innerHeight;
    const toolbarHeight = toolbar.offsetHeight;
    const newEditorHeight = windowHeight - toolbarHeight - 36;
    editorStyle.height = `${newEditorHeight}px`;
})
window.addEventListener('resize', () => {
    const toolbar:any = document.getElementById("toolbar")
    const windowHeight = window.innerHeight;
    const toolbarHeight = toolbar.offsetHeight;
    const newEditorHeight = windowHeight - toolbarHeight - 36;
    editorStyle.height = `${newEditorHeight}px`;
});
</script>

<style scoped lang='less'>
.content {
    width: calc(100% - 1px);
    height: 100%;
    background-color: transparent;
    .title {
        height: 35px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        .el-input {
            width: 100%;
            height: 35px;
            border: none;
            background-color: transparent !important;
            border-right: 1px solid #ccc;
            font-size: large;
        }
        .el-button {
            margin-left: 10px;
        }
        .el-button:hover {
            background-color: #6e6d6d;
            border: 1px solid skyblue;
        }
    }
    .div-editor {
        height: calc(100% - 35px);
        width: 100%;
        z-index: 1;
        #toolbar {
            border-bottom: 1px solid #ccc;
            border-top: 1px solid #ccc;
        }
        #editor {
            // height: calc(100vh - 70px) !important;
            overflow: auto;
            width: 100%;
        }
    }
}
.preview {
    width: 100vw;
    height: calc(100vh - 1px);
    .preview-body {
        width: 90%;
        height: 100vh;
        margin: 0 auto;
        .title {
            width: 100%;
            height: auto;
            word-wrap:break-word;
        }
        .main {
            width: 100%;
            height: auto;
            border-top: 1px dashed #ccc;
            margin-top: 10px;
            word-wrap:break-word;
        }
    }
}
</style>
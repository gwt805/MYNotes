<template>
  <div class="div-create">
    <div class="div-title">
      <el-input v-model="title" placeholder="标题"></el-input>
    </div>
    <div ref="divRef" id="aieditor" />
    <div class="div-btn">
      <el-button type="info" @click="cancle()">返回</el-button>
      <el-button type="primary" @click="save()">保存</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import "aieditor/dist/style.css"
import { AiEditor } from "aieditor";
import { useDark } from '@vueuse/core'
import { useRouter } from "vue-router";
import { onMounted, onUnmounted, ref, watch } from "vue";
import { article_get, article_put } from "@/api/article";
import { public_elmsg_success, public_elmsg_warning } from "@/utils/elmsg/index";

const divRef = ref();
const cron = ref()
const cron1 = ref()
const title = ref("")
const router = useRouter();
const aiEditor: AiEditor | any = ref(null);
const article_id: any = router.currentRoute.value.params.id;
const isDark = ref(useDark({ storageKey: 'vitepress-theme-appearance' }));

watch(isDark, (newVal, oldVal) => {
  console.log(oldVal)
  if (newVal) {
    document.getElementById("aieditor")?.classList.replace("aie-theme-light", "aie-theme-dark")
  }
  else {
    document.getElementById("aieditor")?.classList.replace("aie-theme-dark", "aie-theme-light")
  }
}, { deep: true })


onMounted(() => {
  article_get(article_id).then((res: any) => {
    if (res.code == 0) {
      title.value = res.data.title

      aiEditor.value = new AiEditor({
        element: "#aieditor",
        placeholder: "点击输入内容...",
        content: res.data.article,
        theme: isDark.value ? "dark" : "light"
      })
    }
    else {
      public_elmsg_warning(res.data)
    }
  })
  cron.value = setInterval(()=> {
    if(document.getElementById("aieditor") != null) {
  		const dom:any = document.getElementById("aieditor")
      dom.style.width = '20px'
      dom.style.width = "100%"
      dom.style.height = 'calc(100% - 80px)'
  		clearInterval(cron.value)
  	}
  }, 1000)

  cron1.value = setInterval(()=> {
  	if(document.getElementsByTagName("aie-footer")[0] != null) {
  		document.getElementsByTagName("aie-footer")[0].remove()
  		clearInterval(cron1.value)
  	}
  }, 1000)
})

onUnmounted(() => {
  aiEditor && aiEditor.value.destroy();
})


const cancle = () => {
  router.back()
}

const save = () => {
  article_put(article_id, title.value, aiEditor.value.getHtml()).then((res: any) => {
    if (res.code == 0) {
      public_elmsg_success(res.data)
      router.push("/index")
    }
    else {
      public_elmsg_warning(res.data)
    }
  })
}
</script>

<style scoped lang="less">
.div-create {
  width: 100%;
  height: calc(100% - 80px);
  position: fixed;
  top: 60px;
  left: 0;

  .div-title {
    display: flex
  }

  .el-select {
    width: 200px;
    height: 32px;
  }

  #aieditor {
    min-width: 100%;
    max-width: 100%;
    min-height: calc(100% - 80px);
    max-height: calc(100% - 80px);
  }

  .div-btn {
    display: flex;
    justify-content: space-between;

    .el-button {
      width: 100%;
    }
  }
}
</style>
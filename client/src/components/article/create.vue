<template>
  <div class="div-create">
    <div class="div-title">
      <el-input v-model="title" placeholder="标题"></el-input>
    </div>
    <div id="aieditor" />
    <div class="div-btn">
      <el-button type="info" @click="$router.back()">返回</el-button>
      <el-button type="primary" @click="save()">提交</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import "aieditor/dist/style.css"
import { AiEditor } from "aieditor";
import { useDark } from '@vueuse/core'
import { useRouter } from "vue-router";
import { article_add } from "@/api/article"
import { onMounted, onUnmounted, ref, watch } from "vue";
import { public_elmsg_success, public_elmsg_warning } from "@/utils/elmsg";

const cron = ref();
const cron1 = ref();
const title = ref("");
const router = useRouter();
const aiEditor: AiEditor | any = ref(null);

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
  aiEditor.value = new AiEditor({
    element: "#aieditor",
    placeholder: "点击输入内容...",
    content: '',
    theme: isDark.value ? "dark" : "light"
  })
  cron.value = setInterval(() => {
    if (document.getElementById("aieditor") != null) {
      const dom: any = document.getElementById("aieditor")
      dom.style.width = '20px'
      dom.style.width = "100%"
      dom.style.height = 'calc(100% - 80px)'
      clearInterval(cron.value)
    }
  }, 1000)

  cron1.value = setInterval(() => {
    if (document.getElementsByTagName("aie-footer")[0] != null) {
      document.getElementsByTagName("aie-footer")[0].remove()
      clearInterval(cron1.value)
    }
  }, 1000)
})

const save = () => {
  const user_id:any = window.localStorage.getItem("user_id")
  article_add(user_id, title.value, aiEditor.value.getHtml()).then((res: any) => {
    if (res.code == 0) {
      public_elmsg_success(res.data)
      router.push("/index")
    }
    else {
      public_elmsg_warning(res.data)
    }
  })
}

onUnmounted(() => {
  aiEditor && aiEditor.value.destroy();
})
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
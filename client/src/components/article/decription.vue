<template>
	<div class="div-create">
		<div class="div-title">
			<h1>{{ title }}</h1>
		</div>
		<div ref="divRef" id="aieditor" />
	</div>
</template>

<script setup lang="ts">
import "aieditor/dist/style.css"
import { AiEditor } from "aieditor";
import { useDark } from '@vueuse/core'
import { useRouter } from "vue-router";
import { onMounted, ref, watch } from "vue";
import { article_get } from "@/api/article";
import { public_elmsg_warning } from "@/utils/elmsg";

const isDark = ref(useDark({ storageKey: 'vitepress-theme-appearance' }));
const router = useRouter();
const article_id: any = router.currentRoute.value.params.id
const divRef = ref();
const aiEditor: AiEditor | any = ref(null);
const title = ref("")
const cron = ref()

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
				element: divRef.value as Element,
				placeholder: "点击输入内容...",
				toolbarKeys: [],
				content: res.data.article,
				theme: isDark.value ? "dark" : "light",
				editable: false,
			})
		}
		else {
			public_elmsg_warning("没有数据找到相关数据喔~")
		}
	})

	cron.value = setInterval(() => {
		if (document.getElementsByTagName("aie-footer")[0] != null) {
			document.getElementsByTagName("aie-footer")[0].remove()
			clearInterval(cron.value)
		}
	}, 1000)
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
		h1 {
			text-align: center
		}
	}

	#aieditor {
		min-width: 100%;
		max-width: 100%;
		min-height: calc(100% - 40px);
		max-height: calc(100% - 40px);
		overflow: auto;
	}
}
</style>
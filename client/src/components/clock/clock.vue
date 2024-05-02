<template>
    <div id="app">
        <svg :width="width" :height="height">
            <a class="fontA" v-for="(tag, index) in tags" :key="`tag-${index}`">
                <text :id="tag.id" :x="tag.x" :y="tag.y" :font-size="10 * (600 / (600 - tag.z))"
                    :fill-opacity="(400 + tag.z) / 600" @click="clickToPage">{{ tag.text }}</text>
            </a>
        </svg>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';

// 定义响应式属性
const width = ref(200); // svg宽度
const height = ref(200); // svg高度
const tagsNum = ref(0); // 标签数量
const RADIUS = ref(100); // 球的半径
const speedX = ref(Math.PI / 360 / 1.5); // 球一帧绕x轴旋转的角度
const speedY = ref(Math.PI / 360 / 1.5); // 球一帧绕y轴旋转的角度
const tags: any = ref([]); // 标签数组
const data = ref(["Python","C++","C#","PHP","Java","Go","R","GitHub","Gitee","VS Code","PyCharm","Linux","Mac","Windows","MySQL","Django","Vue","Flask","Kafka","PostgreSQL", "React","Angular","PyQT5","Echarts","Electron"]);

// 计算属性
const CX = computed(() => width.value / 2); // 球心x坐标
const CY = computed(() => height.value / 2); // 球心y坐标

// 初始化数据
const initData = () => {
    let tagsArray = [];
    tagsNum.value = data.value.length;
    for (let i = 0; i < data.value.length; i++) {
        let tag: any = {};
        let k = -1 + (2 * (i + 1) - 1) / tagsNum.value;
        let a = Math.acos(k);
        let b = a * Math.sqrt(tagsNum.value * Math.PI); // 计算标签相对于球心的角度
        tag.text = data.value[i];
        tag.x = CX.value + RADIUS.value * Math.sin(a) * Math.cos(b); // 根据标签角度求出标签的x,y,z坐标
        tag.y = CY.value + RADIUS.value * Math.sin(a) * Math.sin(b);
        tag.z = RADIUS.value * Math.cos(a);
        tag.id = i; // 给标签添加id
        tagsArray.push(tag);
    }
    tags.value = tagsArray; // 更新标签数组
}

// 纵向旋转
const rotateX = (angleX: any) => {
    const cos = Math.cos(angleX);
    const sin = Math.sin(angleX);
    tags.value.forEach((tag: any) => {
        const y1 = (tag.y - CY.value) * cos - tag.z * sin + CY.value;
        const z1 = tag.z * cos + (tag.y - CY.value) * sin;
        tag.y = y1;
        tag.z = z1;
    });
}

// 横向旋转
const rotateY = (angleY: any) => {
    const cos = Math.cos(angleY);
    const sin = Math.sin(angleY);
    tags.value.forEach((tag: any) => {
        const x1 = (tag.x - CX.value) * cos - tag.z * sin + CX.value;
        const z1 = tag.z * cos + (tag.x - CX.value) * sin;
        tag.x = x1;
        tag.z = z1;
    });
}

// 运动函数
const timer: any = ref(1)
function runTags() {
    if (timer.value == 1) {
        clearInterval(timer);
        timer.value = null;
    }
    timer.value = setInterval(() => {
        rotateX(speedX.value);
        rotateY(speedY.value);
    }, 10);
}

// 点击事件
function clickToPage() { }

// 在组件挂载后初始化数据
onMounted(() => {
    initData();
    runTags();
});

// 在组件卸载前清除定时器
onUnmounted(() => {
    if (timer) {
        clearInterval(timer);
    }
});
</script>
<style scoped lang="less">
#app {
    height: 200px;
    width: 200px;
    position: fixed;
    bottom: 20px;
    left: 0;
    .fontA {
        fill: #60cae9;
        font-weight: bold;
		user-select: none;
    }
}
</style>
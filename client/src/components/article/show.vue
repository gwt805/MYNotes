<template>
	<div class="div-f">
		<div class="div-left">
			<div class="div-top">
				<div class="div-th">
					<el-statistic title="笔记总数量" :value=article_count style="text-align: center;" />
				</div>
				<div class="div-tb">
					<el-dropdown :hide-on-click="true">
						<el-button>今日热点<el-icon class="el-icon--right"><arrow-down /></el-icon></el-button>
						<template #dropdown>
						<el-dropdown-menu>
							<el-dropdown-item v-for="it in left_hot" @click="get_hot(it.index)">{{it.name}}</el-dropdown-item>
							<el-dropdown-item divided @click="get_hot(hot_idx)">刷新一下</el-dropdown-item>
						</el-dropdown-menu>
						</template>
					</el-dropdown>
					<div class="div-ol">
						<ol>
							<li v-for="it in host_data" v-if="hot_idx!=0"><a :href="it.url" target="_blank">{{ it.title }}</a></li>
							<li v-for="it in host_data" v-if="hot_idx==0"><a>{{ it }}</a></li>
						</ol>
					</div>
				</div>
			</div>
			<div class="div-word">
				<clock />
			</div>
		</div>
		<div class="div-card">
			<div class="div-tools">
				<div class="div-tool">
					<el-input placeholder="请输入您要查询的内容" v-model="search_input" autocomplete clearable @change="get_article"><template #prepend><el-button :icon="Search" /></template></el-input>
				</div>
			</div>
			<div class="div-arts">
				<el-card shadow="never" v-for="cit in articles" style="position: relative;">
				<template #header>
					<div class="card-header">
						<a @click="article_desc(cit.id)">{{ cit.title }}</a>
					</div>
				</template>
				<div v-html="cit.article" class="card-body" />
				<template #footer>
					<div class="div-footer">
						<img :src="cit.avatar" alt="user_avatar" class="footer-img" draggable="false" />
						<div>CreatedAt&nbsp;: <span>{{ cit.created_at }}</span></div>
						<div>UpdatedAt&nbsp;: <span>{{ cit.updated_at }}</span></div>
					</div>
				</template>
				<div class="div-card-btn">
					<el-button-group>
						<el-button type="info" @click="$router.push(`/index/article/${cit.id}`)">查看</el-button>
						<el-button type="warning" @click="$router.push(`/index/article/update/${cit.id}`)">编辑</el-button>
						<el-popconfirm width="220" confirm-button-text="确认" cancel-button-text="不要" :icon="InfoFilled" icon-color="#626AEF" title="确定要删除这篇文章嘛?" @confirm="article_del(cit.id)">
							<template #reference>
								<el-button type="danger">删除</el-button>
							</template>
						</el-popconfirm>
					</el-button-group>
				</div>
				</el-card>
			</div>
		</div>
		<div class="div-page">
			<div class="demo-pagination-block">
				<el-pagination v-model:current-page="page_index" v-model:page-size="page_size" :page-sizes=page_size_list :background="true" :layout=page_layout :total=page_totle @size-change="page_size_change" @current-change="page_index_change" />
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import whttp from "@/utils/axios/index";
import clock from "@/components/clock/clock.vue";
import { article_search, article_delete } from "@/api/article";
import { InfoFilled, ArrowDown, Search  } from "@element-plus/icons-vue";
import { public_elmsg_success, public_elmsg_warning } from "@/utils/elmsg";

const router = useRouter();

const search_input = ref("");

const articles: any = ref([]);
const article_count = ref(0);

const left_hot:any = [
	{"name": "世界新闻", "index": 0, "apiUrl": "https://api.vvhan.com/api/60s"}, //{"success":true,"title":"在这里每天60秒读懂世界","banner":"https://picx.zhimg.com/v2-f69d2150f1a9b174385fbc479f11a4eb_720w.jpg?source=d16d100b","time":"03月22日","data":["六部门印发通知：明确预制菜范围，不添加防腐剂，严把原料关。","教育部：严禁在中小学生宿舍内使用明火和大功率电器。","财政部：对符合条件的高校应届毕业生到艰苦边远等地区就业的，其学费实行补偿代偿。","自动续费新规将于7月1日起施行：自动续费前应以显著方式提醒消费者。","发现、查证、澄清！全国教育辟谣平台正式上线。","12306上线“同车换乘”功能：不同车次可无需下车换乘。","我国自主研制的氢能源市域列车成功试跑，续航可达1000公里以上。","调查：我国居民平均在0点后入睡，平均睡眠时长不足7小时。","北京：今年将优化预约挂号统一平台和二三级医院预约挂号服务。","清华大学研究团队预测：日本核污水下月抵达我国海域，预计4月20日最先到浙江。","菲34人无视警告非法登上铁线礁，中国海警：依法登礁并查证处置。","英媒：科学家宣布成功切除细胞中的艾滋病毒。","韩国政府下周起将吊销违反返岗命令医生行医执照。","俄官员：俄武装力量已消灭147名抵乌的法国雇佣兵。","俄罗斯正式宣布普京赢得总统选举，就职仪式将于5月7日举行。","【微语】只有经历过地狱般的磨砺，才能练就创造天堂的力量； 只有流过血的手指，才能弹出世间的绝响。"]}
	{"name": "微博热榜", "index": 1, "apiUrl": "https://api.vvhan.com/api/hotlist/wbHot"}, //{"success": true,"name": "微博","subtitle": "热搜榜","update_time": "2024-05-02 15:46:35","data": [{"index": 1,"title": "梅大高速塌方已致48人死亡","hot": "167.9万","url": "https://s.weibo.com/wei","mobilUrl": "https://s.weibo.com/weibo?"}
	{"name": "头条热榜", "index": 2, "apiUrl": "https://api.vvhan.com/api/hotlist/toutiao"}, //{"success": true,"name": "今日头条","subtitle": "热点","update_time": "2024-05-02 16:00:06","data": [{"index": 1,"title": "广东高速塌陷事故已致48死","hot": "6771.1万","url": "https://www.toutiao.com/trending/73635714675%","mobilUrl": "https://www.toutiao.com/trending/7363"}
	{"name": "知乎热榜", "index": 3, "apiUrl": "https://api.vvhan.com/api/hotlist/zhihuHot"}, //{"success": true,"name": "知乎热榜","subtitle": "热度","update_time": "2024-05-02 15:41:09","data": [{"index": 1,"title": "广东梅大高速路面塌陷事故已发现 23 辆车陷落，已致 48 人死亡，哪些信息值得关注？","hot": "1535 万热度","url": "https://www.zhihu.com/question/654753065","mobilUrl": "https://www.zhihu.com/question/654753065"}
	{"name": "36氪热榜", "index": 4, "apiUrl": "https://api.vvhan.com/api/hotlist/36Ke"}, //{"success": true,"name": "36氪","subtitle": "24小时热榜","update_time": "2024-05-02 15:36:28","data": [{"index": 1,"title": "谁击垮了餐饮小店？","hot": "304.84热度","url": "https://36kr.com/p/2753106356091657","mobilUrl": "https://m.36kr.com/p/2753106356091657"
	{"name": "哔哩哔哩", "index": 5, "apiUrl": "https://api.vvhan.com/api/hotlist/bili"}, //{"success": true,"name": "哔哩哔哩","subtitle": "全站日榜","update_time": "2024-03-28 15:07:40","data": [{"index": 1,"title": "《崩坏：星穹铁道》黄泉角色PV——「你的颜色」","hot": "351.1万","url": "https://b23.tv/BV1Ri421X7sS",
	{"name": "百度热榜", "index": 6, "apiUrl": "https://api.vvhan.com/api/hotlist/baiduRD"}, //{"success": true,"name": "百度热点","subtitle": "指数","update_time": "2024-05-02 15:44:56","data": [{"index": 1,"title": "梅大高速塌方 官方发布安全提示","hot": "490.8万","url": "https://www.baidu.com/s?i%BA","mobilUrl": "https://m.baidu.com/s?"}
	{"name": "抖音热榜", "index": 7, "apiUrl": "https://api.vvhan.com/api/hotlist/douyinHot"}, //{"success": true,"name": "抖音","subtitle": "热点榜","update_time": "2024-05-02 14:41:55","data": [{"index": 1,"title": "梅大高速塌方已致36人死亡","hot": "1077.3万","url": "https://www.douyin.com/search/%A1","mobilUrl": "https://www.douyin.com/search/%"}
	{"name": "IT资讯榜", "index": 8, "apiUrl": "https://api.vvhan.com/api/hotlist/itNews"} //{"success": true,"name": "IT之家","subtitle": "最新资讯","update_time": "2024-05-02 15:58:47","data": [{"index": 1, "title": "国产文字冒险游戏《饿殍：明末千里行》首周销量近十万，好评率 94%","hot": "今日 15:50","url": "https://www.ithome.com/0/765/554.htm","mobilUrl": "https://m.ithome.com/html/0765554.htm"}
]
const hot_idx = ref(0);
const host_data:any = ref([])

const page_index = ref(1);
const page_size = ref(10);
const page_totle = ref(0);
const page_size_list = ref([5, 10, 20, 50, 100])
const page_layout = ref("total, sizes, prev, pager, next, jumper");

const page_size_change = (val: number) => {
	page_size.value = val
	get_article()
}
const page_index_change = (val: number) => {
	page_index.value = val
	get_article()
}

const get_hot = async(idx:number) => {
	hot_idx.value = idx
	await whttp.get(left_hot[hot_idx.value].apiUrl).then((res:any) => {
		host_data.value = res.data
	})
}

const article_desc = (id: string) => {
	router.push({ path: `index/article/${id}` })
}

const article_del = (id:number)=> {
	article_delete(id).then((res:any)=> {
		if(res.code == 0) {
			public_elmsg_success(res.data)
			get_article()
		}
		else {
			public_elmsg_warning(res.data)
		}
	})
}

const get_article = () => {
	article_search(search_input.value.trim(), page_index.value, page_size.value).then((res: any) => {
		if (res.code == 0){
			articles.value = res.data
			article_count.value = res.article_count
			page_totle.value = res.count
		}
		else {
			public_elmsg_warning(res.data)
		}
	})
}
onMounted(() => {
	get_article()
	get_hot(hot_idx.value)
})
</script>

<style scoped lang="less">
.div-f {
	.div-left {
		width: 200px;
		height: calc(100% - 80px);
		position: fixed;
		top: 60px;
		left: 0;
		user-select: none;

		.div-top {
			height: calc(100% - 80px - 125px);
			overflow: auto;
			user-select: none;

			.div-th {
				height: 50px;
			}

			.div-tb {
				width: 200px;
				height: calc(100% - 80px - 235px);
				position: fixed;
				overflow: auto;
				.el-button {
					width: 200px;
					height: 40px;
					position: absolute;
					border: none;
					box-shadow: none;
				}
				.div-ol {
					width: 100%;
					height: calc(100% - 63px);
					position: absolute;
					top: 42px;
					overflow-y: auto;
					overflow-x: hidden;
					ol li {
						margin-left: 25px;
						font-size: 12px;
						color: gray;
						line-height: 20px;

						a {
							color: gray;
							text-decoration: none;
						}
					}
					ol li:hover a {
						font-size: 16px;
						text-decoration: underline;
						display: block;
						transition: transform 0.3s ease-in-out;
						transform: translateX(5px);
					}
				}
			}
		}
	}

	.div-card {
		width: calc(100% - 200px);
		height: calc(100% - 128px);
		position: fixed;
		top: 60px;
		left: 200px;

		.div-tools {
			height: 32px;
			width: calc(100% - 200px);
			position: fixed;
			.div-tool {
				display: flex;
			}
		}

		.div-arts {
			position: absolute;
			top: 32px;
			width: 100%;
			height: calc(100% - 32px);
			overflow: auto;
			.el-card {
				height: 240px;

				.div-card-btn {
					height: 240px;
					width: 200px;
					position: absolute;
					top: 0;
					right: 0;
					opacity: 0; /* 元素完全透明 */
					transition: opacity 0.7s ease;
					.el-button {
						height: 240px;
						margin-left: 7px;
						font-weight: bold;
					}
				}

				.card-body {
					width: 100%;
					height: 80px;
					overflow: hidden;
				}

				.div-footer {
					display: flex;
					color: gray;
					justify-content: space-around;

					.footer-img {
						width: 48px;
						margin-top: -10px;
					}
				}
			}

			.el-card:hover {
				.div-card-btn {
					opacity: 1;
				}
			}
		}
	}

	.div-page {
		width: calc(100% - 200px);
		height: 33px;
		position: fixed;
		bottom: 30px;
		left: 200px;
	}
}
</style>
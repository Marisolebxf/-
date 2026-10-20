# FE-TS-09A · 科技发展规划 M9 整页复刻（综合规划/重点领域/研究分析）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 日常 feature；未用 YAGNI 跳过 D8（token 对齐 Design.md）/ D9（observability + Mock 态种子同步）/ 架构铁律（复用 TiandituMap/PageTabFrame/Arco，未新增依赖） |

## 问题清单

- 无阻塞问题。demo `overviewMapRef` 为死代码（声明后从未挂载 JSX），综合规划 Tab 实际无地图，lumen 侧同步不实现（避免凭空多造一块 UI）。

## 修改内容

### 首轮交付（commit `fc32631`，已推 `origin/dev`）

仓：`lumen-ui-science-pc`

**新文件（12 个，+5429 行）：**
- `src/types/techDevelopmentPlan.ts` — 全部类型定义（冻结 demo 字段形状：flowType/hot_trend/netInflow 等不改写）
- `src/mock/modules/techDevelopmentPlan.ts` — 冻结种子 `createTechDevelopmentPlanDataset()`（六源预警/热点技术/趋势序列 3m|6m|12m/人才流动/载体坐标/产业集群/重叠度矩阵/等级卡/图谱节点等）
- `src/api/situation/techDevelopmentPlan.ts` — `defineApi` 双轨（USE_MOCK 走 mock，false 走网关 `/situation/v1/planning/dataset`，对齐 API-TS-M9）
- `src/views/situation/tech-development-plan/index.vue` — 主入口：PageTabFrame 三 Tab + 数据一次取全 + `ts-tech-development-plan-track` 埋点
- `tabs/OverviewTab.vue` — Tab1 综合发展规划七卡：方向预警（六源均分+预警行+详情 Modal+报告 Modal Word/PDF）/ 全球热点技术 / 动态跟踪（多选≤5+时间/空间切换+口径三卡）/ 多维指标体系（7 分类联动）/ 本地优势（双向条形+洞察）/ 人才流动（OD 桑基+机构 TOPS）/ 科创资源推送（证据 Modal+推送设置 Modal）
- `tabs/KeyAreaTab.vue` — Tab2 重点领域规划：产业集群导航+清除 → 空间布局（TiandituMap+图层切换+图例）→ 竞争力画像（5 指标+维度得分+对标排名）→ 载体三视图（堆叠/区县/清单）→ 土地效益 → 情景方案卡+方案模拟 Modal
- `tabs/ResearchTab.vue` — Tab3 研究领域分析：等级划分 4 卡 → 知识图谱（graph+图例+缩放控件）→ 重叠度（gauge+对比条形）→ 多企业竞争四象限 → 情报报告表+报告 Modal（Word/PDF）+战略 Modal+方案模拟 Modal
- `models/techDevelopmentPlanModel.ts` — 派生计算与 option 构建器（预警过滤/六源均分/报告 HTML/桑基 links/载体过滤/区域画像/重叠度确定性兜底+成对复算+企业汇总/情报报告/ECharts option×6/Word/PDF 产物）
- `styles/demo-tech-development-plan.css` — demo tzp-* 体系冻结移植（`.ant-card-body`→`.arco-card-body`），token 对齐 Design.md
- `techDevelopmentPlan.test.mjs` — ponytail 自检（见测试结果）

**改动（2 个）：**
- `src/mock/register.ts` — 注册 `tsTechDevelopmentPlanDataset`
- `src/router/menu.ts` — 映射 `tech-development-plan` → 页面组件

**复用（未新造轮子）：** `PageTabFrame`、`TiandituMap`（含 tooltipHtml/popup 事件）、`IndustrySelect`、`MetricSpecHint`、`MockBadge`、`@/utils/observability.createTraceId`、`chartOptions`（CHART_BASE/baseTooltip）、Arco（card/select/modal/tag/progress/descriptions/spin/checkbox/tooltip/button）。

### 走查修复迭代（用户 DOM 走查反馈三轮，commit `ce812a9`，已推 `origin/dev`）

**根因主线：`x-vue-echarts` init 竞态** —— 三 Tab 均用 `v-if` 切换挂载，flex 容器 `height:auto` 下 echarts init 时读到 0 高死锁（canvas 存在但 0×0）。统一修法：自适应图表加显式高度（`flex: 0 0 auto` + 定高），与 Tab3 `__graph` 先例一致。

- **Tab3 研究分析**：知识图谱 0 高空白（`.tzp-research-grid__graph` 定高 320px）；竞争四象限企业胶囊溢出（默认选 `['1','2']` 2 家 + `overflow:hidden`）；报告表格空（过滤参数 `'all'`→`'全部'`）
- **Tab2 重点领域**：TiandituMap 容器 1px 塌陷（`.tzp-map-container > .tzp-map-real { min-height:300px }` + `@vue:mounted` 调 `invalidateSize()`）；布局重排——科技载体+土地用途同行各 3 列、资源配置优化建议独占 6 列、方案 A/B/C 三卡横排（grid areas 改 6 列）；土地效益图 0 高死锁（`__land x-vue-echarts` 定高 220px）
- **Tab1 综合规划**：趋势折线/本地优势条形 0 高死锁（`__trend`/`__local` 定高 260px）；**人才 OD 桑基不渲染根因是 `src/config/echarts.ts` 按需注册漏 `SankeyChart`**（demo 全量 `window.echarts` 无此问题），补注册；本地优势三按钮 demo 原为静态装饰（查证 `TechDevelopmentPlan.tsx` L2846–L2850 无 onClick），按 D10 页签可交互要求补真实切换：`localAdvantageTab` 状态 + `role=tablist/tab` + `aria-selected`，mock 补「创新能力对比/成果产出对比」两维度种子（`localAdvantageInnovation`/`localAdvantageOutput`），`types` 同步扩展
- **筛选条迭代（commit `b2c7a0d` + `27ed9a9`）**：`<label>` 包裹 `a-select` 致下拉闪开即关（改 `<div>`）；控件形状对齐 demo（高 34px / #dbe6f5 边框 / 圆角 4px / label 上置）

**走查验证方式**：Chromium CDP 实测——canvas `getImageData` 像素采样确认三 Tab 全部图表实绘（趋势 25934 / 空间分布切换重绘 14008 / 本地优势 7249 且切换维度后数据联动 / OD 桑基 4670 / 知识图谱非零）；`tzp-local-advantage-tabs` 点击后 selected 状态与图表序列切换确认。

## 测试结果

- `npx vue-tsc --noEmit -p tsconfig.app.json` → 0 错误
- `node --experimental-strip-types src/views/situation/tech-development-plan/techDevelopmentPlan.test.mjs` → ✅ 全过（种子一致性：六源分 0-100/热点池≥5/重叠度兜底幂等 20-95/balanced 档阈值分级/矩阵基准对/dataset 契约字段非空 + 接线断言：register/menu/API 双轨/埋点/TiandituMap 复用 + 视图结构断言：三 Tab demo 区块标题逐字/载体三视图/集群导航/图层切换/报告导出）
- `pnpm run build` → ✅ 17s 构建绿（chunk 体积警告为存量，非本任务引入）
- 走查修复后复验：`vue-tsc` 0 错；浏览器 CDP 像素采样三 Tab 图表全部实绘（见修改内容「走查验证方式」）

## 遗留风险

- `USE_MOCK=false` 时 REST 契约依赖后端 `/situation/v1/planning/dataset`（API-TS-M9 §数据聚合接口）尚未就绪；当前 Mock 态可完整演示。
- Word 导出走 `.doc` HTML 模板（demo 同款），复杂样式在 Word 中可能降级——demo 原样保留。
- demo `TechDevelopmentPlan.tsx` 中部分英文 UI 文案（如人才流向图 node 名）已随种子冻结，后续如需统一中文随 API 契约一起改。
- 本地优势「创新能力/成果产出」两维度种子为 lumen 侧补充（demo 三按钮静态无数据）；口径未经 data-agent 定义，接入真实接口时以后端契约覆盖。
- M8 遗留的 `ComparisonCascadeSelect.vue` 本地未提交改动（非本任务范围）仍留在工作区。
- `ce812a9` 推送触发的 CI 尚未回查，签收前应确认 pipeline 绿 + K8s dev 可访问。

## CI/CD（必填）

- 分支：`dev`
- commit：`fc32631`（首轮整页复刻）→ `b2c7a0d`（下拉闪关修复）→ `27ed9a9`（筛选条形状对齐）→ `ce812a9`（三轮走查修复，均 `[agent:frontend]` 标注）
- pipeline URL / ID：GitLab CI 自动触发（push 已完成 `56b2624..ce812a9`）
- 部署 namespace / 镜像 tag：CI 流水线自动（K8s dev）
- K8s rollout：待 CI（前端静态部署，历史成功率稳定）
- dev 测试 URL / 命令与结果：CI 绿后 K8s dev 环境「科技发展态势 → 科技发展规划」菜单；本地 `pnpm dev` 已可访问（mock 态，走查修复已实测）

## 可观测性（建议）

- 前端埋点：`ts-tech-development-plan-track` CustomEvent（tab-change / overview-filter-change / keyarea-cluster-select / keyarea-map-carrier-click / research-strategy-open 等），`createTraceId()` 注入
- OTEL_SERVICE_NAME：前端静态站（沿用仓内既有配置）

## 涉及文件

见「修改内容」清单（12 新 + 2 改，均在 `lumen-ui-science-pc`）。

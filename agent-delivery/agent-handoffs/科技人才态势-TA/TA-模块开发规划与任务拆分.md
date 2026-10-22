# 科技人才态势（TA）模块开发规划与任务拆分

- 时间：2026-10-20 定稿
- 作者：agent:coordinator-agent（规划；对齐 TS/DR 模式，监管：human:孔东 / human:李伟）
- 范围：展示系统「科技人才态势」大模块 4 个四级页面正式开发（全球领域人才态势 / 关注地区人才态势 / 重点科技人才画像 / 人才引进推荐评估）
- 工作仓：`repos/lumen-ui-science-pc`（正式）· `repos/demo-ui-science`（原型只读对照）
- 人员：前端 human:孔东 · 接口 human:李伟（BE 只建 1 张契约单，内部拆分由李伟自决）
- 需求真源：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.1.4.3；SRS 分册 `bid-reference/srs/02-科技信息展示系统/科技人才态势/*.md`（87 叶：全球 23 / 关注地区 11 / 画像 28 / 推荐评估 25）
- 原型真源：`demo-ui-science/src/pages/talent-trend/`（4 页 + 36 组件 jsx ≈ 11k 行 + 纯函数模块 17 个 + `data.js` 1554 行冻结种子 + 16 个 `*.test.mjs` + 4 个 css ≈ 3.1k 行）；菜单经 `App.jsx` 现行绑定
- 契约输入：SCI-INT 集成卡已 ready_to_sign —— `agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A12.yaml`（全球，INT-A-TAL-1100~1122）、`A13.yaml`（关注地区，INT-A-X-1200~1210）、`A14.yaml`（画像，INT-A-X-1300~1327）、`A15.yaml`（推荐评估，INT-A-X-1400~1424）；调用链草案/metric 挂接/无源项结论直接引用，本文不复制
- 本文用途：模块开工真源；task-registry 建单依据；FE/BE 契约对齐底稿

> 历史区分：`agent-handoffs/科技人才态势-DS15/` 是 2026-06 UX/UI 试点（DS-15 画像页 sandbox），`demo-ui-science/src/pages/talent-preview/`（4.2k 行 data.js 旧版）是当时的产物，**App.jsx 主菜单已不引用，不作为复刻真源**；复刻真源只有 `src/pages/talent-trend/`。

## 0. 已定口径与待拍板决策项

| # | 决策项 | 结论 / 默认倾向 |
|---|---|---|
| D1 | demo 两套人才页（talent-preview 旧 / talent-trend 新）以哪套为准 | **talent-trend**（App.jsx 现行主菜单绑定，git 持续维护至 2026-10）；talent-preview 仅试点遗留 |
| D2 | 跨页跳转（demo `navigation.js` 单例：全球→画像/推荐评估带 talentId） | **vue-router query 参数**（`?talentId=`）+ Pinia 模块 store；不复刻单例轮询 |
| D3 | 无源项（华人占比/迁徙事件/成本模型/合作网络图点边等，集成卡 IP-10 清单） | **mock 态照 demo 渲染 + 🧪 MockBadge**（复刻期不删区块）；真机联调按集成卡 IP-10 空态 + ⚠️，禁止 fixture 填数顶替 |
| D4 | PDF/Excel 导出（画像 2 个 + 尽调 1 个 + 贡献匹配 1 个报告导出；分布图 XLSX 导出） | **照搬 demo 机制**（专用打印页 + print；XLSX 用仓内已装 xlsx）；角色/频控策略照 demo，对齐 TS D1 |
| D5 | 合作网络/研究领域图谱渲染 | demo 即 ECharts graph（无 G6）→ lumen 沿用 `chartOptions`/`GraphChart` 封装；Nebula 只在 BE 侧（Java→Python 链路），前端不感知 |
| D6 | 写操作演示态（订阅 SubscriptionDrawer / 基础信息写回 / 批量导入） | 会话级/localStorage 演示态，**不替 BE 拍板契约**；真实写回走 A14 升级项（ADS 人工层，李伟侧），偏离记 handoff |

## 1. 全局技术约束（4 页统一遵守）

1. **UI 栈**：Vue3 `<script setup>` + Arco Design Vue + UnoCSS；token 按 `Design.md`（主色 `#165DFF`、正文 14px、控件 32px、圆角 4px）。**Arco 优先**（demo 原生 `<select>`/`<input>`/`AutoComplete` 必换 `a-select`/`a-input`/`a-auto-complete`；Arco bug 修根因不回退原生）。
2. **复刻五件套**：布局、交互、样式、评审、Mock 开关数据；禁止以「更简」另起 UI；互斥 `display` 不叠同一节点。
3. **Mock 统一开关**：种子**冻结自 demo `talent-trend/data.js`**（4 个 getter：global/focusRegion/profile/recommend；确定性生成、派生链禁手写、禁 `Math.random`，若 demo 种子含随机须先定化并记 handoff），头注释标真源 + 同步任务 ID；`USE_MOCK=false` 零 fixture 渲染（D12）。
4. **地图**：全球分布/迁徙（leaflet 世界地图）与深圳视图复用 `TiandituMap`/`UnifiedLeafletMap` 底座能力（图层组/marker/热力/视口聚焦/isolation 层级）；中国视图 choropleth 用 ECharts map。天地图 key 沿用 `VITE_TIANDITU_KEY`。
5. **调用链**：前端 → Java REST → Python `/internal/*`（IP-08 叶）→ 只读 ADS；路径/DTO/枚举**由 Java 侧（李伟）按集成卡 contract_draft 主导定稿**，前端不猜路径。D12：不指向任何 demo-* 服务。
6. **D9 血缘**：每个统计数字旁 ⓘ（MetricSpecHint）+ metric_id（集成卡已挂 6 个：M_TALENT_BASE_98_1 / DEEP_157_1 / DEEP_162_1 / DEEP_164_1 / GRAPH_110_1 / GRAPH_111_1）；无源叶按集成卡 `metric_missing` 清单登记，不伪闭合；Mock 态 🧪 MockBadge。
7. **可观测**：pageview + `X-Trace-Id`/`traceparent` 沿用仓内 observability 机制。
8. **16 个 `*.test.mjs` 状态机**：按断言语义摘选移植最小自检（搜索定位/迁徙年份切片/难度 Tab 逻辑/报告导出构造等）。

## 2. 公共组件复用清单（先查 TS 沉淀，不新造）

> 真源：`agent-handoffs/科技发展态势-TS/TS-demo-lumen复刻经验清单.md` §2.3。**第二处出现即封装**；封装件样式自含。

| 已沉淀 | TA 用途 |
|---|---|
| `PageTabFrame` | 4 页 L5 Tab 页框（demo 全用 PageTabFrame/WorkbenchTabs） |
| `StatCard` / `KpiDeck` | 全球页 KPI 行、洞察面板指标卡 |
| `TiandituMap` / `UnifiedLeafletMap` | 全球分布/迁徙图、深圳视图（leaflet）；热力/视口聚焦/flyTo |
| `chartOptions` + `src/config/echarts.ts` | line/bar/pie/radar/gauge/graph；中国 choropleth 需确认 map 注册（新图型先查按需注册） |
| `GraphChart` | 合作网络/研究领域图谱（roam/图例） |
| `MetricSpecHint`（D9 ⓘ）/ `MockBadge`（🧪） | 每个统计数字旁 |
| `ExportFlowPanel` / ExportButton 语义 | XLSX/报告导出挂槽 |
| `IndustrySelect` | 产业级联筛选（demo 直接复用同名件，lumen 已有） |
| `defineApi` 双轨 + `request.ts` + `models/*.ts` 纯函数派生层 | `src/api/talent.ts` + `src/views/talent/models/` |

**TA 模块私有件**（模块目录 `views/talent/` 内）：`tl-filter-bar` 筛选行变体（学历/职称/时间/评估对象）、人才地图（迁徙流向/时间轴播放）、机构列表面板、区域/机构/城市三类详情抽屉、画像 7 Tab 面板族、尽调/贡献/领域图谱报告打印页、对比面板、订阅抽屉。demo 的 `fieldConfig.js`（筛选配置）进模块目录。

## 3. 任务拆分（registry 建单蓝图）

### 3.1 接口侧（1 张大单，human:李伟 自行拆分）

| ID | 任务 | 说明 |
|---|---|---|
| BE-TA-CONTRACT-01 | 科技人才态势 — Java 接口契约定义与数据需求评审（4 页 87 叶，出 API-TA 文档） | **输入 = SCI-INT A12–A15 四份集成卡**（contract_draft/久新行 SRS-98/110/111/157/160/162/164/无源 IP-10 清单/升级项：ads_talent_geo_agg、人才主键、人工层写回、talent·talent_coop 图点边）；路径/DTO/枚举由 Java 侧主导定稿；**契约 → 实现 → 数据对接的内部拆分、排期由 human:李伟 自行决策建单**（参照 DR 模式） |

### 3.2 前端侧（基座 1 单 + 整页 4 单）

| ID | 任务 | demo 真源（行数） | 体量 |
|---|---|---|---|
| FE-TA-S01 | 模块基座：路由挂接（4 菜单项替换 DevelopingView）/跨页跳转机制（D2）/mock 种子冻结（data.js 1554 行）/api 双轨/公共件盘点/D9 挂点/共享 style.css（1223 行）token 抽取 | `data.js` + `style.css` + `navigation.js` + `fieldConfig.js` | M |
| FE-TA-01A | 全球领域人才态势整页复刻（23 叶）：双 Tab（分布图/最新动态）；地图搜索定位/图层切换/迁徙热区/年度时间轴播放（globalTalentTime）/华人研究员占比饼图/机构列表+排名/区域·机构详情抽屉/城市动态抽屉/XLSX 导出/跳画像·推荐评估 | `GlobalTalentPage`(158)+`DistributionInsightView`(494)+`TalentMap`(456)+`InsightPanel`(383)+`ActivityPanel`(330)+`InstitutionListPanel`(103)+`TalentTimelineBar`(71)+`RegionDetailDrawer`(236)+`InstitutionDetailDrawer`(170)+`CityActivityDrawer`(166)+纯函数 6 个 | L |
| FE-TA-02A | 关注地区人才态势整页复刻（11 叶）：筛选行（产业/学历/职称/时间）+ 关键词 AutoComplete 定位；中国视图（choropleth+省份下钻+学历结构+迁徙曲线）与深圳视图（天地图+区/园区标记+机构层级）Segmented 切换、双 pane 保活 | `FocusRegionPage`(138)+`ChinaTalentView`(634)+`ShenzhenTalentView`(427)+`focusRegionSearch`(183)+`focus-region.css`(505) | L |
| FE-TA-03A | 重点科技人才画像整页复刻（28 叶）：人才筛选（机构/职称/地区/产业/关键词）+ 7 Tab（基础画像[含治理写回]/关联画像/分析画像/近期成果/合作网络图谱/研究领域图谱[836 行最大件]/荣誉奖项与国际合作）+ 订阅抽屉 + 批量导入 + 画像 PDF/领域图谱报告导出 | `TalentProfilePage`(439)+7 个 Profile 面板(3847)+`SubscriptionDrawer`(50)+`profileReportExport`(171)+`fieldMapReportExport`(68)+`talent-profile.css`(1200) | XL |
| FE-TA-04A | 人才引进推荐评估整页复刻（25 叶）：模块简介+筛选（产业/评估目标/对象搜索真生效）+ 已应用摘要条 + 规格说明条 + 4 Tab（学科贡献度分析[含贡献匹配报告]/学者引进难度预测/引进成本预测/人才尽调报告与推荐[含对比面板]）+ 3 个报告导出（尽调/贡献匹配/成本） | `TalentRecommendPage`(210)+`ContributionTab`(739)+`CostTab`(653)+`ReportTab`(290)+`DueDiligenceReport`(296)+`TalentComparePanel`(247)+`DifficultyTab`(165)+`ContributionMatchReport`(192)+`RecommendSpecBar`(23)+纯函数 4 个+`talent-recommend.css`(174) | L |

依赖：`FE-TA-01A/02A/03A/04A` depends_on `FE-TA-S01`；FE 单不依赖 BE 契约（mock 先行，契约冻结后联调，对齐 TS/DR 模式）。

### 3.3 批次

| 批次 | 内容 | 备注 |
|---|---|---|
| 批 1 | FE-TA-S01 + FE-TA-01A ＋ BE-TA-CONTRACT-01 启动 | 基座 + 全球页可验（地图/迁徙/时间轴全能力试点）；契约评审前置 |
| 批 2 | FE-TA-02A + FE-TA-03A | 关注地区复用批 1 地图沉淀；画像页体量最大单独排 |
| 批 3 | FE-TA-04A + 联调收尾 | 报告导出族 + 契约冻结后真机联调 |

FE 合计 ≈ 24–28 工日；每批独立上 K8s dev 验收。

## 4. 各页 FE 拆分与 BE 接口用途（契约对齐，详见集成卡）

> FE 每单 DoD 统一：与 demo 逐区块截图比对（五件套）、Design token、D9 ⓘ/🧪、观测头、test.mjs 最小自检移植、`pnpm type-check` 0 错 + 自检 + `pnpm build` 三绿；**完工停本地工作区等人工验收**（2026-10-20 闸门），不自动 commit/push。

### 全球领域人才态势（A12 卡，excel 246–268）
- FE：分布图（散点/热力/迁徙流向三图层切换 + 年度时间轴播放）/ 搜索定位（人才/机构/区域候选）/ 区域与机构详情抽屉 / 华人占比饼图 / 顶尖机构列表 / 最新动态 Tab（城市动态抽屉）/ XLSX 导出
- BE 接口用途（A12 contract_draft，路径 Java 定）：① 区域人数聚合（SQL-98 落 `ads_talent_geo_agg`，升结构项）② 人才流动边表（SRS-157，事件定义未拍板前 IP-10）③ 学术力快照（SRS-162，H 指数）④ 实体识别/关系（SRS-110/111）⑤ 招入推荐（SRS-164，仅匹配度）
- **无源空态（联调期）**：华人占比（1105）、动态气泡（1110）、动态热力（1111）、最新动态（1119）、荣誉奖项（1121）、出访记录（1122）等 10 张 metric_missing 卡

### 关注地区人才态势（A13 卡，excel 269–279）
- FE：筛选行 + 搜索定位；中国视图（省级 choropleth/学历职称结构/代表性专家/流动历史曲线）；深圳视图（区/园区/载体层级 leaflet）；报告导出
- BE 接口用途：① 中国/深圳人数聚合（同 SQL-98，IP-06/IP-09）② 迁徙（SRS-157）③ 深圳园区/载体地理维（1205 升结构，落地前不下钻）④ 智能报告（1210 未核实，IP-10）
- 底图与行政区边界未核实（DN-A13-01）：dev 用天地图现行配置，不对接未点名地图服务

### 重点科技人才画像（A14 卡，excel 280–307）
- FE：人才检索列表 + 7 Tab 画像 + 订阅 + 导入 + 报告导出（见 §3.2）
- BE 接口用途：① 人才主档（talent_key 占位，主键 C01 P0-1 未定前详情不开查）② 学术力（SRS-162）/画像增强（SRS-160）③ 实体识别（SRS-110）④ 基础信息写回走 ADS 人工层再投影（升李伟）⑤ 合作网络/领域图谱点边（talent·talent_coop 未建，9 张升结构卡确认前空态）
- **隐私脱敏（DN-A14-PRIVACY）未拍板前接口不返回敏感字段**；FE mock 态照 demo

### 人才引进推荐评估（A15 卡，excel 308–332）
- FE：筛选/搜索/已应用摘要 + 4 Tab（贡献度/难度/成本/尽调报告）+ 3 报告导出 + 对比面板（见 §3.2）
- BE 接口用途：① 招入推荐（SRS-164）② 画像增强（SRS-160）③ 实体识别（SRS-110）
- **无源空态（联调期）**：六条无源指标（005 沟通障碍/006 文化融合/007 流动壁垒/010 引进阻力/013 成本模型/025 团队协同）+ 成本采集族（319–325，DN-A15-COST 未关闭前不出费用数字，不用 mock 金额填）

## 5. 避坑清单（开工必读，真源：TS 复刻经验清单）

1. **Arco**：`#option="{ data }"` 插槽签名；`<label>` 禁包裹 `a-select`（闪开即关）；cascader 多选用标准多选 + `allow-clear` 禁自绘 footer；图标显式 import；AutoComplete 对应 `a-auto-complete`。
2. **封装**：第二处出现即封装；封装件样式自含（复用他页类名会裸奔）；先查 §2 清单不新造。
3. **渲染**：fixed 弹层（三类详情抽屉/订阅）`Teleport to body`；图表容器显式高度防 init 0 高死锁（画像 7 Tab 切换高发）；中国 choropleth 是新图型先查 `echarts.ts` 按需注册；地图 frame `isolation: isolate`；Segmented 双 pane 保活用 `v-show` 语义（demo hidden 类）不叠互斥 display。
4. **数据**：首屏同步初值防白屏；dev slot props 失效用数据签名 key 规避（demo `searchRevision`/`token: Date.now()` 同款机制直接保留）；种子冻结禁 Math.random；写操作演示态不替 BE 拍板。
5. **工程**：类型门一律 `pnpm type-check`（vue-tsc 空跑教训）；表格操作列按钮防压缩变形；多选标签 `:max-tag-count` 折叠；test.mjs 最小自检；交付三绿；**完工停本地等人工验收，不自动 push**。
6. **TA 特有**：迁徙时间轴播放（setInterval）卸载清理 + 页面不可见暂停；报告导出用专用打印页（不 window.print 整页）；跨页跳转带 talentId 落 query；demo 两套人才页只认 talent-trend（§0 D1）。

## 6. 风险与跟踪

| # | 风险 | 动作 |
|---|---|---|
| R1 | 画像页体量最大（FE-TA-03A，demo 4.5k 行）压批 2 | 批 1 地图/抽屉/图表沉淀最大化复用；必要时 03A 拆两批交付（先 4 Tab 后 3 Tab+导出），拆分由执行时 coordinator 定 |
| R2 | 契约依赖集成卡未签收（A12–A15 均 ready_to_sign） | 契约单以卡为输入开工；签收不影响 FE（mock 先行）；卡内容变更走 BE-TA-CONTRACT-01 评审记录 |
| R3 | 无源项空态与 demo 演示效果差异引发走查争议 | §0 D3 口径前置写进每单 DoD：mock 态照 demo，真机空态不删区块；走查对照 demo Mock 态 |
| R4 | 人才主键未定（C01 P0-1）阻塞画像/推荐详情联调 | 契约用 talent_key 占位；主键拍板进度跟 BE-TA-CONTRACT-01；FE 联调期以 mock id 顶 |
| R5 | demo 种子若含随机/时间函数导致冻结失败 | S01 冻结时定化处理并在头注释标注，handoff 记录偏离 |

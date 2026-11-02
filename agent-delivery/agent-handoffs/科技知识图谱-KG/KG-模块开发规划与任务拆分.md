# 科技知识图谱（KG）模块开发规划与任务拆分

- 时间：2026-11-02 定稿
- 作者：agent:coordinator-agent（规划；对齐 TS/TA/DR/ACH 模式，监管：human:孔东 / human:李伟）
- 范围：展示系统「科技知识图谱」大模块 4 个四级页面正式开发（分析展示 / 指标展示 / 算法展示 / 服务展示，55 叶 L6）
- 工作仓：`repos/lumen-ui-science-pc`（正式）· `repos/demo-ui-science`（原型只读对照）
- 人员：前端 human:孔东 · 接口 human:李伟（BE 只建 1 张契约单，内部拆分由李伟自决）
- 需求真源：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.1.4.5；SRS 分册 `bid-reference/srs/02-科技信息展示系统/科技知识图谱/*.md`（55 叶：分析 8 / 指标 15 / 算法 15 / 服务 17，excel 403–457）
- 原型真源：`demo-ui-science/src/pages/tech-knowledge-graph/`（48 文件：4 页 jsx ≈ 5.4k 行 + 算法/状态机纯函数 js ≈ 3.5k 行 + `mockData.js` 43KB 确定性种子 + `style.css` 21KB `kg-*` 类体系 + 13 个 test/selfcheck.mjs）；经 `App.jsx` + `pageRouting.js` 现行绑定（`knowledge-graph-*`）
- L6 真源：demo `kgL6Functions.js`（seq 400–454 全量导出，SRS 55 项一比一）；lumen 侧 `views/knowledge-graph/` 目前为空、`menu.ts` graph 组 4 项已占位（DevelopingView 回落）
- 本文用途：模块开工真源；task-registry 建单依据；FE/BE 契约对齐底稿

---

## 0. 待拍板决策项（开工前由监管人拍板，默认倾向先行）

| # | 决策项 | 背景 | 默认倾向 |
|---|---|---|---|
| D1 | 算法展示三算法（路径/中心性/社群）与智能分析中心 demo 为**前端 JS 演算**，正式算法（Python）接入排期未定 | demo `pathSearchAlgo`/`centralityAlgo`/`communityAlgo`/`kgIntelligence` 均为确定性前端实现（带 selfcheck） | **照 demo 前端演示 + 🧪**（复刻期算法层移植为 `models/*.ts` 纯函数）；BE 契约单登记 Python 算法真算需求（Java→Python `/internal/*`），不阻塞 FE |
| D2 | 服务展示实时监控 / 实时流开关（RealtimeMonitorPanel） | demo 有实时监控卡（开关 + 演示流） | 对齐 TS-D2 / DR-D3 已拍板口径：**轮询 + 定时刷新**（首版 30s、间隔常量化、页面不可见暂停、卸载清理） |
| D3 | 分享 / 收藏 / 查询历史 / 订阅通知写操作 | demo 全为前端会话态/localStorage（`kgShareRegistry`/`shareHistory` 等） | 对齐 TA-D6：**localStorage 会话级演示态**，不替 BE 拍板契约；真实写接口归 BE-KG-CONTRACT-01 评审 |

## 1. 全局技术约束（4 页统一遵守）

1. **UI 栈**：Vue3 `<script setup>` + Arco Design Vue + UnoCSS；token 按 `Design.md`（主色 `#165DFF`、底 `#D8E7FC`、正文 14px、控件 32px、圆角 4px）。**Arco 优先**（demo antd 组件逐项对应替换；原生 `<select>`/`<input>` 禁留）。
2. **复刻五件套**：布局、交互、样式、评审、Mock 开关数据；禁止以「更简」另起 UI；互斥 `display` 不叠同一节点。
3. **Mock 统一开关**：种子**冻结自 demo `mockData.js`**（确定性生成器 `_kgSeed=20260826`、派生链禁手写、禁 `Math.random`），头注释标真源路径 + 同步任务 ID；`USE_MOCK=false` 零 fixture 渲染（D12）。
4. **图表**：ECharts（vue-echarts）；graph（force/roam/全屏）、line/bar/pie/radar/gauge —— `src/config/echarts.ts` 已全量按需注册（GraphChart/ChordChart/SankeyChart 等在册），复用 `chartOptions`/`GraphChart`/`ChartCard` 封装，禁页内直拼 token。
5. **调用链**：前端 → Java REST → Python `/internal/*`（真算算法）→ 只读 ADS / Nebula（BE 侧）；**前端不直连图谱服务、不感知 nGQL**（铁律 3/7）。路径/DTO/枚举由 Java 侧（human:李伟）主导定义，前端不猜路径。
6. **D9 血缘**：每个统计数字旁 ⓘ（MetricSpecHint）+ metric_id（demo 种子已自带，如 `serviceKpis[].metric_id`、`M_KG_*` 系，沿用原值；缺位按占位 id 规则登记）；Mock 态 🧪 MockBadge；不伪闭合。
7. **可观测**：pageview + `X-Trace-Id`/`traceparent` 沿用仓内 observability 机制，不新造。
8. **13 个 test/selfcheck.mjs**：按断言语义摘选移植最小自检（`graphFilter.test`/`kgIntelligence.test`/`patternRecognition.test`/`dynamicQuery.test` + `centralityAlgo`/`communityAlgo`/`pathSearchAlgo`/`fusionMetrics`/`decisionModel`/`modelingGraphBuilder`/`integrationSecurity`/`queryAssetDeepAnalysis`/`shareHistory`/`blacklistTrigger` selfcheck）。

## 2. 公共组件复用清单（先查 TS 沉淀，不新造）

> 真源：`agent-delivery/agent-handoffs/科技发展态势-TS/TS-demo-lumen复刻经验清单.md` §2.3。**第二处出现即封装**；封装件样式自含。

| 已沉淀 | KG 用途 |
|---|---|
| `PageTabFrame`（+page-tab-frame.css） | 指标页 3 Tab / 算法页 Radio 切换面板 / 服务页 3 Tab（demo WorkbenchTabs 对应物） |
| `StatCard` / KPI 行 | 四页 KPI 概览（demo `kg-kpi-card`/`serviceKpis` 对应物） |
| `chartOptions`（CHART_BASE/baseTooltip）+ `GraphChart` + `graphModel` | 分析页图谱画布/时序演化/全屏探索；服务页建模网络图/图表构建；算法页三算法可视化 |
| `InsightDetailDrawer` | 指标页黑名单详情（demo 同名引用）、分析页智能分析下钻 |
| `MetricSpecHint`（D9 ⓘ）/ `MockBadge`（🧪） | 每个统计数字旁（demo `MetricInfo`→MetricSpecHint、`MockBadge` 直接对应） |
| `ExportFlowPanel` / ExportButton 语义 | 服务页分享清单导出 / 深度分析报告导出 |
| `defineApi` 双轨 + `request.ts` + `models/*.ts` 纯函数派生层 | `src/api/knowledgeGraph.ts` + `src/views/knowledge-graph/models/` |
| mock modules 机制（`setupMocks`/register） | `src/mock/modules/knowledgeGraph*.ts` |

**KG 不需要**：TiandituMap/UnifiedLeafletMap（四页无地理落点）。
**KG 模块私有件**（`views/knowledge-graph/components/`，≥2 处出现才封装）：`KgL6SectionTitle`（sr-only 规则 scoped 补 1px 裁剪，TS-M1 教训）、KPI 卡变体、算法面板族外壳、分享操作下拉（Dropdown 复合动作）等。

## 3. 任务拆分（registry 建单蓝图）

### 3.1 接口侧（1 张大单，human:李伟 自行拆分）

| ID | 任务 | 说明 |
|---|---|---|
| BE-KG-CONTRACT-01 | 科技知识图谱 — Java 接口契约定义与数据需求评审（四页 55 叶，出 API-KG 文档） | 以本文 §4「接口用途与数据需求」为输入；路径/DTO/枚举由 Java 侧主导定义；**契约定义 → 实现 → 数据对接的内部拆分、排期由 human:李伟 自行决策建单**（参照 DR/TA 模式） |

### 3.2 前端侧（基座 1 单 + 整页 4 单，Epic：E-FE-KNOWLEDGE-GRAPH）

| ID | 任务 | demo 真源（行数） | 体量 |
|---|---|---|---|
| FE-KG-S01 | 模块基座：路由挂接（menu.ts graph 组 4 项换真实组件）/四页页壳/mock 种子冻结（mockData.js 43KB）/api 双轨/kg-* style token 抽取/D9 挂点盘点 | `mockData.js` + `style.css`(21KB) + `KgL6SectionTitle` + `kgL6Functions.js` | M |
| FE-KG-01A | 分析展示整页复刻（8 叶）：动态查询/数据过滤/多维分析/交互式可视化（graph+全屏）/时序演化/模式识别/预测/分类聚类/智能推荐（智能分析中心 Hub） | `AnalysisDisplay.jsx`(677) + `KgIntelligenceHub.jsx`(364) + `kgIntelligence.js`(17KB) + `graphFilter.js`(4KB) + 3 test.mjs | L |
| FE-KG-02A | 指标展示整页复刻（15 叶）：告警条 + KPI 行 + 3 Tab——黑名单触发（监测指标/专家规则/触发记录/黑名单库/通知联动/审计日志）/融合统计指标（整合/权重三场景/相关性/一致性/综合评分）/优化决策模型（动态指标/规则联合/算法选择/训练历史/风险预警/反馈闭环） | `IndicatorDisplay.jsx`(165) + `BlacklistTriggerPanel`(16KB) + `FusionIndicatorsPanel`(15KB) + `OptimizeDecisionPanel`(17KB) + `fusionMetrics`/`decisionModel` + 4 selfcheck | L |
| FE-KG-03A | 算法展示整页复刻（15 叶）：三算法切换——路径搜索（多算法/最优路径/多样性/场景化/交互查询）/中心性（度/紧密/中介/PageRank/综合）/社群发现（多算法/结构识别/属性分析/演化追踪/可视化划分）；算法层移植 `models/*.ts` 纯函数 + 🧪 | `AlgorithmDisplay.jsx`(51) + `PathSearchPanel`(343)+`pathSearchAlgo`(17KB) + `CentralityPanel`(838)+`centralityAlgo`(16KB) + `CommunityPanel`(421)+`communityAlgo`(18KB) + 4 selfcheck | L |
| FE-KG-04A | 服务展示整页复刻（17 叶，XL）：KPI 行 + 3 Tab——图分享（一键分享/多格式导出/链接权限/嵌入预览/撤回恢复/历史追溯/同步通知中心）/图查询（智能搜索/多维筛选/列表·网格·缩略图三视图/详情预览/历史收藏 + 深度分析抽屉）/图分析集成（多源 ETL/智能建模工作台/图表构建/实时监控[D2 轮询]/决策联动/权限审计） | `ServiceDisplay.jsx`(1624) + 分享族 4 件（`shareHistory`/`kgShareExport`/`kgShareRegistry`/`kgShareSync`）+ 集成族 4 面板 + `modelingGraphBuilder` + 6 selfcheck/test | XL |

依赖：`FE-KG-01A/02A/03A/04A` depends_on `FE-KG-S01`；FE 单不依赖 BE 契约（mock 先行，契约冻结后联调，对齐 TS/DR/TA 模式）。

### 3.3 批次

| 批次 | 内容 | 备注 |
|---|---|---|
| 批 1 | FE-KG-S01 + FE-KG-01A ＋ BE-KG-CONTRACT-01 启动 | 基座 + 分析页（graph 全屏/智能分析全能力试点）可验；契约评审前置 |
| 批 2 | FE-KG-02A + FE-KG-03A | 两个「三面板 Tab 族」页，复用批 1 PageTabFrame/KPI 沉淀 |
| 批 3 | FE-KG-04A + 联调收尾 | 最大件（1624 行 + 分享状态机族）单独排；契约冻结后真机联调 |

FE 合计 ≈ 24–30 工日；每批独立上 K8s dev 验收。

## 4. 各页 FE 拆分与 BE 接口用途（契约输入，路径由 Java 定）

> FE 每单 DoD 统一：与 demo 逐区块截图比对（五件套）、Design token、D9 ⓘ/🧪、观测头、test/selfcheck.mjs 按断言语义摘选移植最小自检、`pnpm type-check` 0 错 + 自检 + `pnpm build` 三绿、**完工停本地工作区等 human:孔东 人工验收**（2026-10-20 闸门），不自动 commit/push。

### 分析展示（seq 400–407，8 叶）
- FE：动态查询（关键词/实体属性/时间范围 + 查询历史）/ 数据过滤（实体类型/关系类型/领域/地域多维筛选）/ 多维切片（总览/领域/机构/作者 Segmented→a-radio-button）/ 交互式可视化（ECharts graph network 视图 + 节点选中列表 + 全屏探索 Modal[Teleport]）/ 时序演化（line+bar + dataZoom）/ 智能分析中心（模式识别/异常检测/趋势预测/聚类分析 insight 卡 + InsightDetailDrawer 下钻 + Tab 高亮回跳）/ 动态 KPI 行
- BE 接口用途：① 图谱节点/边目录查询（类型/字段/地域过滤 + 分页）② 切片聚合（领域/机构/作者维度统计）③ 时序演化序列（按年实体/关系计数）④ 智能分析结果（模式/异常/预测，真算走 Python `/internal/*`）⑤ 查询历史（写接口）

### 指标展示（seq 408–422，15 叶）
- FE：实时告警条 + KPI 行（活跃告警/融合指标数/模型准确率/已处理事件）+ 3 Tab：黑名单触发（图谱监测指标卡/专家规则库表/触发记录表 + 详情抽屉[图谱指标/规则判别/自动拦截联动三段]/黑名单库/通知联动/审计日志）；融合统计指标（指标整合列表/权重配置三场景预设/两两相关系数/一致性检验/评估对象综合评分）；优化决策模型（动态指标卡/专家规则联合/算法选择/训练历史表/风险预警/反馈闭环 Timeline）
- BE 接口用途：① 告警与 KPI 统计 ② 黑名单触发记录/黑名单库/通知/审计日志（含写：确认/复核）③ 融合指标定义/权重场景/相关性/一致性/评分 ④ 决策模型动态指标/训练历史/风险预警/反馈（含写：反馈提交）

### 算法展示（seq 423–437，15 叶）
- FE：三算法 Radio.Group 切换：路径搜索（起点终点选择/多算法[BFS/最短路径/权重优先]/路径结果列表 + graph 高亮/多样性对比/场景化标签）；中心性（算法维度切换[度/紧密/中介/PageRank]/结果排行表 + 对比图/节点详情）；社群发现（算法切换[Louvain/标签传播]/社群结构图/属性特征分析/演化追踪）
- **算法层移植为 `models/*.ts` 纯函数 + 🧪「演示级，未接算法仓」**（D1）；真实算法 Python 化归 BE 契约 + 算法中台
- BE 接口用途：① 图算法执行（路径搜索/中心性/社群发现，Java→Python `/internal/*`）② 算法结果查询与缓存 ③ 图谱数据快照（算法输入子图）

### 服务展示（seq 438–454，17 叶）
- FE：KPI 行（serviceKpis 含 metric_id）+ 3 Tab：图分享（一键分享 Modal[名称/类型/格式/平台/权限/同步开关]/多格式导出 png·pdf·html·xlsx/链接权限面板[复制/二维码/有效期/密码]/嵌入预览下载/撤回恢复/操作历史追溯时间线/实时同步通知中心 Drawer）；图查询（AutoComplete 关键词智能搜索 + 查询历史/时间范围·实体类型·业务线·发布方·标签多维筛选/列表·网格·缩略图三视图[AssetThumb SVG 族]/资产详情预览抽屉/查询历史与收藏 + QueryAssetDeepAnalysisDrawer 深度分析）；图分析集成（多源接入 ETL 面板/智能建模工作台[实体类型勾选·自定义·标签·关系定义·Steps 四步·AI 抽取开关·网络化展现]/图表构建[bar/line/pie 切换]/实时监控轮询[D2]/决策联动表/分级权限与安全审计面板[useIntegrationSecurityState]）
- BE 接口用途：① 分享 CRUD（创建/撤回/恢复/导出计数）+ 访问令牌校验 ② 分享操作日志与通知（写）③ 查询资产目录与检索（多维筛选 + 分页）④ 收藏/查询历史（写）⑤ ETL 数据源清单与任务状态 ⑥ 实时监控统计（轮询）⑦ 权限与审计日志查询

## 5. 避坑清单（开工必读，真源：TS 复刻经验清单 + KG 特有）

1. **Arco 通用**：`#option="{ data }"` 插槽签名；`<label>` 禁包裹 `a-select`；cascader 多选标准 + `allow-clear`；图标显式 import（`@arco-design/web-vue/es/icon`）；控件 32px/圆角 4px；年份范围 `a-range-picker mode="year"`。
2. **KG 特有组件映射**：antd `Segmented`（分析页切片、服务页视图切换）→ **Arco Vue 无对应件，用 `a-radio-group type="button"`**；`Space.Compact` → `a-input-group`；`Statistic` → 仓内 `StatCard`；antd `Steps`/`Timeline`/`Dropdown` → `a-steps`/`a-timeline`/`a-dropdown` 均有对应。`a-progress` percent 是 0–1（antd 0–100 需 /100）；`a-tag` 需样式层对齐 antd 视觉（height:auto/4px 圆角）。
3. **算法纯函数层**：`pathSearchAlgo`/`centralityAlgo`/`communityAlgo`/`kgIntelligence` 移植 `models/*.ts` 保持确定性种子与 demo 断言语义，selfcheck.mjs 一并移植；UI 挂 🧪。
4. **分享状态机族**（`shareHistory`/`kgShareRegistry`/`kgShareExport`/`kgShareSync` 4 件）是独立纯函数模块，整块移植不拆散；写操作 localStorage 会话级（D3）。
5. **布局/渲染**：全屏图谱 Modal `Teleport to body`；图表容器显式高度防 init 0 高死锁；`v-if` 切换图 + flex 容器加 `flex: 0 0 auto` + 定高；新图型查 `src/config/echarts.ts`（已全量在册）。
6. **`kg-*` 样式自含**：demo `style.css` 按选择器命中规则整块抽取进 `styles/demo-knowledge-graph.css`；antd 专有规则 scoped 层 Arco 等价替换；封装件复用他页类名必裸奔。
7. **数据/状态**：首屏同步初值防白屏；mock 种子冻结；`USE_MOCK=false` 零 fixture；写操作演示态不替 BE 拍板。
8. **工程**：类型门一律 `pnpm type-check`（vue-tsc 空跑教训）；表格操作列按钮防压缩；多选标签 `:max-tag-count`；状态机移植保留最小自检；交付三绿；**完工停本地等人工验收**。

## 6. 风险与跟踪

| # | 风险 | 动作 |
|---|---|---|
| R1 | 算法真算（Python）排期未定，FE 演示算法与真算结果口径不一 | D1 照 demo 演示 + 🧪；BE-KG-CONTRACT-01 内登记 Python 算法需求；真算上线后前端只换数据源不改 UI |
| R2 | 服务展示体量最大（1624 行 + 分享状态机族）压批 3 | 批 1/2 沉淀的 Tab 框/KPI/表格件最大化复用；必要时批 3 增员或拆 04A 为 04A+04B |
| R3 | 服务展示曾有 `FE-DISPLAY-KG-SERVICE-ALIGN-L01`（demo 侧合规对齐，review 态） | 复刻以 demo 当前 HEAD 为真源；该单产物若已合入 demo 则已包含在真源内，无需单独处理 |
| R4 | metric 正名：demo 种子 metric_id（`M_KG_*` 系）是否已入 metric-registry | S01 盘点；未入册的按 D9 流程正式登记或对齐已登记 id（handoff 注明） |

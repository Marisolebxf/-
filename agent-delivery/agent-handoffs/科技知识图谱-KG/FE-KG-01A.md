# FE-KG-01A · 分析展示 — 整页复刻（动态查询/数据过滤/多维分析/交互式可视化/时序演化/智能分析中心 Hub）

> demo 真源：`repos/demo-ui-science/src/pages/tech-knowledge-graph/AnalysisDisplay.jsx`(677) + `KgIntelligenceHub.jsx`(364) + `kgIntelligence.js`(17KB) + `graphFilter.js`(4KB)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（4h 锁，2026-11-04 22:32 起） |
| 说明 | 认领时依赖 FE-KG-S01 为 `integration`（三绿+浏览器验证过、mock/api/样式基座已可用于本单）；基座产物全部核对后开工 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 派单 DoD 未显式标强度，按日常 feature = full。未用 YAGNI 跳过 D8 token / D9 ⓘ🧪 / 可观测埋点 / 架构铁律（ECharts graph 禁 G6 直连）。算法层按规划 D1「照 demo 前端演示 + 🧪」，未自造真算 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 问题清单

- 无阻塞。metric 正名沿用 S01 盘点结论（见下方 D9）

## 修改内容

**仓：`repos/lumen-ui-science-pc`（dev，完工停本地工作区等孔东人工验收，未 commit/push）**

1. **算法层移植**（`src/views/knowledge-graph/models/`）：
   - `kgTypes.ts`：消费端契约类型（KgNode/KgEdge/KgIntelligenceResult 等）
   - `graphFilter.ts`：`filterKnowledgeGraph`/`sliceKnowledgeGraph`/`buildTimelineSeries` + `bindKeywordScenePresets`（场景词预设由页面注入，保持模块纯函数、无种子 import——node strip-types 直跑先例兼容）
   - `kgIntelligence.ts`：`discoverEmergingTechPath`/`detectPatternsAndAnomalies`/`buildTrendPredictions`/`clusterEntities`/`recommendResources`/`runKgIntelligence`/`buildPathMiniChartOption`/`anomaliesToInsightCards`，逻辑与 demo 断言语义逐行冻结（含 DEMO_ANOMALIES 兜底演示数据）
2. **智能分析中心 Hub**（`components/KgIntelligenceHub.vue`）：四 Tab（自动模式识别[潜在模式/关联路径发现+mini graph/异常点表+线索 Tag 行/变化趋势图]/预测分析[markLine 历史分界+三序列]/分类与聚类[簇散点+簇列表]/智能推荐[匹配度 Progress 0-1 /100 修正]）；Tab 高亮回跳（highlightSignal → 切回 pattern）；面板头 🧪 MockBadge ×4
3. **图谱画布**（`components/KgGraphCanvas.vue`）：ECharts graph force（demo G6 → 铁律 ECharts；类型着色/尺寸=√value*3+12/选中节点蓝环高亮/roam/邻接 emphasis/空态 a-empty；容器显式高度）
4. **整页**（`analysis/index.vue`，替换 S01 页壳）：
   - §400 动态查询：场景词 a-select（种子 dynamicQueryKeywordOptions 4 词）+ 实体属性（类型/领域/地域）+ 时间范围 Segmented→a-radio-group type=button（全部/近1年/近3年/自定义+a-slider range）+ 即时反馈行 + 查询历史（会话态 ≤8，D3 不替 BE 拍板）
   - §401 数据过滤：关系类型/作者 + 视图切换（网络图/列表/统计图）+ 重置/导出（JSON 摘要下载）
   - §402 多维切片：全景/机构/领域/时间演化/合作网络 Segmented→radio-button + 值选择器
   - §403 交互式可视化：KgGraphCanvas 500px + 列表视图 a-table（行点击=节点详情）+ 统计图视图（机构 Top8 横向 bar）+ 全屏 a-modal（92vw/620px/unmount-on-close）+ 右侧智能分析洞察卡（模式识别/异常检测，点击下钻）+ 领域分布 pie
   - 时序演化：line（实体 areaStyle）+ bar（关系）+ dataZoom inside+slider
   - 动态 KPI 行：匹配实体/匹配关系/覆盖领域/检索反馈（ⓘ 占位 metric_id + KgKpiCard 自带 🧪）
   - 详情下钻：InsightDetailDrawer（复用仓内结构化组件，map-object kind 承载 KG 实体五段：tags/summary/metricCards/sections/actions）
5. **自检**（`analysis/FE-KG-01A.test.mjs`）：demo 四份 test.mjs 断言语义摘选移植（graphFilter/dynamicQuery/kgIntelligence/patternRecognition）+ FE-KG-01A 接线组（Hub/画布/全屏/抽屉/ⓘ/🧪/Arco 全替换/禁 Math.random·Date.now）；`node --experimental-strip-types` 直跑 models+seed
6. **样式**：demo kg-\* 类体系已由 S01 整块抽取（`styles/demo-knowledge-graph.css`）直接命中；页内新增少量补充类（kg-filter-grid/kg-analysis-card 等，语义对齐 demo 行内样式）

## 测试结果（三绿 + 浏览器目检）

- `pnpm type-check`（vue-tsc --build）：**0 错**
- `node src/views/knowledge-graph/analysis/FE-KG-01A.test.mjs`：**5 组全绿**
- `node src/views/knowledge-graph/kg.selfcheck.mjs`（S01 基座防回归）：**全绿（9 组）**
- `pnpm build`：**绿**（48s，无本页相关告警）
- 浏览器目检（dev :5200 `/graph/graph-analysis`，admin 登录）：
  - 标题「分析展示」；KPI 4 卡、筛选卡 2 张、ECharts 7 实例
  - Hub 四 Tab 文案齐（自动模式识别/预测分析/分类与聚类/智能推荐）；模式列表 10 行；算法标注 4 条（Isolation Forest/LSTM+Prophet/Louvain/协同过滤）；🧪 MockBadge ×5（Hub 头 1 + Tab 4）；空态 0
  - 关键词下拉选项 = 种子 4 场景词；实体类型字典渲染正常
  - 时序图 canvas、洞察卡 ×4、图谱画布 canvas 均在 DOM
  - 截图：`kg-analysis-top.png` / `kg-analysis-hub.png` / `kg-analysis-pattern.png` / `kg-analysis-bottom.png`（本机 Temp cursor/screenshots/）

## D9 数据血缘（按 data-lineage-policy §2.3 执行契约）

- 每个统计数字旁 ⓘ：KPI 行经 KgKpiCard `metricId` 挂 MetricSpecHint（占位 id：`M_KG_ANALY_MATCHED_NODES` / `M_KG_ANALY_MATCHED_EDGES` / `M_KG_ANALY_COVERED_FIELDS` / 图谱画布卡 `M_KG_ANALY_GRAPH_VIZ`；**均为占位，未入 metric-registry，待 data-agent 正名对齐 `M_SCIUI_KGANALY_*` 系**——沿用 S01 handoff 盘点口径）
- Mock 态 🧪：KgKpiCard 自带 + Hub 面板头 ×4 + 异常点演示行「演示数据」Tag（demo isDemo 语义）
- 不伪闭合：算法面板标注「Wave0 Mock / 演示」，预测标虚线分界，异常兜底行明示演示数据

## 架构合规自检（公约 §2 逐条）

- ✅ 调用链：前端不直连图谱服务/不感知 nGQL；数据经 api/knowledgeGraph.ts 双轨（mock/网关占位 contractPending）
- ✅ D8：Arco 全替换（Segmented→a-radio-group type=button / Select→a-select / Table→a-table / Modal→a-modal / Progress 0-1 修正 / 图标显式 import IconArrowRise 等）；token 走 chartOptions CHART_BASE + 主色 #165dff
- ✅ D12：零 demo 仓依赖；mock 种子冻结自 demo（S01 已逐行校验）
- ✅ 图谱铁律：demo G6 → ECharts graph（复用 echarts.ts 注册），未引 @antv/g6 新链路
- ✅ 可观测：trackKgInteraction 埋点（page-mounted/关键词/重置/导出/节点点击/洞察点击/高亮/推荐应用/全屏）
- ✅ 互斥 display 不叠同一节点（v-if 三视图切换）；fixed 弹层 Teleport（Arco Modal/Drawer 默认 body）

## 遗留风险

- metric_id 占位正名（`M_KG_ANALY_*` 4 条 + S01 已盘点 `M_KG_SVC_*`）待 data-agent 入 registry
- 智能分析为前端 JS 演算（规划 D1 已拍板「演示 + 🧪」）；Python 真算接入由 BE-KG-CONTRACT-01 登记，届时前端只换数据源
- demo `knowledgeGraphKPIs`（静态全库 KPI）demo 分析页未消费，lumen 侧头部 KPI 行用动态 KPI（demo dynamicKpis 语义），与 demo 一致
- Arco a-table `showTotal` 用布尔（仓内先例），与 demo「共 N 条」文案略简——视觉差异微小，走查如需逐字可后补

## CI/CD（必填）

- 分支：`dev`（lumen-ui-science-pc，**未 commit/push——孔东监管限定：完工停本地工作区等人工确认**）
- commit：—（待孔东验收后由监管会话 commit）
- pipeline：—（同上）
- dev 验证：本机 `pnpm dev` :5200 目检通过（见测试结果）

## 涉及文件

- `src/views/knowledge-graph/analysis/index.vue`（重写，S01 页壳 → 整页）
- `src/views/knowledge-graph/analysis/FE-KG-01A.test.mjs`（新增）
- `src/views/knowledge-graph/components/KgIntelligenceHub.vue`（新增）
- `src/views/knowledge-graph/components/KgGraphCanvas.vue`（新增）
- `src/views/knowledge-graph/models/kgTypes.ts`（新增）
- `src/views/knowledge-graph/models/graphFilter.ts`（新增）
- `src/views/knowledge-graph/models/kgIntelligence.ts`（新增）

## 2026-11-05 孔东走查调整（第 2 轮，任务仍处 integration 停本地）

用户走查反馈 4 点，处理如下：

1. **去掉顶级 tab「图谱分析」**：该页仅单占位页签无切换语义，移除 `PageTabFrame` 包裹（含 TABS/activeTab），`KgPageHeader` 标题 + 主内容直挂。`kg.selfcheck.mjs` §7 断言同步调整（analysis 页不再要求 PageTabFrame/#header，其余三页不变）
2. **KPI 指标卡行下移**：由页顶 `#header` 插槽移至「数据过滤与筛选」卡（§2）与「多维度分析」切片卡（§3）之间——KPI 数字本就实时联动筛选结果，位置贴近筛选区；新增 `.kg-analysis-kpi-row`（padding 0 + margin-bottom 16px）
3. **「网络图/列表/统计图」radio 用途解答**（未改码）：下方「交互式可视化」卡的**视图模式切换**（`viewMode`），分别渲染 ECharts 力导向网络图 / a-table 实体列表 / 机构 Top8 统计柱图
4. **洞察卡 hover/选中效果 + 横向滚动条修复**：根因 = demo 真源 `.kg-analysis-card:hover { transform: translateX(4px) }`（styles/demo-knowledge-graph.css L429）在窄列把卡片右移 4px 撑出滚动区。本页以更高 specificity（`.kg-analysis-page .kg-analysis-card`）覆盖为阴影/边框 hover 反馈并 `transform: none`；`.kg-insight-scroll` 锁 `overflow-x: hidden`；新增选中态 `is-active`（点击卡片 → 蓝边 #165dff + #f0f5ff 底 + 阴影，`selectedAnalysisId` 状态驱动，demo 无此态系走查新增）

验证：三绿复跑全过（type-check 0 错 / FE-KG-01A.test.mjs 5 组 / kg.selfcheck.mjs 9 组 / build 绿）；浏览器 CDP 目检：页签条消失、KPI 行位于筛选卡(bottom 403px)与切片卡(top 547px)之间、洞察区无横向滚动条（clientW=scrollW=359）、卡片 computed transform=none、is-active 点击后 bg=#f0f5ff/bd=#165dff、视图切换（网络图↔列表）功能正常、页面无可见横向滚动条。



- actual_tokens ≈ 132k（读 demo 真源 + 基座核对 + 实现 + 三绿 + 目检）+ 2026-11-05 走查调整 ≈ 10k
- model_used：glm-5.3（Cursor agent 会话）
- actual_cost ≈ $1.7；cost_warn：否

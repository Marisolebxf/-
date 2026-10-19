# 科技数据资源（DR）模块开发规划与任务拆分

- 时间：2026-10-19 定稿
- 作者：agent:coordinator-agent（规划；对齐 TS 模式，监管：human:孔东 / human:李伟）
- 范围：展示系统「科技数据资源」大模块 4 个视窗（总体 / 接入 / 主题 / 应用）正式开发
- 工作仓：`repos/lumen-ui-science-pc`（正式）· `repos/demo-ui-science`（原型只读对照）
- 人员：前端 human:孔东 · 接口 human:李伟（自行拆分 BE 内部任务）
- 需求真源：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.1.4.4；SRS 分册 `bid-reference/srs/02-科技信息展示系统/科技数据资源/*.md`
- 原型真源：`demo-ui-science/src/pages/data-resources/`（四窗 jsx ~3.9k 行 + `mockData.js` 1680 行冻结种子 + 8 个 `*.test.mjs` 状态机）
- 模块定位：**运营视窗**（表格 + 状态图密集），非七要素探索页；CROSS-KG §8.7 **默认不扫全图**
- 本文用途：模块开工真源；task-registry 建单依据；FE/BE 契约对齐底稿

---

## 0. 待拍板决策项（开工前由监管人拍板，默认倾向先行）

| # | 决策项 | 背景（原型核对报告 2026-10-10，Owner human:郭万迎） | 默认倾向 |
|---|---|---|---|
| D1 | 需规遗漏/错位项是否在 lumen 补齐 | 总体视窗 seq 333 报表导出未挂载、seq 343 缺异常告警、seq 344 指标错位（质量五维替代连接活跃度/调用频率/失败率）；接入视窗 356 缺业务专题/项目方向、367 缺数据表维度；应用视窗 384 缺调用时间/频率/接口/业务系统 | **照 demo 复刻为准**（已评审页铁律）；核对报告 B 清单项列为「评审补齐 backlog」，待孔东逐项拍板后另立补齐单，不在整页复刻单内顺手改 |
| D2 | 超范围指标去留 | 四窗共 19 处超范围（资源利用率/质量五维/行业均值/活跃用户/QPS/并发峰值等），demo 已评审含这些项 | **照搬 demo**（对齐已评审页；后续以甲方验收口径回归） |
| D3 | 应用视窗「实时应用监控」轮询口径 | demo 有实时监控卡片（QPS/响应/成功率/告警） | 对齐 TS D2：**轮询 + 定时刷新**（间隔常量化、页面不可见暂停、卸载清理，首版 30s） |

## 1. 全局技术约束（4 视窗统一遵守）

1. **UI 栈**：Vue3 `<script setup>` + Arco Design Vue + UnoCSS；token 按 `Design.md`（主色 `#165DFF`、正文 14px、控件 32px、圆角 4px）。**Arco 优先**（demo 原生 `<select>`/`<input>` 必换 `a-select`/`a-input`；Arco bug 修根因不回退原生）。
2. **复刻五件套**：布局、交互、样式、评审、Mock 开关数据；禁止以「更简」另起 UI；互斥 `display` 不叠同一节点。
3. **Mock 统一开关**：种子**冻结自 demo `mockData.js`**（确定性生成、禁 `Math.random`、派生链禁手写），头注释标真源 + 同步任务 ID；`USE_MOCK=false` 零 fixture 渲染（D12）。
4. **调用链**：前端 → Java REST → 只读运营库/日志（设计文档 §5：`/display/v1/data-ops/**` 倾向，最终路径由 Java 侧定义）；Java 聚合、不写算法、不直连 nGQL、**运营日志不写入 Nebula**。
5. **权限与频控**：本模块权限点**独立于态势页**，严于业务展示；导出行数/频控照 demo（详细设计 §6）。
6. **D9 血缘**：运营统计指标同样要 ⓘ（MetricSpecHint）+ metric_id（可占位）；Mock 态 🧪 MockBadge；缺数据不伪闭合。
7. **可观测**：pageview + `X-Trace-Id`/`traceparent` 注入（沿用仓内已有 observability 机制，不新造）。

## 2. 公共组件复用清单（先查 TS 沉淀，不新造）

> 真源：`agent-delivery/agent-handoffs/科技发展态势-TS/TS-demo-lumen复刻经验清单.md` §2.3。**第二处出现即封装**；封装件样式自含。

| TS 已沉淀 | DR 用途 |
|---|---|
| `PageTabFrame` / page-tab-frame.css | 四视窗 Tab 页框（视窗内 L5 分组 = Tab） |
| `StatCard` / `KpiDeck` | 各窗 KPI 概览（demo KPICard/StatCard 对应物） |
| `chartOptions`（CHART_BASE/baseTooltip）+ `src/config/echarts.ts` | line/bar/pie/radar/gauge/graph 全覆盖 DR 图表；**新图型先查按需注册** |
| `MetricSpecHint`（D9 ⓘ）/ `MockBadge`（🧪） | 每个统计数字旁 |
| `ExportFlowPanel` / ExportButton 语义 | 各窗导出（355/399 等）；DR 复用导出流，角色/频控策略照 demo |
| `defineApi` 双轨（mock/网关）+ `request.ts` | `src/api/dataResources.ts` |
| `models/*.ts` 纯函数派生层 + `*.test.mjs` 最小自检 | demo 8 个 test.mjs 按断言语义摘选移植 |

**DR 不需要**：TiandituMap（四视窗无地理落点）、InsightDetailDrawer L6 五段（DR 详情抽屉按 demo `DetailDrawer.jsx` 简化结构，属模块私有件放 `views/data-resources/components/`）。
DR 模块私有件（≥2 处出现才封装）：视窗 KPI 行、来源结构对比卡、问题资源统计报表、调用趋势分析块等——先落模块目录，跨模块复用才升 `src/components/`。

## 3. 任务拆分（registry 建单蓝图）

### 3.1 接口侧（1 张大单，human:李伟 自行拆分）

| ID | 任务 | 说明 |
|---|---|---|
| BE-DR-CONTRACT-01 | 科技数据资源 — Java 接口契约定义与数据需求评审（四视窗，出 API-DR 文档） | 以本文 §4「接口用途与数据需求」为输入；路径/DTO/枚举由 Java 侧主导定义；**契约定义 → 实现 → 数据对接的内部拆分、排期由 human:李伟 自行决策建单**（参照 TS：BE-TS-CONTRACT-02/IMPL-01/DATA-01 模式） |

### 3.2 前端侧（基座 1 单 + 视窗页面集 4 单）

| ID | 任务 | demo 真源 | 体量 |
|---|---|---|---|
| FE-DR-S01 | 模块基座：路由挂接/四窗页壳/公共件盘点接入/mock 种子冻结/api 双轨/D9 挂点 | `mockData.js`(1680 行) + `style.css` token 抽取 | M |
| FE-DR-01A | 总体视窗整页复刻（17 L6，4 L5 分组） | `OverviewWindow.jsx`(716) + BigDataCenterDetail(532)/ResourceSourceAnalysisDetail(624)/SemanticThemeAggregation(221)/ResourceAppSubjectList(166)/CumulativeCallTrendAnalysis(181) 等 | L |
| FE-DR-02A | 接入视窗整页复刻（21 L6，5 L5 分组） | `AccessWindow.jsx`(665) + AccessSourceAnalysisDetail(582)/AccessDataResourceDetail(523)/AccessHistorySituation(430)/AccessResourceDetailQuery(278) + accessMultiFilter 状态机 | L |
| FE-DR-03A | 主题视窗整页复刻（8 L6，2 L5 分组） | `ThemeWindow.jsx`(685) + themeTableSchema/themeResourceMeta 状态机 | M |
| FE-DR-04A | 应用视窗整页复刻（24 L6，6 L5 分组） | `ApplicationWindow.jsx`(1273) + AssetApplicationBasicSummary(178) + businessAppFilter 状态机；实时监控轮询（D3） | L |

依赖：`FE-DR-01A/02A/03A/04A` depends_on `FE-DR-S01`；FE 单不依赖 BE 契约（mock 先行，契约冻结后联调，对齐 TS 模式）。

### 3.3 批次

| 批次 | 内容 | 备注 |
|---|---|---|
| 批 1 | FE-DR-S01 + FE-DR-01A ＋ BE-DR-CONTRACT-01 启动 | 基座 + 总体视窗可验；契约评审前置 |
| 批 2 | FE-DR-02A + FE-DR-03A | 接入/主题（表单检索密集，复用批 1 沉淀） |
| 批 3 | FE-DR-04A + 联调收尾 | 应用视窗最大（24 L6） |

FE 合计 ≈ 22–26 工日；每批独立上 K8s dev 验收。

## 4. 各视窗 FE 拆分与 BE 接口用途（契约输入，路径由 Java 定）

> FE 每单 DoD 统一：与 demo 逐区块截图比对（五件套）、Design token、D9 ⓘ/🧪、观测头、状态机 test.mjs 移植、`pnpm type-check` 0 错 + 自检 + `pnpm build` 三绿、push `origin/dev`。

### 总体视窗（seq 330–346）
- FE：KPI 概览（7 指标卡）/ 资源来源分析与详情（5 来源 + 结构 + 趋势 + 质量可靠性）/ 接入资源详情查询（元数据表）/ 多源整合分析（主题分布 + 归类）/ 大数据资源中心详情（主题库分类 + 深度浏览 + 关联检索 + 实时更新监控）/ 资源关联关系（知识图谱 canvas + 节点边分析 + 关联导航 + 语义聚合）/ 资源应用状态（系统监控 + 接口跟踪 + 主体列表 + 累计调用趋势）
- BE 接口用途：① 资源总览 KPI（类型数/总量/主题库数/数据源数/日调用量/活跃用户/利用率）② 来源结构分析（来源类别/组成/趋势/质量评估）③ 资源详情检索（元数据/学科/采集时间/更新频率/关联项目）④ 主题库目录与详情（分类树 + 更新动态）⑤ 关联关系图谱数据（节点/边，**非 Nebula 全图扫描**，运营库聚合）⑥ 应用状态监控（可用性/响应/告警）⑦ 主体列表与调用趋势

### 接入视窗（seq 347–367）
- FE：接入总览（完成度 KPI + 渠道占比 + 归集量统计 + 多维筛选）/ 来源分析详情（渠道归集量 + 属性展示 + 结构对比 + 分组 + 明细导出）/ 资源详情（主题归类 + 分区明细 + 多维检索 + 可视化面板）/ 历史接入（渠道表名记录 + 更新周期统计 + 趋势 + 历史检索）/ 问题资源（识别列表 + 复现与批量检索 + 分级优先级 + 统计报表）
- BE 接口用途：① 接入任务完成度统计 ② 渠道归集量与来源结构 ③ 资源属性明细（分区/主题/质量等级）④ 历史归集记录与更新周期分析 ⑤ 问题资源识别/分级/统计报表 ⑥ 明细导出（频控）

### 主题视窗（seq 368–375）
- FE：主题库分类浏览（学科树 + 标签）/ 多维检索筛选 / 资源分布可视化 / 资源详情与元数据 / 数据库详情（元属性 + 表结构字段 + 关联关系图谱 + 智能搜索）
- BE 接口用途：① 主题库分类树与统计概览 ② 数据库/数据集列表与多维筛选 ③ 数据集元属性详情 ④ 数据表结构与字段 schema ⑤ 数据集关联关系（引用/衔接/交叉）

### 应用视窗（seq 376–399）
- FE：资产应用总览（排行榜 + 详情视图 + 基本情况汇总 + 多维筛选 + 实时监控轮询[D3]）/ 资源使用详情（字段属性 + 来源部门 + 筛选 + 可视化报表）/ 主题被调用（基本信息统计 + 用户与系统追踪 + 趋势周期 + 排行对比）/ 供应方被调用（部门归集 + 累计次数 + 频率趋势 + 多维展示）/ 需求方调用详情（名称归集 + 次数 + 行为分布 + 检索筛选）/ 业务应用调用详情（应用归集 + 次数 + 检索筛选 + 明细导出报告）
- BE 接口用途：① 资产应用排行与详情 ② 实时监控统计（轮询）③ 资源使用详情与部门统计 ④ 主题/供应方/需求方/业务应用四类调用统计（累计 + 趋势 + 多维）⑤ 调用明细检索与导出报告（频控）

## 5. 避坑清单（开工必读，真源：TS 复刻经验清单）

1. **Arco**：`#option="{ data }"` 插槽签名；`<label>` 禁包裹 `a-select`（闪开即关）；cascader 多选用标准多选 + `allow-clear` 禁自绘 footer；图标显式 import；年份范围 `a-range-picker mode="year"`。
2. **封装**：第二处出现即封装；封装件样式自含（复用他页类名会裸奔）；先查 §2 清单不新造。
3. **渲染**：fixed 弹层 `Teleport to body`；图表容器显式高度防 init 0 高死锁；新图型查 `src/config/echarts.ts` 按需注册。
4. **数据**：首屏同步初值防白屏；dev slot props 失效用数据签名 key 规避；写操作演示态不替 BE 拍板。
5. **工程**：类型门一律 `pnpm type-check`（vue-tsc 空跑教训）；表格操作列按钮防压缩变形；多选标签 `:max-tag-count` 折叠；状态机移植保留最小自检 test.mjs；交付三绿。
6. **DR 特有**：权限点独立于态势页（契约含权限/频控）；运营日志不进 Nebula；图谱区块是运营库聚合数据（ECharts graph），不走图谱服务。

## 6. 风险与跟踪

| # | 风险 | 动作 |
|---|---|---|
| R1 | D1 遗漏/错位项口径未拍板即开工 | 复刻单按 demo 为准；B 清单进评审补齐 backlog，孔东拍板后另立单 |
| R2 | 运营库/日志读面数据源未落 ADS 方案 | BE-DR-CONTRACT-01 内含数据需求评审，Mock 先行不阻塞 FE |
| R3 | 应用视窗体量最大（24 L6）压批 3 | 批 2 沉淀的检索表格件最大化复用；必要时批 3 增员 |

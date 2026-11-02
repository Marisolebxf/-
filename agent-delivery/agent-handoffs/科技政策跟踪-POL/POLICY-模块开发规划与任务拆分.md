# 科技政策跟踪（POL）模块开发规划与任务拆分

- 时间：2026-11-02 定稿
- 作者：agent:coordinator-agent（规划；对齐 TS/TA/DR/ACH 模式，监管：human:孔东 / human:李伟）
- 范围：展示系统「科技政策跟踪」大模块 **7 个四级页面**正式复刻开发（科创政策全景 / 政策分析评价 / 政策效果推演 / 智能政策库构建 / 智能政策拆解 / 多维政策对比 / 智能研报生成）
- 工作仓：`repos/lumen-ui-science-pc`（正式）· `repos/demo-ui-science`（原型只读对照）
- 人员：前端 human:孔东 · 接口 human:李伟（BE 只建 1 张契约单，内部拆分由李伟自决）
- 需求真源（两册）：
  - 原生 3 页：`bid-reference/srs/02-科技信息展示系统/科技政策跟踪/`（46 叶：全景 22 / 分析 13 / 推演 11，excel 200–245）
  - 核增 4 页：`bid-reference/srs/02-科技信息展示系统/政策对比功能升级（核增需求）/`（17 叶：治理 4 / 拆解 4 / 对比 4 / 研报 5）
- 原型真源：`demo-ui-science/src/pages/policy-tracking/`（≈24k 行：jsx/js/ts ≈20.7k + css ≈3.7k + 60 文件）；菜单经 `src/data.js` navGroups + `src/pageRouting.js` 现行绑定
- 契约输入：`agent-handoffs/政策模块-E7/`（PROD-POLICY-definition / DATA-POLICY-metric-seed / ALGO-POLICY-fullset / QA-POLICY-acceptance-report）；demo 侧核增验收 `agent-handoffs/展示系统-政策跟踪/DISPLAY-POLICY-GAP-AC-L01.md`（档 A 37 条能力 + 档 C 94 条闸门已过）
- 指标现状：POLICY 域 **35 个指标全部 D1=aligned、D4=mock**（28 个带 SRS refs；`metrics/registry/cfg_metric-POLICY-seed.yaml` + `metric-readiness-matrix-POLICY.yaml`，查询走 metric-registry MCP，禁直读）
- 本文用途：模块开工真源；task-registry 建单依据；FE/BE 契约对齐底稿

> 历史区分：`agent-handoffs/展示系统-政策跟踪/` 是 demo 侧 GAP 原型任务（DISPLAY-POLICY-GAP-AC-L01），不是 lumen 复刻规划；本文才是 lumen 侧开工真源。

---

## 0. 已定口径和待拍板决策项

| # | 决策项 | 结论 / 默认倾向 |
|---|---|---|
| D1 | 新增 4 菜单命名 | **照 demo 现名**：智能政策库构建 / 智能政策拆解 / 多维政策对比 / 智能研报生成。SRS 分册名「政策数据治理」与 demo 菜单名「智能政策库构建」为同页双名（`pageRouting.js` 保留双名映射）；permCode / 权限清单文档注明对应关系 |
| D2 | demo 权限试点（`POLICY_TOPIC_PERMS` Persona/Level/屏幕锁 + `PolicyRouteGuard`/`BlankMountedPage`） | **不复刻**（demo 演示装置）；lumen 走门户 permCode 门控。Q030（30 页级别+屏幕口径）仍 🟡 待甲方，期间不做级别限制 |
| D3 | 全景页体量（demo 5.5k+ 行） | **拆 2 单**（01A 检索主链路 / 01B 其余 Tab），对齐 TA-03A 画像页 XL 先例；执行时可按人力合单单交付 |
| D4 | 旧 topic「政策匹配」深链（demo `initialOpenMatch`） | 路由 query `?tab=match` 等价直达动向 Tab + 匹配弹窗；**不建菜单**（demo 侧同款语义：能力在全景「政策匹配与推送」，深链不进独立页） |
| D5 | 核增 4 页是否并单 | **按页拆 4 单**（对齐 ACH 模式）；共享 `policyPcData.js` 基座在 S01 冻结，4 单可并行；执行时可两两合并 |
| D6 | 高级检索 DSL 族（demo 为 TSX React 组件） | Vue 化重写（FilterPanel/ConditionBuilder/queryEngine/types），断言语义以 `queryEngine.group.test.mjs` 为准移植最小自检；**禁直接搬 TSX**（D12 隔离要求重写） |
| D7 | 写操作演示态（订阅/收藏/最近查询/对比会话槽/收件箱） | 会话级/localStorage 演示态，**不替 BE 拍板契约**；真实写回走 BE-POL-CONTRACT-01 升级项，偏离记 handoff（对齐 TA D6） |
| D8 | 核增 4 页分轨横幅（BoundaryBanner + ReviewOnly） | 评审层能力按仓 AGENTS.md **集中单目录**管理（现状 `src/components/lineage/` 组织方式，不散落各组件）；评审模式关闭后 DOM 零泄漏 |

## 1. 全局技术约束（7 页统一遵守）

1. **UI 栈**：Vue3 `<script setup>` + **Arco Design Vue** + UnoCSS；token 按 `Design.md`（主色 `#165DFF`、正文 14px、控件 32px、圆角 4px）。**Arco 优先**：demo 重度使用 antd（Select/Table/Tabs/Drawer/Steps/Tree/Rate/Progress/Collapse/Descriptions…），复刻全量换 Arco 对应件；Arco bug 修根因不回退原生。
2. **复刻五件套**：布局、交互、样式、评审、Mock 开关数据；禁止以「更简」另起 UI；互斥 `display` 不叠同一节点。
3. **Mock 统一开关**：种子**冻结自 demo `policy-tracking/`**（`policyData.js` 2378 行 + `policyPcData.js` 955 行 + `policyDetailContent.js` + `policyPanoramaGapMock.js` + `policy-metrics-catalog.json` + `policySubscription.js` 等；确定性生成、派生链禁手写、禁 `Math.random`，若 demo 种子含随机/时间函数须先定化并记 handoff），头注释标真源 + 同步任务 ID；`USE_MOCK=false` 零 fixture 渲染（D12）。
4. **图表**：ECharts 走仓内 `chartOptions`/`VChart` 按需注册（`src/config/echarts.ts` 已含 Map/Lines/Geo/Heatmap/Graph/Sankey 等，政策页所需图型已全覆盖，新图型先查再注册）；中国/深圳 choropleth 移植 `ensureChinaMap.js`/`ensureShenzhenMap.js` 的 geojson 注册机制（内联 geojson 或静态资源，禁运行时外网拉取）。
5. **调用链**：前端 → Java REST → Python `/internal/*` → 只读 ADS；路径/DTO/枚举**由 Java 侧（李伟）按 E7 handoff + 指标 seed 主导定稿**，前端不猜路径。D12：不指向任何 demo-* 服务。
6. **D9 血缘**：每个统计数字旁 ⓘ（`MetricSpecHint`）+ metric_id；POLICY 域 35 指标过渡态从 `metric-readiness-matrix-POLICY.yaml` 生成**只读镜像模块**（集中单文件，头注释注明真源路径 + 同步任务 ID）；`pending_hint` 缺口文案不前端硬编码；Mock 态 🧪 MockBadge；QPOL-01/03/05/07 口径 🟡 期间 UI 加 ⚠️ 角标（照 demo PendingBadge 语义）。
7. **可观测**：pageview + `X-Trace-Id`/`traceparent` 沿用仓内 observability 机制。
8. **demo 带自检的最小移植**：`PolicyPanorama.test.mjs` / `PolicyPcPages.test.mjs` / `policySubscription.test.mjs` / `PolicyContentDetailDrawer.test.mjs` / `displaySearchResultUtils.refine.test.mjs` / `DisplayAdvancedFilterPage.test.mjs` / `queryEngine.group.test.mjs` / `policyWorkbenchTabs.test.mjs` 按断言语义摘选移植（每单至少覆盖所改状态机）。

## 2. 公共组件复用清单（先查沉淀，不新造）

> 真源：`agent-handoffs/科技发展态势-TS/TS-demo-lumen复刻经验清单.md` §2.3。**第二处出现即封装**；封装件样式自含。

| 已沉淀（lumen） | POL 用途 |
|---|---|
| `WorkbenchLayout` / `PageTabFrame` | 页壳 + Tab 框（demo 7 页全用 WorkbenchTabs/工作台布局） |
| `MetricSpecHint`（D9 ⓘ）/ `MockBadge`（🧪） | 每个统计数字旁 |
| `common/StatCard` | KPI 卡（demo PolicyStatCard 语义等价，样式差异在模块内覆写） |
| `chart/` 族 + `chartOptions` | line/bar/pie/radar/gauge/graph/heatmap/lines/map |
| `export/ExportFlowPanel` | Excel/PDF/Word 导出挂槽（demo policyTrackingExport/policyPcExport 语义） |
| `workbench/FilterBar` | 检索筛选行基件（全景筛选条变体在模块内扩展） |
| `defineApi` 双轨 + `request.ts` + `src/mock/modules/*` | `src/api/policy.ts` + `src/mock/modules/policy*.ts` |
| 门户权限码机制（`menu.ts` navItem permCode） | 新增 4 菜单注册 |

**POL 模块私有件**（模块目录 `views/policy/` 内）：
- `components/`：PolicyStatCard（如与公共 StatCard 视觉差异大）、MetricSpecTrigger（D9 触发器，读模块指标镜像）、PendingBadge（QPOL 🟡 ⚠️ 角标）
- 检索族：SearchHub（智能/关键词/高级三模式）、FilterPanel+ConditionBuilder+queryEngine（DSL 布尔组合，Vue 化）、displayFieldLibrary（字段库）、结果工具（排序/二次筛选/分组）
- 详情抽屉：PolicyContentDetailDrawer（政策内容详情）
- 对比族：新旧对比 / 详情对比 / 部门对比 / 标杆比对 4 弹窗 + 对比会话槽
- 订阅族：订阅抽屉 + 我的订阅/收件箱
- 分析族：`analysis/` 9 组件（维度条/地理面板/三联画像/区域实施/主题热力/结构联动/报告模板导出/趋势指标/区域组对比）+ `interpret/` 5 组件（热点诊断/智能摘要推送/多媒体辅助/主题指标交互/useBoundEchart）
- 推演族：EstimateWorkbench / InterpretWorkbench / sharedCharts
- 核增族：治理 3 Tab / 拆解四能力 + 条款树 / 对比工作台 / 研报四板块 + ChainSteps 页间导航（vue-router 串联）

## 3. 任务拆分（registry 建单蓝图）

### 3.1 接口侧（1 张大单，human:李伟 自行拆分）

| ID | 任务 | 说明 |
|---|---|---|
| BE-POL-CONTRACT-01 | 科技政策跟踪 — Java 接口契约定义与数据需求评审（7 页 63 叶：原生 46 + 核增 17，出 API-POL 文档） | **输入 = 政策模块-E7 handoff**（PROD definition / DATA metric-seed / ALGO fullset）+ `cfg_metric-POLICY-seed.yaml`（35 指标 8 件套）+ SRS 两分册 + DISPLAY-POLICY-GAP-AC 档 A/C 清单；路径/DTO/枚举由 Java 侧主导定稿；**契约 → 实现 → 数据对接的内部拆分、排期由 human:李伟 自行决策建单**（参照 DR/TA 模式）；写操作（订阅/收藏/对比槽）是否服务端化在契约评审拍板 |

### 3.2 前端侧（基座 1 单 + 整页 8 单，全景拆 2）

| ID | 任务 | demo 真源（行数） | 体量 |
|---|---|---|---|
| FE-POL-S01 | 模块基座：**菜单重建 3→7**（`router/menu.ts` 补 4 项 + permCode + fullBleed 判定 + 组件解析；`docs/门户菜单权限注册清单.md` 同步补 4 行 + 机读 JSON）/ `views/policy/` 目录骨架 / mock 种子冻结（policyData 2378 + policyPcData 955 + catalog.json 167 + subscription 等）/ `api/policy.ts` 双轨 / D9 只读镜像（35 指标）/ 地图 geojson 注册（中国/深圳）/ 共享 css（PolicyPanorama.css 1296 + PolicyPcPages.css 158 等）token 抽取进 `styles/demo-*.css` | 菜单 + 种子 + catalog + css | M |
| FE-POL-01A | 科创政策全景 · **检索主链路**整段复刻（SRS 全景叶 1–13 区段）：SearchHub 三模式（智能/关键词/高级 DSL：顶层 AND/OR + 一层条件组 + 单条件 NOT）/ FilterPanel+ConditionBuilder+queryEngine Vue 化 / 字段库 / 检索结果列表（表格+卡片双视图）/ 智能排序 / 二次筛选（facets）/ 分类分组 / Excel/PDF 导出 / 政策详情抽屉 / 最近查询 / 收藏 | Panorama 检索段 + `search/` 全族（DisplayPolicySearchHub 232 + advanced 族 2050 + utils 268 + config 141 + css 273）+ Drawer 225 + export 段 | XL |
| FE-POL-01B | 科创政策全景 · **其余 4 Tab**（SRS 全景叶 14–22 区段）：政策动向跟踪（趋势时间线 + 来源同步监控 + **企业匹配推送**，深链 `?tab=match`）/ 政策舆情评估（情感分析 + 传播指标）/ 政策重点比对（新旧版本对比 / 多政策详情对比 / 部门政策对比 / 标杆比对 4 弹窗 + 对标报告）/ 订阅中心（订阅方案 CRUD + 推送收件箱） | Panorama 动向/舆情/比对段 + policyMatch 110 + policySubscription 86 + 4 对比弹窗 | L |
| FE-POL-02A | 政策分析评价整页复刻（13 叶）：3 主 Tab（分析报告可视化 / 结果解读多维展示 / 推荐方案交互展示）+ 文本详情 3 子 Tab（基本条件/支持力度/实施路径）+ `analysis/` 9 组件（含地理 choropleth + 主题热力 + 区域组对比）+ `interpret/` 5 组件（热点诊断板 / 智能摘要推送 / 多媒体辅助 / 主题指标交互）+ 报告模板导出 | PolicyAnalysis 2286 + analysis 族 2986 + css 1061 | L |
| FE-POL-03A | 政策效果推演整页复刻（11 叶）：2 Tab —— 效果预估工作台（EstimateWorkbench：产业影响图随政策缩放 / 创新预测 / 区域政策类型 / 四项识别 + 综合分闸门）/ 科技政策推演工作台（InterpretWorkbench：选文本 / 非导图图表 / 覆盖面 / 历史路径）+ sharedCharts（1161 行图表族） | Simulation 165 + estimate 867 + interpret 727 + sharedCharts 1161 + css 467 | L |
| FE-POL-04A | 智能政策库构建（政策数据治理）整页复刻（核增 4 叶）：治理 Tab（数据清洗 / 结构分类 / 血缘追踪）+ 治理 KPI + 基库构建开关（进度闸门）+ 批次管理 | PolicyPcPages `PolicyGovernance` 段（231–691）+ policyPcData 共享 | M |
| FE-POL-05A | 智能政策拆解整页复刻（核增 4 叶）：政策选择 + 四能力 Tab（语义理解 / 条款精细化拆解 / 关键指标提取 / 政策实体关联）+ 条款树（5 类条款色标）+ KG 绑定开关 + 指标库就绪闸门 | PolicyPcPages `PolicyParse` 段（692–1051） | M |
| FE-POL-06A | 多维政策对比整页复刻（核增 4 叶）：会话槽对比篮（展示侧分轨，禁写专题对比篮）+ 对比维度/区域/级别筛选 + 权重调节 + 差异发现（阈值识别）+ 对比图谱 + 汇总导出 | PolicyPcPages `PolicyCompareUpgrade` 段（1052–1723）+ policyPcExport 段 | M |
| FE-POL-07A | 智能研报生成整页复刻（核增 5 叶）：四板块（政策深度分析 / 洞察结论自动提炼 / 行业数据联动 / 权威源引用）+ 结论↔条款溯源 + 模板就绪 + PDF/Word 导出 + ChainSteps 页间导航 | PolicyPcPages `PolicyInsightReport` 段（1724–2051）+ policyPcExport 165 | M |

依赖：`FE-POL-01A/01B/02A/03A/04A/05A/06A/07A` depends_on `FE-POL-S01`；FE 单不依赖 BE 契约（mock 先行，契约冻结后联调）；01B depends_on 01A（同页共享检索状态）；04A–07A 共享 S01 冻结的 policyPcData 种子与 ChainSteps，可并行。

### 3.3 批次

| 批次 | 内容 | 备注 |
|---|---|---|
| 批 1 | FE-POL-S01 + FE-POL-01A ＋ BE-POL-CONTRACT-01 启动 | 基座 + 检索主链路可验（DSL 布尔组合是本模块最高风险件，先行试点）；契约评审前置 |
| 批 2 | FE-POL-01B + FE-POL-02A | 全景收尾 + 分析评价（interpret 族体量大单独排） |
| 批 3 | FE-POL-03A + FE-POL-04A | 推演双工作台 + 核增首页 |
| 批 4 | FE-POL-05A + FE-POL-06A + FE-POL-07A + 联调收尾 | 核增尾 3 页（共享基座可并行）+ 契约冻结后真机联调 |

FE 合计 ≈ 30 工日；每批独立上 K8s dev 验收。

## 4. 各页 FE 拆分要点与 BE 接口用途（契约对齐）

> FE 每单 DoD 统一：与 demo 逐区块截图比对（五件套）、Design token、D9 ⓘ/🧪/⚠️、观测头、test.mjs 最小自检移植、防漏扫描（`产品实现规程.md` 附录 D，含分析工作区时另按附录 E）；交付三绿（`pnpm type-check` 0 错 + 自检全绿 + `pnpm build` 绿）；**完工停本地工作区等人工验收**（2026-10-20 闸门），不自动 commit/push。

### 科创政策全景（SRS excel 200–221，22 叶）
- 01A FE：检索主链路（见 §3.2）；01B FE：动向/舆情/比对/订阅四区段（见 §3.2）
- BE 接口用途：① 政策库检索（多维筛选 + DSL 布尔 + 排序 + 分页 + facets 二次筛选）② 政策详情（全文 + 条款 + 版本历史）③ 舆情分析（情感分布 + 传播指标）④ 部门/标杆对比聚合 ⑤ 企业匹配推送 ⑥ 订阅与收件箱（写操作，契约评审定服务端化范围，见 D7）⑦ 来源同步监控（jobs/状态）
- **指标挂接**：POLICY 域 35 指标中全景相关（政策总量/类型分布/时效/连续性等；QPOL-01/05/07 🟡 项 UI ⚠️）

### 政策分析评价（excel 222–234，13 叶）
- FE：见 §3.2；BE：① 分析报告数据（维度得分/指标序列）② 结果解读（热点诊断/摘要推送素材）③ 推荐方案（优劣排序/模拟归档）④ 文本三段（基本条件/支持力度/实施路径）⑤ 地理/区域组对比聚合
- **指标挂接**：政策关联度/产业适配（QPOL-03 🟡，匹配阈值 0.6 临时默认）

### 政策效果推演（excel 235–245，11 叶）
- FE：见 §3.2；BE：① 预估参数与产业影响数据（随政策选择缩放）② 创新预测序列 ③ 区域政策类型聚合 ④ 推演文本库与历史路径 ⑤ 综合分（闸门）
- **注意**：推演按钮 demo 有 `BTN_DS_SIMULATE` L2 权限试点——lumen 不复刻级别锁（D2），按钮常可用

### 核增 4 页（excel 617–633 区段，17 叶）
- FE：见 §3.2；BE（共享）：① 治理批次/KPI/血缘追踪 ② 拆解条款树 + 指标提取 + KG 实体关联（Nebula 经 Java→Python 链路，前端不感知）③ 对比会话槽语义（展示侧分轨）④ 研报模板/洞察/行业数据/权威源 ⑤ PDF/Word 导出服务端渲染 or 前端打印页（契约评审定）
- **分轨铁律**（demo BoundaryBanner 语义）：与专题服务系统 `/policy/*`、门户 `/policy-portal/*` 分轨；对比对象仅存展示侧会话槽，**禁止写入专题系统对比篮**

## 5. 避坑清单（开工必读，真源：TS 复刻经验清单 + TA 避坑 §5）

1. **Arco**：`#option="{ data }"` 插槽签名；`<label>` 禁包裹 `a-select`（闪开即关）；cascader 多选用标准多选 + `allow-clear` 禁自绘 footer；图标显式 import（`@arco-design/web-vue/es/icon`）；`a-progress` percent 是 0–1 小数（demo antd 0–100 直抄会 9900%）；`a-tag` 需覆写定高/圆角对齐 demo 视觉；控件高 32px/圆角 4px。
2. **封装**：第二处出现即封装；封装件样式自含（复用他页类名会裸奔）；先查 §2 清单不新造。
3. **渲染**：fixed 弹层（全景 4 对比弹窗 + 详情抽屉 + 订阅抽屉 + 匹配弹窗）一律 `Teleport to body`；图表容器显式高度防 init 0 高死锁（推演双工作台 Tab 切换、分析 interpret 族高发；`.arco-tabs-pane > x-vue-echarts > .echarts-host` min-height 传导先例）；Arco 类名是 `arco-tabs-pane` 不是 `arco-tabs-tabpane`（antd CSS 移植静默失效坑）；地图 frame `isolation: isolate`。
4. **数据**：首屏同步初值防白屏；dev slot props 失效用数据签名 key 规避；种子冻结禁 Math.random（demo `policyData.js` 如含 Date.now/随机须定化并记 handoff）；`USE_MOCK=false` 零 fixture；写操作演示态不替 BE 拍板。
5. **工程**：类型门一律 `pnpm type-check`（vue-tsc 空跑教训）；表格操作列按钮防压缩变形；多选筛选标签 `:max-tag-count` 折叠；交付三绿；**完工停本地等人工验收，不自动 push**。
6. **POL 特有**：
   - 高级检索 DSL 是 demo 内唯一 TSX 族，Vue 化时类型语义（`types.ts` 283 行）同步转 `.ts`，`queryEngine` 纯函数直接语义等价移植 + group 测试摘选；
   - demo `mocks/policy-metrics-catalog.json` 是 D9 指标目录的页面侧快照，lumen 改从 readiness-matrix 镜像生成（AGENTS.md 过渡态契约），**不照抄 JSON**；
   - 旧 topic「政策匹配」深链用 `?tab=match`（D4），路由守卫不做菜单项；
   - 核增 4 页 ChainSteps 用 vue-router push 串联（demo `onTopicChange`）；
   - demo `ReviewOnly`/`BoundaryBanner` 属评审层，集中管理 + 评审模式自闸 + 关闭后零泄漏（D8）。

## 6. 风险与跟踪

| # | 风险 | 动作 |
|---|---|---|
| R1 | 全景页体量最大（01A+01B demo ≈8.4k 行）压批 1/2 | 01A 先行试点 DSL 高风险件；01B 依赖 01A 状态层复用；必要时 01B 再拆（比对弹窗族 / 订阅族），拆分由执行时 coordinator 定 |
| R2 | BE 契约依赖 E7 handoff 完整性（PROD 定义 2026-08 版）与 demo 演进差异 | 契约单以 E7 + SRS + demo 现行为输入；差异走 BE-POL-CONTRACT-01 评审记录 |
| R3 | QPOL-01/03/05/07 口径 🟡 待甲方引发统计数字返工（QA 报告已预警） | 复刻期 mock 态照 demo + ⚠️ 角标；口径闭合前不伪闭合；甲方拍板后只改镜像+角标 |
| R4 | demo 权限试点（L0/L1/L2 + 屏幕锁）与 lumen 全放开差异引发走查争议 | D2 口径前置写进每单 DoD：不复刻级别锁，走查对照 demo 解锁态 |
| R5 | 高级检索 DSL Vue 化语义漂移（布尔组合/NOT/组嵌套） | `queryEngine.group.test.mjs` 断言全量移植；布尔式预览字符串逐例比对 demo |
| R6 | 写操作（订阅/收藏/对比槽/收件箱）契约未定 | D7 会话级演示态先行；契约评审定服务端化范围；FE 预留 api 层切换点 |
| R7 | 核增 4 页与专题/门户分轨边界（demo 横幅语义） | D8 分轨横幅照搬语义；对比槽仅会话级；联调期验证不写专题对比篮 |

# LUMEN-CHAIN-FE-REPLICA-FIX-L01 · 产业链分析 — demo→lumen 单仓复刻修复

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：直连 Python、抄 React/TSX、新加 npm 包、用 Demo fixture 伪造 Q056/QC07、维护写侧接后端。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 2026-08-17 孔东确认单仓合并开工；本 handoff 提交时转 `integration`（联调）。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D8/D9/D10、评审挂点、诚实空、只调 Java、Vue 抽组件。复用 G6 / Leaflet / `@/review` / `SystemReportReader` / 已装 ECharts，不另起 UI 体系。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | Demo 产业中心页与本仓工作区页精读对照，禁止 compress 代替。 |

## 范围与实现

`lumen-ui-topic` 单仓补齐 demo→lumen 复刻缺口（W0–W4 + 人审续修）。前端只调 Java catalog / snapshot / overview / analysisTask GetResult。

### W0 卫生

- `a-alert` 改默认插槽，产业中心页不再用 React 的 `content` prop。
- 必填只留 Arco `required` 一星，去掉手写 `diagnosis-required-asterisk`。
- 诊断 / 区域 / 深圳同壳 Tab：`tabsFor*Workspace` 仅当前叶子 + 记录。
- `IndustryReviewMount` 五种 kind（追溯 / 指标 / 缺失 / Mock / Pending）。
- 查询推荐 / 结果卡抽 `IndustrySearchObjectCard`；`a-spin` 加 `block`；推荐卡含领域、推荐理由、查看摘要、入篮态。

### W1 门户

- 专题全景内嵌 `IndustryPanoramaGraph` + 对象详情；链节点可下钻进全景页。
- 区域 / 深圳双地图：`IndustryRegionMap`（天地图）；深圳各区无 Java 点位时诚实空，不抄 Demo `SHENZHEN_REGION_POINTS` 企业数。
- 资讯列表点开 Timeline / Drawer。

### W2 结果

- 周期 / 瓶颈 / 区域 / 深圳结果板接 `GetResult` 解析；无字段则空布局，禁止页面写死「—」。
- 新增 `IndustryBottleneckGraph`（G6 html 节点）。
- Q056 / QC07 仍走 `metricDisplay` 诚实空。

### W3 全景专业

- 图谱 / 结构列表切换；专业页详情三 Tab = **关联企业 / 主流技术路线 / 市场规模**（已去掉「科研与服务机构」）。
- 演进快照仅当 Java `evolutionStates.length > 1`，不伪造时间轴；演进五类图例可展示，节点变化只标 Java 真实字段。

### W4 报告 + 维护

- 诊断 / 区域 / 深圳结果页「查看报告」挂已有 `SystemReportReader`（`view=report`）。
- 维护 15 项导航壳（`CHAIN_ZONE_TAB_META`）；写侧按钮 disabled。

### 人审续修（2026-08-17 第一轮）

Tab `TITLE_MOUNTS`、资讯 Timeline、查询 header 归评审、卡片拉满、高筛去面包屑、全景/周期/区域/深圳评审挂点。

### 人审续修（2026-08-17 第二轮 5 条）

1. 示例查询：`SearchHub` 点击示例**只填框**，不 `emit('search')` / `emit('smartParse')`（与 Demo 一致；中途曾误改为立即搜索，已改回）。
2. 专题全景 Tab：去掉未选中 Tab 自定义悬停，走 Arco line 默认态。
3. 门户全景：`SharedMapChrome` + 阶段图例 + 右栏对象详情（无「概况/关联/演进」）。
4. 高筛：`SearchHub` 常驻 + `advanced-inline`；`FilterPanel` 对齐企业查询。
5. 结果内筛选 `ResultToolbar` + Demo 结果卡字段。

### 人审续修（2026-08-17 第三轮 6 条）

1. 全景专业页查询条件：`policy-analysis-filter-row` 横排（Select 304px），压住 Arco vertical FormItem 100% 宽导致的竖堆。
2. 全景图谱：`SharedMapChrome` 操作栏 + 演进五类图例抬到 `z-index:620`，画布固定 520px。
3. 去掉常驻右栏 aside；点击节点/边打开 `a-drawer`（`industry-topic-detail-drawer`），`loadSnapshot` 不再自动选首节点。
4. 诊断产业参数：选择列（disabled checkbox）+ 周期 `InputNumber mode="button"` 调参；Q056 市场规模保持空/disabled，禁止 12800。
5. 诊断记录：任务状态筛选 + 按当前 workspace 分析类型收窄。
6. 区域产业指数评价对照 Demo：评价模式、官方/个人模板、工作集勾选/添加/移除、可调权重与均分、配置即时汇总（不伪造指数）、评审挂点、记录筛选。

### 人审续修（2026-08-17 第四轮 · 深圳三页 + 竞争力 + 过程条）

对照 `demo-ui-topic`：

1. **深圳产业情况分析对比**：四级 Cascader（全球/全国/区域/深圳）、未就绪灰显、默认上海/北京/苏州、四维只读权重表、主体区域只读「深圳」、记录状态筛选、过程挂点 `CHAIN-SZ-F02-COMPARE-TITLE`。
2. **深圳产业发展分析**：有效对比结果 Select（含 PDF 无效项）、发展目标勾选、无来源禁止空跑；结果板含来源依据三栏、只读抽屉、三类建议、路径表、全球案例 Gap。
3. **区域产业竞争力评价结果板**：柱状排名 / 三维热力 / 多区域 GIS 占位 / 排名明细 / 版本边界。无 Java rows 不编造指数。ECharts 补注册 `HeatmapChart` + `VisualMapComponent`。
4. **竞争力配置「三大一级维度权重」**：表列对齐 Demo（选择/名称/分组/状态/权重/来源/说明+查看抽屉）；默认 40/35/25；提交键仍为 `industry_foundation` / `academic_ecology` / `innovation_ecology`。
5. **过程 Steps 图标偏移**：Arco Vue 节点是 `arco-steps-item-node`（默认 `margin-left: 58px`），补零边距与居中，连线仍按 Demo 五等分。

诚实性：不抄 Demo `buildComparisonResult` / `buildCompetitivenessResult` 的 94/88/82%、成长期后段、固定建议文案。

## 修改内容（本单落地）

| 区域 | 作为 |
|------|------|
| 查询 | `SearchHub` 示例只填框；`FilterPanel` / `ResultToolbar` / `IndustrySearchObjectCard` 对齐 Demo 字段与布局 |
| 专题全景 / 全景专业 | `SharedMapChrome`、演进图例、节点抽屉、`IndustryPanoramaDetail` 三 Tab |
| 诊断 | 参数勾选+调参、记录筛选、周期/瓶颈结果板、过程壳 wait_view |
| 区域指数 | 评价模式、官方/个人模板、工作集、即时汇总（不估综合指数） |
| 区域竞争力 | 三维权重表 + 结果可视化空态骨架 |
| 深圳对比/发展 | Cascader、四维只读、来源 Select、结果板空态骨架 |
| 过程条 | Vue Steps 节点居中，对齐 Demo 五等分 |
| 报告/维护 | `IndustryChainReportHost`；维护壳只读 |

## 偏离说明

- 深圳各区地图：Java overview 当前只回城市级点（如 440300），区级空态诚实，不用 Demo 区级假企业数。
- 周期折线 / 旅程 / 对标表 / 竞争力热力：有 GetResult 字段才画；Python 后到时保持空板。
- 全景演进：契约扩展 `evolutionStates?`，无数据不展示双图。
- 竞争力提交键保持 lumen Java 契约，不改成 Demo 的 `enterprise` / `academic` / `support`。
- 示例查询最终态=只填框（与 Demo 一致）。

## 产物清单

- 代码仓：`repos/lumen-ui-topic`（`origin/dev`）
- 页面：`src/views/industry-center/*.vue` + `industryDiagnosis.css` / `industryOverview.css` / `industrySearch.css` / `industryTopicAnalysis.css`
- 组件：`src/components/industry-center/Industry*ResultBoard.vue`、`IndustryReviewMount.vue`、`IndustryWorkspaceTabs.vue`、`IndustryPanoramaDetail.vue`、`IndustryBottleneckGraph.vue`、`IndustryRegionMap.vue`、`IndustryChainReportHost.vue`、`IndustrySearchObjectCard.vue` 等
- 配置/解析：`src/config/industryWorkspace.ts`、`src/config/industryMaintenance.ts`、`src/config/echarts.ts`、`src/utils/industryChainTask.ts`
- 自检：`industryReplicaFix.selfcheck.mjs`、`industryChainTask.selfcheck.mjs`、`industrySearchModel.selfcheck.mjs`
- 本 handoff

## 测试结果

- `node src/views/industry-center/industryReplicaFix.selfcheck.mjs` 绿（含 Cascader/四维/发展目标/竞争力表列/过程 node 选择器）
- `node src/utils/industryChainTask.selfcheck.mjs` 绿（含深圳空解析、PDF 不可作发展输入）
- `node src/utils/industrySearchModel.selfcheck.mjs` 绿
- `npm run type-check` 绿
- 本机 `npm run dev` 可看；K8s 随 `origin/dev` CI

## 遗留风险

- 周期 / 区域 / 深圳 GetResult 字段名若与解析器不一致，结果板会空（诚实）而不是假数；**联调请按 Java 实包微调 parser**。
- 维护写侧仍归 OPS。
- GIS 区域热力为占位（`CHAIN-REG-F03-COMP-HEATMAP-GIS`），不伪造地理热力。
- 个人模板仅 localStorage，不进 Java。

## 联调说明（integration）

- 前端已 push `lumen-ui-topic` `origin/dev`，只打 `gkxlumen-platform-gateway`。
- 请 Java 对照：`chain:regional:competitiveness` 的 `dimension_weights`；`chain:shenzhen:shenzhen_comparison` / `shenzhen_development` 的 `benchmarks` / `source_comparison_task_id` / `goals`。
- 期望：有字段则填结果板；无字段保持空骨架。禁止用 Demo fixture 补 82% / 成长期后段 / 竞争力演示分。
- 联调确认后请在 registry `note` 写「联调通过」以便 AV-1。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`ac115f8` `feat(chain): demo→lumen 复刻修复 W0–W4 与人审续修 [agent:frontend-agent]`
- pipeline URL / ID：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines（push 后触发）
- 部署 namespace / 镜像 tag：K8s dev（CI 触发）
- K8s rollout：随 CI
- dev 测试 URL / 命令与结果：本地 `npm run type-check` 绿；自检三条绿；已 push `28dc019..ac115f8`

## 可观测性

- 沿用现有 industry / analysisTask 请求链 `X-Trace-Id`；本单未新开直连。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 前端不跑算法 |
| 2 调用链 FE→Java | ✅ |
| 3 Nebula | ✅ 不直连 |
| 4 可观测 | ✅ 沿用现有 |
| 5 CI | ✅ 本单 push `origin/dev` |
| 6 demo2 不 merge lumen | ✅ Vue 重写 |
| 7 只调 Java | ✅ |
| 8 标准表 / 诚实空 | ✅ Q056/QC07 / 深圳对比 / 竞争力 |
| 9 D8 | ✅ Arco + token |
| 10 D9 | ✅ ReviewMount / ReviewMetricBadges 自闸 |
| 11 D10 | ✅ Tab / Alert / 必填星号 |
| 12 D12 | ✅ 不打 demo 服务 |

## 涉及文件

- `src/config/industryWorkspace.ts`
- `src/config/industryMaintenance.ts`
- `src/config/echarts.ts`
- `src/utils/industryChainTask.ts`
- `src/composables/useIndustryAnalysisJob.ts`
- `src/components/industry-center/**`
- `src/components/search/SearchHub.vue` / `ResultToolbar.vue`
- `src/components/filter/FilterPanel.vue`
- `src/views/industry-center/*.vue` + 配套 css
- `src/api/industry/types.ts`

## cost（完工回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 280000（会话估计，含对照 Demo、三页重写、权重表与过程条） |
| model_used | cursor-grok-4.6 |
| actual_cost | 待账单核对 |
| cost_warn | yellow |

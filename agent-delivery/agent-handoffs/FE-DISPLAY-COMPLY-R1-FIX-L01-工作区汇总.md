# FE-DISPLAY-COMPLY-R1-FIX-L01 · 展示系统第一轮合规验收 — 修复完善补全（问题清单逐项闭合）

> 本文档汇总 2026-11-17 `lumen-ui-science-pc` 工作区全部未提交改动（含孔东本地多会话并行产出）；
> **任务状态保持 `in_progress` 不变**（孔东 2026-11-17 17:40 确认开工，修复项按后续指令持续执行中）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 日常 bugfix/合规修复默认 full；未用 YAGNI 跳过 D8/D9/D10、可观测、架构铁律；复刻对齐已评审页与 token，未另起 UI/交互。 |

## 问题清单（本轮已闭合项，来源：孔东当会话逐项指令 + 合规验收第一轮记录）

| # | 来源 | 问题 | 状态 |
|---|------|------|------|
| 1 | 孔东 2026-11-17 指令 | 科技全域态势 OverviewTab 饼图模式因子卡：数值未进标题栏、图例挤压饼图空间 | ✅ |
| 2 | 孔东 2026-11-13 裁定 | 标题带「（2019年）」年份后缀（`distributionTitle` / `stats` / `factorCards`） | ✅ |
| 3 | 孔东 2026-11-17 指令 | 饼图图例文字过小；分布图例外容器过宽挤压环形图 | ✅ |
| 4 | 孔东 2026-11-17 指令 | 横向排行柱图 hover 无整行高亮、柱端无数值 | ✅ |
| 5 | 孔东 2026-11-17 指令 | 趋势图 tooltip 过长溢出视口 | ✅ |
| 6 | 孔东 2026-11-17 指令 | 分布面板解释文字挤换行标题 | ✅ |
| 7 | 孔东 2026-11-17 指令 | 影响因素页红问号泄漏到标准视图；指标卡横向滚动 | ✅ |
| 8 | 孔东 2026-11-17 指令 | 要素地图列表视图无分页 | ✅ |
| 9 | 孔东 2026-11-17 指令 | 三创新监测页（全球/湾区/深圳）地图 marker 叠首字文字、视觉杂乱 | ✅ |
| 10 | 孔东 2026-11-17 指令 | 地图点标记 30px 过大；改 8px 基准并随缩放联动 | ✅ |
| 11 | 孔东 2026-11-17 反馈（并行会话） | 统计汇总导出改 Excel 三 sheet（表头/合并/数据完整） | ✅ |
| 11a | 孔东 6:16 修正（并行会话） | 年粒度时间筛选改外显「时间范围按钮 + 弹窗 Slider 时间轴」形态 | ✅ |
| 11b | 孔东 7:06 修正（并行会话） | 全球创新详情「更新频率」胶囊按钮右置；banner 内 popover 左开防溢出 | ✅ |
| 11c | 合规验收 2540（并行会话） | 价值报告内容区收不到滚动、导出按钮不可达 | ✅ |
| 11d | 合规验收 2491/2287 回归（并行会话） | 项目点位详情、真实候选优先展示回归自检 | ✅ |
| 12 | 孔东 2026-11-17 21:05 指令（二轮） | 详情筛选「创新成果分类」280px 过窄换行 | ✅ |
| 13 | 孔东 2026-11-17 21:12 指令（二轮） | 结果抽屉自绘 150 页全量按钮分页 | ✅ |
| 14 | 孔东 2026-11-17 21:17 指令（二轮） | 结果表列宽挤压换行、名称省略无 tooltip、更新时间/创新价值无排序 | ✅ |
| 15 | 孔东 2026-11-17 21:36 指令（二轮） | 详情弹窗被结果抽屉遮挡（z-index）；排序箭头双显、价值表头不可折行；抽屉排序下拉冗余 | ✅ |
| 16 | 孔东 2026-11-17 21:41 指令（二轮） | 要素/事件列表视图分页改 Arco 组件带跳转 | ✅ |
| 17 | 孔东 2026-11-17 21:44 指令（二轮） | 结果表排序 icon 对齐科创事件表双三角 caret 样式 | ✅ |
| 18 | 孔东 2026-11-17 21:46 指令（二轮） | 事件表时间列 76px 过窄日期折行 | ✅ |
| 19 | 孔东 2026-11-17 21:49 指令（二轮） | 结果抽屉分页补跳转（show-jumper） | ✅ |

## 修改内容

### A. 科技全域态势 · 总览 Tab（本会话）

- `OverviewTab.vue` + `demo-situation.css`：
  - 饼图模式因子卡数值（如「102,045 家」）移入 `.stat-cell__head` 标题栏正中（3 列 grid `1fr auto 1fr` 精确居中，位于拖拽把手与关闭按钮之间）；
  - `.stat-cell__chart` / `.figma-line-chart` 高度 118px → 148px；
  - KPI 卡红问号（D1 missing）加双闸（`isReviewFeatureEnabled() && reviewStore.reviewMode`），标准视图零泄漏。
- `chartBuilders.ts`：
  - `buildFactorCardPieOption`：图例右侧纵向滚动（`orient: 'vertical'` + `type: 'scroll'`），饼心左移放大（`center ['34%','50%']` / `radius ['34%','64%']`），tooltip 对齐分布环形图格式，图例字号 10px；
  - `buildDistributionDonutOption`：默认隐藏扇区外显文字与内置 ECharts 图例（DOM 图例为准），环形图居中放大；
  - `buildDistributionRankBarOption`：tooltip 改 `trigger: 'axis'` + `axisPointer shadow`（整行高亮，与纵向图一致），柱端右侧显示格式化数值，`grid.right` 48 防裁剪；
  - `buildTrendMultiLineOption`：tooltip `confine: true` + `max-width: 280px` 换行，防视口截断。
- `situationModel.ts`：导出 `stripLabelYearSuffix()`（`/（\d{4}年）/g`），`index.vue` 在数据入口对 `distributionTitle` / `stats` / `factorCards` 统一剥年份后缀（后端未发新码也正确；scope 后缀保留）。

### B. 科技全域态势 · 影响因素 Tab（本会话）

- `InfluenceTab.vue`：红问号 `IconQuestionCircle` 收进评审模式（双闸 `reviewVisible`）。
- `demo-situation.css`：`.influence-factor-tabs` 改 `repeat(4, minmax(0, 1fr))` 4 列网格，消灭横向滚动。

### C. 要素地图列表视图分页（本会话）

- `FactorMapSection.vue`：补分页，对齐科创事件 `GlobalEventSection` 行为与视觉（`EVENT_PAGE_SIZE = 7`、页码跳转、排序/筛选变化重置回第 1 页、aria 可达）。

### D. 三创新监测页地图点标记（本会话）

- 新增 `src/components/map/mapMarkerScale.ts`：`markerSizeForZoom(zoom)` —— zoom 5 基准 8px、每级 ×1.15、钳制 [6,18]px；配套断言自检 `mapMarkerScale.test.mjs`。
- 全球 `InnovationDetail.vue` + `detailMonitorModel.ts`：去掉 marker 首字（'企'/'论'/'机'/'文'/'研'）恢复纯色实心圆；区分受控 `mapZoom`（区域定位）与实时 `mapLiveZoom`（`@zoom-change`），点位与项目 marker 随缩放联动。
- 湾区 `bayMapMarker.ts` + `OverviewTab.vue`：去文字、`iconSize` 支持随缩放，保留 canvas 尺寸常量。
- 深圳 `CarrierTab.vue`：去文字、脉冲与选中环尺寸随 `iconSize` 联动。

### E. 统计汇总 Excel 导出（并行会话，同任务）

- `situationModel.ts` 新增 `buildOverviewStatsExportSheets()`：三 sheet 全量导出（统计汇总/构成分布/年度趋势矩阵），标题通栏合并、口径说明区、趋势矩阵行=年份列=序列；CSV 旧口径（父页 ExportFlowPanel）保持不动。
- `shared/reportExport.ts`：sheet 协议扩展 `merges` / `colWidths`（`!merges` / `!cols`）。

### F. 年粒度时间筛选 Slider（并行会话，同任务）

- `SituationFilterBar.vue`：年粒度外显改「时间范围按钮（YYYY–YYYY）+ 弹窗 Arco Slider range 时间轴」，值域=后端真实年度序列索引，上抛口径与 RangePicker 完全一致（先例 tech-index ActivityRadarPanel）。

### G. 全球创新详情更新频率 + 滚动修复（并行会话，同任务）

- `InnovationDetail.vue` + `demo-global-innovation.css`：更新频率胶囊复用实时 Tab 交互（hover/focus 可达），如实标「按年度（非实时）」不宣称实时；按钮右置（`margin-left:auto` 防 `sr-only` 全局泄漏贴左）；banner 内 popover 左开防溢出；2540 价值报告内容区允许纵向滚动直达导出按钮。

### H. 二轮修复（2026-11-17 晚，本会话，commit `d378b3d`）

- **结果抽屉 Arco 分页**（`InnovationDetail.vue`）：自绘 150 页全量按钮分页改 `a-pagination`（`size="small"` + `show-total` + `show-jumper` 带跳转）；删除自绘按钮/汇总 CSS。
- **结果表排序 + 列宽**（`InnovationDetail.vue` + `demo-global-innovation.css`）：
  - 「更新时间」「创新价值 / 资助金额」两列表头可排序：科创事件表同款 **8px 双三角 caret**（上下灰三角常显，`is-asc`/`is-desc` 激活方向变蓝），复用 `detailListSortKey` 状态机（`sortDetailInnovations` 四向）；
  - 价值列表头允许两行（文字折行、caret 居中钉末尾），列宽回收 12%；
  - 列宽重分配（和=100%）：名称 26 / 类型领域 15 / 区域 11 / 更新时间 12 / 价值 12 / 操作 24；全列 `nowrap` + td `ellipsis`；
  - 成果名称外裹 `a-tooltip`（`position="tl"`，内容=名称：描述），省略内容悬停可见；
  - 抽屉工具栏「创新价值排序」下拉移除（面板头部下拉保留——卡片列表无表头仍需）。
- **详情弹窗层级**（`demo-global-innovation.css`）：`gi-modal-overlay` / `gi-detail-drawer-overlay` z-index 1000 → **4400**，压过结果抽屉（4200）、低于对比飞行点（5000）；从结果表点「详情」不再被遮挡。
- **两列表视图分页统一**（`FactorMapSection.vue` + `GlobalEventSection.vue` + `demo-situation.css`）：要素/事件列表分页均改 `a-pagination`（`show-total` + `show-jumper`），删除自绘按钮/跳转输入框样式与 `eventPageJump`/`factorPageJump` 等死状态；`factorMap.test.mjs` 断言同步（`<a-pagination` + `show-jumper`）。
- **事件表时间列加宽**（`demo-situation.css`）：第 4 列 76 → 104px + `nowrap`，日期与期间两行均不折行。
- **详情筛选宽度**（`InnovationDetail.vue`）：「创新成果分类展示」cascade `:width` 280 → 400（配合并行会话已将 `--type` 组 `max-width` 提至 420px），3 tag + `+N` 单行不换行。

## 测试结果（2026-11-17 本机实测，三绿）

| 检查 | 命令 | 结果 |
|------|------|------|
| 类型门 | `pnpm type-check`（vue-tsc --build） | ✅ exit 0（一轮 / 二轮均过） |
| 单测/自检 | `overviewTab / factorMap / situationExport / situationFilterBar / bayMapMarker / mapMarkerScale / globalInnovationExport / mapPointDetail / innovationMonitor` 共 9 脚本 | ✅ 全通过（二轮复跑全绿） |
| 构建 | `pnpm build` | ✅ 一轮 1m1s / 二轮 44s（仅 chunk>500kB 既有告警） |

## 遗留风险

- 一轮改动已随 `4e71975` 推送；**二轮改动已随 `d378b3d` 推送 origin/dev**（孔东 2026-11-17 21:50 逐字指令放行）。下游需重点回归：饼图卡标题栏在极窄卡宽下的换行、Slider 弹窗在触屏端可用性、结果表两行表头在更窄抽屉宽度的表现。
- 本轮改动均未触碰观测埋点（`observability.ts` 既有链路不变）。
- 后端年份后缀剥离为前端兜底；后端若永久下发新口径，`stripLabelYearSuffix` 可保留无害。

## CI/CD（必填）

- 分支：`dev`
- commit：一轮 `4e71975`（22 文件 +896/−131）/ 二轮 `d378b3d`（6 文件 +206/−211），均已 push origin/dev
- pipeline URL / ID：GitLab CI 自动触发（push 后链路）
- 部署 namespace / 镜像 tag：CI → K8s dev 自动 rollout（`zhipu-tts` ns，既定链路）
- K8s rollout：待 CI 完成（push 即触发，未人工干预）
- dev 测试 URL / 命令与结果：本机 `pnpm dev` 手工走查 + 9 测试脚本通过（见「测试结果」）

## 可观测性（建议）

- OTEL_SERVICE_NAME：`lumen-ui-science-pc`（既有配置，本轮未改）
- traceId（dev 抽样）：本轮纯 UI 改动未走后端链路，未采样
- Tempo / Loki：无新增埋点需求

## 涉及文件

**一轮（commit `4e71975`，22 文件 +896/−131）**

本会话：
- `src/views/situation/overview/components/OverviewTab.vue`
- `src/views/situation/overview/components/InfluenceTab.vue`
- `src/views/situation/overview/components/FactorMapSection.vue`
- `src/views/situation/overview/index.vue`
- `src/views/situation/overview/models/chartBuilders.ts`
- `src/views/situation/overview/models/situationModel.ts`（本会话年份剥离 + 并行会话 Excel 导出）
- `src/views/situation/overview/styles/demo-situation.css`
- `src/views/situation/overview/overviewTab.test.mjs`
- `src/views/situation/overview/factorMap.test.mjs`
- `src/views/situation/bay-innovation/tabs/OverviewTab.vue`
- `src/views/situation/bay-innovation/utils/bayMapMarker.ts`
- `src/views/situation/global-innovation/models/detailMonitorModel.ts`
- `src/views/situation/global-innovation/tabs/InnovationDetail.vue`（本会话 marker + 并行会话更新频率）
- `src/views/situation/shenzhen-innovation/tabs/CarrierTab.vue`
- `src/components/map/mapMarkerScale.ts`（新增）
- `src/components/map/mapMarkerScale.test.mjs`（新增）

并行会话（同任务 FE-DISPLAY-COMPLY-R1-FIX-L01）：
- `src/views/situation/overview/components/SituationFilterBar.vue`
- `src/views/situation/shared/reportExport.ts`
- `src/views/situation/global-innovation/styles/demo-global-innovation.css`
- `src/views/situation/overview/situationExport.test.mjs`
- `src/views/situation/overview/situationFilterBar.test.mjs`
- `src/views/situation/global-innovation/globalInnovationExport.test.mjs`

**二轮（commit `d378b3d`，6 文件 +206/−211）**

- `src/views/situation/global-innovation/tabs/InnovationDetail.vue`（Arco 分页带跳转 / 表头双三角排序 / 名称 tooltip / 筛选宽度 400）
- `src/views/situation/global-innovation/styles/demo-global-innovation.css`（分页样式清理 / 排序 caret / 列宽 / 弹窗 z-index 4400）
- `src/views/situation/overview/components/FactorMapSection.vue`（Arco 分页带跳转）
- `src/views/situation/overview/components/GlobalEventSection.vue`（Arco 分页带跳转）
- `src/views/situation/overview/styles/demo-situation.css`（分页样式清理 / 时间列 104px）
- `src/views/situation/overview/factorMap.test.mjs`（分页断言同步）

# FE-TS-01A · 科技全域态势（M1）整页复刻（v2 返工交付）

> 仓库：`repos/lumen-ui-science-pc`；路由 `/trend/tech-overall-situation`。
> v2：按评审意见（"UI+样式+功能+操作全量复刻 demo"）整体返工组件层；数据层（mock/api/model）沿用 v1。
> v2.1：修用户实测三问题（地图容器高度塌陷 / 事件列表不可见 / 时间弹窗点外不关闭）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `coordinator_dispatch` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未加 npm 依赖；demo 样式以"选择器命中规则整块抽取"方式 1:1 移植（4636 行）而非重写；D9 挂位/双轨 mock/打点保留。 |

## v2.1 修复（用户实测反馈）

13. **地图 marker 悬停提示对齐 demo（用户反馈第八批）**：demo 真源 = SharedRegionMap.jsx L517-522 `bindTooltip(buildMapHoverTooltipHtml(region,'object'), { className: 'soft-workbench__map-hover-tooltip …', direction: 'top', offset: [0,-12], opacity: 1 })` + mapPreview.js L161-173（双行：`<strong>名称 · 类型</strong><span>影响力 N.N ↑趋势</span>`）。实现：①TiandituMap `MapPointItem` 加 `tooltipHtml`/`tooltipClassName`（有则套 demo 类名+offset[0,-12]，无则回落原纯文本）；②FactorMapSection 加 `buildHoverTooltipHtml`（区域点类型=首个启用图层要素名 legendEnabledKeys 过滤、对象点=OBJECT_TYPE_LABELS；trend 仅 ↑↓ 前缀展示，前导+归一↑，方向色 up #d93026/down #14804a）；③GlobalEventSection 事件点同款（类型=事件类型 label）；④demo-situation.css 补齐抽取缺失的 strong/span 排版与 --up/--down 趋势色规则，hover-tooltip 规则选择器双写 `.ts-map`（本仓 TiandituMap 根容器 = demo map-host 等价层）。已知偏离：事件点影响力不做 value 数字解析（demo 公式对"2026-02 ·…"文本会显示 202602.0 噪声），直接回落 86.4 + ponytail 注释，接入真实指标后删。实测：区域点"东京 · 企业/影响力 86.6"、对象点（zoom≥11）"香港科技大学(广州) · 高校/实验室/影响力 88.9"带 --object 类、事件点样式同款；tooltip 均位于 marker 上方（leaflet-tooltip-top、间隙≈9px）、白卡 rgba(255,255,255,.96)/边框 rgba(194,210,231,.82)/圆角 6px/11px。`pnpm type-check` 0 error。

12. **页壳双层 main 嵌套消除 + 右栏边框对齐 demo（用户反馈第七批）**：对齐 demo App.jsx L6831 真源结构（`figma-page > main.global-situation-page > section.global-situation-tab-content.content-shell-figma`）。①本页路由 meta 加 `fullBleed`，DefaultLayout 容器变 `div.content-shell--flush`（去白卡壳只留定位，页面根保留唯一 main）；②WorkbenchLayout 加 demo 同款 `shellTag`/`shellClass` props，本页壳挂 `section.global-situation-tab-content content-shell-figma`——激活 demo-situation.css 中已抽取但此前无 DOM 命中的玻璃壳（8px padding/白边 8px 圆角/渐变+blur(8px)）与 `.analysis-panel`/`.map-section` 576px 白边 rgba(255,255,255,.78) 规则（=反馈 2 的边框/背景对齐）；③壳补 demo 基类 `.content-shell-figma` 的 flex column（原抽取块只有覆盖值，缺它 work-area 塌成内容高 2664px）；④`--figma-content-shell-padding`/`--panel-border` 等 demo :root 变量在页根作用域补定义；⑤三处 fixed 弹层（InsightDetailDrawer/ExportFlowPanel/InfluenceTab 查看更多）补 `Teleport to body`——demo 真源即 createPortal(document.body)，玻璃壳 backdrop-filter 会把壳内 fixed 的 containing block 捕获到壳上（遮罩会盖不到侧边栏/头）；⑥页面 scoped work-area 覆盖对齐 demo 值（gap 8px / margin-top 16px / 右栏 576px），窄视口（<1500px）列下限用 minmax(0,1fr) 防 620px floor 裁右栏（demo 假定宽屏，行为差异注释在源码）。实测：#app 内 main 仅 1 个（global-situation-page）；壳 SECTION 玻璃样式（padding 8px/border rgba(255,255,255,.86)/blur(8px)/radius 8px）；work-area 667px 高、列 587+576、gap 8px、margin-top 16px；analysis-panel/map-section 均带 576px 宽白边+rgba(255,255,255,.78) 背景；事件 Tab 主画布满宽 1171px；三弹层均 parentIsBody=true 且 fixed 盖满视口（903px）；普通页（global-innovation-monitor）壳不变（MAIN+白卡+12px 圆角、无 flush）。`pnpm type-check` 0 error、`pnpm build-only` 成功。

1. **地图/事件列表不显示**：根因 = demo `.map-section` 是其 work-area **grid cell**（`grid-area: map` 自动获高），本仓 WorkbenchLayout 用的 flex 布局，slot 内 `.map-section` 无显式高度 → 内容塌陷至 2px（marker/数据均在 DOM 但不可见）。修复 = FactorMapSection/GlobalEventSection scoped 层补高度链（`.map-section{flex:1;min-height:0}` → `.soft-workbench__map-frame{flex:1}` → `.ts-map{height:100%}`）。实测：要素地图 628px/30 点/图例 11；事件地图 628px/5 点，列表视图 628px 高 5 行。
2. **时间筛选弹窗点击外部不隐藏**：demo 仅 trigger 切换。补 document mousedown 外部点击关闭（ref 判定 `.unified-time-filter` 包含关系，卸载移除监听）。实测：点开 → 点外部关闭 ✓。
3. **科创要素下拉显示异常**（选项文字空白 + 色点 fallback）：根因 = Arco 2.58.0 `#option` 作用域插槽参数为 `{ data: 选项原始对象 }`（源码 `optionSlot({ data: optionInfo.raw })`），首版解构 `{ label, color }` 全 undefined。修复 = `#option="{ data }"` 渲染 `data.label`，色点 `--factor-filter-color: data.color`；页面 factorSelectOptions 逐项携带冻结图例色（demo FactorFilter optionRender 语义）。
4. **地图自定义操作区被遮挡**：根因 = TiandituMap(Leaflet) 原生控件 z-index 800-1000 / pane 200-700 外溢，压过自定义控件（视图切换 z12 / 热力开关与重要性条 z30，demo 用自定义 toolbar 无此冲突）。修复 = 两地图组件 `.soft-workbench__map-frame { isolation: isolate }` 圈住 Leaflet 层级 + frame 内图例(1100)/预览卡(1150)/空态(1200) 抬升 + 事件重要性条 top 56→76 避让原生 zoom 控件（高约 60px）。实测：要素 Tab 视图切换/热力/图例与事件 Tab 重要性条 elementFromPoint 均命中自身、barTop(303)>zoomBottom(302) 无重叠。
5. **日期范围不能手动选择**：两处根因——①"自定义"快捷按钮错误地把范围塌成单年（demo L1772-1778 语义 = 仅切粒度不动范围）；②面板内起/止年份下拉用 Arco a-select，弹层在本环境不可靠（demo 原实现 TimeRangeFilter 即**原生 select**）。修复 = 起止年换原生 `<select class="filter-input year">`（demo 同款）+ onQuickActionClick 按真源语义分流。实测：改 2022-2026 / 2022-2025 联动 trigger 与 currentYear；"自定义"保持 2022-2025 不变；"近7天"塌 2025 单年+日粒度 ✓。
6. **对照补齐（用户反馈第三批）**：①地图缩放工具栏换 demo 自定义款（mapToolbar.js 四件：放大/缩小/复位/全屏，`.map-toolbar` 样式补提取，TiandituMap expose zoomIn/zoomOut、原生 zoomControl 关闭、全屏走 map-frame requestFullscreen）；②导出按钮换 demo `analysis-export`（图标+状态文字）、新增"我的收藏"图标按钮（`top-follow-button` + 数量角标 + 面板，useFollow 接线，地图预览卡"加入收藏/取消收藏"入口）；③布局满宽（demo M1 右栏固定 576px、主画布 1fr 吃满、analysis-panel width:100% 覆盖提取 css 的 478px 旧值；页面级 :deep 覆盖不改共用 WorkbenchLayout）。④Arco 图标须显式 import（`@arco-design/web-vue/es/icon`）——unplugin ArcoResolver 在本仓未接管 icon-* 标签（输出为未知元素），已按组件显式导入。实测：工具栏 146×34 四键 SVG 图标、放大两格视野 17→13 marker、复位还原、事件 Tab 同款工具栏；收藏链路 marker→预览卡→加入收藏→角标 1→面板 1 项；右栏 576 满格无空白。
7. **对照补齐（用户反馈第四批）**：①自定义工具栏 z35→1100（demo 值适配其无 Leaflet 原生层；isolation 后仍需高于 marker 层 z600）；②收藏/导出按钮 hover 提示换 a-tooltip（原生 title 在提取 css 环境下显示异常）；③总览 Tab 图表类型切换（折线/柱状/饼）+ 导出统计拆到第二行左右布局（第一行=当前领域+统计指标）。实测：工具栏命中自身、hover 出"我的收藏"提示、chart-head 2 子元素 + actions 行左切换右导出。
8. **辅助标题占行（用户反馈第五批）**：demo `pp-l6-section-title`（"放大/缩小"/"拖动平移"）为无障碍标题，其 sr-only 规则在 styles.css 之外故提取缺失导致可见占行。修复 = 两地图组件 scoped 补 sr-only（1px 裁剪），并补齐 demo 同款"拖动平移"标题。实测：两标题均 1×1 隐藏、工具栏贴框顶 16px。
9. **统计指标控件（用户反馈第六批）**：①"统计指标展示功能"标签加 nowrap（8 字一行显示）；②下拉换原生 select（demo L4186 原实现即原生 select，样式提取 css 已有 `.overview-stat-controls select` 规则；Arco a-select 弹层在本环境闪现消失，与年份/科创要素下拉同源）。实测：标签单行、选"分布比例"联动饼图出现。
10. 已知工具限制：IAB 自动化无法点开 Arco select 弹层（CUA/Playwright/dispatch/键盘均无效，v1 起如此，与本页代码无关——组件链 InputTag→SelectView→ResizeObserver→Trigger→Select 正常、无渲染错误）；插槽签名经 Arco 源码核对，弹层内显示请以人工刷新验证为准。
11. 复核：`pnpm type-check` 0 error、`pnpm build-only` 成功（dist 已重建）。

## v2 返工范围（对照 demo App.jsx 逐函数复刻）

- **页面结构对齐 demo global-situation-page（L6831-6950）**：页级 `global-workbench-tabs`（科创要素/科创事件双 Tab，切事件 Tab 时右栏收起、主画布全宽）+ 富 FilterBar + work-area（无左/底栏）。
- **SituationFilterBar**（demo FilterBar L1112-1420 + UnifiedEventTimeFilter L1700-1875 全量）：地域级联/学科领域级联（industryDeepCascadeOptions）/科创要素多选/统一时间控件（5 粒度 + trigger + 面板：近7天/近30天/本月/自定义 + 首尾跳转 + 年份滑杆 + 季度/日历演示态 + 起止年）/关键词检索（本地输入态 + 分类候选面板 + 范围摘要 + localStorage 历史）/事件类型多选（事件 Tab）/导出按钮。
- **FactorMapSection**（demo MapSection L2511-2839）：地图/列表视图切换、热力开关、demo 同款 divIcon marker（soft-workbench__map-marker--level/object，色取首个图例要素）、图例（11 类型可点开关图层 + 热力四级渐变）、点位预览卡（影响力指数/所在区域/关联要素 + 查看详情→L6）、对象点叠加（局部视图近似 demo zoom 阈值）、要素列表表（8 列 + 类型/热力/时间三态排序 + 查看/在地图中查看）。
- **GlobalEventSection**（demo L2176-2494）：地图/列表切换、重要性分级条（全部/高/中/低 + 演示口径提示）、热力开关、事件态地图（环形偏移点位 + 事件图例）、事件表（科创事件/类型/重要性/时间三态排序 + 事件详情/在地图中查看 + 共N条 x/y页 + 页码 + 跳至N页）。
- **AnalysisPanel 四 Tab**（demo L5284-5372）：Tab 名冻结 demo analysisTabs（实时数据监控/影响力/聚类分析/要素比较）。
  - OverviewTab（L3926-4295）：chart-head（当前领域/统计指标/折线柱饼切换/导出统计）+ scope-pill + 已隐藏卡恢复条 + 分布面板（饼/折线/柱三态 + 图例）+ 要素卡网格（stat-cell：拖拽排序 + 隐藏 + spark 趋势 + ⓘ/🧪 挂位）。
  - InfluenceTab（L4543-4826）：scope 条/要素卡列/公式注释/核心指标/技术产出子类表/TOP5 条形/查看更多自绘抽屉。
  - ClusterTab（L4828-5090）：要素下拉/4 预设卡/**CSS 点阵四象限**（--x/--y 变量，对齐 demo 非 ECharts）/点选联动/分类列表 TOP5+查看更多。
  - ElementCompareTab（L5093-5282）：推荐组合/复选网格(≤4≥2)/多线趋势。
- **样式**：`styles/demo-situation.css`（4636 行）——按选择器命中从 demo styles.css 整块抽取（同名类 + 同取值），antd 专有在组件 scoped 层以 Arco 等价替换。
- 删除 v1 自创结构组件（MapSection/EventSection 旧版）；TiandituMap 扩展 divIcon marker（html/iconSize/iconAnchor/zIndexOffset/tooltipDisabled，受控无内置数据）。

## 重大发现：dev 模式 slot 子组件 props 更新失效（环境级）

- 现象：dev（vue 3.5.34 + vite 7.3.3）下，异步 mock 数据（200ms）到达后，**slot 内子组件不因 props 变化重渲染**（props/computed 均已更新、render 产物正确、$forceUpdate 无效）；生产构建（preview 实测）一切正常。
- 排除项：vite-plugin-vue-devtools（临时无 devtools 配置复测仍复现）；编译产物（dynamicProps/patchFlag 完好）；mock/api 层（页面内重放请求全部正确）。
- **规避（已落地，生产行为等价 demo 筛选变化重置语义）**：主画布（FactorMapSection/GlobalEventSection）与 AnalysisPanel 绑数据签名 key（demo fieldScopeSignature 同款语义）；四个 Tab 内容根绑数据签名 key；关键词输入改 FilterBar 本地态。全部交互经浏览器实测恢复。
- 建议：后续任务单独立 issue 给 platform 侧（升级 vue/vite 或最小复现上报），本仓 dev 验证页面时如遇"数据到了界面不动"优先怀疑此处。

## 验收证据（浏览器实测）

- 生产模式（vite preview，3101）：图例 11 按钮/热力 4 级/要素卡 9 张/marker 30 全渲染。
- dev 模式（3100/3102，USE_MOCK=true）实测通过：
  - 要素 Tab：图例 11 + 点选开关图层（disabled 2→3）；列表视图 30 行 8 列 + 类型/热力/时间三态排序；预览卡；
  - 事件 Tab：重要性条（全部/高/中/低）、5 事件点位、事件图例（热点/舆情）、事件表 5 行 + 分页"共 5 条 1/1 页"+ 跳转、事件详情抽屉（四段）+ footer 动作；
  - 分析面板：影响力 4 卡 + TOP5 + 子类表（专家卡因测试中图例关闭而过滤，行为正确）；聚类 4 预设卡/32 点阵/图例/分类列表 TOP5/8+查看更多；要素比较（推荐组合按可用集裁剪 + 3/4 复选 + 趋势对比图）；
  - 控件：统一时间（trigger"2020-2026 年粒度·2026" + 快捷 4 项 + 年份滑杆 + 起止下拉）；关键词面板（"深圳"→企业 1/组织机构 1 + 候选项）；
  - 导出：config（CSV + 30 行策略）→ 生成 → 下载（v1 已通，状态机未改动）。
- `pnpm type-check` 0 error；`pnpm build-only` 成功（production 已重建，dist 恢复正式版）。

## 偏离与决策记录

- v1 的类型加法/底座修复（types 4 处、InsightDetailDrawer footer bug、lib 类型修复、detailModel relations 兼容、TiandituMap dblclick）全部保留。
- 聚类散点用 demo 的 CSS 点阵而非 ECharts（demo 原样即 CSS 点）。
- 事件时间轴控件在 FilterBar（demo 结构），v1 的右栏 EventSection 已删除；事件浏览在事件 Tab 主画布（demo GlobalEventSection）。
- FilterBar 无"重置"按钮（demo 无；如需重置可后续在 tabs 行补）。
- 对象点叠加用"局部视图"（regions ≤16 或含 localDetail）近似 demo 的 zoom 阈值显示。

## CI/CD（必填）

- 分支：`dev`（工作区未提交，零 git 操作）
- dev 测试：`VITE_APP_USE_MOCK=true pnpm dev` → `/trend/tech-overall-situation`（注意上述 dev 已知问题及规避均已落地）

## 涉及文件（v2 增量）

**新增**：`src/views/situation/overview/styles/demo-situation.css`、`components/{SituationFilterBar,FactorMapSection,GlobalEventSection}.vue`
**重写**：`components/{OverviewTab,InfluenceTab,ClusterTab,ElementCompareTab,AnalysisPanel}.vue`、`index.vue`
**删除**：v1 `components/{MapSection,EventSection}.vue`
**修改**：`components/map/TiandituMap.vue`（divIcon 扩展）、`models/situationModel.ts`（+关键词分类/历史/范围摘要）、`src/router/menu.ts`（fullBleed meta）、`src/layouts/DefaultLayout.vue` + `src/assets/layout/layout.css`（content-shell--flush 变体）、`src/components/workbench/WorkbenchLayout.vue`（shellTag/shellClass props）、`src/components/drawer/InsightDetailDrawer.vue` + `src/components/export/ExportFlowPanel.vue` + `components/InfluenceTab.vue`（Teleport body）
**清理**：临时 `vite.debug.config.ts`、`dist-mock/` 已删除；dist 已重建为 production。

## 遗留风险

- dev 模式环境级 props 更新问题（见"重大发现"）：已规避主要面，建议 platform 侧根治；若后续新增依赖 props 深链的交互在 dev 下"不动"，按同模式加数据签名 key。
- metric_id（`TS-M1-*`）为前端占位，D9 正式接入 `/metrics/v1/catalog` 后替换。
- 事件态地图锚点在非默认地域选择下与 demo 全量池的取模基可能不同（种子 9 事件默认视口下与 demo 逐点一致）。

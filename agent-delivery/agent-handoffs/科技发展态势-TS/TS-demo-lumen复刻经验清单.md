# demo → lumen 复刻经验清单（TS 模块 01A~10A 沉淀）

> 真源：本文件。维护方式：每次整页复刻交付后，把本轮新教训**追加进对应分类**（附出处任务 ID + commit）。
> 消费方：后续所有 demo→lumen 页面复刻任务（建单时在 note 引用本文件；执行 agent 开工必读）。
> 仓级强制摘要：`repos/lumen-ui-science-pc/AGENTS.md`「demo→lumen 复刻经验」节（与本文件不一致时以本文件为准）。
> 建立：2026-10-19，coordinator 汇编自 FE-TS-S01/01A~09A handoffs；**2026-10-19 human:孔东 裁定两条原则**（见 §1/§2）。

---

## 1. Arco 使用规范（原则：Arco 优先，bug 修根因）⚠️ 用户裁定

> **裁定原文（2026-10-19）**：「demo 用原生 select 的不换 Arco a-select。这条不算，能用 Arco 现成组件的要换掉，有 bug 要解决 bug 而不是回到原生 select。」

1. **能用 Arco 现成组件的一律用 Arco**：demo 用原生 `<select>`/`<input>` 的，lumen 复刻时必须换 `a-select`/`a-input` 等 Arco 对应组件（对齐 D8 前端规范唯一来源）。**禁止以「Arco 有 bug」为由回退原生控件**——bug 要修根因。
   - 历史回退案例（后续复刻同类页时需回补 Arco 化）：M1 起止年下拉（FE-TS-01A v2.1 修 5）、M7 DetailPage 详情筛选（FE-TS-07A 遗留）、M9 筛选条曾部分回退（FE-TS-09A b2c7a0d 只修了 label 包裹问题）。
2. **Arco 已知坑与根因修法**（修层叠/插槽/触发链，不换组件）：
   - `#option` 作用域插槽参数是 `{ data: 选项原始对象 }`（Arco 2.58.0 源码 `optionSlot({ data: optionInfo.raw })`）；直接解构 `{ label, color }` 全 undefined → 用 `#option="{ data }"` 渲染 `data.label`（M1 v2.1 修 3）。
   - `<label>` 包裹 `a-select` 致下拉**闪开即关** → label 与控件分离，用 `<div>` 包裹 + 独立 `<label>`（M9 b2c7a0d）。
   - `a-select` 弹层「闪现消失」：优先排查层叠上下文边界（`isolation`/`transform`/`backdrop-filter` 祖先）与 Trigger 挂载容器，而非换原生。
   - cascader **无 `popup-render` 插槽**（只消费 empty/label/prefix）：多选一律标准 Arco cascader 多选 + 原生 `allow-clear`，**禁自绘 footer/确认按钮/防误关**（M8 ComparisonCascadeSelect 自绘版两轮回退教训，f008cdb 终版收敛）。
   - 收窄自定义选择器范围（如 `.tien-field button`），避免覆盖 Arco 内部清除图标（M7）。
3. **Arco 图标必须显式 import**：`@arco-design/web-vue/es/icon`；unplugin ArcoResolver 在本仓不接管 `icon-*` 标签，未导入会渲染为未知元素（M1 v2.1 修 6）。
4. **控件 token**：控件高 32px（`.gi-btn--sm` 同理）、按钮圆角 4px（M8 3200adc）、主色 `#165DFF`；年份范围选择统一 `a-range-picker mode="year"`（M4 沉淀标准，防 `[Date, undefined]` 半选 NaN 需守卫）。

## 2. 组件复用与封装（原则：第二处出现即封装）⚠️ 用户裁定

> **裁定原文（2026-10-19）**：「多处出现的组件要及时封装，方便公用和后期维护。」

1. **同一交互/结构/样式在第 2 处出现时必须封装**：升公共组件（跨模块复用 → `src/components/`）或页内子组件（单模块私有 → 模块目录），禁止复制粘贴类名体系或整段模板。
2. **页内复用他页类名必须样式自含**：组件用了他页 css 类名但该样式只存在于另一页的 css 文件时，离开那页即「样式裸奔」（M8 清空按钮 56b2624 复发教训）——封装组件时 scoped/页内 css 必须自带全部所需规则。
3. **移植公共组件先核对其样式导入**：demo 组件常自带 `import './xxxComponents.css'`（如 `SectionPanel.jsx` 第 3 行）；移植成 `.vue` 时漏掉这行 → 样式仍留在原页面 css，跨模块复用即裸奔（FE-TA-01A 顶尖机构洞察走查教训）。修法按 `PageTabFrame` 先例：组件目录自含 css + 组件内 import；只抽该组件所需块，不整文件复制。
4. **已沉淀公共件（复刻新页先查此清单，不新造）**：
   - `PageTabFrame`（Tab 页框）、`IndustrySelect`（产业级联）、`SearchableCascadeFilter`（可搜索级联筛选）、`MetricSpecHint`（D9 ⓘ）、`MockBadge`（🧪）、`StatCard`/`KpiDeck`
   - `TiandituMap`（天地图底座：divIcon marker/tooltipHtml/图层组/热力/视口聚焦）、`InsightDetailDrawer`（L6 五段）、`ExportFlowPanel`
   - `chartOptions`（CHART_BASE/baseTooltip token 主题）、`models/*.ts` 纯函数派生层、`defineApi` 双轨（mock/网关）
   - `SectionPanel`（FE-TA-01A 起自含 section-panel.css，跨模块可复用）
5. **封装件接口契约写 JSDoc**；不预设用不到的抽象（ponytail：单模块私有不升公共）。

## 3. demo 样式移植

1. demo 样式按**「选择器命中规则整块抽取」**进 `styles/demo-*.css`（同名类 + 同取值），token 对齐 Design.md；antd 专有规则在组件 scoped 层以 Arco 等价替换（如 `.ant-card-body`→`.arco-card-body`，M9）。
2. `pp-l6-section-title` 等无障碍标题的 **sr-only 规则在 styles.css 之外**，整块抽取会漏 → 占行可见；scoped 补 1px 裁剪（M1 v2.1 修 8）。
3. 互斥 `display` 不叠同一节点（GKX 护栏 3）。
4. 页壳结构对齐 demo 真源（如 M1 双层 main 嵌套消除 + `content-shell--flush`/fullBleed 机制，v2.1 修 12）。

## 4. 布局与渲染

1. **fixed 弹层一律 `Teleport to body`**：玻璃壳 `backdrop-filter` 会把壳内 fixed 的 containing block 捕获到壳上，遮罩盖不到侧边栏/头（M1 v2.1 修 12⑤，demo 真源即 createPortal）。
2. **图表容器显式高度**：`v-if` 切换挂载 + flex 容器 `height:auto` 下 echarts init 读 0 高死锁（canvas 存在但 0×0）→ 自适应图加 `flex: 0 0 auto` + 定高（M9 ce812a9 主线根因）。
3. **新图表类型检查 `src/config/echarts.ts` 按需注册**（demo 全量 `window.echarts` 无此问题；M9 漏 SankeyChart 教训）。
4. **Leaflet 层级冲突**：原生控件 z 800–1000 / pane 200–700 压自定义控件 → 地图 frame `isolation: isolate` 圈住层级 + 自定义控件/图例/预览卡抬升 z（M1 v2.1 修 4/7）。
5. **地图容器塌陷**：grid cell 高度链（`.map-section{flex:1;min-height:0}` → frame → `.ts-map{height:100%}`）+ `@vue:mounted` 调 `invalidateSize()`（M1 修 1、M9 Tab2）。
6. **vue-echarts 8 内部 host 高度链断裂（`.echarts-host` 中间层）**：组件根是 `<x-vue-echarts style="height:100%;min-height:Npx">`，canvas 实际挂内部 `.echarts-host{height:100%}`——参照 `height:auto` 的父级解析为 0（CSS 规范：min-height 撑起的高度不参与子元素百分比解析），canvas init 0 高且 ResizeObserver 无变化永不恢复（TA-02A 深圳 pane 三 tab 全空白根因）。修法：`.arco-tabs-pane > x-vue-echarts > .echarts-host { min-height: 280px }` 传导 min-height，保留 demo `height:auto` 自适应语义。**附带坑**：Arco 类名是 `arco-tabs-pane` 不是 antd 的 `arco-tabs-tabpane`，从 antd CSS 移植 `.arco-tabs-tabpane` 选择器全部静默失效。

## 5. 数据与状态

1. **首屏同步初值防白屏**：同步 DEFAULT/种子初值渲染，`onMounted` 后台刷新，失败仅 warning 不挡页（M7 教训）。
2. **dev 模式 slot 子组件 props 更新失效（环境级）**：vue 3.5.34 + vite 7.3.3 dev 下异步数据到达后 slot 内子组件不重渲染（生产正常）；按 demo 同款**数据签名 key** 规避（M1 重大发现；根治需 platform 侧升级/上报）。
3. **mock 种子冻结自 demo**：确定性生成、派生链禁手写、禁 `Math.random`；头注释标真源路径 + 同步任务 ID；`USE_MOCK=false` 零 fixture 渲染（D12）。
4. 写操作演示态（demo「Mock 可点」不落库同语义）保持会话级/localStorage，**不替 BE 拍板契约**，偏离记 handoff。

## 6. 工程验证

1. **类型门一律 `pnpm type-check`**：`vue-tsc --noEmit` 在本仓（project-references，根 tsconfig `files: []`）是**空跑**——M2 曾因此漏 89 错（FE-TS-02A「类型门修复」节）。
2. 表格操作列按钮 `flex-wrap: wrap` + 按钮 `flex-shrink: 0; white-space: nowrap` 防压缩变形（M4 修 2）。
3. 多选筛选标签超限：`:max-tag-count` + CSS 单行 clamp 折叠为 `+n`（M5）。
4. 状态机移植保留**最小自检** `test.mjs`（demo 带 `*.test.mjs` 的按断言语义摘选；ponytail 要求，M8 55 项/M7 42 项先例）。
5. 交付验证三绿：`pnpm type-check` 0 错 + 自检全绿 + `pnpm build` 绿；交互走查用 CDP 像素采样确认图表实绘（M9 先例）。

---

## 附：出处索引

| 任务 | 关键教训 |
|---|---|
| FE-TS-S01 | 底座组件清单、Mock 开关机制 |
| FE-TA-S01 | 人才模块基座（种子冻结/Pinia 导航/4 页壳） |
| FE-TA-01A | SectionPanel 移植漏自含样式 → 跨模块 tt-* 裸奔（走查修正）；PowerShell 字符级替换损坏 .vue（改用 Write 重写） |
| FE-TS-01A | Arco #option 插槽签名、层叠/isolation、Teleport、sr-only、dev slot props 失效、数据签名 key |
| FE-TS-02A | pnpm type-check 真门（89 错教训）、G6/xlsx 新增依赖记录 |
| FE-TS-03A | 三阶段状态机、InsightDetailDrawer 下钻扩展 |
| FE-TS-04A | RangePicker(year) 沉淀、按钮防变形、弹窗内边距统一 |
| FE-TS-05A | 多选标签 +n 折叠、models 纯函数派生 |
| FE-TS-06A | （handoff 并入 07A 同批提交）register/menu 交织提交先例 |
| FE-TS-07A | 首屏同步初值、Arco Form/Cascader 表单化、选择器收窄 |
| FE-TS-08A | cascader 无 popup-render（两轮回退终版收敛）、样式自含、按钮 token |
| FE-TS-09A | echarts init 竞态显式高度、按需注册 SankeyChart、label 包裹闪关、D10 静态装饰补真实交互 |

# 通用交互组件与栅格体系 · Design.md 完善派单话术

> **生命周期（2026-07-12）**：已完成历史派单。任务 `E-PROD-UXUE-COMP-L02` 已于 2026-06-24 完成，规则已沉淀到 `agent-delivery/Design.md`；本文件只保留派单与验收追溯，不再作为现行规范输入、再次派发或要求回填。

> **任务 ID**：E-PROD-UXUE-COMP-L02
> **用途**：接力《UX-UE 通用交互组件规范.md》和 Figma 交互组组件库，派给 **ui-agent / UI 同学** 直接完善 `agent-delivery/Design.md`。
> **目录**：`agent-delivery/agent-handoffs/产品整体定义/`
> **上游输入**：`UX-UE 通用交互组件规范.md`、Figma 交互组组件库、当前 `Design.md`
> **输出真源**：`agent-delivery/Design.md`
> **编排依据**：用户 2026-06-24 决策采用方案 1：不另起 `UI-通用交互组件视觉规范.md`，直接完善权威 `Design.md`。

---

## 派单话术开始

/goal ui-agent

## 身份

你是 **ui-agent** —— 资深 UI 设计师 / UI 工程师。你需要严格遵循 `agent-delivery/Design.md`、Figma 交互组组件库，以及《UX-UE 通用交互组件规范.md》，把通用交互组件、24 栅格体系、间距 token、断点策略和验收清单统一沉淀到权威 `Design.md`。

本任务是**产品整体定义类规范接力**，不是业务页面重做；只改编排文档，不改业务代码，不新增独立 UI handoff 文档。

## 任务

直接完善 `agent-delivery/Design.md`，重点覆盖以下内容。

### 1. 顶部导航、左侧导航

- 明确顶部导航、左侧导航是 **Figma 定制化组件**，不直接等同 Arco `Menu` / `Tabs`。
- 保留菜单 / 页签语义、激活态、悬停态、禁用态、键盘可达与无障碍状态。
- 补充高度、宽度、层级、图标/文本关系、折叠态、选中态、hover、disabled、focus-visible。
- 说明哪些状态由 UI 规范约束，哪些业务权限/路由逻辑交给 frontend-agent。

### 2. 一级 Tab、二级圆角 Tab、按钮组

- 对齐 Figma `TAB和按钮组` frame。
- 明确一级 Tab、二级圆角 Tab、按钮组的使用边界、视觉层级、间距、圆角、选中态、hover、disabled、loading、溢出处理。
- 补充 Arco API 映射：哪些可用 Arco 原生组件，哪些是“定制组件 + Arco 语义”。
- 不把主导航误写成普通 tabs；一级 Tab 用于页面内同级内容切换，二级圆角 Tab 用于局部维度切换，按钮组用于动作或模式组合。

### 3. 地图图例与热力图例

- 基础图例固定在地图容器右下角，跟随地图容器显示。
- 热力开关开启时：地图叠加热力覆盖层，同时展示基础图例和热力强度分级图例。
- 热力开关关闭时：隐藏热力覆盖层和热力强度分级图例，保留基础图例和点位 / 区域对象。
- 热力强度分级只表达密度或强度趋势，不用于精确读取单点数值。
- 图例不遮挡核心地图对象；全屏时图例需要保留。

### 4. Arco 外围 + 可视化内核

- 明确图表、地图、图谱不是纯 Arco 组件。
- Arco 负责外围容器、工具栏、筛选、图例、状态、弹层、反馈。
- ECharts / GIS / 图谱库负责渲染内核。
- 说明 loading、empty、error、selected、hover、brush、fullscreen 等状态如何由外围与内核协同。
- 避免 frontend-agent 把可视化交互全部误认为 Arco 组件能力。

### 5. 24 栅格体系、间距 token、断点策略

- 写入页面级 24 栅格系统：栅格从当前左侧导航右边界开始计算。
- 展开态：`offset 200 / 24 columns / 56px column / 16px gutter`。
- 收起态：`offset 64 / 24 columns / 62px column / 16px gutter`，主内容横向扩展。
- PC 端所有断点保持 `24 columns` 和 `16px gutter` 不变，只调整 column width、导航状态和面板策略。
- 写入页面级 / 卡片级 / 表单级 / 浮层级的栅格复用规则。
- 写入间距 token：`4 / 8 / 12 / 16 / 24 / 32`。
- 将筛选区默认 gap 收敛为 `16px`，宽松场景为 `24px`，不得使用 `20px` 字段间距。

### 6. Design.md §14 检查与验收

- 把导航、Tab、按钮组、地图/热力图例、Arco 外围 + 可视化内核边界纳入 `Design.md §14`。
- 把 24 栅格、固定 gutter、展开/收起态 offset、间距 token 和断点策略纳入 `Design.md §14`。
- 验收标准需包含：图表、地图、图谱必须由专业可视化内核承载，Arco 只负责外围容器、工具栏、图例、状态反馈和弹层。

## 必读

- `agent-delivery/Design.md`
- `agent-delivery/智能体编排与派单手册.md` §6.1、§9.1d
- `agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`
- Figma：交互组组件库，重点看顶部导航、左侧导航、`TAB和按钮组`、24 栅格 Layout Guide
- 可参考同目录先例：`UI-权限视觉规范-企业维度.md`

## 输出

只输出到：

`agent-delivery/Design.md`

不要再新增：

`agent-delivery/agent-handoffs/产品整体定义/UI-通用交互组件视觉规范.md`

## 硬约束

- 不改 lumen 正式工程。
- 不写业务逻辑。
- 不扩大权限态细则，权限继续引用专项权限文档。
- 不把顶部导航 / 左侧导航误写成直接使用 Arco 原生组件。
- 不新增一套脱离 `Design.md` 的视觉 token。
- 不把地图、图表、图谱的可视化内核实现误写成 Arco 组件能力。
- 不改变 PC 端 `24 columns` 与 `16px gutter` 的硬约束。
- 不使用 `20px` 作为表单 / 筛选区字段 gap。
- 中文产出，文案克制，直接给下游可执行规格。

## DoD

- `Design.md` 覆盖顶部导航、左侧导航、一级 Tab、二级圆角 Tab、按钮组、地图图例、热力图例、可视化内核边界。
- `Design.md` 覆盖 24 栅格体系、栅格复用层级、间距 token、断点策略。
- `Design.md §14` 覆盖上述新增规范的检查项和验收标准。
- 每类组件至少包含常态、悬停、选中、禁用、加载、空态/异常或不可用态。
- token 表完整，且能追溯到 `Design.md`。
- 明确哪些组件是 Arco 原生，哪些是 Figma 定制组件 + Arco 语义，哪些是专业可视化内核。
- commit 本地，不 push；hash 记入任务回填或交付说明。

## Handoff

完成后回填：

- `task-registry.yaml` 中 `E-PROD-UXUE-COMP-L02` 状态。
- `evidence: Design.md`。
- DoD 对照说明。
- commit hash。

中文产出，开始执行。

## 派单话术结束

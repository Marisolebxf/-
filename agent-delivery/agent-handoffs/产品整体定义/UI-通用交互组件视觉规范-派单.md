# UI 通用交互组件视觉规范 · 派单话术

> **用途**：接力《UX-UE 通用交互组件规范.md》，派给 **ui-agent / UI 同学** 输出视觉规范、组件状态、token 对照与 frontend-agent 接力建议。
> **目录**：`agent-delivery/agent-handoffs/产品整体定义/`
> **上游输入**：`UX-UE 通用交互组件规范.md`
> **下游接力**：UI 评审通过后，再派 `frontend-agent` 做 lumen 工程化复刻。
> **编排依据**：`agent-delivery/智能体编排与派单手册.md` §6.1、§9.1d：UI/UE 链路为 `ux-agent → ui-agent → UI/UE 评审/甲方汇报 → frontend-agent`。

---

## 派单话术开始

/goal ui-agent

## 身份

你是 **ui-agent** —— 资深 UI 设计师 / UI 工程师，严格遵循 `agent-delivery/Design.md`、Figma 交互组组件库，以及《UX-UE 通用交互组件规范.md》。你的任务是把 UX 交互规范转成 UI 可落地的视觉规范、组件状态、token 使用建议和必要的 demo2 沙箱验证建议。

本任务是**产品整体定义类规范接力**，不是业务页面重做；优先产出规范文档，必要时再建议 demo2 沙箱验证方案。

## 任务

接力《UX-UE 通用交互组件规范.md》，为通用交互组件补充 UI 视觉落地说明，重点覆盖以下内容。

### 1. 顶部导航、左侧导航

- 明确顶部导航、左侧导航是 **Figma 定制化组件**，不直接等同 Arco `Menu` / `Tabs`。
- 需要保留菜单 / 页签语义、激活态、悬停态、禁用态、键盘可达与无障碍状态。
- 输出 UI 视觉规则：高度、宽度、层级、图标/文本关系、折叠态、选中态、hover、disabled、focus-visible。
- 说明哪些状态由 UI 规范约束，哪些业务权限/路由逻辑交给 frontend-agent。

### 2. 一级 Tab、二级圆角 Tab、按钮组

- 对齐 Figma `TAB和按钮组` frame。
- 明确一级 Tab、二级圆角 Tab、按钮组的使用边界、视觉层级、间距、圆角、选中态、hover、disabled、loading、溢出处理。
- 补充 UI 侧 Arco API 映射：哪些可用 Arco 原生组件，哪些是“定制组件 + Arco 语义”。
- 不把主导航误写成普通 tabs；一级 Tab 用于页面内同级内容切换，二级圆角 Tab 用于局部维度切换，按钮组用于动作或模式组合。

### 3. 地图图例与热力图例

- 基础图例固定在地图容器右下角，跟随地图容器显示。
- 热力开关开启时：地图叠加热力覆盖层，同时展示基础图例和热力强度分级图例。
- 热力开关关闭时：隐藏热力覆盖层和热力强度分级图例，保留基础图例和点位 / 区域对象。
- 热力强度分级只表达密度或强度趋势，不用于精确读取单点数值。
- 图例不遮挡核心地图对象；全屏时图例需要保留。

### 4. Arco 外围 + 可视化内核

- 明确图表、地图、图谱不是纯 Arco 组件。
- UI 侧需要定义外围容器、工具栏、筛选、状态、弹层、反馈样式。
- ECharts / GIS / 图谱库负责渲染内核；UI 规范需要说明二者联动时的 loading、empty、error、selected、hover、brush、fullscreen 等状态展示。
- 输出“Arco 外围”和“可视化内核”的边界说明，避免 frontend-agent 把可视化交互全部误认为 Arco 组件能力。

## 必读

- `agent-delivery/Design.md`
- `agent-delivery/智能体编排与派单手册.md` §6.1、§9.1d
- `agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`
- Figma：交互组组件库，重点看顶部导航、左侧导航、`TAB和按钮组`
- 可参考同目录先例：`UI-权限视觉规范-企业维度.md`

## 输出

在产品整体定义目录输出：

`agent-delivery/agent-handoffs/产品整体定义/UI-通用交互组件视觉规范.md`

内容至少包含：

1. 顶部导航 / 左侧导航视觉规则。
2. 一级 Tab / 二级圆角 Tab / 按钮组视觉规则。
3. 地图基础图例 / 热力强度图例视觉规则。
4. `Arco 外围 + 可视化内核` 的 UI 视觉边界。
5. 状态矩阵：default / hover / active / selected / disabled / loading / empty / error / focus-visible。
6. token 对照表：颜色、字号、圆角、间距、描边、阴影、控件高度。
7. Arco API 与定制组件边界说明。
8. 给 frontend-agent 的实现接力：组件名、props 建议、CSS token / class 命名建议、验收注意事项。
9. Design.md §14 或现行验收清单对照。

## 硬约束

- 不改 lumen 正式工程。
- 不写业务逻辑。
- 不扩大权限态细则，权限继续引用专项权限文档。
- 不把顶部导航 / 左侧导航误写成直接使用 Arco 原生组件。
- 不新增一套脱离 Design.md 的视觉 token。
- 不把地图、图表、图谱的可视化内核实现误写成 Arco 组件能力。
- 中文产出，文案克制，直接给下游可执行规格。

## DoD

- 覆盖顶部导航、左侧导航、一级 Tab、二级圆角 Tab、按钮组、地图图例、热力图例、可视化内核边界。
- 每类组件至少包含常态、悬停、选中、禁用、加载、空态/异常或不可用态。
- token 表完整，且能追溯到 `Design.md`。
- 明确哪些组件是 Arco 原生，哪些是 Figma 定制组件 + Arco 语义。
- 末尾附给 frontend-agent 的接力建议。
- commit 但不 push，hash 记入文档末尾。

## Handoff

完成后在 `UI-通用交互组件视觉规范.md` 末尾附：

- DoD 对照表。
- Design.md 对照表。
- 给 frontend-agent 的实现接力。
- 开放项与需 UI/UE 评审项。
- commit hash。

中文产出，开始执行。

## 派单话术结束


# Handoff · FE-ENT-topbar-hierarchy（企业中心顶部层级与 ContextBar 分层落地）

- **角色 / 执行方**：`[agent:frontend-agent]`
- **日期**：2026-07-01
- **目标仓**：`repos/demo-ui-topic`（原型仓，实际分支由 coordinator 指定）
- **任务 ID**：`FE-ENT-TOPBAR-HIERARCHY`
- **上游规则**：
  - `docs/ia/enterprise/ENT-IA.md`
  - `docs/ia/enterprise/ENT-element-master-design.md`
  - `docs/ia/enterprise/ENT-search-design.md`
  - `gkx-orchestration/agent-delivery/Design.md`
  - `gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`
  - `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-UE-IA-L03a-topbar-hierarchy.md`
  - `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/PM-ENT-global-search-scope-confirmation.md`

> 本任务只落地企业中心顶部层级与搜索 / 筛选归位，不重构左侧四个二级菜单，不删除旧路由，不新增“企业检索”固定 Tab。

---

## 1. 背景问题

当前企业中心四个二级页面顶部区域容易把下列信息混在一起：

| 元素 | 当前歧义 |
|---|---|
| 页面标题“企业中心 · 企业总览” | 与左侧菜单当前位置、面包屑功能重复 |
| 当前页 / 当前 Tab 标识 | 同时可能出现在标题、Tag、Tab 选中态中 |
| 全局搜索、刷新等页面操作 | 容易被理解成当前二级页能力，也可能被理解成企业中心或系统级能力 |
| ContextBar：产业 / 时间 / 区域 | 需要表达跨 Tab 保留的基础分析口径，但不能承载所有筛选 |
| 页内一级 Tab：态势概览 / 企业分布 / 重点对象 / 风险机会 | 需要明确是当前二级页面内部的视角切换，不是左侧二级菜单 |

前端需要按新规则拆清顶部层级，使用户能识别：当前位置、页内视角、跨 Tab 基础口径、局部筛选和页面操作分别属于哪里。

---

## 2. 范围

### 2.1 必须覆盖的页面

企业中心四个二级页面共用同一顶部结构：

| 二级页面 | 路由示例 | 说明 |
|---|---|---|
| 企业总览 | `/enterprise-center/overview` | 当前重点验收页 |
| 企业全景 | `/enterprise-center/panorama` 或现有等价路由 | 保持现有 IA 与旧路由兼容 |
| 企业洞察 | `/enterprise-center/insight` 或现有等价路由 | 保持现有 IA 与旧路由兼容 |
| 企业决策 | `/enterprise-center/decision` | 当前重点验收页 |

以代码实际路由为准；不得为本任务调整左侧四个二级菜单的信息架构。

### 2.2 不纳入范围

- 不新增企业检索固定 Tab。
- 不把企业检索作为左侧第五个二级菜单。
- 不在系统 Header 增加“全局搜索”。
- 不删除旧总览入口、旧检索入口或兼容路由。
- 不实现产品尚未确认的系统级全局搜索。
- 不重做企业画像、企业检索、企业列表的数据模型。

---

## 3. 顶部最终结构

四个二级页面统一使用下列结构：

```text
EnterprisePageTop
├─ ContextBar
│  └─ 基础分析口径：产业 / 时间 / 区域 / 企业群（如已有产品确认）
├─ PrimaryWorkbenchTabs
│  └─ 当前二级页面内的一级 Tab，例如：态势概览 / 企业分布 / 重点对象 / 风险机会
└─ TabContentHeader
   └─ 当前 Tab 的业务结论、状态、局部操作或局部 FilterBar
```

### 3.1 不显示路径型页面标题

四个二级页面不在正式 UI 顶部显示“企业中心 · 企业总览”这类路径型标题。

保留方式：

- 可保留为 `document.title`、route meta、埋点字段、无障碍名称。
- 左侧菜单 active 状态负责表达当前二级页面。
- 当前 Tab 只由 `PrimaryWorkbenchTabs` 选中态表达。
- 不在右上角重复显示“当前 Tab” Tag。

### 3.2 面包屑规则

四个二级页面不显示面包屑。

深层横向能力页按 `source` 显示新 IA 面包屑，例如：

```text
企业中心 / 企业总览 / 企业检索
企业中心 / 企业决策 / 企业画像
```

深层页显示面包屑后，不再额外显示重复路径型标题；只有业务对象标题或结果主题可显示，例如企业名称、报告名称、检索结果主题。

---

## 4. ContextBar 与局部 FilterBar

### 4.1 基础 ContextBar

ContextBar 是企业中心级基础分析口径，只承载跨二级页、跨 Tab 保留的基础条件。

| 字段 | 规则 |
|---|---|
| 产业 | 允许跨四个二级页面继承 |
| 时间 | 允许跨四个二级页面继承 |
| 区域 | 允许跨四个二级页面继承 |
| 企业群 | 仅在产品与数据口径确认后启用；未确认时不得硬塞到 ContextBar |

ContextBar 固定在页内一级 Tab 上方。

### 4.2 局部 FilterBar

每个 Tab 的专业筛选放在内容区局部 FilterBar、图表工具条、表格工具条或二级分段控件中。

不得把所有筛选塞进 ContextBar。

| 筛选类型 | 放置位置 |
|---|---|
| 企业类型、规模、资质、名单类型 | 当前 Tab 内容区局部 FilterBar |
| 风险等级、机会等级、评分维度 | 当前 Tab 内容区局部 FilterBar 或图表工具条 |
| 招引 / 培育、强链 / 补链 | 二级分段控件或当前内容区局部 FilterBar |
| 单链 / 多链、技术力 / 商业力 | 二级分段控件 |
| 表格排序、列显隐、结果内搜索 | 表格工具条 |

### 4.3 不适用条件

如果某个二级页面或 Tab 不支持某个基础口径，不能静默隐藏或忽略。

前端需要显示下列状态之一：

- `不适用`
- `禁用`
- `继承但不参与计算`

并通过 Tooltip、说明文案或字段旁状态说明原因。

### 4.4 跨页继承提示

当用户从一个二级页面跳到另一个二级页面，且携带 ContextBar 条件时，应显示一次可关闭提示。

示例：

```text
已沿用 企业总览 的口径：产业=集成电路，区域=深圳，时间=近三年。
```

提示要求：

- 使用 Arco `Alert`、`Message` 或 `Notification`。
- 必须可关闭。
- 关闭提示不清除已继承条件。
- 提供“调整口径 / 清除继承条件”入口。

---

## 5. 搜索与刷新

### 5.1 搜索

本任务不落地“企业中心全局搜索”固定入口。

原因：全局搜索的作用域尚未产品确认，已单独生成 `PM-ENT-GLOBAL-SEARCH-SCOPE` 产品确认任务。

前端落地规则：

- 四个二级页面顶部不放“全局搜索”。
- 系统 Header 不新增搜索。
- 企业检索能力以场景化入口出现，例如“查找企业”“选择企业”“添加对比企业”“筛选企业集合”“打开高级检索”。
- 场景化入口跳转企业检索页时，需要带 `source`、`tab`、`industry`、`region`、`time` 等上下文参数。
- 深层检索页按 `source` 显示面包屑，并恢复来源上下文。

### 5.2 刷新

不默认展示“刷新”按钮。

只有存在真实刷新语义时才显示，并使用明确文案：

| 场景 | 文案 |
|---|---|
| 后端数据重新拉取 | 刷新数据 |
| 模型、评分、诊断重新执行 | 重新计算 |
| 外部数据源同步 | 同步最新 |

如果页面只是 Mock 或静态演示，不显示刷新按钮。

---

## 6. 开发 / 验收态提示处理

类似“来源：企业中心 IA”“旧总览入口保留为兼容路由”“Wave 0 Mock / 待维护字段保留提示”的内容，不属于正式顶部结构。

落地规则：

- 正式演示默认隐藏。
- 如需验收态提示，应下沉到指标、图表、表格或字段旁。
- 使用 `Tag`、`Badge`、`Tooltip`、局部 `Alert` 表达 Mock、待维护、待确认、更新时间。
- 不使用大面积蓝色顶部提示条承载 IA 来源或开发说明。

---

## 7. 建议代码定位

frontend-agent 需要先在 `repos/demo-ui-topic` 中定位实际实现，不要按文件名臆测。

优先搜索：

```bash
rg -n "enterprise-center|企业中心|企业总览|企业决策|ContextBar|global-workbench-tabs|analysis-tabs|刷新|全局搜索" repos/demo-ui-topic/src
```

重点关注：

- 企业中心路由配置
- 左侧菜单 active 判断
- 四个二级页面的 page shell / shared layout
- `ContextBar` 或等价组件
- 页内一级 Tab 组件
- 搜索入口与刷新按钮出现位置
- DevStatusNotice / Mock / pending / update time 等提示组件

---

## 8. 验收标准

### 8.1 视觉与交互验收

- 四个二级页面顶部不显示“企业中心 · xxx”路径型标题。
- 四个二级页面不显示面包屑。
- 当前 Tab 不进入标题，不在右上角重复 Tag，只由一级 Tab 选中态表达。
- ContextBar 在一级 Tab 上方。
- 专业筛选在内容区局部 FilterBar 或工具条中。
- 页面顶部没有“全局搜索”固定入口。
- Header 没有新增系统级搜索。
- 无真实刷新语义时，不显示刷新按钮。
- 开发 / IA / Mock 说明不以大蓝条占据页面顶部。

### 8.2 行为验收

- 切换一级 Tab 时，ContextBar 基础口径保留。
- 修改 ContextBar 时，当前二级页 / 当前 Tab 数据随之更新或重新计算。
- 局部 FilterBar 不自动污染 ContextBar。
- 跨二级页携带 ContextBar 时，有一次可关闭继承提示。
- 深层企业检索 / 企业画像按 `source` 显示面包屑。
- 旧路由仍可访问并按新结构归位。

### 8.3 工程验收

- 使用现有 Arco / 项目封装组件，不新增第二套 UI 控件体系。
- 不引入 Ant Design、原生假按钮、页面私有 Select/Search/Button 克隆。
- 保持 `Design.md` 约束：浅蓝白工作台、32px 控件、16px 间距节奏、`.global-workbench-tabs` / `.analysis-tabs` 既有约定。
- 运行目标仓已有检查，至少包括：

```bash
npm run design:check
npm run build
```

如目标仓没有对应脚本，需在交付说明中写明替代验证方式。

---

## 9. 派单话术

请 frontend-agent 执行 `FE-ENT-TOPBAR-HIERARCHY`。

目标是在 `repos/demo-ui-topic` 落地企业中心四个二级页面的顶部层级归位：四个二级页面共用同一顶部结构，正式 UI 不显示重复路径型标题、不显示面包屑；当前 Tab 只由页内一级 Tab 选中态表达；ContextBar 固定在一级 Tab 上方，只承载产业 / 时间 / 区域等基础分析口径；每个 Tab 的专业筛选下沉到内容区局部 FilterBar、图表 / 表格工具条或二级分段控件。

请不要新增企业检索固定 Tab，不要把企业检索放入左侧二级菜单，不要在页面顶部或系统 Header 增加“全局搜索”。企业检索暂按场景化入口处理，并通过 `source` 与上下文参数回到深层检索 / 画像页。刷新按钮也不要默认展示，只有真实“刷新数据 / 重新计算 / 同步最新”语义时才保留。

实施前请先阅读：

- `docs/ia/enterprise/ENT-IA.md`
- `docs/ia/enterprise/ENT-element-master-design.md`
- `docs/ia/enterprise/ENT-search-design.md`
- `gkx-orchestration/agent-delivery/Design.md`
- `gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`
- `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-UE-IA-L03a-topbar-hierarchy.md`
- `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/PM-ENT-global-search-scope-confirmation.md`

交付时请回填：

- 实际修改的页面 / 组件 / 样式文件
- 四个二级页面顶部结构截图或说明
- ContextBar 与局部 FilterBar 的最终位置
- 搜索入口、刷新按钮、开发提示条的处理结果
- 旧路由兼容验证
- `npm run design:check` / `npm run build` 或替代验证结果
- 未纳入范围与待 PM 确认项


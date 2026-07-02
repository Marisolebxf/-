# Handoff · FE-ENT-search-state-closure（企业高级检索状态闭环）

| 项 | 内容 |
| --- | --- |
| 任务 ID | FE-ENT-SEARCH-STATE-CLOSURE |
| 角色 / 执行方 | frontend-agent |
| 仓库 | `repos/demo-ui-topic` |
| 触发来源 | UE Lead 搜索页评审（ENT-UE-IA-L07 补充） |
| 上游规则 | `ENT-UE-IA-L07-capabilities.md`、`ENT-search-design.md` v1.2.1 |
| 状态 | Ready for frontend-agent |

## 1. 背景

当前从企业中心场景入口进入 `/development/search` 后，SearchHub 仅按 URL `mode` 高亮默认模式，用户仍可切换其它模式。这个行为本身正确，但界面未解释“默认模式不是锁定模式”，容易让用户误解入口任务和三模式之间的关系。

同时，搜索页初始态会直接渲染固定企业结果列表。当前结果来自前端 Mock seed，而非用户已执行的检索条件。该表现会让用户误以为系统已经按“筛选深圳企业 / 查找风险企业 / 导入候选企业集合”等入口任务自动完成筛选。

## 2. 目标

1. 保持 SearchHub 三模式可切换。
2. 明确 `mode` 只是入口默认模式，不是模式锁定。
3. 支持场景入口传递 `task` 参数，并在 SearchHub 局部显示任务提示。
4. 搜索页无用户检索动作时进入初始态，不自动展示固定结果列表。
5. 定义并落地初始态、有结果态、空结果态、示例数据态。
6. Mock seed 结果必须标注“示例数据 / Mock”，不得伪装为真实命中。

## 3. 实施范围

建议先定位当前实现，以下文件名仅作为已知入口：

- `src/app/pages/development/SearchPage.tsx`
- `src/app/components/search/SearchScaffold.tsx`
- `src/app/components/search/SearchHub.tsx`
- `src/app/components/search/ResultToolbar.tsx`
- `src/app/components/search/ResultList.tsx`
- `src/app/pages/enterprise/analysisShared.tsx`
- `src/app/pages/enterprise/enterpriseCenterRouteMap.ts`
- `scripts/check-enterprise-ia.mjs`

不得新增系统 Header 全局搜索，不得新增企业检索固定 Tab，不得把 `/development/search` 放进左侧菜单。

## 4. 交互规则

### 4.1 URL 参数

场景入口进入搜索页时 URL 应至少包含：

```text
source=/enterprise-center/...
tab=...
mode=keyword|smart|advanced
task=筛选深圳企业
```

`industry/region/time` 可继续作为来源上下文元数据传递，但搜索页默认不应用为筛选条件。

### 4.2 SearchHub 局部提示

当 URL 存在 `task` 时，在 SearchHub 区域内显示轻量提示，不放在页面顶部。

示例：

```text
已为“筛选深圳企业”打开高级筛选，可切换关键字或智能搜索。
```

提示需要随当前初始 `mode` 变化：

- `keyword`：关键字检索
- `smart`：智能搜索
- `advanced`：高级筛选

用户切换模式后，提示可保留为来源说明，也可弱化为“当前可自由切换三种检索方式”；不得暗示用户被锁定在某模式。

### 4.3 ResultArea 四态

| 状态 | 触发条件 | 前端表现 |
| --- | --- | --- |
| 初始态 | 未输入关键词、未应用高级筛选、未点击热词或模板 | 不展示固定企业列表；展示推荐条件模板、最近查看、常用筛选入口或简洁空态 |
| 有结果态 | 用户明确执行检索 / 智能解析 / 高级筛选 / 热词 / 模板后命中企业 | 展示结果工具条、结果列表和动作 |
| 空结果态 | 明确检索后无命中 | 展示空态，提供放宽条件、清空筛选、切换模式 |
| 示例数据态 | 使用 `ENTERPRISE_LIST` 等 Mock seed 作为结果来源 | 在结果工具条或结果来源处标注“示例数据 / Mock” |

## 5. 验收

- 从 `筛选深圳企业` 进入搜索页：默认高级筛选，但可切换关键字和智能搜索；局部提示说明来源任务。
- 从 `查找重点企业` 进入搜索页：默认关键字检索，但可切换智能搜索和高级筛选。
- `/development/search` 直达：显示“高级检索”和来源返回条默认企业总览；无 task 提示。
- 搜索页初始态不展示固定结果列表。
- 输入关键词或应用筛选后才展示结果列表。
- 造一个无命中检索，出现空态。
- Mock 结果显示“示例数据 / Mock”。
- 四个企业中心二级页顶部仍无常驻搜索、无面包屑、无重复路径标题。
- 旧路由兼容不破坏。
- `node scripts/check-enterprise-ia.mjs` 通过。
- `npm run design:check` 通过。
- `npm run build` 通过。

## 6. 交付回填

frontend-agent 完成后，请在本文件末尾新增“交付回填”小节，至少包含：

- 实际修改的页面 / 组件 / 样式 / 脚本文件。
- `task` 参数和 SearchHub 局部提示的实现方式。
- 初始态 / 有结果态 / 空结果态 / 示例数据态截图或说明。
- `/development/search` 直达与场景入口 URL 验证。
- 旧路由兼容验证。
- `node scripts/check-enterprise-ia.mjs`、`npm run design:check`、`npm run build` 结果。
- 未纳入范围与待 PM/UE 确认项。

## 7. 可复制派单话术

```text
请 frontend-agent 执行 FE-ENT-SEARCH-STATE-CLOSURE。

目标是在 repos/demo-ui-topic 落地企业高级检索状态闭环：场景入口的 mode 只作为默认模式，不锁定 SearchHub；入口需携带 task 并在 SearchHub 局部提示来源任务；搜索页初始态不再展示固定 Mock 结果列表；结果区补齐初始态、有结果态、空结果态、示例数据态；Mock seed 结果必须标注“示例数据 / Mock”。

实施前请先阅读：
- gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-UE-IA-L07-capabilities.md
- repos/demo-ui-topic/docs/ia/enterprise/ENT-search-design.md
- gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/FE-ENT-search-state-closure.md
- gkx-orchestration/agent-delivery/Design.md
- gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md

不要新增系统级全局搜索，不要新增企业检索固定 Tab，不要把 /development/search 放进左侧菜单，不要默认应用来源 industry/region/time 到搜索页筛选。

交付时请回填：
- 实际修改文件
- task 参数与局部提示实现
- 四态结果区说明或截图
- 场景入口 URL 和直达 URL 验证
- 旧路由兼容验证
- node scripts/check-enterprise-ia.mjs / npm run design:check / npm run build 结果
- 未纳入范围与待确认项
```

## 8. 交付回填（2026-07-01）

### 8.1 实际修改文件

- `repos/demo-ui-topic/src/app/pages/enterprise/enterpriseCenterRouteMap.ts`
- `repos/demo-ui-topic/src/app/pages/enterprise/analysisShared.tsx`
- `repos/demo-ui-topic/src/app/pages/development/SearchPage.tsx`
- `repos/demo-ui-topic/src/app/components/search/SearchHub.tsx`
- `repos/demo-ui-topic/src/app/components/search/SearchScaffold.tsx`
- `repos/demo-ui-topic/scripts/check-enterprise-ia.mjs`

### 8.2 task 参数与 SearchHub 局部提示

- `buildEnterpriseSearchUrl` 增加 `task?: string`，仅写入 URL query。
- `SearchEntryButton` 使用按钮可见文案作为 `task`：`task: typeof children === "string" ? children : undefined`。
- `SearchPage` 读取 `sourceTask = params.get('task')`，传入 `SearchScaffold`；`industry/region/time` 仍只作为 URL 元数据，不接入筛选状态。
- `SearchHub` 在自身卡片内显示局部提示，例如：`已为“筛选深圳企业”打开高级筛选，可切换关键字或智能搜索。`；提示不放页面顶部，不锁定模式。

### 8.3 四态结果区

- 初始态：`hasSubmittedSearch=false`，只展示推荐条件模板、常用筛选入口、最近查看说明；不展示固定 `ENTERPRISE_LIST`。
- 有结果态：用户执行关键字、智能解析、热词或有效高级筛选后，展示 `ResultToolbar`、`ResultList` 和画像/对比/名单/收藏/导出等动作。
- 空结果态：明确检索后无命中，显示“未找到匹配企业”，提供“清空条件”和“放宽筛选”。
- 示例数据态：所有 seed 命中结果旁显示 `示例数据 / Mock`，不伪装真实检索结果。

### 8.4 URL 与路由验证

- 直达 URL：`http://127.0.0.1:4176/development/search`
  - 验证结果：显示“高级检索”；来源返回条为“来自 企业总览”；无 task 提示；初始态不显示结果列表或 Mock 标识。
- 场景入口 URL：`http://127.0.0.1:4176/development/search?source=/enterprise-center/panorama&tab=shenzhen&mode=advanced&task=筛选深圳企业&industry=集成电路&region=南山区&time=last-3y`
  - 验证结果：返回条为“来自 企业全景 / 深圳企业”；默认选中“高级筛选”；SearchHub 局部提示来源任务；`industry/region/time` 未自动产生命中结果。
- 有结果验证：在关键字检索输入 `深芯微` 后出现“深芯微集成电路股份有限公司”、结果工具条和 `示例数据 / Mock`。
- 空结果验证：在关键字检索输入 `不存在企业XYZ` 后出现空态、“清空条件”和“放宽筛选”。
- 旧路由兼容：`http://127.0.0.1:4176/enterprise/competitiveness` 可打开，选中企业中心“竞争力”Tab；`/development/search` 未进入左侧菜单。

### 8.5 检查结果

- `node scripts/check-enterprise-ia.mjs`：通过，输出 `enterprise IA contract passed`。
- `npm run design:check`：通过，输出 `Design contract checks passed`。
- `npm run build`：通过，Vite 构建完成；保留既有 chunk size warning。

### 8.6 未纳入范围与待确认项

- 未新增系统级全局搜索。
- 未新增企业检索固定 Tab。
- 未把 `/development/search` 放入左侧菜单。
- 未把来源 `industry/region/time` 默认应用到搜索页筛选。
- 未接入真实检索接口；当前结果仍来自前端 Mock seed，已在结果区标注。

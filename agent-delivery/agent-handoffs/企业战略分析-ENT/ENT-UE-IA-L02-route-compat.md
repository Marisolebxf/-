# ENT-UE-IA-L02 企业中心旧路由兼容与残留整改交付记录

| 字段 | 内容 |
|---|---|
| 任务 ID | ENT-UE-IA-L02 |
| 任务名称 | 企业中心 IA - 旧路由兼容与 active menu/tab 映射 |
| 执行角色 | frontend-agent |
| 目标仓库 | `repos/demo-ui-topic` |
| 前置任务 | ENT-UE-IA-L01 |
| 当前状态 | 已完成（frontend-agent 回填） |
| 生成日期 | 2026-07-01 |
| 文档用途 | 记录 L02 派单依据、执行范围、最终映射、验证结果和后续 L03/L07 待办 |

## 0. 最新结论

`ENT-UE-IA-L02` 已完成。当前代码已在不删除旧路由的前提下，将旧 `/development/*` 与 `/enterprise/*` URL 统一映射到企业中心新 IA：左侧 active menu、页面内 Tab、标题和横向能力入口均按「企业中心 / 企业总览 / 企业全景 / 企业洞察 / 企业决策」口径收敛。

后续不需要再回改 `ENT-IA.md`、`ENT-element-master-design.md`、`ENT-search-design.md` 作为 L02 前置条件；它们仍作为上位规范。下一步若继续推进，应进入：

- L03：企业总览深层内容整合。
- L07：企业检索完整横向能力闭环。
- 独立修复：产业链 `ChainProfilePage.tsx` 的 `design:check` 既有失败。

## 1. 背景结论

L01 已完成企业中心外壳收敛：左侧企业相关入口已统一为「企业中心」下四个二级菜单，旧 `/development/*` 与 `/enterprise/*` 路由保留直达能力。

L02 执行前的剩余问题不是重新设计 IA，而是把旧页面、旧路由、旧标题和横向能力入口继续收敛到新 IA 口径：

- 旧 URL 直达时，应高亮对应「企业中心」二级菜单，并选中对应页面内一级 Tab。
- 旧页面内标题、面包屑、route handle title 不应继续强化「门户-企业发展 / 企业分析」来源拆分。
- 企业检索、企业画像、对比篮、收藏、最近查看是横向能力，不应作为左侧菜单或固定主 Tab 承担主导航职责。
- 企业中心页内筛选上下文应在菜单、Tab、旧路由跳转时保留。

## 2. 权威依据

按以下优先级执行，不另起 IA：

1. `repos/demo-ui-topic/docs/ia/enterprise/ENT-IA.md`
2. `repos/demo-ui-topic/docs/ia/enterprise/ENT-element-master-design.md`
3. `repos/demo-ui-topic/docs/ia/enterprise/ENT-search-design.md`
4. `gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`
5. `gkx-orchestration/agent-delivery/Design.md`
6. 当前前端实现：`repos/demo-ui-topic/src/app/**`

## 3. 整改范围（已执行）

本任务只做 L02 兼容与残留收敛，不做深层业务页重写。

### 已执行

- 旧路由到新 IA 的 active menu / active tab 映射。
- 旧路由下的标题、面包屑、route handle title 新 IA 口径收敛。
- 企业检索入口的横向能力化处理。
- 企业中心 ContextBar 上下文保留。
- `scripts/check-enterprise-ia.mjs` 增强，覆盖本次整改契约。

### 未纳入 L02

- 不删除旧 `/development/*` 与 `/enterprise/*` 路由。
- 不重写 ECharts / 表格 / mock 数据。
- 不新增后台内容管理入口。
- 不把企业画像、企业检索放回左侧菜单。
- 不把 E-36/E-37 做成前台菜单或前台页面。

## 4. 执行前残留清单（已处理或转后续）

| 优先级 | 分类 | 执行前问题 | 处理结果 |
|---|---|---|---|
| P0 | 旧路由兼容 | 旧 URL 直达时无法高亮对应企业中心二级菜单，也无法选中对应页面内 Tab。 | 已新增 `enterpriseCenterRouteMap.ts`，`Layout` 与 `EnterpriseCenterPage` 均消费同一映射。 |
| P0 | 标题口径 | 旧 route handle title 仍使用「企业发展概况 / 企业概览 / 重点企业全景图 / 企业引育决策」等旧口径。 | 已在 `routes.tsx` 收敛为「企业中心 · 二级菜单 · Tab」口径。 |
| P0 | Tab 命名 | 企业总览 Tab 是「总览看板 / 结构分布 / 重点名单 / 更新动态」，与 ENT-IA 不一致。 | 已改为「态势概览 / 企业分布 / 重点对象 / 风险机会」。 |
| P1 | 横向能力 | 企业检索以「名单视图」固定放在企业全景 Tab 中，容易被理解为主导航页面。 | 已移除固定「名单视图」Tab；`/development/search` 保留为横向检索能力落地页。 |
| P1 | 交互未接 | 企业中心顶部「全局搜索」按钮只有视觉入口。 | 已接入 `/development/search`，并携带来源、产业和当前 Tab 上下文。 |
| P1 | 上下文保留 | 企业中心聚合页 ContextBar `onChange` 为空实现。 | 已上提为页面状态，并持久到 `sessionStorage`，避免菜单/Tab/旧路由切换时静默丢失。 |
| P1 | 面包屑一致性 | 旧页面内面包屑仍需统一映射到二级菜单和 Tab。 | 检索和画像页已改为企业中心横向能力口径；旧业务页由企业中心聚合页承载。 |
| P2 | 注释和骨架债务 | 分析层公共骨架仍写着“分析层由左侧 TopicSidebar 承载导航”。 | 已更新为企业洞察/决策可由企业中心 Tab 或旧路由兼容承载。 |
| P2 | 旧视觉债务 | `DevelopmentOverview` 仍保留旧门户页面注释、`recharts` 和硬编码色值。 | L02 仅修正面包屑末级为「企业分布」；深层视觉重构转 L03。 |
| P2 | 深度分析跳转 | 企业画像整页「深度分析」只弹 Mock 消息。 | 已改为跳转企业决策 / 能力评估，并携带 `enterprise_code`。 |

## 5. 最终映射表

映射源已沉淀为 `repos/demo-ui-topic/src/app/pages/enterprise/enterpriseCenterRouteMap.ts`，避免 Layout、路由、面包屑和 Tab 各写一套。

| 旧路由 | 新菜单 | Tab | 备注 |
|---|---|---|---|
| `/development/overview` | 企业总览 | 企业分布 | 门户概况承载 |
| `/enterprise/overview` | 企业总览 | 态势概览 | 分析驾驶舱归总览 |
| `/development/key-enterprises` | 企业全景 | 重点企业 | E-33 |
| `/development/star-enterprises` | 企业全景 | 明星企业 | E-34 |
| `/development/shenzhen` | 企业全景 | 深圳企业 | E-35 |
| `/development/search` | 横向能力 | 企业检索 / 高级检索落地页 | 不作为左侧菜单；来源上下文决定返回位置 |
| `/development/enterprise/:enterpriseCode` | 横向能力 | 统一企业画像 | 不作为左侧菜单；面包屑回到来源或企业全景 |
| `/enterprise/type-distribution` | 企业洞察 | 类型分布 | E-21 |
| `/enterprise/domain-distribution` | 企业洞察 | 领域分布 | E-22 |
| `/enterprise/status-analysis` | 企业洞察 | 深圳现状 | E-25 |
| `/enterprise/supply-chain` | 企业洞察 | 供应链 | E-28 |
| `/enterprise/pain-points` | 企业洞察 | 痛难点 | E-29 |
| `/enterprise/capability` | 企业决策 | 能力评估 | E-23/E-24 |
| `/enterprise/competitiveness` | 企业决策 | 竞争力 | E-30 |
| `/enterprise/recommendation` | 企业决策 | 招引培育 | E-26/E-27 |

## 6. 执行改动文件

| 文件 | 已执行改动 |
|---|---|
| `src/app/pages/enterprise/EnterpriseCenterPage.tsx` | 统一 Tab 命名；接入 ContextBar state；接入全局搜索按钮；消费 legacy route 映射。 |
| `src/app/components/Layout.tsx` | active/open group 使用企业中心路由映射，不只按 `child.path` 前缀。 |
| `src/app/routes.tsx` | 旧路由 handle title 收敛到新 IA；必要时把旧路由渲染指向企业中心页并带默认 Tab。 |
| `src/app/pages/development/SearchPage.tsx` | 明确作为横向检索能力落地页；支持来源上下文与返回路径。 |
| `src/app/pages/development/EnterpriseProfilePage.tsx` | 深度分析按钮真实跳转；画像面包屑支持来源上下文。 |
| `src/app/pages/development/portalShared.tsx` | 面包屑映射集中化，避免页面散落硬编码。 |
| `src/app/pages/enterprise/analysisShared.tsx` | 更新旧注释；SearchEntryButton 跳转携带来源上下文。 |
| `scripts/check-enterprise-ia.mjs` | 增强检查：Tab 名称、旧路由映射、handle title、横向能力不作为主导航。 |

## 7. 验收标准

- 左侧仍只暴露「企业中心」四个二级菜单，不出现旧企业三级菜单。
- 直接访问每个旧 `/development/*` 与 `/enterprise/*` URL 时，左侧打开「企业中心」并高亮对应二级菜单。
- 旧 URL 直达时，页面标题、面包屑、Tab 选中态均使用新 IA 口径。
- 企业总览 Tab 与 `ENT-IA.md` 对齐为「态势概览 / 企业分布 / 重点对象 / 风险机会」。
- 企业检索和企业画像不进入左侧菜单；不作为固定主导航 Tab；作为横向能力可直达、可返回来源。
- ContextBar 的产业、区域、时间窗在企业中心二级菜单、Tab、旧路由跳转间不静默丢失。
- E-36/E-37 仍不进入企业中心前台菜单；前台只展示来源、更新时间、Mock、待维护、待确认提示。
- `node scripts/check-enterprise-ia.mjs` 通过，并新增覆盖本任务的关键断言。
- `npm run build` 通过。
- 若触碰 UI 契约文件，运行 `npm run design:check`；若仍失败，必须说明是否为既有非企业中心失败。

## 8. 验证路径

本地预览重点验证以下 URL：

```text
/enterprise-center/overview
/enterprise-center/panorama?tab=list
/enterprise-center/insight
/enterprise-center/decision
/development/overview
/development/search
/development/key-enterprises
/development/star-enterprises
/development/shenzhen
/enterprise/overview
/enterprise/type-distribution
/enterprise/domain-distribution
/enterprise/status-analysis
/enterprise/supply-chain
/enterprise/pain-points
/enterprise/capability
/enterprise/competitiveness
/enterprise/recommendation
```

浏览器当前可从 `/enterprise-center/panorama?tab=list` 开始回归：确认它不再被理解为“企业检索主菜单”，而是企业全景中的名单/结果视图或横向检索入口。

## 9. 原派单话术（留档）

请执行 `ENT-UE-IA-L02`。目标是在不删除旧路由的前提下，完成企业中心旧 URL 兼容、active menu/tab 映射、标题/面包屑新 IA 口径收敛，并处理当前 L01 后残留的企业检索横向能力、ContextBar 上下文保留和企业总览 Tab 命名不一致问题。

实施前请先阅读：

- `repos/demo-ui-topic/docs/ia/enterprise/ENT-IA.md`
- `repos/demo-ui-topic/docs/ia/enterprise/ENT-element-master-design.md`
- `repos/demo-ui-topic/docs/ia/enterprise/ENT-search-design.md`
- `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-UE-IA-L01-nav-tabs.md`
- 本文件

交付时请回填：

- 改动文件清单
- 旧路由 -> 新菜单/Tab 映射表
- 验证命令与结果
- 未处理的 L03/L07 后续项

## 10. frontend-agent 交付回填（2026-07-01）

### 10.1 改动文件清单

本次 L02 代码改动聚焦 `repos/demo-ui-topic`：

| 文件 | 改动摘要 |
|---|---|
| `src/app/pages/enterprise/enterpriseCenterRouteMap.ts` | 新增企业中心单一映射源，统一维护模块、Tab、旧路由、横向能力、检索 URL 和深度分析 URL。 |
| `src/app/components/Layout.tsx` | 左侧菜单 active/open group 改为消费企业中心路由映射；旧 `/development/*`、`/enterprise/*` URL 可高亮企业中心对应二级菜单。 |
| `src/app/pages/enterprise/EnterpriseCenterPage.tsx` | 企业总览 Tab 改为「态势概览 / 企业分布 / 重点对象 / 风险机会」；企业全景移除固定「名单视图」检索 Tab；兼容 `tab=list` 回落到「重点企业」；ContextBar 状态上提并持久到 `sessionStorage`；全局搜索按钮跳 `/development/search` 并携带来源。 |
| `src/app/routes.tsx` | 旧企业 URL 保留，但除检索/画像外均渲染 `EnterpriseCenterPage`，由当前 pathname 选中对应页面内 Tab；旧 route handle title 收敛为「企业中心 · 二级菜单 · Tab」口径。 |
| `src/app/pages/development/SearchPage.tsx` | 检索页改为「企业中心 · 企业检索」横向能力落地页；面包屑回到来源路径；文案明确不进入左侧菜单、不作为固定页面 Tab。 |
| `src/app/pages/development/EnterpriseProfilePage.tsx` | 企业画像整页的「深度分析」由 Mock 提示改为真实跳转企业决策 / 能力评估，并携带 `enterprise_code`。 |
| `src/app/pages/development/portalShared.tsx` | 企业检索面包屑链接改为 `/development/search`；画像抽屉的「深度分析」接入企业中心深度分析 URL。 |
| `src/app/pages/enterprise/analysisShared.tsx` | 更新旧“TopicSidebar”注释；`SearchEntryButton` 跳横向检索能力并携带来源路径。 |
| `src/app/pages/development/DevelopmentOverview.tsx` | 面包屑末级由「结构分布」改为新 IA 口径「企业分布」。 |
| `scripts/check-enterprise-ia.mjs` | 增强 L02 静态契约：检查新 Tab 命名、旧 Tab 移除、旧路由映射、handle title、横向检索不作为固定主 Tab、ContextBar 持久化和深度分析跳转。 |

本文件同步回填交付结果。

### 10.2 旧路由 -> 新菜单/Tab 映射表

| 旧路由 | 新菜单高亮 | 页面内 Tab / 横向能力 | 当前处理 |
|---|---|---|---|
| `/development/overview` | 企业总览 | 企业分布 | 保留旧 URL，渲染企业中心总览页并选中「企业分布」。 |
| `/enterprise/overview` | 企业总览 | 态势概览 | 保留旧 URL，渲染企业中心总览页并选中「态势概览」。 |
| `/development/key-enterprises` | 企业全景 | 重点企业 | 保留旧 URL，渲染企业中心全景页并选中「重点企业」。 |
| `/development/star-enterprises` | 企业全景 | 明星企业 | 保留旧 URL，渲染企业中心全景页并选中「明星企业」。 |
| `/development/shenzhen` | 企业全景 | 深圳企业 | 保留旧 URL，渲染企业中心全景页并选中「深圳企业」。 |
| `/development/search` | 企业全景 | 横向能力：企业检索 | 保留独立检索落地页，不作为固定主 Tab；通过来源参数返回企业中心。 |
| `/development/enterprise/:enterpriseCode` | 企业全景 | 横向能力：统一企业画像 | 保留独立整页画像；深度分析跳企业决策 / 能力评估并携带企业对象。 |
| `/enterprise/type-distribution` | 企业洞察 | 类型分布 | 保留旧 URL，渲染企业中心洞察页并选中「类型分布」。 |
| `/enterprise/domain-distribution` | 企业洞察 | 领域分布 | 保留旧 URL，渲染企业中心洞察页并选中「领域分布」。 |
| `/enterprise/status-analysis` | 企业洞察 | 深圳现状 | 保留旧 URL，渲染企业中心洞察页并选中「深圳现状」。 |
| `/enterprise/supply-chain` | 企业洞察 | 供应链 | 保留旧 URL，渲染企业中心洞察页并选中「供应链」。 |
| `/enterprise/pain-points` | 企业洞察 | 痛难点 | 保留旧 URL，渲染企业中心洞察页并选中「痛难点」。 |
| `/enterprise/capability` | 企业决策 | 能力评估 | 保留旧 URL，渲染企业中心决策页并选中「能力评估」。 |
| `/enterprise/competitiveness` | 企业决策 | 竞争力 | 保留旧 URL，渲染企业中心决策页并选中「竞争力」。 |
| `/enterprise/recommendation` | 企业决策 | 招引培育 | 保留旧 URL，渲染企业中心决策页并选中「招引培育」。 |

兼容说明：旧 `/enterprise-center/panorama?tab=list` 会保留 URL，但页面内自动选中「重点企业」，不再显示「名单视图」固定 Tab。

### 10.3 验证命令与结果

```bash
node scripts/check-enterprise-ia.mjs
```

结果：通过，输出 `enterprise IA contract passed`。

```bash
npm run build
```

结果：通过。Vite 构建成功；仍有既有 chunk size 大于 500 kB 警告。

```bash
npm run design:check
```

结果：未通过，失败点为既有非企业中心问题：

```text
src/app/pages/industry/ChainProfilePage.tsx must use standard tab classes instead of Arco Tabs
```

该失败与本次 ENT-UE-IA-L02 改动无关，L01 handoff 中也已记录同一类既有产业链页面契约问题。

浏览器验证：

- 当前 `/enterprise-center/panorama?tab=list`：左侧高亮「企业全景」，页面标题「企业中心 · 企业全景」，Tab 选中「重点企业」，不再出现「名单视图」，控制台无 error。
- 旧 `/enterprise/domain-distribution`：URL 保留，左侧高亮「企业洞察」，页面标题「企业中心 · 企业洞察」，Tab 选中「领域分布」，控制台无 error。

### 10.4 未处理的 L03/L07 后续项

- L03：企业总览仍是聚合承载，`EnterpriseOverview` 与 `DevelopmentOverview` 的深层内容尚未按「态势概览 / 企业分布 / 重点对象 / 风险机会」彻底整合；`DevelopmentOverview` 仍有旧视觉债务（Recharts、硬编码色值、旧门户页面结构）。
- L07：企业检索仍是 `/development/search` 兼容/高级检索落地页，尚未实现全局搜索抽屉、顶部搜索建议浮层、跨页对比篮/收藏/最近查看的完整产品闭环。
- 深层业务页内的部分按钮仍有 Mock 提示，例如某些导出、补链招引、行业分析跳转，未在 L02 范围内重写。
- `npm run design:check` 的产业链 `ChainProfilePage.tsx` Tab 契约失败需单独派发，不属于企业中心 L02。

### 10.5 补充修复记录（2026-07-01）

- 修复 `/development/search` 面包屑直接显示「企业中心 / 企业检索」的问题。
- 检索页现在根据 `source` 参数解析来源二级菜单：
  - `source=/enterprise-center/overview` 显示「企业总览 / 企业检索」。
  - `source=/enterprise-center/panorama` 显示「企业全景 / 企业检索」。
- 左侧 active menu 同步消费 `source` 参数；检索页从企业总览进入时高亮「企业总览」，从企业全景进入时高亮「企业全景」。
- 已在 `scripts/check-enterprise-ia.mjs` 增加断言，防止检索页面包屑再次硬编码为「企业中心」。

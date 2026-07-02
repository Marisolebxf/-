# ENT-UE-IA-L03 企业总览深层内容整合派单

| 字段 | 内容 |
|---|---|
| 任务 ID | ENT-UE-IA-L03 |
| 任务名称 | 企业中心 IA - 企业总览四视角深层内容整合 |
| 执行角色 | frontend-agent |
| 目标仓库 | `repos/demo-ui-topic` |
| 前置任务 | ENT-UE-IA-L01、ENT-UE-IA-L02 |
| 当前状态 | 已完成（frontend-agent 回填） |
| 生成日期 | 2026-07-01 |
| 文档用途 | 派发企业总览深层内容整改，要求 frontend-agent 实施后回填改动文件、路由/Tab 行为、验证结果和后续项 |

## 0. 派单话术

frontend-agent 请执行 `ENT-UE-IA-L03`。目标是在不改变企业中心四个二级菜单、不删除旧路由的前提下，完成「企业总览」页内四个一级 Tab 的深层内容整合：

- `态势概览`
- `企业分布`
- `重点对象`
- `风险机会`

本任务重点处理 L02 后遗留的企业总览内容混排、旧标题/旧页面壳嵌套、旧门户视觉债务、占位 Tab 未实现、总览与企业全景边界不清问题。不要推进 L07 企业检索完整闭环，不要重写企业全景/企业洞察/企业决策深层页。

实施前请先阅读：

- `repos/demo-ui-topic/docs/ia/enterprise/ENT-IA.md`
- `repos/demo-ui-topic/docs/ia/enterprise/ENT-element-master-design.md`
- `repos/demo-ui-topic/docs/ia/enterprise/ENT-search-design.md`
- `gkx-orchestration/agent-delivery/Design.md`
- `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-UE-IA-L01-nav-tabs.md`
- `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-UE-IA-L02-route-compat.md`
- 本文件

交付时请回填：

- 改动文件清单
- 企业总览四个 Tab 的最终承载内容
- 旧路由兼容与默认 Tab 行为
- 验证命令与结果
- 未处理的 L04/L07 后续项

## 1. 背景结论

L01 已完成企业中心左侧 IA 和页面内 Tab 框架。L02 已完成旧路由兼容、active menu/tab 映射、标题/面包屑口径和横向检索入口初步收敛。

当前 `企业总览` 仍是“聚合承载”状态：页面内四个 Tab 虽已命名为新 IA，但内容仍直接复用旧页面或占位组件，导致用户看到的是旧建设来源、旧页面壳和新 IA 混在一起。

L03 的目标不是新增 IA，而是把企业总览四个 Tab 变成真正按任务组织的总览页：

| Tab | 用户问题 | 承接范围 |
|---|---|---|
| 态势概览 | 这个产业的企业整体发展到什么程度了？ | E-20 / E-32 总体态势、核心指标、趋势、结论 |
| 企业分布 | 企业在哪里、按区域/产业/规模如何分布？ | E-32 全球/全国/区域分布、分布趋势、区域热力 |
| 重点对象 | 哪些企业或企业群值得重点关注？ | E-20 触点 / E-33 入口摘要，不替代企业全景深页 |
| 风险机会 | 当前有哪些异常、风险、机会和建议动作？ | E-20 风险机会摘要，跳转企业洞察/企业决策 |

## 2. 权威依据

按以下优先级执行：

1. `repos/demo-ui-topic/docs/ia/enterprise/ENT-IA.md`
2. `repos/demo-ui-topic/docs/ia/enterprise/ENT-element-master-design.md`
3. `gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`
4. `gkx-orchestration/agent-delivery/Design.md`
5. 当前前端实现：`repos/demo-ui-topic/src/app/**`

关键约束：

- 左侧仍只暴露「企业中心」下四个二级菜单。
- 企业总览页内一级 Tab 必须是「态势概览 / 企业分布 / 重点对象 / 风险机会」。
- 企业检索、企业画像、对比篮、收藏、最近查看仍是横向能力，不作为固定 Tab。
- 业务趋势色遵守 `Design.md §4.3`：上升红、下降绿。
- 总览页内不得再出现旧用户侧口径「门户-企业发展」「企业分析总览」「战略驾驶舱」作为主标题。

## 3. 当前问题清单

| 优先级 | 分类 | 当前问题 | 期望处理 |
|---|---|---|---|
| P0 | 内容归位 | `EnterpriseCenterPage` 的企业总览 Tab 直接复用 `EnterpriseOverview`、`DevelopmentOverview`、`KeyEnterprisesPanorama` 和占位组件。 | 建立企业总览专属四视角内容，不把旧整页壳原样嵌入。 |
| P0 | 旧标题残留 | `EnterpriseOverview` 仍以「企业分析总览」为页面主语，含 P0/P1/P2 等旧分析链文案。 | 企业总览内主标题、结论、说明统一为新 IA 口径。 |
| P0 | 占位未实现 | 「风险机会」仍是 Placeholder，且文案写“待 L02 细化映射”。 | 实现可验收的风险机会摘要视图，至少包含风险、机会、建议动作和跳转入口。 |
| P1 | 视觉债务 | `DevelopmentOverview` 使用 Recharts、lucide、硬编码颜色和旧门户页面结构。 | 收敛到项目既有 Arco / `EChart` / `MetricCard` / CSS token 体系。 |
| P1 | 嵌套页面壳 | 总览 Tab 内部仍显示旧面包屑或旧页面级 padding/标题，形成“页中页”。 | Tab 内容应是企业总览页面内区域，不再显示额外面包屑。 |
| P1 | 边界不清 | 「重点对象」直接渲染完整 `KeyEnterprisesPanorama`，容易与企业全景「重点企业」重复。 | 在企业总览只做 TopN / 企业群 / 异常对象摘要；深层全景跳 `/enterprise-center/panorama?tab=key`。 |
| P1 | 指标口径 | E-20 与 E-32 指标分散在两个旧页，metric_id 和 Mock/Pending 标识不统一。 | 统一使用 `MetricCard`、`M_ENT_*`、`PendingBadge` / `MockBadge` 口径。 |
| P2 | 校验缺口 | `check-enterprise-ia.mjs` 主要覆盖 L01/L02，未卡住总览占位和旧文案回退。 | 增加 L03 静态契约。 |

## 4. 整改范围

### 4.1 必须执行

- 为企业总览四个 Tab 建立清晰、独立、可维护的内容承载。
- 移除企业总览 Tab 内的旧面包屑、旧页面主标题和旧建设来源文案。
- 把 `态势概览` 聚焦 E-20/E-32：JudgmentStrip、核心指标、历年趋势、关键结论和下钻入口。
- 把 `企业分布` 聚焦 E-32：全球/全国/区域分布、区域热力、分布趋势和地图/图表占位。
- 把 `重点对象` 聚焦总览摘要：重点企业 TopN、企业群标签、异常/高潜对象、画像/对比/全景跳转。
- 把 `风险机会` 从 Placeholder 改为真实摘要：风险卡、机会卡、建议动作、跳转企业洞察/企业决策。
- 更新 `scripts/check-enterprise-ia.mjs`，覆盖 L03 的关键契约。
- 保持 L02 的旧路由兼容、active menu/tab 映射和 ContextBar 持久化不回退。

### 4.2 不纳入本任务

- 不删除旧 `/development/*` 与 `/enterprise/*` 路由。
- 不推进 L07 企业检索完整闭环。
- 不重写企业全景的 E-33/E-34/E-35 深层页面。
- 不重写企业洞察、企业决策深层算法/数据模型。
- 不新增 E-36/E-37 后台内容管理菜单。
- 不引入新的设计系统或 Ant Design。

## 5. 建议实现方案

实现方式可由 frontend-agent 根据代码结构微调，但需满足以下产品结果。

### 5.1 组件归位

建议新增企业总览专属承载，例如：

- `src/app/pages/enterprise/EnterpriseOverviewTabs.tsx`

或拆为更细组件：

- `EnterpriseSituationOverview`
- `EnterpriseDistributionOverview`
- `EnterpriseKeyObjectsOverview`
- `EnterpriseRiskOpportunityOverview`

然后由 `EnterpriseCenterPage.tsx` 的 `overview` Tab 映射直接引用这些总览专属组件。

避免继续把旧整页组件原样作为 Tab 内容嵌入。若需要复用旧页面中的图表 option、mock 数据或列表，可抽取为数据/子组件复用，不保留旧页面壳。

### 5.2 四个 Tab 内容要求

| Tab | 必备内容 | 主要跳转 |
|---|---|---|
| 态势概览 | 一句话结论、核心 MetricCard、历年新增趋势、全国/重点区域摘要、关键下钻入口 | 企业洞察 / 企业决策 |
| 企业分布 | 区域分布图表、区域热力、产业/规模分布、全球/全国口径提示、科研人数 Pending 口径 | 企业洞察 / 类型分布 |
| 重点对象 | TopN 企业、重点企业群、标签/资质摘要、加入对比篮、打开画像、进入企业全景 | 企业全景 / 重点企业 |
| 风险机会 | 风险项、机会项、异常指标、建议动作、待维护/待确认提示 | 企业洞察 / 痛难点、企业决策 / 招引培育 |

### 5.3 UI 与交互要求

- 使用 `global-workbench-tabs` 保持页面内一级 Tab 样式。
- 使用 `MetricCard` 承载统计数字，保留 `metric_id`、ⓘ、Mock/Pending 标识。
- 图表优先使用项目现有 `EChart` 封装；不要在企业总览新增 Recharts 依赖面。
- 所有色值走 `--sci-*` token；趋势类遵循上升红、下降绿。
- 操作按钮使用 Arco `Button` 和 Arco icon；不要新增 page-private native button。
- 卡片/面板按 Design.md 的轻蓝白工作台风格，避免大屏化、营销化、霓虹渐变。
- 空态、加载态、锁态、Mock/待维护/待确认提示必须保留，不静默隐藏。

## 6. 路由与兼容要求

| 入口 | 期望行为 |
|---|---|
| `/enterprise-center/overview` | 默认进入「态势概览」。 |
| `/enterprise-center/overview?tab=situation` | 选中「态势概览」。 |
| `/enterprise-center/overview?tab=distribution` | 选中「企业分布」。 |
| `/enterprise-center/overview?tab=key-objects` | 选中「重点对象」。 |
| `/enterprise-center/overview?tab=risk-opportunity` | 选中「风险机会」。 |
| `/enterprise/overview` | 保留旧 URL，左侧高亮「企业总览」，选中「态势概览」。 |
| `/development/overview` | 保留旧 URL，左侧高亮「企业总览」，选中「企业分布」。 |

从企业总览进入 `/development/search` 时，`source` 参数继续指向 `/enterprise-center/overview`，检索页左侧 active 和面包屑仍按 L02 修复逻辑展示「企业总览 / 企业检索」。

## 7. 验收标准

- 企业总览四个 Tab 均有真实内容，不再出现“待 L02 细化映射”。
- 企业总览 Tab 内不再出现旧页面主标题「企业分析总览」「门户-企业发展」「战略驾驶舱」。
- 企业总览 Tab 内不再显示额外面包屑；面包屑规则仍由企业中心外层和深层横向能力处理。
- `/enterprise/overview`、`/development/overview` 旧路由兼容不回退。
- `ContextBar` 的产业、区域、时间窗在四个 Tab 间保持，不静默清空。
- 重点对象只做总览摘要和入口，不替代企业全景「重点企业」深层页。
- 风险机会能把用户导向企业洞察/痛难点或企业决策/招引培育。
- 趋势类颜色符合上升红、下降绿。
- 新增/修改静态检查覆盖上述关键点。

## 8. 验证命令

在 `repos/demo-ui-topic` 下执行：

```bash
node scripts/check-enterprise-ia.mjs
```

预期：通过，并覆盖 L03 的总览四 Tab、旧文案、占位移除、旧路由兼容断言。

```bash
node scripts/check-trend-semantics.mjs
```

预期：通过，确认趋势类语义仍为上升红、下降绿。

```bash
npm run build
```

预期：通过。允许保留既有 chunk size 警告。

```bash
npm run design:check
```

预期：若仍失败，需说明是否仍为既有非企业中心问题 `src/app/pages/industry/ChainProfilePage.tsx must use standard tab classes instead of Arco Tabs`。若本任务触碰到相关文件，应一并修复或明确拆单。

## 9. 浏览器回归路径

本地预览重点验证：

```text
/enterprise-center/overview
/enterprise-center/overview?tab=situation
/enterprise-center/overview?tab=distribution
/enterprise-center/overview?tab=key-objects
/enterprise-center/overview?tab=risk-opportunity
/enterprise/overview
/development/overview
/development/search?source=%2Fenterprise-center%2Foverview&industry=electronic-information&tab=situation
```

检查项：

- 左侧高亮始终为「企业总览」。
- 页面标题为「企业中心 · 企业总览」。
- Tab 选中态与 URL 参数一致。
- 旧路由不出现旧页面壳和旧标题。
- 从全局搜索进入检索页后面包屑为「企业总览 / 企业检索」。
- 控制台无 error。

## 10. 交付回填模板

frontend-agent 完成后，请在本文件下方新增「交付回填」小节，至少包含：

### 10.1 改动文件清单

| 文件 | 改动摘要 |
|---|---|
| 待回填 | 待回填 |

### 10.2 企业总览四 Tab 最终承载

| Tab | 最终组件/文件 | 内容摘要 | 主要跳转 |
|---|---|---|---|
| 态势概览 | 待回填 | 待回填 | 待回填 |
| 企业分布 | 待回填 | 待回填 | 待回填 |
| 重点对象 | 待回填 | 待回填 | 待回填 |
| 风险机会 | 待回填 | 待回填 | 待回填 |

### 10.3 旧路由兼容结果

| 旧路由 | 高亮菜单 | 选中 Tab | 结果 |
|---|---|---|---|
| `/enterprise/overview` | 企业总览 | 态势概览 | 待回填 |
| `/development/overview` | 企业总览 | 企业分布 | 待回填 |

### 10.4 验证命令与结果

| 命令 | 结果 |
|---|---|
| `node scripts/check-enterprise-ia.mjs` | 待回填 |
| `node scripts/check-trend-semantics.mjs` | 待回填 |
| `npm run build` | 待回填 |
| `npm run design:check` | 待回填 |

### 10.5 未处理后续项

- L04：待回填。
- L07：待回填。
- 其他既有非企业中心问题：待回填。

## 11. frontend-agent 交付回填（2026-07-01）

### 11.1 改动文件清单

| 文件 | 改动摘要 |
|---|---|
| `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseOverviewTabs.tsx` | 新增企业总览四视角专属承载：态势概览、企业分布、重点对象、风险机会；统一使用 `MetricCard`、`EChart`、`SectionPanel`、Arco Button/Icon 和 `--sci-*` token，不再嵌旧整页壳。 |
| `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCenterPage.tsx` | 企业总览四个 Tab 改为渲染专属组件；移除「风险机会」占位；保留企业全景/企业洞察/企业决策深层页原映射。 |
| `repos/demo-ui-topic/src/app/pages/enterprise/enterpriseCenterRouteMap.ts` | 补齐 `suggestion` Tab 类型与标签，避免企业决策预留视角类型不一致；未改变企业总览旧路由映射。 |
| `repos/demo-ui-topic/scripts/check-enterprise-ia.mjs` | 增加 L03 静态契约：检查四个总览专属组件、禁止总览嵌旧页面壳、禁止旧标题/面包屑/占位文案回退、检查风险机会跳转到痛难点与招引培育。 |
| `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-UE-IA-L03-overview-integration.md` | 回填本次交付记录。 |

### 11.2 企业总览四 Tab 最终承载

| Tab | 最终组件/文件 | 内容摘要 | 主要跳转 |
|---|---|---|---|
| 态势概览 | `EnterpriseSituationOverview` / `EnterpriseOverviewTabs.tsx` | E-20/E-32 总体态势判断、核心指标、近 12 月趋势、重点产业结构、关键下钻入口。 | 企业分布、类型分布、深圳现状、综合竞争力。 |
| 企业分布 | `EnterpriseDistributionOverview` / `EnterpriseOverviewTabs.tsx` | 深圳区域分布、产业领域分布、区域热力、全球/全国口径与科研人数 Pending 提示。 | 类型分布（带区域参数）。 |
| 重点对象 | `EnterpriseKeyObjectsOverview` / `EnterpriseOverviewTabs.tsx` | 重点企业 TopN、画像抽屉、对比篮、规模/资质摘要、重点企业群摘要；只做总览入口，不替代企业全景深页。 | 企业全景 / 重点企业、统一企业画像。 |
| 风险机会 | `EnterpriseRiskOpportunityOverview` / `EnterpriseOverviewTabs.tsx` | 风险异常、机会建议、待维护提示和后续处置路径；从 Placeholder 改为真实摘要视图。 | 痛难点、供应链、招引培育、深圳现状。 |

### 11.3 旧路由兼容结果

| 旧路由 | 高亮菜单 | 选中 Tab | 结果 |
|---|---|---|---|
| `/enterprise/overview` | 企业总览 | 态势概览 | 保留旧 URL，继续由 `EnterpriseCenterPage module="overview"` 承载，默认选中态势概览。 |
| `/development/overview` | 企业总览 | 企业分布 | 保留旧 URL，继续由 `EnterpriseCenterPage module="overview"` 承载，默认选中企业分布。 |
| `/enterprise-center/overview` | 企业总览 | 态势概览 | 新 IA 默认入口不变。 |
| `/enterprise-center/overview?tab=distribution` | 企业总览 | 企业分布 | URL Tab 参数保持可直达。 |
| `/enterprise-center/overview?tab=key-objects` | 企业总览 | 重点对象 | URL Tab 参数保持可直达。 |
| `/enterprise-center/overview?tab=risk-opportunity` | 企业总览 | 风险机会 | URL Tab 参数保持可直达。 |

从企业总览点击「全局搜索」仍进入 `/development/search`，并携带 `source=/enterprise-center/overview`、当前产业与当前 Tab，上游 L02 的横向检索定位未回退。

### 11.4 验证命令与结果

| 命令 | 结果 |
|---|---|
| `node scripts/check-enterprise-ia.mjs` | 通过，输出 `enterprise IA contract passed`。 |
| `node scripts/check-trend-semantics.mjs` | 通过，输出 `Trend semantic contract passed.`。 |
| `npm run build` | 通过，Vite 构建成功；仍有既有 chunk size 大于 500 kB 警告。 |
| `npm run design:check` | 未通过，失败点仍为既有非企业中心问题：`src/app/pages/industry/ChainProfilePage.tsx must use standard tab classes instead of Arco Tabs`。本次未修改该文件。 |
| 浏览器自动化 smoke test | 未完成：项目 Playwright bundled Chromium 未安装；改用系统 Chrome 无头启动时被 macOS 权限/沙箱中止。已保留本地预览服务路径供人工核验。 |

本地预览服务：

```text
http://127.0.0.1:4174/
```

重点人工核验路径：

```text
/enterprise-center/overview
/enterprise-center/overview?tab=distribution
/enterprise-center/overview?tab=key-objects
/enterprise-center/overview?tab=risk-opportunity
/enterprise/overview
/development/overview
```

### 11.5 未处理后续项

- L04：企业全景仍沿用既有 `KeyEnterprisesPanorama`、`StarEnterprises`、`ShenzhenEnterprises` 深层页；本次只在总览「重点对象」提供摘要与入口，未重写 E-33~E-35。
- L07：企业检索仍是 `/development/search` 兼容/高级检索落地页；未实现顶部搜索建议浮层、全局检索抽屉、跨页收藏/最近查看完整闭环。
- 企业洞察/企业决策深层页仍保留既有按钮 Mock、权限细粒度和图表 token 后续项；本任务未扩大处理。
- 既有非企业中心问题：`npm run design:check` 仍卡在产业链 `ChainProfilePage.tsx` Tab 契约，需要独立派单修复。

### 11.6 Bugfix 追加记录（2026-07-01）

| 问题 | 根因 | 修复 |
|---|---|---|
| 企业总览「态势概览 / 企业分布 / 重点对象」内 ECharts 图表配色丢失。 | L03 新增的 `EnterpriseOverviewTabs.tsx` 把 `var(--sci-primary)`、`var(--sci-chart-*)` 等 CSS custom properties 直接传入 ECharts canvas option；ECharts 不解析 CSS 变量，导致渲染颜色失效或回退。 | 图表 option 中的 `color`、`itemStyle.color`、`lineStyle.color` 改为解析后的 hex 常量；DOM 样式继续保留 `--sci-*` token。`check-enterprise-ia.mjs` 增加契约，禁止总览 ECharts option 再直接写 CSS var。 |

补充验证：

| 命令 / 检查 | 结果 |
|---|---|
| `node scripts/check-enterprise-ia.mjs` | 通过，覆盖 ECharts option 不直接使用 CSS var 的回归契约。 |
| `node scripts/check-trend-semantics.mjs` | 通过。 |
| `npm run build` | 通过，仍仅有既有 chunk size 警告。 |
| in-app browser 截图检查 | `/enterprise-center/overview?tab=situation` 中折线图和环图颜色已恢复。 |

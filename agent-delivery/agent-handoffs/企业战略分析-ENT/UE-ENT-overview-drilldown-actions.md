# Handoff · UE-ENT-OVERVIEW-DRILLDOWN-ACTIONS（企业总览下钻与风险机会动作交互细化）

| 项 | 内容 |
| --- | --- |
| 任务 ID | UE-ENT-OVERVIEW-DRILLDOWN-ACTIONS |
| 角色 / 执行方 | ux-agent / UE Lead |
| 仓库 | `agent-delivery` |
| 触发来源 | `PM-ENT-OVERVIEW-ACTION-REQ` 产品复议结论 |
| 上游规则 | `PM-ENT-overview-action-requirement-confirmation.md`、`ENT-UE-IA-L03-overview-integration.md`、`UX-UE 通用交互组件规范.md` |
| 状态 | Completed by ux-agent / UE Lead |

## 1. 背景

PM 已复议确认：企业总览里的“下钻”不应被前端理解为底部铺一组跳转按钮，而应是用户点击 KPI 卡、趋势图、环形图/产业结构图、地图、对象卡等数据载体后，带当前上下文进入具体分析。

风险机会 Tab 同理，不应保留底部“后续处置路径”按钮组；动作应内联到具体风险项或机会项卡片内，绑定风险/机会对象。

本任务先由 UE 细化交互，不直接要求 FE 实现。

## 2. UE 目标

1. 明确态势概览中哪些数据载体可点击、点击后进入哪里、携带哪些上下文。
2. 明确哪些数据载体不可点击，以及不可点击时的可见状态或说明。
3. 明确风险/机会卡片内动作的层级、文案、目标和对象绑定规则。
4. 明确无数据、无权限、无对象上下文、Mock/待确认口径时的降级交互。
5. 输出可交给 frontend-agent 的实现边界和验收口径。

## 3. 需要细化的交互清单

### 3.1 态势概览

| 数据载体 | UE 需定义 |
| --- | --- |
| KPI 卡 | 是否整卡可点、是否有显式动作区、目标页/抽屉、指标口径说明如何展开 |
| 近 12 月趋势图 | 点击点位、图例、时间段或工具条后的动作；是否进入趋势明细或类型分布 |
| 环形图 / 产业结构图 | 点击分组后的动作；如何表达当前选中维度和点击值 |
| 地图 / 区域视图 | 点击区域后的动作；区域筛选、返回和继承口径如何展示 |
| 重点对象卡 | 点击企业对象打开画像抽屉还是进入企业全景；对比篮/收藏是否保留 |

态势概览不得再设置独立底部“关键下钻入口 / 建议继续查看”区块。

### 3.2 风险机会

| 卡片类型 | UE 需定义 |
| --- | --- |
| 风险项 | “研判风险原因”“查看影响对象”等动作放在卡片什么位置，何时显示 |
| 供应链风险项 | 如何进入供应链分析，如何携带节点/企业/风险维度 |
| 机会项 | 如何表达“查看深圳链位缺口”“生成候选名单”等动作 |
| 待维护 / 待确认项 | 不具备对象时如何降级，不展示强动作时的说明文案 |

风险机会不得再设置独立底部“后续处置路径”区块。

## 4. 上下文规则

UE 需要把下列字段映射到交互说明中，作为 FE 后续实现依据。

态势概览数据载体下钻：

```text
industry
timeRange
region
source=/enterprise-center/overview
sourceTab=situation
sourceMetric 或 sourceChart
region_code / enterprise_code / metric_id / dimension / clickedValue / timePoint（按触发源补充）
```

风险机会卡片动作：

```text
source=/enterprise-center/overview
sourceTab=risk-opportunity
riskType 或 opportunityType
industry
timeRange
region
riskLevel / riskDimension / suggested_action / enterprise_codes[] / chainNode / region_code / chain_gap（按对象补充）
```

## 5. UE 交付物

ux-agent 完成后，请在本文件末尾新增“UE 交付回填”，至少包含：

- 态势概览数据载体交互矩阵：触发源、动作文案、目标、上下文、无状态降级。
- 风险机会卡片动作矩阵：卡片类型、动作文案、目标、对象参数、无状态降级。
- 页面结构调整建议：哪些底部区块移除，动作放回哪些模块。
- 后续 FE 任务建议：建议任务 ID、实施文件、验收命令。
- 需要 PM 再确认的问题。

## 6. 可复制派单话术

```text
请 ux-agent / UE Lead 执行 UE-ENT-OVERVIEW-DRILLDOWN-ACTIONS。

目标是先细化企业总览“下钻”和“风险机会动作”的交互规则，而不是让 FE 直接把底部按钮改样式。PM 已确认：态势概览的下钻必须来自 KPI 卡、趋势图、环形图/产业结构图、地图/区域视图、重点对象卡等数据载体点击，并携带当前上下文；风险机会 Tab 不保留底部“后续处置路径”，动作必须内联到具体风险项或机会项卡片。

请重点输出：
- 态势概览数据载体交互矩阵：触发源、动作文案、目标页面/抽屉、上下文参数、无状态降级。
- 风险机会卡片动作矩阵：卡片类型、动作文案、目标页面、风险/机会对象参数、无状态降级。
- 明确移除“关键下钻入口 / 建议继续查看”和“后续处置路径”两个底部区块。
- 给 frontend-agent 的后续实施边界和验收口径。

实施前请阅读：
- gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/PM-ENT-overview-action-requirement-confirmation.md
- gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/UE-ENT-overview-drilldown-actions.md
- gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-UE-IA-L03-overview-integration.md
- gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md

不要新增左侧菜单，不要新增企业检索固定 Tab，不要新增系统级全局搜索，不要把无对象、无指标、无图表上下文的裸跳转按钮包装成“下钻”或“处置路径”。
```

## 7. UE 交付回填（2026-07-01）

### 7.1 交互总原则

| 规则 | UE 结论 |
| --- | --- |
| 下钻定义 | 下钻只能由当前页面已呈现的数据载体触发，包括 KPI 卡、趋势图点位、环形图 / 产业结构图分组、地图 / 区域视图、重点对象卡。点击后必须带上当前 ContextBar 口径和触发对象。 |
| 动作归属 | 动作必须贴近被解释的数据。KPI 的动作在 KPI 卡内，图表点位动作从图表 tooltip / 选中态承接，区域动作在地图 / 区域卡中，风险机会动作在具体风险项或机会项卡片内。 |
| 禁止形态 | 不再保留底部「关键下钻入口 / 建议继续查看」区块；不再保留底部「后续处置路径」区块；不使用无对象、无指标、无图表上下文的裸跳转按钮包装为下钻或处置路径。 |
| 上下文继承 | 所有跨页动作携带 `source=/enterprise-center/overview`、`sourceTab`、`industry`、`timeRange`、`region`；目标页显示一次上下文继承提示，并允许用户调整 / 清除。 |
| 降级策略 | 无数据时保留容器和标题，显示 `Empty` / 待维护说明；无权限时入口可见但禁用并通过 tooltip 说明；上下文缺失时禁用强动作，改为「先选择指标 / 区域 / 对象」。 |
| 搜索边界 | 不新增左侧菜单、不新增企业检索固定 Tab、不新增系统级全局搜索。需要查企业时只能在重点对象、风险机会等内容区使用场景化入口，例如「查找重点企业」「查找影响对象」。 |
| 依据标识 | 需求原文只确认“数据载体点击后带上下文下钻”和“风险/机会动作绑定具体对象”。具体到 tooltip 是否增强、进入哪个深层页、英文参数枚举、异常原因抽屉、禁用文案等，属于 UE 推导项，必须在文档和后续页面标识为「UE 推导 · 待讨论」，不得作为已签收需求直接开发。 |

### 7.2 态势概览数据载体交互矩阵

| 触发源 | 触发方式 / 触发态 | 动作文案 | 目标页面 / 抽屉 | 上下文参数 | 无状态降级 |
| --- | --- | --- | --- | --- | --- |
| KPI 卡：企业总数 `M_ENT_TOTAL_COUNT` | 整卡可聚焦；hover 显示右上角轻量动作；点击卡片主区域进入明细 | 查看企业总量明细 | `/enterprise/type-distribution` 或企业洞察 / 类型分布 | `source=/enterprise-center/overview`、`sourceTab=situation`、`sourceMetric=M_ENT_TOTAL_COUNT`、`metric_id=M_ENT_TOTAL_COUNT`、`industry`、`timeRange`、`region`、`clickedValue` | 指标无值时不进入明细，卡片显示 `Empty` / `PendingBadge`；无权限时动作禁用并提示「暂无查看企业明细权限」。 |
| KPI 卡：新增企业 `M_ENT_NEW_COUNT` | 整卡可点；趋势数字可作为同一入口，不单独做按钮组 | 查看新增趋势明细 | 企业洞察 / 深圳现状或 `/enterprise/status-analysis` | `sourceTab=situation`、`sourceMetric=M_ENT_NEW_COUNT`、`metric_id=M_ENT_NEW_COUNT`、`dimension=new_enterprise`、`industry`、`timeRange`、`region` | 缺少时间窗时入口禁用，提示「请选择时间范围后查看新增趋势」。 |
| KPI 卡：创新型企业 `M_ENT_INNOVATIVE_COUNT` | 整卡可点；`ⓘ` / 口径说明只展开说明，不跳转 | 查看创新企业结构 | `/enterprise/type-distribution?dimension=qualification` | `sourceMetric=M_ENT_INNOVATIVE_COUNT`、`metric_id=M_ENT_INNOVATIVE_COUNT`、`dimension=qualification`、`industry`、`timeRange`、`region` | 若指标为 Mock / 待维护，仅允许打开口径说明，不展示强跳转。 |
| KPI 卡：专利总量 `M_ENT_PATENT_TOTAL` | 整卡可点；趋势状态保留说明 | 查看创新能力关联 | 企业决策 / 能力评估或 `/enterprise/capability` | `sourceMetric=M_ENT_PATENT_TOTAL`、`metric_id=M_ENT_PATENT_TOTAL`、`dimension=patent`、`industry`、`timeRange`、`region` | 专利字段无数据时保留口径说明，动作降级为「查看指标口径」。 |
| 近 12 月趋势图 | 点击折线点位；tooltip 中提供单一动作；图例只控制显隐，不跳转 | 查看该月趋势明细 | 企业洞察 / 深圳现状或趋势明细抽屉 | `sourceChart=enterprise_trend_12m`、`timePoint`、`clickedValue`、`industry`、`timeRange`、`region` | 未命中点位不触发跳转；空序列显示空态和「调整时间范围」。 |
| 近 12 月趋势图异常点 | 需求依据支持“趋势拐点可查看原因”；具体是否在 tooltip 增强、是否标记异常点为可点，属于 UE 推导，需标识「UE 推导 · 待讨论」 | 查看趋势异常原因（文案待确认） | 默认建议为异常原因抽屉；仅当异常点已被归类为风险项并具备 `riskType/riskDimension` 时，才可进入 `/enterprise/pain-points`（目标页为 UE 推导，待确认） | 已确认基础参数：`sourceChart=enterprise_trend_12m`、`timePoint`、`clickedValue`、`industry`、`region`；UE 推导参数：`dimension=growth_change`、`riskDimension=growth` | 未计算异常原因时不展示强动作；如需提示「异常原因待模型输出」，该文案也标识为 UE 推导，待全员讨论。 |
| 环形图 / 产业结构图分组 | 点击分组扇区；选中态高亮并同步说明 | 查看类型结构 | `/enterprise/type-distribution` | `sourceChart=industry_structure`、`dimension=industry`、`clickedValue=<分组名>`、`industry`、`timeRange`、`region` | 分组值为空或占比为 0 时不跳转，tooltip 显示「当前分组暂无企业样本」。 |
| 环形图 / 产业结构图图例 | 图例点击仅筛选 / 高亮图表，不承担跨页跳转 | 高亮该结构分组 | 当前图表内联动，不跨页 | `sourceChart=industry_structure`、`activeLegend` | 图例只剩一个系列时禁止继续隐藏，保持至少一个可见系列。 |
| 地图 / 区域视图区域 | 点击地图区域、区域热力卡或区域排行行；区域进入选中态 | 查看区域分布 | `/enterprise-center/overview?tab=distribution` 或 `/enterprise/type-distribution` | `sourceChart=region_map`、`region_code`、`clickedValue=<区域名>`、`industry`、`timeRange`、`region` | 底图未加载时保留工具栏和图例并提示重试；区域无数据时显示空态，不进入空目标页。 |
| 地图 / 区域视图框选 | 框选生成临时空间选择上下文；显示清除入口 | 查看框选企业 | 场景化高级检索 `/development/search`，仅作为对象集合查询 | `sourceChart=region_map`、`selectionType=box`、`region_code[]`、`enterprise_codes[]`、`industry`、`timeRange` | 框选命中 0 个对象时显示「未命中企业，调整框选范围」，不跳搜索页。 |
| 重点对象卡 / TopN 行 | 点击企业名打开抽屉；行内对比仍是对比动作，不替代画像 | 打开企业画像 | 统一企业画像 Drawer；必要时深链 `/development/enterprise/:enterpriseCode` | `sourceChart=key_object_topn`、`enterprise_code`、`enterprise_name`、`industry`、`timeRange`、`region` | 无企业编码时企业名不可点击，显示「企业编码待维护」。 |
| 重点企业群卡 | 点击企业群条目或链位标签 | 查看企业群对象 | `/enterprise-center/panorama?tab=key` 或场景化高级检索 | `sourceChart=key_object_group`、`dimension=chain_stage`、`clickedValue=<链位/企业群>`、`enterprise_codes[]`、`industry`、`region` | 企业集合为空时只展示群组说明，不展示查看入口。 |

### 7.3 风险机会卡片动作矩阵

| 卡片类型 | 动作文案 | 目标页面 | 风险 / 机会对象参数 | 无状态降级 |
| --- | --- | --- | --- | --- |
| 风险项：新增增速回落 | 研判增速回落原因 | `/enterprise/pain-points` 或企业洞察 / 痛难点 | `source=/enterprise-center/overview`、`sourceTab=risk-opportunity`、`riskType=growth_slowdown`、`riskLevel`、`riskDimension=growth`、`industry`、`timeRange`、`region`、`enterprise_codes[]` | 若没有 `riskType` 或风险等级，按钮禁用并显示「风险对象待识别」；不展示底部通用痛难点按钮。 |
| 风险项：上游材料依赖 | 查看供应链风险 | `/enterprise/supply-chain` | `riskType=supply_dependency`、`riskLevel`、`riskDimension=supply_chain`、`chainNode=upstream_material`、`enterprise_codes[]`、`industry`、`region` | 若无 `chainNode`，动作降级为「查看风险说明」，不跳供应链页。 |
| 风险项：指标口径待维护 | 查看维护口径 | 当前卡片展开说明或企业分布 Tab | `riskType=data_quality`、`riskDimension=data_maintenance`、`metric_id`、`pendingRef`、`industry`、`timeRange` | 待维护项不提供强处置动作；只显示 `PendingBadge`、口径说明和责任字段。 |
| 风险项：影响企业集合 | 查看影响对象 | `/development/search` 场景化高级检索或对象列表 Drawer | `riskType`、`riskLevel`、`enterprise_codes[]`、`sourceTask=查看影响对象`、`industry`、`timeRange`、`region` | 企业集合为空时显示「暂无可验证影响对象」，不跳空检索。 |
| 供应链风险项 | 查看节点风险 | `/enterprise/supply-chain` | `riskType=supply_chain_risk`、`chainNode`、`riskDimension`、`enterprise_codes[]`、`industry`、`region` | 节点未识别时入口禁用；卡片保留原因摘要和「待供应链节点匹配」。 |
| 机会项：低空经济高潜 | 生成招引培育名单 | `/enterprise/recommendation` | `opportunityType=low_altitude_growth`、`suggested_action=attract_or_cultivate`、`region_code`、`enterprise_codes[]`、`industry`、`timeRange` | 无候选企业集合时动作降级为「查看机会说明」，不生成空名单。 |
| 机会项：新能源链主带动 | 查看链位缺口 | `/enterprise/supply-chain` 或企业洞察 / 深圳链位缺口 | `opportunityType=new_energy_chain_owner`、`chain_gap`、`chainNode`、`suggested_action=fill_chain_gap`、`enterprise_codes[]`、`industry`、`region` | 未识别 `chain_gap` 时只展示机会摘要和「链位缺口待计算」。 |
| 机会项：集成电路封测协同 | 查看协同对象 | `/enterprise/status-analysis` 或对象列表 Drawer | `opportunityType=ic_packaging_collaboration`、`suggested_action=collaboration_match`、`enterprise_codes[]`、`region_code`、`industry` | 对象不足 2 个时禁用协同动作，说明「协同对象不足」。 |
| 机会项：区域招商 / 培育建议 | 生成区域候选名单 | `/enterprise/recommendation` | `opportunityType=regional_candidate`、`suggested_action`、`region_code`、`enterprise_codes[]`、`industry`、`timeRange` | 缺少区域上下文时提示「先选择区域后生成名单」。 |
| 待确认机会 / 待维护机会 | 查看口径说明 | 当前卡片内展开，不跨页 | `opportunityType=data_pending`、`pendingRef`、`industry`、`timeRange` | 不展示主按钮；仅保留说明、更新时间和维护来源。 |

### 7.4 页面结构调整建议

| 页面区域 | 调整结论 | FE 落点 |
| --- | --- | --- |
| 态势概览底部「关键下钻入口」 | 移除整个底部 Section。原「查看企业分布」「类型分布分析」「深圳现状分析」「综合竞争力」不得作为无上下文按钮组保留。 | `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseOverviewTabs.tsx` 中 `EnterpriseSituationOverview` 的 `SectionPanel title="关键下钻入口"`。 |
| KPI 卡 | 保留为可解释的数据载体。按指标类型补点击事件、可访问名称、禁用 / loading / empty 态。`ⓘ` 或口径说明只打开说明，不做跨页跳转。 | `MetricCard` 调用处或 MetricCard 扩展事件。 |
| 趋势图 | 点击点位进入趋势 / 异常研判；图例只做图表内筛选。 | `EnterpriseSituationOverview` 的 `trendOption` 增加结构化点击处理。 |
| 环形图 / 产业结构图 | 点击分组进入类型结构；图例不跨页。 | `EnterpriseSituationOverview` 的 `industryOption` 增加 `sourceChart=industry_structure`。 |
| 地图 / 区域视图 | 区域点击携带 `region_code`；区域卡可作为地图缺省态的替代入口。 | `EnterpriseDistributionOverview` 的区域热力卡和后续真实地图容器。 |
| 重点对象卡 | 企业名打开画像抽屉；对比篮 / 收藏保持对象级辅助动作。 | `EnterpriseKeyObjectsOverview`、`EnterpriseObjectRow`。 |
| 风险机会底部「后续处置路径」 | 移除整个底部 Section。原「痛难点诊断」「供应链风险」「招引培育行动」不得作为底部通用跳转按钮保留。 | `EnterpriseRiskOpportunityOverview` 的 `SectionPanel title="后续处置路径"`。 |
| 风险 / 机会卡片动作 | 每张卡片内保留 0-2 个对象绑定动作；主动作必须携带 `riskType` 或 `opportunityType`。待维护卡片不展示强动作。 | `riskItems`、`opportunityItems` 数据结构需补对象参数和禁用原因。 |

### 7.5 给 frontend-agent 的后续实施边界

建议新建 FE 任务：`FE-ENT-OVERVIEW-DRILLDOWN-ACTIONS`。

| 项 | 边界 |
| --- | --- |
| 必须改 | 删除 `EnterpriseOverviewTabs.tsx` 中「关键下钻入口」和「后续处置路径」两个底部 Section；将动作迁回 KPI、趋势图、产业结构图、区域视图、重点对象行、风险 / 机会卡片。 |
| 必须补 | 为数据载体点击统一构造上下文参数；至少覆盖 `source`、`sourceTab`、`industry`、`timeRange`、`region`、`sourceMetric` / `sourceChart`、`riskType` / `opportunityType`。 |
| 必须保留 | 企业中心四个二级菜单、企业总览四个一级 Tab、旧路由兼容、ContextBar 状态继承、重点对象画像抽屉 / 对比篮既有能力。 |
| 禁止做 | 不新增左侧菜单；不新增企业检索固定 Tab；不新增系统级全局搜索；不新增底部推荐区；不把无上下文按钮改名后继续保留。 |
| 非本任务 | 不重写企业洞察 / 企业决策深层页；不实现真实后端处置流、工单、政务办理；不扩大到 L07 企业检索完整闭环。 |

### 7.6 FE 验收口径

| 验收项 | 通过标准 |
| --- | --- |
| 旧底部区块移除 | 页面源码和渲染结果均不再出现「关键下钻入口」「建议继续查看」「后续处置路径」。 |
| 数据载体下钻 | KPI、趋势点位、产业结构分组、区域视图、重点对象至少各有一个可验证对象级下钻；点击参数包含当前 ContextBar 和触发对象。 |
| 风险机会卡片动作 | 风险项动作携带 `riskType`，机会项动作携带 `opportunityType` 或 `suggested_action`；待维护项不展示强动作。 |
| 降级状态 | 无数据、无权限、无对象、上下文缺失时不跳空页；布局稳定，显示禁用原因或空态说明。 |
| 搜索 / 导航边界 | 左侧菜单不新增企业检索；企业检索不成为固定 Tab；企业中心顶部不新增常驻全局搜索。 |
| 静态契约 | `scripts/check-enterprise-ia.mjs` 增加断言：禁止旧区块标题回退；检查 `sourceTab=situation`、`sourceTab=risk-opportunity`、`sourceMetric` / `sourceChart`、`riskType` / `opportunityType` 等关键字段。 |
| 建议验证命令 | 在 `repos/demo-ui-topic` 执行 `node scripts/check-enterprise-ia.mjs`、`node scripts/check-trend-semantics.mjs`、`npm run build`；若 `npm run design:check` 仍因既有非企业中心问题失败，需标明不是本任务引入。 |

### 7.7 UE 推导项标识清单（待全员讨论）

以下内容不按“已确认需求”处理。若后续需要在页面中展示，应使用轻量浮层 / Popover / Tooltip 标识为「UE 推导 · 待讨论」，说明依据和待确认点；标识本身只服务评审，不改变下钻功能。

| 位置 | 需求依据支持到哪里 | UE 推导 / 待讨论内容 | 页面标识建议 |
| --- | --- | --- | --- |
| 近 12 月趋势图普通点位 | 支持趋势图点位下钻，并带 `timePoint`、`clickedValue`、当前产业/区域/时间窗上下文。 | tooltip 中是否放“查看该月趋势明细”、是否直接进入深圳现状或趋势明细抽屉。 | 在趋势图标题右侧放「UE 推导 · 待讨论」浮层，说明普通点位的承接形态待确认。 |
| 近 12 月趋势图异常点 / 拐点 | 支持“趋势拐点查看原因”。 | 是否增强 tooltip、动作文案“研判增速变化原因”、是否进入 `/enterprise/pain-points`、是否需要异常原因抽屉、`dimension=growth_change` 与 `riskDimension=growth` 参数名、禁用文案“异常原因待模型输出”。 | 在趋势图标题右侧或异常点 tooltip 内放「UE 推导 · 待讨论」浮层；进入痛难点前必须先确认该异常点已被风险归因。 |
| KPI 卡到具体深层页 | 支持 KPI 卡作为数据载体下钻，并携带 `sourceMetric/metric_id`。 | 每个 KPI 的默认目标页，如创新型企业到类型结构、专利总量到能力评估、企业总数到类型分布等。 | 在 KPI 卡动作区或 `ⓘ` 旁标识「目标页待讨论」，不影响口径说明。 |
| 环形图 / 产业结构图分组 | 支持点击结构分组进入类型/结构分析，并携带 `dimension`、`clickedValue`。 | `sourceChart=industry_structure`、`dimension=industry` 等参数命名，以及是否只进入 `/enterprise/type-distribution`。 | 在图表标题右侧标识，浮层说明“参数枚举与目标页待接口/PM 确认”。 |
| 地图 / 区域视图框选 | 支持地图/区域点击查看区域分布。 | 框选企业、`selectionType=box`、`region_code[]`、`enterprise_codes[]`，以及是否跳 `/development/search`。 | 仅在启用框选能力时显示浮层；未确认前不把框选作为必做验收。 |
| 风险项默认动作 | 支持风险项卡片内动作，并进入痛难点或供应链验证原因。 | 具体风险类型枚举、默认动作文案、默认目标页、`riskType/riskDimension/riskLevel` 命名，以及某个风险项究竟进入痛难点还是供应链。 | 每个风险卡动作按钮旁可放「UE 推导 · 待讨论」浮层；风险对象缺失时不展示强动作。 |
| 机会项默认动作 | 支持机会项进入深圳现状或招引培育，并携带机会类型、建议动作、区域或链位缺口。 | 低空经济、新能源链主、封测协同等样例动作，候选名单生成条件，`opportunityType/suggested_action/chain_gap` 枚举。 | 每个机会卡动作按钮旁可放「UE 推导 · 待讨论」浮层；无候选集合时不展示生成类动作。 |
| 无状态降级文案 | 支持无对象、无指标、无图表上下文时不展示裸跳转。 | 具体提示文案，如“异常原因待模型输出”“风险对象待识别”“链位缺口待计算”。 | 空态 / 禁用态旁标识文案待确认，避免被误认为最终产品文案。 |

### 7.8 PM 已处理问题（来自 `PM-ENT-overview-action-requirement-confirmation.md` §4.3）

| 问题 | PM 处理结论 | FE / UE 后续口径 |
| --- | --- | --- |
| KPI 卡点击目标是直接跨页还是先打开指标明细抽屉？ | 本期不新增指标明细抽屉。KPI 卡可直接进入既有企业洞察 / 企业决策页面，但必须携带 `sourceMetric`、`metric_id`、`industry`、`timeRange`、`region` 等上下文；`ⓘ` / `MetricSpecCard` 只承载指标口径说明。 | FE 可先实现跨页下钻；指标明细抽屉如需建设，另立任务，不阻塞本期移除底部按钮组。 |
| `enterprise_codes[]` 是否已有真实集合接口？ | 当前不按真实接口已就绪处理。只有卡片、榜单、地图框选或风险/机会对象本身已有明确企业集合时，才可传 `enterprise_codes[]`；没有集合时不得伪造对象，也不得生成名单或处置承诺。 | Demo / Mock 可用现有样本企业集合，但必须贴近触发对象并标注 Mock / 待接入；集合为空时不展示强动作。 |
| 风险 / 机会的枚举值是否由 PM 固定？ | PM 先固定业务枚举口径，不固定最终接口字段名。UE 文档中的英文 key 可作为 Wave 0 临时前端契约，但不是后端 API 终稿。 | 本期允许使用 `growth_slowdown`、`supply_dependency`、`data_quality`、`supply_chain_risk`、`low_altitude_growth`、`new_energy_chain_owner`、`ic_packaging_collaboration`、`regional_candidate` 等临时 key；后续由 PM / 数据 / FE 统一映射表。 |
| 页面是否需要显示「UE 推导 · 待讨论」浮层？ | 需要，但仅限评审 / 验收环境。正式演示和生产默认隐藏。浮层用于标识“需求依据支持到哪里、UE 推导到哪里、待确认点是什么”，不代表动作已签收。 | FE 若执行标识任务，应通过显式开关控制，例如评审态配置、dev status 或本地开关；浮层使用轻量 Tooltip / Popover，贴近具体 KPI、图表标题、风险/机会动作按钮或空态文案，不新增页面顶部说明条。 |

### 7.9 PM 边界声明

| 类型 | 是否允许进入 FE 实施 | PM 边界 |
| --- | --- | --- |
| 数据载体点击下钻 | 允许 | KPI、趋势图点位、结构图分组、地图区域、重点对象卡均可作为下钻入口，但必须带上下文。 |
| 趋势异常点 / 拐点动作 | 条件允许 | 需求支持“查看原因”，但默认承接应优先为趋势异常原因抽屉或趋势明细；只有当异常点已被归因为风险项，并具备 `riskType/riskDimension` 时，才可进入痛难点。 |
| 默认目标页和英文参数枚举 | 允许作为 Wave 0 临时契约 | 目标页、参数名、枚举 key 需要在评审态浮层标识为 UE 推导；后续接真实数据或后端 API 时再收敛。 |
| 生成名单 / 招引培育动作 | 条件允许 | 必须有候选企业集合、机会类型和建议动作；无对象时不展示强动作，不允许生成空名单。 |
| 「UE 推导 · 待讨论」页面浮层 | 允许但仅评审态 | 服务全员讨论，不作为正式用户界面；不得替代需求确认流程。 |

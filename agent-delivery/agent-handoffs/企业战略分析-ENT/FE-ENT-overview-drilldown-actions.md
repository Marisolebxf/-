# Handoff · FE-ENT-OVERVIEW-DRILLDOWN-ACTIONS（企业总览数据载体下钻与风险机会卡片动作实施）

| 项 | 内容 |
| --- | --- |
| 任务 ID | FE-ENT-OVERVIEW-DRILLDOWN-ACTIONS |
| 角色 / 执行方 | frontend-agent |
| 目标仓库 | `repos/demo-ui-topic` |
| 前置任务 | `PM-ENT-OVERVIEW-ACTION-REQ`、`UE-ENT-OVERVIEW-DRILLDOWN-ACTIONS` |
| 状态 | Ready for frontend-agent |
| 生成日期 | 2026-07-01 |

## 1. 目标

在企业总览页中按 PM / UE 结论完成动作归位：

- 移除态势概览底部「关键下钻入口 / 建议继续查看」区块。
- 移除风险机会底部「后续处置路径」区块。
- 将下钻动作迁回 KPI 卡、趋势图、产业结构图、区域视图、重点对象卡等数据载体。
- 将风险 / 机会动作内联到具体风险项或机会项卡片。
- 对属于 UE 推导的目标页、参数枚举、异常点增强、禁用文案等，仅在评审 / 验收环境显示「UE 推导 · 待讨论」轻量浮层；正式演示和生产默认隐藏。

## 2. 必读依据

- `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/PM-ENT-overview-action-requirement-confirmation.md` §4.3
- `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/UE-ENT-overview-drilldown-actions.md` §7.2 ~ §7.9
- `gkx-orchestration/agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-UE-IA-L03-overview-integration.md`
- `gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`
- `gkx-orchestration/agent-delivery/Design.md`

## 3. 实施范围

| 文件 / 区域 | 要求 |
| --- | --- |
| `src/app/pages/enterprise/EnterpriseOverviewTabs.tsx` | 删除两个底部 Section；补 KPI、趋势图、结构图、区域视图、重点对象、风险/机会卡片动作归位。 |
| `src/app/pages/enterprise/EnterpriseOverviewTabs.tsx` | 下钻参数必须携带 `source=/enterprise-center/overview`、`sourceTab`、`industry`、`timeRange`、`region`，并按触发源补 `sourceMetric` / `sourceChart` / `metric_id` / `timePoint` / `clickedValue` / `riskType` / `opportunityType`。 |
| `src/app/pages/enterprise/EnterpriseOverviewTabs.tsx` | `enterprise_codes[]` 只有在当前卡片、榜单、框选或风险/机会对象已有真实或 Mock 企业集合时传递；不得伪造对象集合。 |
| `src/app/pages/enterprise/EnterpriseOverviewTabs.tsx` | KPI 本期直接跨页到既有企业洞察 / 企业决策页面；不新增指标明细抽屉。`ⓘ` / `MetricSpecCard` 继续只表达口径。 |
| `src/app/pages/enterprise/EnterpriseOverviewTabs.tsx` | 趋势异常点默认优先进入异常原因抽屉或趋势明细；只有已归因为风险项并具备 `riskType/riskDimension` 时，才进入痛难点。 |
| `scripts/check-enterprise-ia.mjs` | 增加静态契约：禁止旧底部标题回退；检查关键下钻参数、风险/机会对象参数和评审态浮层开关边界。 |

## 4. 禁止事项

- 不新增左侧菜单。
- 不新增企业检索固定 Tab。
- 不新增系统级全局搜索。
- 不新增底部推荐 / 处置按钮组。
- 不把无对象、无指标、无图表上下文的裸跳转按钮包装成下钻或处置路径。
- 不新增真实后端处置流、工单、政务办理。
- 不在正式演示 / 生产默认显示「UE 推导 · 待讨论」浮层。

## 5. 验收口径

| 验收项 | 通过标准 |
| --- | --- |
| 旧区块移除 | 页面源码和渲染结果不再出现「关键下钻入口」「建议继续查看」「后续处置路径」。 |
| 数据载体下钻 | KPI、趋势点位、结构图分组、区域视图、重点对象至少各有一个对象级下钻，且带当前 ContextBar 和触发对象。 |
| 风险机会动作 | 风险项动作携带风险对象参数；机会项动作携带机会对象或建议动作参数；无对象时不展示强动作。 |
| UE 推导标识 | 目标页、参数枚举、异常点增强、禁用文案等 UE 推导项只在评审 / 验收环境以 Tooltip / Popover 轻量展示。 |
| 降级状态 | 无数据、无权限、无对象、上下文缺失时不跳空页，显示禁用原因或空态说明。 |
| 边界不回退 | 左侧菜单、企业总览四 Tab、旧路由兼容、ContextBar 持久化不回退。 |

## 6. 验证命令

在 `repos/demo-ui-topic` 下执行：

```bash
node scripts/check-enterprise-ia.mjs
node scripts/check-trend-semantics.mjs
npm run build
npm run design:check
```

若 `npm run design:check` 仍因既有非企业中心问题失败，需在回填中说明，不应归因到本任务。

## 7. 简短派单话术

```text
请 frontend-agent 执行 FE-ENT-OVERVIEW-DRILLDOWN-ACTIONS。

目标是按 PM/UE 已确认口径修改企业总览页：移除态势概览底部「关键下钻入口 / 建议继续查看」和风险机会底部「后续处置路径」两个 Section；把下钻动作迁回 KPI 卡、趋势图、产业结构图、区域视图、重点对象卡，把风险/机会动作内联到具体风险项或机会项卡片，并携带当前 ContextBar 与触发对象上下文。

注意边界：KPI 本期直接跨页，不新增指标明细抽屉；enterprise_codes[] 只有在真实或 Mock 对象集合存在时传递；风险/机会枚举可先作为 Wave 0 临时前端契约；趋势异常点默认优先趋势明细/异常原因抽屉，只有已归因为风险项才进入痛难点；「UE 推导 · 待讨论」浮层只在评审/验收环境显示，正式演示和生产默认隐藏。

禁止新增左侧菜单、企业检索固定 Tab、系统级全局搜索、底部推荐按钮组，也不要把无对象、无指标、无图表上下文的裸跳转包装成下钻或处置路径。

实施前请阅读：
- PM-ENT-overview-action-requirement-confirmation.md §4.3
- UE-ENT-overview-drilldown-actions.md §7.2~§7.9
- ENT-UE-IA-L03-overview-integration.md
- UX-UE 通用交互组件规范.md

验收需更新 check-enterprise-ia 静态契约，并执行 check-enterprise-ia、check-trend-semantics、npm run build、npm run design:check。
```

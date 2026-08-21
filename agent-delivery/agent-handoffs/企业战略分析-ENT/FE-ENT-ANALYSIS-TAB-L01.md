# FE-ENT-ANALYSIS-TAB-L01 · 招引/培育三 Tab 并列

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用风险历史表模式 + 现有 analysisTaskList；未新造任务中心类型。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom。 |

## 范围与实现

招引、培育页 WorkbenchTabs 三项并列：条件筛选推荐、候选工作台、最近分析。最近分析读 `analysisTaskList`（talent_recommend + 当前 subType）。URL `entry=history`。不含重点企业类型/领域。

## 偏离

无。监管人要求三 Tab 并列（不嵌在「当前分析」下），按此实现。

## 产物清单

- lumen-ui-topic `fb3cab5`（`dev`）
- 本 handoff

## 问题清单

- 本轮不做重点企业类型/领域历史 Tab（K1-C）。
- 最近分析与条件筛选、候选工作台**三 Tab 并列**（监管人改口，不嵌在「当前分析」下）。

## 修改内容

- `EnterpriseRecruit.vue`：WorkbenchTabs 增加「最近分析」。
- `RecruitHistoryTable.vue`：本 subType 任务列表；恢复 / 按此配置新建 / HTML 报告。
- `useRecruit.ts` + `recruitRoute.ts`：`entry=history`；切历史不走发起分析。
- 自检：`recruitRoute.selfcheck.mjs`。

## 验收证据

## 测试结果

- `node src/composables/recruitRoute.selfcheck.mjs` 通过。
- 2026-08-21 `human:孔东` 验收通过：招引/培育三 Tab 并列；历史恢复/切 Tab 过程不丢。联调通过。

## 遗留风险

- 过程保活（离页续订 SSE）在 `FE-ENT-ANALYSIS-RESUME-L01`。
- 本叶不含重点企业类型/领域历史。

## 成本（必填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.43 |
| cost_warn | green |
| 口径 | 无 Console 精确 in/out，按估算回填；frontend 默认 80/20 × Sonnet 价表 |

## CI/CD（必填）

- 分支：`dev`（lumen-ui-topic `fb3cab5`）
- pipeline：待 push
- K8s rollout：N/A

## 涉及文件

- `repos/lumen-ui-topic/src/views/enterprise/EnterpriseRecruit.vue`
- `repos/lumen-ui-topic/src/composables/useRecruit.ts`
- `repos/lumen-ui-topic/src/composables/recruitRoute.ts`
- `repos/lumen-ui-topic/src/composables/recruitRoute.selfcheck.mjs`
- `repos/lumen-ui-topic/src/components/enterprise/recruit/RecruitHistoryTable.vue`

## 架构合规自检

1✅ 2✅ 3✅ 4✅ 5✅ 6✅ D12✅

# FE-ENT-ANALYSIS-RESUME-L01 · 企业分析 Job 页过程态保活

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
| 说明 | 修根因：切「当前分析」误走 showConfiguration；用会话 store + running 列表恢复，不 keep-alive 全站。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom。 |

## 范围与实现

评估/风险/招引 Job 页：切 Tab、点侧栏同 leaf、离页再进，恢复 configuration|processing|result，不 `showConfiguration` 清任务；历史 Tab 不关 SSE。Pinia 会话 + `analysisTaskRunning` 续订 #109。侧栏 `mergeMenuQuery`。不含重点企业类型/领域与产业链扫尾。

## 偏离

无。

## 产物清单

- lumen-ui-topic `fb3cab5`（`dev`）
- 本 handoff

## 问题清单

- 不含重点企业类型/领域；不含产业链工作区扫尾。
- 服务端 Job 本身不因关 SSE 停止；回页续订 #109。

## 修改内容

- 评估/风险：`showCurrentAnalysis` 恢复 configuration|processing|result；历史 Tab 不清 `task_id`、不关流。
- 招引/培育：mode 袋提升到模块级；离页再进 restore + 续订。
- Pinia `enterpriseAnalysisSession`；进页无 URL 任务时 peek 或 `analysisTaskRunning`。
- 侧栏 `mergeMenuQuery`：同 path 同 workspace 保留 task_id / analysis_view / view / entry。

## 附录 E 自检

- [x] E.1 本叶覆盖评估、风险、招引/培育
- [x] E.2 未改开始分析语义（招引历史 Tab 禁止直接发起）
- [x] E.3 切 Tab 不 create
- [x] E.4 单飞仍走 analysisTaskGate
- [x] E.5 当天复用未改
- [x] 深链/浮层仍走 restoreTask

## 验收证据

## 测试结果

- 2026-08-21 `human:孔东` 验收通过：评估/风险/招引切 Tab 与离页再进，过程态保持。联调确认。

## 遗留风险

- 本机曾混用 pnpm 导致 `node_modules` 损坏；已改回 `npm install`。勿对 npm 仓再跑 `pnpm exec vue-tsc`。
- 不含重点企业类型/领域；不含产业链工作区扫尾。

## 成本（必填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.65 |
| cost_warn | green |
| 口径 | 无 Console 精确 in/out，按估算回填；frontend 默认 80/20 × Sonnet 价表 |

## CI/CD（必填）

- 分支：`dev`（lumen-ui-topic `fb3cab5`）
- pipeline：待 push

## 涉及文件

- `useEnterpriseRisk.ts` / `useEvalTask.ts` / `useRecruit.ts`
- `EnterpriseRisk.vue` / `EnterpriseEvaluation.vue`
- `DefaultLayout.vue`
- `stores/enterpriseAnalysisSession.ts`

## 架构合规自检

1✅ 2✅ 3✅ 4✅ 5✅ 6✅ D12✅

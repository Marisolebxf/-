# FE-CHAIN-ANALYSIS-RESUME-L01 · 产业链 Job 页过程态保活

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
| 说明 | 复用企业 Pinia 会话 + 招引同款「记录 Tab 不清 task_id」；未新造任务中心。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom。 |

## 范围与实现

仓：`lumen-ui-topic`。诊断 / 区域 / 深圳 / 全景与企业 `FE-ENT-ANALYSIS-RESUME-L01` 等同：切记录 Tab、切同页叶子、离页再进、侧栏同 leaf 不丢过程态。不改 I2-12「开始分析」语义。

## 偏离

无。

## 产物清单

- 本手改代码（待监管人确认后 commit）
- 本 handoff

## 问题清单

- 不含企业页；不含政策 / 服务链。

## 修改内容

- 诊断/区域/深圳：`openRecordsTab` 不清 `task_id`；切回叶子按会话恢复 processing/result。
- `useIndustryAnalysisJob`：Pinia `chain` 袋 + `analysisTaskRunning` 离页续订；记录态不关 SSE。
- 侧栏 `KEEP_ANALYSIS_QUERY` 增加 `demo_state`。
- 自检：`industryJobResume.selfcheck.mjs`。

## 附录 E 自检

- [x] E.1 本叶覆盖全景、诊断、区域、深圳
- [x] E.2 未改开始分析 / 重新分析
- [x] E.3 切 Tab 不 create
- [x] E.4 单飞仍走 industryAnalysisGate
- [x] E.5 当天复用未改

## 验收证据

## 测试结果

- `node src/utils/industryJobResume.selfcheck.mjs` 通过。
- 请人工：诊断跑到一半 → 诊断记录 → 原叶子，步骤继续；再去查询再回该叶子，应回到过程/结果。

## 遗留风险

- 侧栏点**另一**叶子（周期→关键环节）仍换袋，不共用一条 Job。

## 成本（必填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.43 |
| cost_warn | green |
| 口径 | 无 Console 精确 in/out，按估算回填；frontend 默认 80/20 × Sonnet 价表 |

## CI/CD（必填）

- 分支：`dev`（lumen-ui-topic `029f9b7`）
- pipeline：待 push

## 架构合规自检

1✅ 2✅ 3✅ 4✅ 5✅ 6✅ D12✅

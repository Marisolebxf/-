# FIX-POL-INTENSITY-FP-L02 · 政策详细对比「计算支持力度」报错修复（analysis_fp 缺失被服务端拒）

- **仓**：`lumen-ui-science-pc` · commit **`aba7c0a`**（2026-11-04 已推 `origin/dev`）
- **类型 / 状态**：bugfix · in_progress（CI 部署后走查复测转测）
- **强度**：ponytail full
- **trace**：`4fa7527693513afcfb2e88d56b77d6d5`（用户 2026-11-04 13:46:22 提交）

## 走查问题

政策全景 → 政策详细对比弹窗，点「计算支持力度」报错；Network 里 `jobs` 请求 Response 为红字 `{code:1, msg:...}`，界面不回填力度分。

## 排查结论（线上证据，gkx-trace 规约）

- **Tempo（lumen 30202）**：trace `4fa75276…` 链路 `gateway → gkxlumen-display POST /v1/policy/panorama/jobs → gkxlumen-topic-async-service-biz POST /topic/v1/analysis/tasks` **全程 HTTP 200**（任务创建成功，时长 160ms）。
- **Loki（lumen 30311）**：13:46:20–13:52 全服务窗口内**无任何 `/internal/policy/jobs/execute` 调用**（`gkxlumen-entan-py-api` access log 只有 `docs/{id}` 与 `indicators`）——任务创建后**下游未执行**。
- **代码对照**：`AnalysisTaskServiceImpl#create` 对 `PolicyAnalysisTypes.isPolicy()` 类型走 `createFingerprintGatedTask`，**强校验 `analysis_fp`（64 位小写 SHA-256）**，缺失即 `R.failed("analysis_fp 不能为空")`（HTTP 200 + `code:1`，所以 trace 全绿但业务失败）。
- 前端 `compareLive.ts#intensityJobBodyOf` 只发 `{ sub_type:'policy_intensity', params:{ policy_ids } }`，**未带 `analysis_fp`** → 直接命中该校验。

> 传输成功、业务被拒：断点在「async-service 创建门禁」，不在网关/Python。

## 修复内容（前端 3 文件）

| 文件 | 改动 |
|---|---|
| `src/views/policy/panorama/compareLive.ts` | `intensityJobBodyOf(policyIds, analysisFp)` 增加指纹入参，请求体带 `analysis_fp` |
| `src/views/policy/panorama/components/ComparisonModal.vue` | `runIntensity` 用既有 `sha256Hex`（`@/api/policy`）生成指纹：`policy-intensity:<ids 排序后 join>` → 同条件同指纹，当天幂等复用、不掺随机 |
| `src/views/policy/panorama/components/BenchmarkCompareModal.vue` | 218 可视化 `runLiveViz` 同链路同修 |

指纹惯例复用仓内已有先例：`evaluationWiring.ts`（DS11 解读 Job）同用 `sha256Hex` + `analysis_fp`。

## 附带发现（不在本单修，已登记）

1. **`gkxlumen-element`** 13:38/13:45/13:48 三次 `gapfill 读表失败：Unknown column 'topic_or_metric' in 'field list'`——`SHELL_SQL`（`gapfill_policy_eval_shell`）SELECT 列与实表不符 → 弹窗顶部「部分字段获取失败（已返回的目录与正文不受影响）」横幅来自这里（214 条件/材料附带列为空）。需 DDL/SQL 对齐，属 element/数据侧单。
2. **`gkxlumen-topic-async-service-biz`** `evaluation_templates` 查询持续报 `Unknown column 'thresholds_json'`——模板表缺列，与政策力度无关。

## 验证

- `FE-POL-CMP-LIVE.test.mjs` 全绿（新增指纹断言：Job 体含 `analysis_fp`、组件生成指纹锚点）
- `pnpm type-check` 绿
- 政策族回归（VIZ-WIRING / FIX-POL-ANALYSIS-APPLY-L01 / FE-POL-02A / CMP-LIVE / TREND-LIVE）全绿
- 复测口径（dev 部署后）：点「计算支持力度」→ Network `jobs` 响应 `code:0` + 任务号；任务完成后力度分回填六维表

## 架构合规自检

| 条 | 结论 |
|---|---|
| 调用链不越层 | ✅ 仍走 前端 → display → async-service → lumen-algo-py，零新端点 |
| I2-12 切条件不自动起任务 | ✅ 指纹仅在用户点击时生成；同条件幂等复用反而强化「同条件只一条」 |
| D9 诚实性 | ✅ 不造分，任务失败仍空态 |
| ponytail | ✅ 最小 diff（3 文件），复用已有 `sha256Hex`，无新依赖 |

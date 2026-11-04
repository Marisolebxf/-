# SITUATION-TS-TRACKING-EVAL-L01 · 真实评估接入（久新模型装配 + 运行态进度）

> 任务：`SITUATION-TS-TRACKING-EVAL-L01` ｜ 状态：`integration`（等人工走查）｜ agent：`frontend-agent`
> 监管人：`human:孔东` ｜ 仓：`lumen-ui-science-pc` + `lumen-svc-platform` ｜ 日期：2026-11-03
> 设计说明真源：`repos/lumen-ui-science-pc/docs/tracking-真评估接入设计.md`（§1–§12）

## 1. 目标

把 DS-03「技术发展跟踪」的评估从**演示种子**切到**久新评估模型真实产出**：
三阶段（setup → running → result）中 running 必须真跑、进度真回、result 真算，不许再用 mock 假分。

## 2. 落地实现

| 层 | 文件 · 方法 | 说明 |
|---|---|---|
| 前端 API | `src/api/situation/tracking.ts` · `startTrackingEvaluation` / `fetchTrackingEvaluationProgress` / `fetchTrackingEvaluationResult` | 走 `evaluation/run → {taskId}/progress → {taskId}/result`，`USE_MOCK=false` 直连网关 |
| 前端页 | `src/views/situation/tracking/index.vue` | `startEvaluation()` 冻结口径后提交；`pollEvaluationProgress()` 轮询（失败按 `Message.error` 如实报，不吞）；`evaluationProgressStage` 三态切换 |
| 前端结果页 | `components/ResultDashboard.vue` | 消费 `dataset`（真实 top-N），KPI/五视图/榜单全部来自 dataset |
| display 网关 | `TrackingController#runEvaluation` / `#evaluationProgress` / `#evaluationResult` | `POST /v1/situation/tracking/evaluation/run`（异步任务 + 线程池）、`GET /evaluation/{taskId}/progress`、`GET /evaluation/{taskId}/result` |
| 域服务 | `RemoteTrackingArtifactClient` → `gkxlumen-topic-async-service#TrackingEvaluationController` | 任务编排、久新取数、落 `tech_evaluation_history` |

关键口径（不许回退）：

- **KPI 是「潜力综合分均值」，不是热度均值** —— 标签已正名为「综合潜力指数」，避免口径错挂。
- **无源字段恒 `null`**：成熟度 / 投资额久新评估表无此两维 → `record.put("maturity", null)` / `("investment", null)`，**不造 0**。
- **前端不重算评分**：`records` 按后端 `potential_rank` 排序后仅做格式化。

## 3. 契约（实测）

`POST /v1/situation/tracking/evaluation/run` → `{ taskId, status }`；`progress` → `{ stage, percent, message }`；
`result` → `TrackingDataset`（`records` top-20、`bubbles`、`heatMatrix`、`relations`、`evaluationHistory`）。

## 4. 实测证据（2026-11-03）

- `POST /dataset` → `code=0`、`records=20`、`heatMatrixYears` 有数据、`relations>0`。
- 页面跑评估：setup → running（真轮询）→ result，`KPI 综合潜力指数 88 ↑0.5%`，五视图全渲染。
- 历史落库：`tech_evaluation_history` 实测 `runId=0c9303e5…` / `4c699bb3…` 等多次落库日志。
- 与 mock 轨隔离：`VITE_APP_USE_MOCK=false`，mock 模块零执行（见 `mock-ledger.md` 技术发展跟踪登记）。

## 5. 遗留与风险

1. `DS-03-METRIC-OPEN-L01` 6 个开放项未闭合 → 本页数字**暂无已签收指标**，D9 只能落 D1 missing 红问号（见 PERSIST 单）。
2. 评估任务为内存态 + 线程池（单机 local 实测通过；多副本需分布式任务/取消语义，未做）。
3. 长任务中断恢复未做（页面刷新后无法续看跑动中的 taskId）。

## 6. 纪律

⚠️ 人工验收闸门（2026-10-20 裁定）：改动已本地 commit（前端 `e5c5085` / 后端 `44b7843` / 台账 `b0cfe7eb`），**未 push**，等 `human:孔东` / `human:唐绍祖` 走查通过后推 `origin/dev`。

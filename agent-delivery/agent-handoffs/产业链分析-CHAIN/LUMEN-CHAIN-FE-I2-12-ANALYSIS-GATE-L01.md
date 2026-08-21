# LUMEN-CHAIN-FE-I2-12-ANALYSIS-GATE-L01 · lumen 产业链分析工作区 — I2-12 开始分析与当日条件复用

> 对照 `templates/handoff-template.md`；内容按本叶 as-built。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:李伟` |
| claim_type | `pull` |
| 说明 | 2026-08-20 李伟确认开工；已由 `claimed` 转 `in_progress`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 Java `analysisTask*` + 本仓 composable；门控从 demo `b5e6430` 语义移植为 Vue，不贴 JSX。未用 YAGNI 跳过 I2-12 / W4 / 附录 E。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂 Headroom MCP。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改调用链：仍前端 → Java `analysisTaskCreate/List/Detail`；无新跨层边 |
| 会签态 | N/A（纯前端门控，I2-11 可与模块联调图共用） |

## 范围与实现

仓：`lumen-ui-topic`。范围仅全景 / 诊断 / 区域 / 深圳；不含企业、政策、服务链。

对照：`demo-ui-topic` `b5e6430` + `产品实现规程.md` I2-12 / 附录 E / **Q-ANALYSIS-01**。

- 切条件不自动 `create`（四页无 `watch`→`createJob`）。
- 条件栏主按钮「开始分析」；当天成功另有「重新分析」。
- 稳定 `taskType` = 现有 `chain:*:*`；产业/链/区域等进 `analysis_fp`。
- 同用户 + 同 type + 同指纹仅一条 `running` 可恢复；不同指纹不把旧产业任务拽回来。
- 当天（`Asia/Shanghai` 自然日，锚点 `endTime`/`createTime`，仅 `success`）点「开始分析」打开结果；「重新分析」才再 `create`（仍受同指纹单飞约束）。
- Mock Create 互斥改为按指纹，不再按 type 误复用。

## 附录 E 扫描摘要

| 步骤 | 页 | 结果 |
|------|----|------|
| E.1 | 全景 / 诊断(cycle·key_link·bottleneck) / 区域(index·competitiveness) / 深圳(comparison·development) | 已扫；查询/概览/维护不在本叶 |
| E.2 | 四页条件栏「开始分析」；当天成功有「重新分析」 | P0 0 |
| E.3 | 无切条件自动 create | P0 0 |
| E.4 | `findInFlightAnalysis(..., fingerprint)` | P0 0 |
| E.5 | `findSucceededAnalysisToday` + `forceRerun` | P0 0 |
| 深链 | `analysisTaskRoutes` 带 `analysis_fp`；URL 已有 `task_id` 只 hydrate 不 create | 通过 |

自检：`node src/utils/industryAnalysisGate.selfcheck.mjs` → ok。

## 复刻五维 + W4

| 维 | 说明 |
|----|------|
| 布局 | 条件栏 CTA 位置未改，只换文案与加「重新分析」 |
| 交互 | I2-12 门控；全景在脏条件 / 当日成功 / 进行中均可点「开始分析」打开结果或恢复过程 |
| 样式 | 复用现有 `diagnosis-actions` / `panorama-context-actions` |
| 评审 | 未改 `@/review` 挂点 |
| Mock | `USE_MOCK=false` 仍只打 Java；开关开时 mock 按指纹互斥 |
| W4 | 本叶目标，已过自检 |

## 架构合规自检

1. 调用链前端→Java：✅  
2. 算法不在 Java / 前端：✅  
3. Nebula 未改：✅  
4. 可观测：未删既有 hydrate/create 路径：✅  
5. D12 未打 demo 服务：✅  
6. 未 merge demo 仓：✅  

## 偏离

- Demo `b5e6430` 产业页当时可能尚未单独露出「重新分析」；本叶按规程 I2-12 / Q-ANALYSIS-01 补了该按钮。
- Java 若仍「同 type 一条 running」无指纹互斥，前端会拒绝把不同指纹的 reused 任务当当前条件打开（提示「条件不同」）。真源互斥以后端为准，须联调确认。

## 测试结果

- `node src/utils/industryAnalysisGate.selfcheck.mjs` ok
- `node src/utils/industryChainTask.selfcheck.mjs` ok
- `node src/views/industry-center/industryReplicaFix.selfcheck.mjs` ok
- `node src/views/industry-center/industryPanoramaPage.selfcheck.mjs` ok
- `npm run type-check`（vue-tsc）ok

复核后补修：全景当日复用入口、诊断/区域指纹补参数、恢复进行中先 hydrate、切 tab 清指纹、列表按 type 过滤。

2026-08-21 正式链路返修：

- 失败证据：`CHAIN-20260821-003`，trace-id `9da259abf8a5deb0cdafacf243036d02`，`INPUT_OBJECT_INVALID: as_of required`。
- 根因：全景「最新快照」使用空选择值，Create 时遗漏 `as_of`；本地 Mock 未校验而漏检。
- 修复：从 snapshot 的真实日期字段或演进刻度解析 `as_of`；解析不到则前端阻止创建并提示，禁止伪造日期；Mock 明示固定快照日期。
- 返修验证：全景自检、I2-12 门控自检、产业链任务自检、`npm run type-check` 均通过。

## 遗留风险

- 列表接口若 `userId` 为空：门控按「无 userId = 当前用户」匹配。
- Java 若仍按 type 复用进行中任务、无指纹互斥：前端拒绝切换并提示。
- K8s 须对返修提交重新点验。

## CI/CD

- 分支：`dev`
- commit：`cecf1e2`（`lumen-ui-topic` `origin/dev`）
- 返修 commit：`a3302b8`（补齐全景真实 `as_of`）
- pipeline / rollout：随 CI

## 可观测性

- 沿用现有 analysisTask 请求；未新增埋点文件。

## 涉及文件

- `repos/lumen-ui-topic/src/utils/industryAnalysisGate.ts`
- `repos/lumen-ui-topic/src/utils/industryAnalysisGate.selfcheck.mjs`
- `repos/lumen-ui-topic/src/composables/useIndustryAnalysisJob.ts`
- `repos/lumen-ui-topic/src/composables/analysisTaskRoutes.ts`
- `repos/lumen-ui-topic/src/mock/enterprise/analysisTaskStore.ts`
- `repos/lumen-ui-topic/src/views/industry-center/IndustryPanoramaPage.vue`
- `repos/lumen-ui-topic/src/views/industry-center/IndustryDiagnosisPage.vue`
- `repos/lumen-ui-topic/src/views/industry-center/IndustryRegionalPage.vue`
- `repos/lumen-ui-topic/src/views/industry-center/IndustryShenzhenPage.vue`
- `repos/lumen-ui-topic/src/utils/industryWorkspaceRuntime.js`
- `repos/lumen-ui-topic/src/mock/industry/industryApi.ts`
- `repos/lumen-ui-topic/src/views/industry-center/industryPanoramaPage.selfcheck.mjs`

# SYNTH-REVIEW-FIX-JAVA-L01 · SYNTH 三 commit 评审修复（Important I1–I4 + Minor M2/M6）

> 修复对象：SYNTH 三 commit（`0fdc245` / `14e3fd2` / `084b2d1`）评审结论「需修后放行」。本单只修评审点名项，不扩范围。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api`（api-agent） |
| supervised_by | `human:侯佳伟`（后端 Lead；registry 无本单独立条目，挂靠 E8 SYNTH 既有 api-agent 任务族，评审单修复由派单直接授权） |
| claim_type | `pull`（用户 `/goal` 派单直授，修复单） |
| 说明 | registry 查无 `SYNTH-REVIEW-FIX-JAVA-L01` 条目（task-get/task-query 双确认）；按派单原文任务 ID 命名 handoff，未虚构 registry 认领记录 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只修评审点名项：每项取最小 diff（I1 删法大于加法；I2 借 elements 现成模式；I4 直接用仓 formatter）；未用 YAGNI 跳过任何公约要求 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 headroom 环境；纯 Java 本地修复 + 单测，无 K8s/线上操作 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（bugfix 修复单，未新增/修改服务间边；调用链仍为 前端 → Java 门面 → Python `/internal/v1/synth/*`，与 COLLAB/VIT 册既有图一致） |
| 图 diff | 无 |
| 会签态 | N/A |

## 问题清单（评审原文要点）

- **I1** `SynthCollabGraphService` 双传一致性判定缺陷：未解析 meta 就判 `SNAPSHOT_BATCH_MISMATCH`；`snapshotDerivesBatch` 注释与实现矛盾（`task:A|graph:calc_A` 自洽对被误 400）
- **I2** `SynthVitalitySnapshotService` `readBatch`/`latestCalcBatchId` 的 `catch(Exception)` 吞 Python 400
- **I3** `SynthVitalitySnapshotService` snapshotId 直读分支把请求 `weight_profile` 塞进 Python 查询、并无条件覆盖回显
- **I4** `AnalysisTaskServiceImpl.findReusableVitalityTask` 签名与首行挤同一行
- **M2** Collab 测试名 `industryAndDepthTruncationPassedThroughToPython`（depth 参数 v1.0.8 已废）
- **M6** `catch(Exception)` 兜底日志 `ex.getMessage()` 可能为 null

## 修改内容（逐项修法）

### I1 · 图谱双传一致性（`SynthCollabGraphService.java`）

- 选派单给出的后者方案：**校验推迟到 meta 解析后按 `meta.graph_batch_id` 比对**。原前置判定（③ 互斥 400）删除，`resolveBatchBinding` 新增语义：仅显式批（无 snapshotId）才省略 meta 二跳；带 snapshotId（含双传）一律走持久 meta 解析，回读值为权威。
- 主流程新增 ③b：仅双传时比对 `graphBatchId != explicitBatch` → 400 `SNAPSHOT_BATCH_MISMATCH`（带观察日志）；meta 解析不到照旧走 `batch_meta_missing` 空图，**不因双传 400**。
- 删除 `snapshotDerivesBatch`（矛盾注释随删）；类 javadoc 与 `@param gapfillBatchId` 同步新语义。

### I2 · 活力 400 原文透传（`SynthVitalitySnapshotService.java`）

- 对齐 elements 快照门面模式：`readBatch` / `latestCalcBatchId` 均改 `catch (FeignException)`——`status()==400` 且 body 非空 → 原文透传；其余状态落 404 语义（`SNAPSHOT_NOT_FOUND`）；`catch(Exception)` 兜底保留。
- 透传通道：private 嵌套载体 `UpstreamRejectedException(content)`，`batchSnapshot` 两处出口（latest 路由 / readBatch）统一接住转 `R.failed(content)`。

### I3 · 直读分支不传请求档、回显以回读值为权威（`SynthVitalitySnapshotService.java`）

- 直读分支查询**不传** `weight_profile`（以该批冻结档为准）；条件最新批路由才携带归一档。
- 回显按派单选定「回读值覆盖回显」：`weight_profile` 以 Python 回读批档为权威（回读缺失时才以查询档保守补位）；`cache_key` 用回读档组装（直读批档可能与请求档不同）；保留既有断言字段。

### I4 · 格式（`AnalysisTaskServiceImpl.java`）

- 对 async-service-biz 模块跑 `mvn spring-javaformat:apply`；`findReusableVitalityTask` 签名与首行恢复分行（同名同名调用方法均无此问题）。format 波及的同模块 77 个历史漂移文件已全部还原（评审范围外），仅保留点名文件（含同文件内 3 处 formatter 规范化：一处三元链换行、两处 javadoc 重排）。

### M2 / M6

- M2：测试更名 `industryAndDepthTruncationPassedThroughToPython` → `industryPassedThroughToPython`；类 javadoc 同步去 depth。
- M6：`SynthVitalitySnapshotService` 兜底日志与新增 `safeContent` 回落一律 `ex.toString()`（防 getMessage 为 null）。

## 测试结果（全部绿）

| 测试类 | 结果 |
|------|------|
| `SynthCollabGraphServiceTest`（gkxlumen-topic） | **14 run, 0 fail**（含新语义 3 条：mismatch 400 / 自洽对放行 / 双传 meta 缺失空图不 400） |
| `SynthVitalitySnapshotServiceTest`（gkxlumen-topic） | **12 run, 0 fail**（含新增 3 条：直读不传档+回读档回显 / latest 400 透传 / 直读 400 透传） |
| `AnalysisTaskServiceImplVitalityFpGateTest`（async-biz） | **8 run, 0 fail** |
| `gkxlumen-topic` 模块全量 | **33 run, 0 fail**，BUILD SUCCESS |
| `gkxlumen-topic-async-service-biz` 模块全量（-am） | **205 run, 0 fail**，BUILD SUCCESS |

- 单测改动：`snapshotAndBatchMismatchReturn400` 按新语义重写（meta 存在且 `graph_batch_id` 不匹配 → 400）；新增 `snapshotAndMatchingBatchPassesThrough`、`snapshotAndBatchWithMetaMissingReturnsEmptyGraphNot400`、`directReadOmitsRequestProfileAndEchoesBatchFrozenProfile`、`upstream400BodyPassedThroughOnLatestRoute`、`upstream400BodyPassedThroughOnDirectRead`。
- 环境备注：本机默认 JDK 8，测试统一用 `JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-21.jdk` 执行。

## 未修清单（登记，评审认可后续单处理）

| 项 | 内容 | 状态 |
|----|------|------|
| M1 | `WEIGHT_PROFILES` 死常量 | 不修，登记 |
| M3 | elements 批一致性宽松 | 不修，登记 |
| M4 | Adapter 同构抽基类 | 不修，登记 |
| M5 / M7 | 评审 Minor 其余项 | 不修，登记 |

## 遗留风险

- I2 载体异常为包内 private 类，若未来有第二调用方直调 `readBatch`/`latestCalcBatchId` 需自行处理 `UpstreamRejectedException`（当前仅 `batchSnapshot` 一个入口，风险可控）。
- I3 直读回显档位依赖 Python 装包回读 `weight_profile`；若 Python 该字段缺失，回显回落查询档（直读时为归一默认 `INDEX_MAIN`），属诚实降级非伪闭合。
- Collab 双传现在每次必走 meta 二跳（原先显式批可省）；多一次 Python 往返，换取绑定权威一致（评审选定的语义）。

## CI/CD（必填）

- 分支：`dev`（本地领先 origin/dev 1 commit，**未 push**，等人工确认）
- commit：`2552185` `fix(synth): 评审修复——图谱双传一致性/活力400透传/直读profile/格式 [agent:api]`
- pipeline URL / ID：无（未 push，未触发 CI）
- 部署 namespace / 镜像 tag：无
- K8s rollout：未涉及（纯本地修复）
- dev 测试 URL / 命令与结果：`mvn -pl gkxlumen-topic -am test` 与 `mvn -pl gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz -am test` 全绿（见上表）

## 可观测性（建议）

- OTEL_SERVICE_NAME：不变（`gkxlumen-topic` / `gkxlumen-topic-async-service`）
- traceId（dev 抽样）：未部署，无抽样
- Tempo / Loki：无新增；日志增强：Collab 双传 mismatch 观察日志（snapshotId/metaBatch/explicitBatch）、活力 400 透传日志（status/content），沿用既有格式

## 涉及文件

- `gkxlumen-topic/src/main/java/com/topcomm/gkxlumen/topic/service/synth/SynthCollabGraphService.java`（I1）
- `gkxlumen-topic/src/main/java/com/topcomm/gkxlumen/topic/service/synth/SynthVitalitySnapshotService.java`（I2/I3/M6）
- `gkxlumen-topic/src/test/java/com/topcomm/gkxlumen/topic/service/synth/SynthCollabGraphServiceTest.java`（I1 用例重写+2 新增 / M2 更名）
- `gkxlumen-topic/src/test/java/com/topcomm/gkxlumen/topic/service/synth/SynthVitalitySnapshotServiceTest.java`（I2/I3 新增 3 用例）
- `gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz/src/main/java/com/topcomm/gkxlumen/topic/async/service/impl/analysis/AnalysisTaskServiceImpl.java`（I4 格式）

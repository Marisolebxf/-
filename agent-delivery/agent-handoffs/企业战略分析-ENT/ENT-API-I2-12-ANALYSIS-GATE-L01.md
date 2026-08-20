# ENT-API-I2-12-ANALYSIS-GATE-L01 完工 Handoff

## 1. 范围与实现

- 对照：`产品实现规程.md` I2-12 / 附录 E、Q-ANALYSIS-01。
- `enterprise_eval`、`risk_insight`、`talent_recommend` 创建契约新增 `analysis_fp` 与 `force`。
- 三类正式创建请求强制校验 `analysis_fp` 非空且为 64 位小写 SHA-256；旧客户端或漏传请求不再绕过单飞门控。
- `analysis_fp` 写入现有 `analysis_task.target_params`，未新增或修改表结构。
- 复用现有 Redis 实现 `userId + analysisType + analysis_fp` 创建锁；并发创建返回同一运行中任务。
- Redis 指纹锁在显式数据库事务开始前获取，锁竞争等待不再占用事务数据库连接。
- 按 `Asia/Shanghai` 与 `end_time` 复用当天成功任务；`force=true` 只跳过成功复用，不绕过运行中单飞。
- `analysis_fp`、`force` 仅为 Java 任务中心控制字段，不透传 Python。

## 2. 产物

- 功能 commit：[`0425a88`](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/commit/0425a88be0fcf4a76e8212041655ab93bee52aaf)
- CI 夹具修复 commit：[`4e9796e`](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/commit/4e9796e7982e5cdcdec77fa24dcdcb5c3bd8f230)
- `AnalysisTaskCreateRequest.java`
- `AnalysisTaskServiceImpl.java`
- `AnalysisTaskServiceImplFingerprintGateTest.java`
- 已推送 `origin/dev`。

## 3. 验收证据

- JDK 21（`--release 17`）编译通过。
- 使用 Maven Surefire 3.5.4 显式执行 JUnit 5：
  - `Tests run: 8, Failures: 0, Errors: 0, Skipped: 0`
- 覆盖：锁先于事务、缺失/非法指纹、运行中复用、当天成功复用、`force` 重跑、跨日/跨用户隔离、并发单飞、控制字段不下发。
- 前端契约联动测试：分析门控测试 10/10 通过，`vue-tsc --build` 通过。
- 首次 Pipeline [#5354](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5354) 暴露两组既有手工 Service 测试未注入新增 `TransactionTemplate`；已由 `4e9796e` 补齐测试夹具。
- 修复 Pipeline [#5355](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5355)：`backend:build`、`helm:lint`、`backend:image:topic-async-service`、`deploy:topic-async-service` 与 `deploy:topic-chain` 均成功；整条 Pipeline 因无关服务保留手动部署项而显示 manual/running。

## 4. 偏离与限制

- 无 DDL、无 ES 变更。
- 为遵守“不改 POM”，未修改仓内旧 Surefire 配置；本地验收用新版插件显式运行 JUnit 5。
- 当前仍使用客户端传入 `user_id`，沿用现网契约；登录态服务端取用户不在本任务范围。

## 5. 架构合规

- D1 算法只在 Python：✅ Java 仅编排、去重，不实现算法。
- D2 调用链：✅ `lumen-ui-topic → gkxlumen-topic-async-service → lumen-topic-py`。
- D3 NebulaGraph：✅ 未涉及图谱变更。
- D4 可观测性：✅ 沿用现有任务审计与状态链路。
- D5 CI/CD：✅ 目标模块构建、镜像和 K8s dev 发布成功。
- D6 demo 只读：✅ 未合并或调用 demo 服务。
- D7/D8/D9/D10/D11：✅ 本后端契约变更未破坏既有要求。
- D12 正式隔离：✅ 无 `demo-svc-topic-py` 或其他 demo 依赖。

ponytail: full — 复用现有 `target_params`、Redis 与任务表，未引入依赖、DDL 或新服务。

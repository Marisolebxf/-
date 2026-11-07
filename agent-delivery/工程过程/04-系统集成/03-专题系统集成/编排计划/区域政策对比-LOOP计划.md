# 区域政策对比 · LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/区域政策对比-合规演示用例.md`
- 系统：科技专题服务系统。不打开页面。本模块经当次点名纳入，专题其他页不跟着进。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

- 状态：2026-11-07 样本满足。验收单 `TOPIC-POL-REGION-DEMO-ACCEPT-LOOP` 改为 `done`。读 `POLICY-20261107-008`（集成电路，五区五维）；技术领域另读 `POLICY-20261105-026`。`TOPIC-POL-REGION-DEMO-FIX-R20261107-DATA`、`TOPIC-POL-REGION-DEMO-FIX-R20261107-ALGO` 已签收 `done`：粤港澳（除深）源行为 0，结果里的 0 是相对指数，未改库、未改代码。查询单不建。补贴标准、准入条件不派补数。

## 1. 要证明什么

可演行的填好请求，返回用例里写明的字段。不证明某一张历史任务上的条数或分数。历史现场里的「关联政策 15 条，归入对比区域 11 条」「深圳 41.7、长三角 8.3」不作为通过线。

通过线：探测 HTTP 200，且可演行与期望一致。对不上时按 §6.5 分类。原测试任务不标完成。

以下保持现状，不算本 LOOP 的失败，也不为此建子任务：

- 补贴标准、准入条件为空。覆盖表已写 `覆盖不到`，并写明不派补数。
- 综合分不改去读创建体里的 `weights`。权重仍等 `QPOL-02`。
- 不把缺信号的维度写成 0 或 50。

## 2. 验收单

人说「按 LOOP 跑」之后再建，本文件不建。

| 项 | 值 |
|---|---|
| ID | `TOPIC-POL-REGION-DEMO-ACCEPT-LOOP` |
| 类型 | `tech_task` |
| 执行 | `qa-agent` |
| 协作 | `data-agent`、`algorithm-agent`；过滤拣不中再加 `api-agent` |
| 状态 | 建为 `ready`，不认领 |
| 报告 | `agent-delivery/agent-handoffs/政策模块-E7/TOPIC-POL-REGION-DEMO-ACCEPT-LOOP.md` |

样本满足且状态行已回写后，验收单改为 `done`。未满足则留 `ready`。

## 3. 后端调用

token 文件：`%USERPROFILE%\.gkx\topic-loop-token`（一行 access_token，仓库外）。请求头 `Authorization: Bearer`、`systemCode: topic`。不打印、不入库。

验收不新签发任务，不带 `force=true`。

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测 | `POST http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/list`，body `{"user_id":"guest","analysisType":"policy_regional","status":"success","page":1,"size":5}` | 只验 token，并看有没有可复用的成功结果 |
| 样本 | 上表里最新一条成功任务的 `GET .../tasks/{taskId}/result?user_id=guest` | 核可演行的字段。创建条件须能对上用例：`industry_vid=chain:INB1303`，五区，五维 |
| 库 | 只读 `demo_gkxlumenx_dwd.policy_base_info` | 仅在结果全空时核对是否还有可归区的政策行。不写口令 |

列表为空，或没有一条成功任务的条件对得上集成电路五区五维：停止。原因写「没有可复用的已签发结果」。这不是接口映射不存在，也不建子任务，不在验收轮 POST 创建。

探测 401、424，或正文为「访问令牌不存在」「用户凭证已过期」「token expired」：验收单 `blocked`，通知 `human:淮政玮`，不建子任务，不再开一轮。探测路径本身 404：同样停止，原因写「接口映射不存在」。

库只 `SELECT`。不写 ODS、供应方库、`gapfill_`、新 ADS。

## 4. 缺口怎么派

只比较用例里数据情况为 `可演` 的行。每轮最多三张。不改前端。补贴标准、准入条件那一行不派单。

| 类 | 何时 | 执行人 | 计划 ID |
|---|---|---|---|
| DATA | 该产业下没有可归入五区的政策，矩阵全空 | `data-agent` | `TOPIC-POL-REGION-DEMO-FIX-R{YYYYMMDD}-DATA` |
| QUERY | 库内政策在，结果区名、维名或 `industry_vid` 对不上请求 | `api-agent` | `TOPIC-POL-REGION-DEMO-FIX-R{YYYYMMDD}-QUERY` |
| ALGO | 行在且请求键一致，但缺信号被写成 0 或 50，或综合分改去读 `weights` | `algorithm-agent` | `TOPIC-POL-REGION-DEMO-FIX-R{YYYYMMDD}-ALGO` |

同一缺口键连续两轮仍在：停止建单，交给 `human:淮政玮`。

子任务 handoff 落盘后，才把验收单拨回 `ready`。下一轮仍读同一条已签发结果；只有数据或算法子任务明确要求重算时，才另签发，签发号写入该子任务 handoff。验收轮自己不签发。

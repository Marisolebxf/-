# 政策时序分析 · LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/政策时序分析-合规演示用例.md`
- 系统：科技专题服务系统。不打开页面。本模块经当次点名纳入，专题其他页不跟着进。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

- 状态：2026-11-07 两轮，样本满足。验收单 `TOPIC-POL-TS-DEMO-ACCEPT-LOOP` 改为 `done`。产业主样本读 `POLICY-20261106-003`。技术领域按口令签发 `POLICY-20261107-021`（关联产业人工智能 `INB1309`，年，三维全开，无 `industry_vid`），`success`，可演行对上。不建子任务。动态库、季月分桶、政策密度指数名义不派单。

## 1. 要证明什么

可演行的填好请求，返回用例里写明的字段。不证明某一张历史任务上的条数或年份。历史现场里的「已关联 29 条」「发布高峰 2021 年 11 条」「连续性 100%」「有效占比 0%」不作为通过线。

通过线：探测 HTTP 200，且可演行与期望一致。对不上时按 §6.5 分类。原测试任务不标完成。

以下保持现状，不算本 LOOP 的失败，也不为此建子任务：

- 没有动态政策库管理页，对象变更不自动重算。
- 选季或月仍按年分桶。
- 没有名为「政策密度指数」的字段。
- 效力层级为「未标注」。`rank` 为空时这样写是预期。
- 支持强度四维全 0。这是命中计数，不是缺列填成演示分。

## 2. 验收单

人说「按 LOOP 跑」之后再建，本文件不建。

| 项 | 值 |
|---|---|
| ID | `TOPIC-POL-TS-DEMO-ACCEPT-LOOP` |
| 类型 | `tech_task` |
| 执行 | `qa-agent` |
| 协作 | `data-agent`、`algorithm-agent`；过滤拣不中再加 `api-agent` |
| 状态 | 建为 `ready`，不认领 |
| 报告 | `agent-delivery/agent-handoffs/政策模块-E7/TOPIC-POL-TS-DEMO-ACCEPT-LOOP.md` |

样本满足且状态行已回写后，验收单改为 `done`。未满足则留 `ready`。

## 3. 后端调用

token 文件：`%USERPROFILE%\.gkx\topic-loop-token`（一行 access_token，仓库外）。请求头 `Authorization: Bearer`、`systemCode: topic`。不打印、不入库。

验收不新签发任务，不带 `force=true`。

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测 | `POST http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/list`，body `{"user_id":"guest","analysisType":"policy_timeseries","status":"success","page":1,"size":5}` | 只验 token，并看有没有可复用的成功结果 |
| 样本 | 上表里最新一条成功任务的 `GET .../tasks/{taskId}/result?user_id=guest` | 核可演行的字段。创建条件须能对上用例：`industry_vid=chain:INB1303`，`granularity=year`，三维全开 |
| 库 | 只读 `demo_gkxlumenx_dwd.policy_base_info` | 仅在结果全空，或 `rank` 非空却仍全部显示未标注时核对。不写口令 |

列表为空，或没有一条成功任务的条件对得上集成电路、年、三维全开：停止。原因写「没有可复用的已签发结果」。这不是接口映射不存在，也不建子任务，不在验收轮 POST 创建。

探测 401、424，或正文为「访问令牌不存在」「用户凭证已过期」「token expired」：验收单 `blocked`，通知 `human:淮政玮`，不建子任务，不再开一轮。探测路径本身 404：同样停止，原因写「接口映射不存在」。

库只 `SELECT`。不写 ODS、供应方库、`gapfill_`、新 ADS。

## 4. 缺口怎么派

只比较用例里数据情况为 `可演` 的行。每轮最多三张。不改前端。动态库、季月分桶、政策密度指数名义这三行不派单。

| 类 | 何时 | 执行人 | 计划 ID |
|---|---|---|---|
| DATA | 该产业下没有可解析年份的政策，三块趋势全空 | `data-agent` | `TOPIC-POL-TS-DEMO-FIX-R{YYYYMMDD}-DATA` |
| QUERY | 库内政策在，结果缺 `density_trend`、`support_trend`、`level_trend` 或 `key_nodes`，或 `industry_vid` 对不上请求 | `api-agent` | `TOPIC-POL-TS-DEMO-FIX-R{YYYYMMDD}-QUERY` |
| ALGO | 行在且请求键一致，但空年被写成 null，或 `rank` 非空却全部仍是「未标注」，或支持强度把没命中写成演示分 | `algorithm-agent` | `TOPIC-POL-TS-DEMO-FIX-R{YYYYMMDD}-ALGO` |

同一缺口键连续两轮仍在：停止建单，交给 `human:淮政玮`。

子任务 handoff 落盘后，才把验收单拨回 `ready`。下一轮仍读同一条已签发结果；只有数据或算法子任务明确要求重算时，才另签发，签发号写入该子任务 handoff。验收轮自己不签发。

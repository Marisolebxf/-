# 深圳政策现状分析 · LOOP 执行编排计划

- 状态：2026-11-07 监管人裁定。支持力度对上，但扶持档位、落地实效没有结果，不算通过。按缺口建子任务并执行；同一缺口键再出现则停止，交给人。
- 流程：`agent-delivery/产品实现规程.md` §6.5（用例 §6.4，SDD §4.1）。本模块经当次点名纳入，专题其他页不跟着进。
- 系统：科技专题服务系统。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

## 1. 这一轮要证明什么

演示锚点 **集成电路 / `industry_vid=chain:INB1303`** 上，已签发任务的结果仍与 2026-11-07 演示实例一致。用例在 `agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/深圳政策现状分析-合规演示用例.md`。签发实例记在 `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-SZ3D-DATA-DEMO-L01.md`。本计划不代替那份覆盖表。

通过线（都要同时成立）：

| 项 | 预期 |
|---|---|
| 支持力度可算 | 是 |
| 政策条数 | 879 |
| 分数 | 33.5585 |
| 名次 | 5 |
| 层级均值 | 0.4653 |
| 扶持档位 | 要有结果。空值或原因「无金额列」不算通过。没有金额源时不得写成 0 |
| 第 4 章落地实效 | 要可算并有结果。原因「实施日、支持对象、反馈全缺」不算通过。不得把空日期或空对象写成 0 分 |
| 第 5 章 | 深圳在榜时有供给结构，条数与分数同上 |
| 库 | `demo_gkxlumenx_dwd.policy_base_info` 中 `city='深圳市'` 仍是 879。正式库只读，不回写 |

以下保持现状，不算本 LOOP 的失败，也不为此建子任务：

- 第 3 章「未提供链名」。已有缺陷包 `LUMEN-POLICY-SZ3D-E1-DEFECT-C1.md`，本循环不改匹配、不改前端。
- 层级均值用现行 0.4653，不追回 10-25 的 0.4579。
- 无城市名的行不补城市。

`LUMEN-POLICY-SZ3D-DATA-DEMO-L01` 停在 `ready_to_sign`，本计划不把它签 `done`。

## 2. 验收单

确认后新建一张，不占用上面那张数据单。

| 项 | 值 |
|---|---|
| ID | `TOPIC-POL-SZ3D-DEMO-ACCEPT-LOOP` |
| 类型 | `tech_task` |
| 执行 | `qa-agent` |
| 协作 | `data-agent`、`algorithm-agent` |
| 状态 | 建为 `ready`，不认领 |
| 依赖 | `LUMEN-POLICY-SZ3D-DATA-DEMO-L01` 已有 handoff。不要求它先 `done` |
| 报告 | `agent-delivery/agent-handoffs/政策模块-E7/TOPIC-POL-SZ3D-DEMO-ACCEPT-LOOP.md` |

一轮写完退回 `ready`。不签 `done`。

## 3. 后端调用

token 文件：`%USERPROFILE%\.gkx\topic-loop-token`（一行 access_token，仓库外）。请求头 `Authorization: Bearer`、`systemCode: topic`。与展示系统的 token 文件分开。不打印、不入库。

验收不新签发任务，不带 `force=true`。

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测 | `GET http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/POLICY-20261107-004/result` | 只验 token 和这条已签发结果还在不在 |
| 库 | 只读 `demo_gkxlumenx_dwd.policy_base_info` | 核对 `city='深圳市'` 的行数，以及深圳行的 `rank` 仍有值 |

探测 401、424，或正文为「访问令牌不存在」「用户凭证已过期」「token expired」：验收单 `blocked`，通知 `human:淮政玮`，不建子任务，不再开一轮。探测 404：同样停止，原因写「接口映射不存在」或「演示任务结果不可读」，不改成补数。

库只 `SELECT`。不写 ODS、供应方库、`gapfill_`、新 ADS。

## 4. 缺口怎么派

只比较第 1 节那几项。每轮最多两张子任务。不改前端，不改锚点匹配。

| 类 | 何时 | 执行人 | 计划 ID |
|---|---|---|---|
| DATA | 深圳 `city` 不足 879，或 `rank` 空；或扶持档位、落地实效因缺列、空列、零日期而没有结果 | `data-agent` | `TOPIC-POL-SZ3D-DEMO-FIX-R{YYYYMMDD}-DATA` |
| ALGO | 行数仍是 879 且 `rank` 在，分数、名次或层级均值对不上；或源列已有非空值，结果板仍写死不可算 | `algorithm-agent` | `TOPIC-POL-SZ3D-DEMO-FIX-R{YYYYMMDD}-ALGO` |

不建 QUERY 单。链名缺口留在已有缺陷包。档位和落地实效没有结果就是缺口。可算条件写在 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-ALGO.md` 的「调研 2026-11-07」：扶持金额单独成表（`policy_id`、`amount`、`caliber`、`source_clause`），不接招标表；落地实效至少要有真实实施日或非空支持对象，反馈表可以没有。没有这些非空值时不得写成 0。

同一缺口键连续两轮仍在：停止建单，交给 `human:淮政玮`。

子任务 handoff 落盘后，才把验收单拨回 `ready`。下一轮仍读 `POLICY-20261107-004` 的结果；只有数据或算法子任务明确要求重算时，才另签发任务，签发号写入该子任务 handoff，验收单改读新号。验收轮自己不签发。

## 5. 确认后的第一轮顺序

1. 按第 2 节建 `TOPIC-POL-SZ3D-DEMO-ACCEPT-LOOP` 为 `ready`。
2. 认领它，`supervised_by=human:淮政玮`。
3. 读本机 topic token，GET 演示任务结果。
4. 探测失败则停。
5. 探测成功则核对第 1 节的数，并 `SELECT` 深圳行数。
6. 有缺口才建第 4 节的子任务。验收当轮不改库、不重算。
7. 写 handoff 一节。支持力度、档位、落地实效都有结果才算通过，验收单留在 `ready`。档位或落地实效没有结果，就建第 4 节的子任务；没有非空源时子任务停住，不写 0。

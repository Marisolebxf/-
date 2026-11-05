# POL-L2-DS12-EST-API · 政策效果推演 · 效果预估 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| lock_hours | 24 |
| 说明 | 认领已完成，状态为 in_progress。本单只写接口设计分册。不改任务状态，不标 integration，不标 ready_to_sign，不标 done |

## 范围

政策效果推演 · 二级「效果预估」。SRS 序号 232–236。用户故事 `US-DS-POL-06`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写契约仓代码，不写 OpenAPI 字段表、DTO、枚举闭包。

浏览器只打 `/display/v1/policy/**`。全页对外一条：`POST /display/v1/policy/simulation/jobs`。一次请求只带一种类。本分册只定义 232–236 的五种。237–242 的种类留给 `POL-L2-DS12-SIM-API`，本文只交叉引用。五叶都不进异步，不加 `policy_simulate`，不进 `PolicyAnalysisTypes`。

| 序号 | 落点 |
|---|---|
| 232 未出台仿真 | 同一 `jobs`。同步。element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 的未出台仿真行。四类参数至少一类。对不上则该次模拟空 |
| 233 新出台预测 | 同一 `jobs`，另一次请求。同步。同表按已出台政策拣行。不调 `parse/jobs`。候选列表复用已有全景检索，那次检索不代替 `jobs` |
| 234 区域空间 | 同一 `jobs`，另一次请求。同步。同表按区域与政策类型拣行。服务端只回行。对不上不造全国通用行 |
| 235 多维评估 | 同一 `jobs`，另一次请求。同步。element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。`metric_id` 留空。灌数归 `POL-L2-DS12-SIM-GAPFILL-L01`，本分册不改行内容 |
| 236 利益攸关方 | 同一 `jobs`，另一次请求。同步。element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行。请求不插入。`metric_id` 留空。灌数归同一张 SIM 灌数单，本分册不改行内容 |

232–234 的行上 `metric_id` 用已有 `M_POLICY_SIMULATE`。D4 保持 mock。不新造 `metric_id`。`M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT` 不顶替推演。

不用 501 充当这五叶的功能。接口不直接返回写死的 mock。无行则空。失败不清其他种类已经返回的区块。

## 偏离

- DoD「不复用 `/topic/v1/policy`」：浏览器和这五叶的内部委托都不打专题政策 URL，也不调用 `POST /topic/v1/analysis/tasks`，不进 `gkxlumen-topic-async-service`。233 的候选列表复用已有全景检索，不代替 `jobs`。本分册不改全景检索。
- DoD 原文和 `指标与501.md` §3.2 把 232–236 写成 501。契约输入清单把整条 `simulation/jobs` 标成 Job。`POL-L2-DS12-EST-ARCH` 把这五叶改成同步读缺项表。本分册按该架构写空态：无行则空，HTTP 成功，不返回 501。架构第 2 节「真推演」未注册时该种类 501，五叶不走那一行，本分册不新增那个 kind。不回头改 DoD 所在的上游文件，不改 SIM-ARCH。
- 不把整条 `jobs` 改成只读预估表。235、236 各读 SIM 组的一张表。237–242 留给 SIM-API。

## 与架构的对应

上游 `sdd/l2/POL-L2-DS12-EST-ARCH.md` 于 2026-11-04 落盘，2026-11-05 只改第 5.4、5.5 节的库.表写法，读法未改。稿头仍是待会签，本分册不把它写成已会签、已签收。本分册按该稿第 2–5 节写路径和委托，不改架构稿。237–242 只对照 `POL-L2-DS12-SIM-ARCH`，不改那份。

- 232 对应架构 §5.1，写成 `simulation/jobs` 的未出台仿真，同步读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`
- 233 对应架构 §5.2，写成同一 `jobs` 的新出台预测，不调 `parse/jobs`
- 234 对应架构 §5.3，写成同一 `jobs` 的区域空间，服务端只回行
- 235 对应架构 §5.4，写成同一 `jobs` 的多维评估，同步读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。读路径在本分册，行内容与灌数不改
- 236 对应架构 §5.5，写成同一 `jobs` 的利益攸关方，同步读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`，请求不插入。公开 kind 用第 2–4 节的「利益攸关方」；「参与意见」是行内容
- 契约输入清单里 `simulation/jobs` 只作路径对照。清单和指标与 501 里的旧 501 空态不覆盖本读法
- 237–242 以 SIM-ARCH 为准，种类正文留给 `POL-L2-DS12-SIM-API`。本分册不改挂

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-EST-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-EST-API.md`

## 未做

- 未改代码，未改 Python，未改 Java，未写契约仓
- 未建表，未灌数，未写 DDL。`POL-L2-DS12-EST-GAPFILL-L01`、`POL-L2-DS12-EST-DATA`、`POL-L2-DS12-SIM-GAPFILL-L01`、`POL-L2-DS12-SIM-DATA` 不在本单执行
- 未冻结枚举、响应字段名和 DTO
- 未改说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研、EST-ARCH、SIM-ARCH、`FE-POL-03A`
- 未改 235、236 的行内容
- 未新建前端单，未会签
- 未调用 `task-update-status`、`task-claim`、`task-update-fields`
- 未 commit，未 push
- 无业务 CI。定义单不部署

## 验收

- 分册已落盘。一条资源的路径、方法、同步（五叶都不进 Job）、内部委托、空态与 EST-ARCH 一致
- 五个种类：未出台仿真（232）、新出台预测（233）、区域空间（234）、多维评估（235）、利益攸关方（236）
- 232–234 读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。235 读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。236 读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`。库名与表名分开写
- 偏离已写明：501 改为读表；五叶不复用 `/topic/v1/policy`，也不进异步白名单
- 空态是空。不返回 501。接口不直接返回写死的 mock。236 请求不插入
- 只汇入 `BE-POL-CONTRACT-01`。未单独冻结第二份 API-POL。未写实现代码
- 未把整条 jobs 改成只读预估表。未改写 237–242 的种类语义
- 未改本单范围外的文件
- 状态保持 in_progress。待 `human:淮政玮` 签收。本单不进入 integration，不进入 ready_to_sign，不进入 done

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。232–236 由 `gkxlumen-display` 委托 `gkxlumen-element` 只读 `gkxlumenx_gapfill` 的三张 `gapfill_` 表。不进异步，不打 `/topic/v1/policy`。Java 不做 NLP，不写算法 |
| 不直连 | ✅ `gkxlumen-display` 不直连库，不直连 Python，不写 nGQL，不打 `/v1/policy/**`。请求路径不进入 Python |
| D12 | ✅ 不调用 `demo-*`。不嵌算法中台页。不把 `/v1/policy/simulate` 写成展示入口 |
| D14 | ✅ 五叶不新建桶，不写对象存储，前端不直连 RustFS |
| D16 / D18 | ✅ 232–234 只点名 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。235、236 只点名 SIM 组两张已定名的表，灌数不在本单，行内容不改。无行则空。接口不直接返回 mock，不用 501 充当功能。236 请求不插入 |
| D9 | ✅ 不新造 `metric_id`。232–234 沿用 `M_POLICY_SIMULATE`。235、236 的 `metric_id` 留空。不改 D4。不把 mock 写成已上线。布局推荐键不顶替推演 |
| 可观测 | ✅ trace 沿既有展示链，display 往 element 带 traceId。本分册不新设计观测点 |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、种类分发、空态、偏离和内部委托。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS12-EST-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 EST-ARCH 第 2 节 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 本单 | 会签未做。不把本单写成已会签。不标 done |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |
| user_story | `US-DS-POL-06` |

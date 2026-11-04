# POL-L2-DS11-VIZ-API · 政策分析评价 · 政策分析报告可视化呈现 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 认领已完成，状态为 in_progress。本单只写接口设计分册。日期 2026-11-03。不标 done，不标 ready_to_sign |

## 范围

政策分析评价 · 二级「政策分析报告可视化呈现」。SRS 序号 219–222。用户故事 `US-DS-POL-05`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写 OpenAPI 字段表、DTO、枚举闭包。条件字段只写架构第 3 节闭集。

浏览器只打 `/display/v1/policy/**`。本二级不新开路径。

| 序号 | 落点 |
|---|---|
| 219 趋势 | `POST /display/v1/policy/evaluation/jobs`。`kind=趋势`。同步。不建任务。element 只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。无行则图空 |
| 220 分区 | 另一次 `POST evaluation/jobs`。`kind=分区`。同步。不建任务。element 只读 `gapfill_policy_eval_partition`。无行则图空 |
| 221 结构关联 | 不设 `/display/v1/policy` 资源。只消费第 7 项已有子图。挂接可空 |
| 222 模板选用 | `GET /display/v1/policy/evaluation/shells`。`kind=模板选用`。同步。element 只读 `gapfill_policy_eval_template`。不读 `gapfill_policy_eval_shell` |

一次 `jobs` 只一种类。趋势与分区分成两次请求。一次请求不能同时同步填趋势并转发异步。219、220、222 不进 `gkxlumen-topic-async-service`，不调 Python。不用 501 充当功能。接口不直接返回写死的 mock。不写对象存储。

已签收解读键 `policy_focus_ads`、`policy_text_parse` 不改。序号 229 不写成异步。方案种类留给 `POL-L2-DS11-PLAN-API`。

## 偏离

- DoD 与 `指标与501.md` 仍把 219、220、222 写成 501。架构改为查缺项表。本分册按架构写空态：无行则空，HTTP 成功，不返回 501。不回头改指标分册、说明书、WBS、契约输入清单。
- DoD「不复用 `/topic/v1/policy`」：浏览器只打 `/display/v1/policy/**`。本二级的三种类不内部委托 `POST /topic/v1/analysis/tasks`。221 不委托专题 `/graph`。
- 说明书第 11.2 节仍把模板选用写在解读行。本分册按架构读 `gapfill_policy_eval_template`，不读壳表。不改说明书，不改已签收解读分册。

## 与架构的对应

上游 `sdd/l2/POL-L2-DS11-VIZ-ARCH.md` 于 2026-11-03 返工后第二轮经架构、算法、数据、产品同意，待 `human:淮政玮` 签收。本分册按该稿第 2–5 节写路径和委托，不改架构稿。

- 219 对应架构 §5.1，写成 `jobs` 的趋势，同步读 `gapfill_policy_eval_trend`
- 220 对应架构 §5.2，写成另一次 `jobs` 的分区，同步读 `gapfill_policy_eval_partition`
- 221 对应架构 §5.3，不设政策资源
- 222 对应架构 §5.4，写成 `shells` 的模板选用，同步读 `gapfill_policy_eval_template`
- 条件字段对应架构第 3 节闭集：切换只有时间、区域、类别；对象只有地区、行业、目标群体；图种只有柱状、热力；模板图表类型只有趋势、柱状、热力、弦线、关系网；格式只有 PDF、Excel
- 契约输入清单里 `evaluation/jobs`、`evaluation/shells` 只作路径对照。清单和指标与 501 里的旧 501 空态不覆盖本读法

## 种类分界

共享 `jobs`：本分册只有趋势、分区，都是同步读，不建任务。解读已签收的 `policy_focus_ads`、`policy_text_parse` 仍是 Job，本分册不改。方案的方案对照、参数模拟、路径与风险（229）留给 `POL-L2-DS11-PLAN-API`，229 保持方案稿的同步读，不进异步。效能得分不改。

共享 `shells`：本分册只有模板选用，只读 `gapfill_policy_eval_template`。解读的解读条目、多媒体条目仍读 `gapfill_policy_eval_shell`，本分册不改、不读。方案的互动意见、方案报告留给 `POL-L2-DS11-PLAN-API`。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-VIZ-API.md`

## 未做

- 未改代码，未改 Python，未改 Java
- 未建表，未灌数，未写 DDL。`POL-L2-DS11-VIZ-DATA` 与 `POL-L2-DS11-VIZ-GAPFILL-L01` 不在本单执行
- 未冻结枚举、响应列名和 DTO
- 未改说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研、READ、PLAN、架构稿、`FE-POL-02A`
- 未新建前端单，未会签
- 未 commit，未 push
- 无业务 CI。定义单不部署
- 不标 done，不标 ready_to_sign

## 验收

- 分册已落盘。219、220、222 的路径、方法、种类、同步读、空态与架构一致。221 无政策资源
- 趋势与分区分属两次 `jobs`。一次请求不能同时同步填趋势并转发异步
- 偏离已写明：501 改为读表空态；模板选用不读壳表
- 空态是空。不返回 501。接口不直接返回写死的 mock。不写对象存储
- 未改本单范围外的文件
- 待会签。状态进入 integration 后停下。不进入 ready_to_sign，不进入 done

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。219、220、222 由 `gkxlumen-display` 转 `gkxlumen-element` 只读缺项表。不进 `gkxlumen-topic-async-service`，不调 Python。Java 不算法 |
| 不直连 | ✅ `gkxlumen-display` 不直连库，不直连 Python，不写 nGQL，不打 `/v1/policy/**` |
| D12 | ✅ 不调用 `demo-*`。不嵌算法中台页。221 不把专题 `/graph` 或中台 `/v1/policy/graph` 写成浏览器地址 |
| D14 | ✅ 222 从当次读到的行生成 PDF 或 Excel。不写对象存储，不新建桶，前端不直连 RustFS |
| D16 / D18 | ✅ 219、220、222 只点名三张 `gapfill_` 表，建表灌数不在本单。221 不建表。无行则空。接口不直接返回 mock，不用 501 充当功能 |
| D9 | ✅ 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不改 219、220、222 在指标分册里的无模型判定文字 |
| 可观测 | ✅ trace 沿既有展示链，display 往 element 带 traceId。本分册不新设计观测点，这三支不进异步任务链 |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、种类分界、空态、偏离和条件闭集。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-VIZ-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 VIZ-ARCH 第 2 节 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 本单 | 会签未做。不把本单写成已会签。不标 done |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |
| user_story | `US-DS-POL-05` |

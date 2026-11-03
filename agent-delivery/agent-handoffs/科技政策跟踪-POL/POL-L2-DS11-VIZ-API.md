# POL-L2-DS11-VIZ-API · 政策分析评价 · 政策分析报告可视化呈现 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 认领已完成，状态保持 in_progress。本单只写接口设计分册。不改注册表，不标 done |

## 范围

政策分析评价 · 二级「政策分析报告可视化呈现」。SRS 序号 219–222。用户故事 `US-DS-POL-05`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写 OpenAPI 字段表、DTO、枚举闭包。不新开资源。

浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 不直连 Python，不直连库，不写算法，不写 nGQL。不把 `/topic/v1/policy`、`/topic/v1/policy/graph` 或 `/v1/policy/**` 写成对外入口。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是本页路径。

| 序号 | 落点 |
|---|---|
| 219 | `POST evaluation/jobs` 的趋势段。同步，不是 Job。只要趋势时不建任务，不转发异步服务，不调 Python。element 只读 `gapfill_policy_eval_trend`。无行则图空 |
| 220 | 同一条 `POST evaluation/jobs` 的分区段。同步，不是 Job。同样不建任务。element 只读 `gapfill_policy_eval_partition`。无行则图空 |
| 221 | 不设 `/display/v1/policy` 资源。不是 Job。只消费第 7 项已有子图。不委托专题 `/graph`。Java 不写 nGQL。无子图则空 |
| 222 | `GET evaluation/shells`。同步，不是 Job。只读 `gapfill_policy_eval_shell` 的模板选用行。解读灌数单不灌模板选用。无选用行则模板区空。要文件只从当次读到的行生成。不灌 PDF、Excel、假日志 |

`counts` 不归本叶。序号 223–231 不进本分册。四叶无行或无子图则空，不写死 mock，不用 501 充当画面。

## 与架构的对应

上游 `sdd/l2/POL-L2-DS11-VIZ-ARCH.md` 按本单派令已签收。会签页 `sdd/l2/会签/POL-L2-DS11-VIZ-SIGNOFF-ARCH.md` 复会签结论为同意。本分册按该稿写路径和委托，不改架构稿，不改会签页。

- 219 对应架构 §2、§5.1：`POST evaluation/jobs` 趋势段。只要趋势时不建任务，不转发异步服务，不调 Python。element 只读 `gapfill_policy_eval_trend`。无行则图空
- 220 对应架构 §2、§5.2：同一条 POST 的分区段。同样不建任务。element 只读 `gapfill_policy_eval_partition`。无行则图空
- 221 对应架构 §2、§5.3：不设 `/display/v1/policy` 资源。只消费第 7 项已有子图。不委托专题 `/graph`。Java 不写 nGQL。无子图则空
- 222 对应架构 §2、§5.4：`GET evaluation/shells`。只读壳表的模板选用行。解读灌数单不灌模板选用。无选用行则模板区空。要文件只从当次读到的行生成。不灌 PDF、Excel、假日志
- 会签页：219、220 是同步读，没有写成已创建的 Job。221 不设资源。222 的空态保留，灌入方不指给解读灌数单
- `counts` 不归本叶。223–231 不进本分册
- 契约输入清单里上述资源行只作路径对照。清单里的 501 列不覆盖签收读法：无行或无子图则空

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-VIZ-API.md`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 调用链 | 浏览器只打 `/display/v1/policy/**`。219、220、222 由 `gkxlumen-element` 只读。221 只消费第 7 项已有子图，不新开查图 |
| 不直连 Python | `gkxlumen-display` 不直连 Python，不直连库。219、220 只要趋势或只要分区时不转发异步服务，不调 Python。Java 不写 nGQL |
| D12 | 不调用 `demo-*` 服务。不把 `/v1/policy/**` 或专题 `/graph` 写成展示入口 |
| D14 | 222 不灌 PDF、Excel，不写对象存储，前端不直连 RustFS |
| D18 | 219、220 只读 gapfill 表。221 无子图则空。222 只读壳表选用行，文件只从当次读到的行生成。接口不直接返回写死 mock。不用 501 充当这四叶的画面 |
| 不改 D4 | 不新造 `metric_id`。不改指标分册里 219、220、222 的「无模型」字样。不把灌数写成已上线 |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、空态、element 只读、趋势和分区不建任务、221 只消费子图、模板选用不进解读灌数单，以及与 `counts`、223–231 的边界。

## 会签态

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-VIZ-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 VIZ-ARCH 第 2 节（219、220 进 element 读缺项表，不进异步任务；221 只消费第 7 项子图；222 读壳表模板选用） |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 本单 | 未会签。不写会签通过。不标 done |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |

定义单未跑控制台分项。cost 未计。`cost_warn` 记 green。

## 未改动

- 未改 WBS、说明书、契约输入清单、调用链与边界、指标与 501
- 未改 VIZ-ARCH、会签页及任何兄弟分册
- 未调 task-registry，未改 `task-registry.yaml`，未改任务状态
- 未写业务代码，未另建 API-POL，未新开资源

# POL-L2-DS12-SIM-API · 政策效果推演 · 科技政策推演 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 已认领，本单不改 |
| 说明 | 任务已处于 in_progress。本单只写接口设计分册。不改任务状态，不标 done，不标 ready_to_sign |

## 范围

政策效果推演 · 二级「科技政策推演」。SRS 序号 237–242。用户故事 `US-DS-POL-06`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写 OpenAPI 字段表、DTO、枚举闭包。

浏览器只打 `/display/v1/policy/**`。不新建作业入口。与效果预估共用已有 `POST /display/v1/policy/simulation/jobs`，一次请求只带一种类。本分册只定义推演侧种类。232–236 交给 `POL-L2-DS12-EST-API`。禁止 `/topic/v1/policy`，禁止第二个分发器，禁止另开 API-POL，禁止新建 Python simulate job。

| 序号 | 落点 |
|---|---|
| 237 文本解析 | 同一 `simulation/jobs`，种类为文本解析。同步读已有 `ads.policy_text_parse` 的解析行。不是作业。请求路径不调用 `polan.text.parse.run`。不灌 gapfill |
| 238 重点可视化 | 同一 `jobs`，另一次请求。同步读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点行。不是作业 |
| 239 影响范围 | 同一 `jobs`，另一次请求。同步读同一张表的影响范围行，跟随该政策的推演上下文。不是作业 |
| 240 政策关联分析 | 无 HTTP 资源。消费已有第 7 项政策子图。不新建接口。Java 不写 nGQL |
| 241 路径预测 | 同一 `jobs`，另一次请求。同步读同一张表的路径环节行。不是作业 |
| 242 解读报告 | 同一 `jobs`，另一次请求。同步读同一张表的解读段落行。不是作业。不产生 PDF、Word 文件 |

调用链：浏览器 → `/display/v1/policy/**` → `gkxlumen-display` → `gkxlumen-element` 读 gapfill 或已有 ADS。Java 不做 NLP，不写 nGQL，不调 `demo-*`。

不用 501 充当功能。接口不直接返回写死的 mock。无行则空。D4 保持 mock。不新造 `metric_id`。失败不清空其他种类已经返回的区块。

235 多维评估行、236 参与意见行的灌数仍归 `POL-L2-DS12-SIM-GAPFILL-L01`（架构第 7、9 节）。读法和种类定义在 EST 半区。本分册不写这两个种类。

## 偏离

- DoD 完成标准写「501 空态」。`task-get` 的 DoD 正文没有「237/242 按 501」或「灌文本解析」。`指标与501.md` 与说明书仍把 237–242 写成 501。`POL-L2-DS12-SIM-ARCH` 把五次读取改成同步读表，240 不设资源。本分册按该架构写空态：无行则空，HTTP 成功，不返回 501。不回头改 DoD 所在注册表，不改指标与 501、说明书、EST-ARCH。
- 说明书 11.2 把文本解析列入 SIM 组要灌清单。架构第 9 节收窄：237 不灌 gapfill，同步读已有 `ads.policy_text_parse`。请求路径不调用 `polan.text.parse.run`。
- 不新建作业入口。237 虽走名为 jobs 的资源，处理是同步读，不是作业。232–236 不在本分册定义。不把整条 `simulation/jobs` 改成只读推演结果表。

## 与架构的对应

上游 `sdd/l2/POL-L2-DS12-SIM-ARCH.md` 为工作区当前稿。稿头仍写待四角色会签。2026-11-05 第 7、9 节已写明两张表和 235/236 灌数归属，读法未改。本分册按该稿第 2–5 节写路径和委托，不改架构稿。共用入口只对照 `POL-L2-DS12-EST-ARCH`：232–236 不属于本分册。不改 EST-ARCH。

- 237 对应架构 §5.1，写成 `simulation/jobs` 的文本解析，同步读 `ads.policy_text_parse`，不是作业，请求不跑解析，不灌 gapfill
- 238 对应架构 §5.2，写成同一 `jobs` 的重点可视化，同步读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点行
- 239 对应架构 §5.3，写成同一 `jobs` 的影响范围，同步读同一张表的影响范围行
- 240 对应架构 §5.6，无 HTTP 资源，消费已有第 7 项读图
- 241 对应架构 §5.4，写成同一 `jobs` 的路径预测，同步读同一张表的路径环节行
- 242 对应架构 §5.5，写成同一 `jobs` 的解读报告，同步读同一张表的解读段落行，不产生 PDF、Word
- 架构 §1.4、§8：真模型注册后对应能力可切异步真算，对外 URL 仍是这一条 `simulation/jobs`。注册不在本分册。当前五次读取保持同步读
- 235、236 的灌数归属对应架构第 7、9 节。种类与读法留给 EST-API / EST-ARCH。本分册不改挂
- 契约输入清单里 `simulation/jobs` 只作路径对照。清单和指标与 501 里的旧 501 空态不覆盖本读法

与架构稿的差异：无。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-SIM-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-SIM-API.md`

## 未做

- 未改代码，未改 Python，未改 Java
- 未建表，未灌数，未写 DDL。`POL-L2-DS12-SIM-GAPFILL-L01`、`POL-L2-DS12-SIM-DATA`、`POL-L2-DS12-EST-API` 不在本单执行
- 未冻结枚举、响应字段名、种类字段名和 DTO
- 未改说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研、SIM-ARCH、EST-ARCH、`FE-POL-03A`
- 未新建前端单，未会签
- 未改任务状态
- 未 commit，未 push
- 无业务 CI。定义单不部署

## 验收

- 分册已落盘。共用 `simulation/jobs` 的路径、方法、同步读（237、238、239、241、242 都不是作业）、240 无资源、内部委托、空态与 SIM-ARCH 一致
- 六个序号：文本解析（237，读）、重点可视化（238，读）、影响范围（239，读）、政策关联分析（240，无资源）、路径预测（241，读）、解读报告（242，读）
- 偏离已写明：旧「501 空态」收窄为无行则空；237 不灌文本解析；不新建作业入口
- 空态是空。不返回 501。接口不直接返回写死的 mock。242 不产生 PDF、Word，不写对象存储
- 232–236 未写入本分册的种类定义
- 未改本单范围外的文件
- 状态保持 in_progress。本单不改状态，不进入 ready_to_sign，不进入 done

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。237 由 `gkxlumen-display` 委托 `gkxlumen-element` 只读 `ads.policy_text_parse`。238、239、241、242 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。240 无新接口。不进异步，不打 `/topic/v1/policy`。Java 不做 NLP |
| 不直连 | ✅ `gkxlumen-display` 不直连库，不直连 Python，不写 nGQL，不打 `/v1/policy/**` |
| D12 | ✅ 不调用 `demo-*`。不嵌算法中台页。不把 `/v1/policy/text/parse` 写成展示路径 |
| D14 | ✅ 242 不产生 PDF、Word，不新建桶，不写对象存储，前端不直连 RustFS |
| D16 / D18 | ✅ 238、239、241、242 只点名 `gkxlumenx_gapfill.gapfill_policy_sim_result`。237 读已有 ADS，不灌 gapfill。240 消费已有图谱。无行则空。接口不直接返回 mock，不用 501 充当功能 |
| D9 | ✅ 不新造 `metric_id`。237 沿用 `M_POLICY_TEXT_PARSE`。240 沿用 `M_POLICY_RELATION_DEGREE`。不改 D4。不把 mock 写成已上线。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿保持 blocked |
| 可观测 | ✅ trace 沿既有展示链，display 往 element 带 traceId。本分册不新设计观测点 |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、种类分发、空态、偏离和内部委托。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS12-SIM-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 SIM-ARCH 第 2 节 |
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

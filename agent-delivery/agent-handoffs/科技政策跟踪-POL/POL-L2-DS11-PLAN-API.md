# POL-L2-DS11-PLAN-API · 政策分析评价 · 推荐方案报告交互展示 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| lock_hours | 4 |
| 说明 | 认领已完成，状态经 claimed 进入 in_progress。本单只写接口设计分册。不标 done，不标 ready_to_sign |

## 范围

政策分析评价 · 二级「推荐方案报告交互展示」。SRS 序号 227–231。用户故事 `US-DS-POL-05`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写 OpenAPI 字段表、DTO、枚举闭包。

浏览器只打 `/display/v1/policy/**`。本二级对外两条：`POST evaluation/jobs`、`GET evaluation/shells`。一次请求只带一种类。五叶都不进异步，不加 `policy_scheme`，不进 `PolicyAnalysisTypes`。都读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。不把整条 jobs 或 shells 改成只读这张表。

| 序号 | 落点 |
|---|---|
| 227 方案对照 | `POST evaluation/jobs`。同步。element 只读方案表的方案对照行。少于两行则对比空 |
| 228 参数模拟 | 同一 `jobs`，另一次请求。同步。按方案和参数档拣行。对不上则预览空。请求内不重算，不调用 `polan.text.simulate` |
| 229 路径与风险 | 同一 `jobs`，另一次请求。同步。按方案拣路径节点和风险。不读图。`metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015` |
| 230 互动意见 | `GET evaluation/shells`。同步。只读意见行。请求不插入。不读壳表，不读模板表 |
| 231 方案报告 | 同一 `shells`，另一次请求。同步。从方案对照行和意见行生成导出内容。不灌文件，不写对象存储。不读壳表，不读模板表。231 不单独占行种类 |

趋势、分区、模板选用留给可视化。焦点、摘要留给解读。异步键只有解读分册的 `policy_focus_ads`、`policy_text_parse`。

不用 501 充当功能。接口不直接返回写死的 mock。无行则空。失败不清空已经返回的 counts 和其他种类。

## 偏离

- DoD「不复用 `/topic/v1/policy`」：浏览器和这五叶的内部委托都不打专题政策 URL，也不调用 `POST /topic/v1/analysis/tasks`。焦点、摘要的内部委托留给解读分册，本分册不改。
- DoD 原文和 `指标与501.md` 把 227–231 写成 501。契约输入清单把整条 `evaluation/jobs` 标成 Job。`POL-L2-DS11-PLAN-ARCH` 把这五叶改成同步读 `gapfill_policy_eval_scheme`。本分册按该架构写空态：无行则空，HTTP 成功，不返回 501。不回头改 DoD 所在的上游文件，不改 VIZ、READ。
- 不把整条 `jobs` 或整条 `shells` 改成只读方案表。

## 与架构的对应

上游 `sdd/l2/POL-L2-DS11-PLAN-ARCH.md` 于 2026-11-03 经架构、算法、数据、产品四角色同意，待 `human:淮政玮` 签收。本分册按该稿第 2–5 节写路径和委托，不改架构稿。边界只对照 `POL-L2-DS11-VIZ-ARCH` 与 `POL-L2-DS11-READ-ARCH`，不改这两份。

- 227 对应架构 §5.1，写成 `evaluation/jobs` 的方案对照，同步读方案表
- 228 对应架构 §5.2，写成同一 `jobs` 的参数模拟，按方案和参数档查，请求内不重算
- 229 对应架构 §5.3，写成同一 `jobs` 的路径与风险，不读图
- 230 对应架构 §5.4，写成 `evaluation/shells` 的互动意见，请求不插入
- 231 对应架构 §5.5，写成同一 `shells` 的方案报告，从方案行和意见行生成，不灌文件
- 契约输入清单里上述资源行只作路径对照。清单和指标与 501 里的旧 501 空态不覆盖本读法
- 趋势、分区、模板选用以 VIZ-ARCH 为准。焦点、摘要以 READ-ARCH 为准。本分册不改挂

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-PLAN-API.md`

## 未做

- 未改代码，未改 Python，未改 Java
- 未建表，未灌数，未写 DDL。`POL-L2-DS11-PLAN-GAPFILL-L01` 与 `POL-L2-DS11-PLAN-DATA` 不在本单执行
- 未冻结枚举、响应字段名和 DTO
- 未改说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研、VIZ、READ、PLAN-ARCH、`FE-POL-02A`
- 未新建前端单，未会签
- 未 commit，未 push
- 无业务 CI。定义单不部署

## 验收

- 分册已落盘。两条资源的路径、方法、同步（五叶都不进 Job）、内部委托、空态与 PLAN-ARCH 一致
- 五个种类：方案对照（227）、参数模拟（228）、路径与风险（229）、互动意见（230）、方案报告（231）
- 偏离已写明：501 改为读表；五叶不复用 `/topic/v1/policy`，也不进异步白名单
- 空态是空。不返回 501。接口不直接返回写死的 mock。230 请求不插入。231 不灌文件、不写对象存储
- 未把整条 jobs 或 shells 改成只读方案表
- 未改本单范围外的文件
- 待 `human:淮政玮` 签收。状态停在 integration，不进入 ready_to_sign，不进入 done

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。227–231 由 `gkxlumen-display` 委托 `gkxlumen-element` 只读 `gapfill_policy_eval_scheme`。不进异步，不打 `/topic/v1/policy`。Java 不算法 |
| 不直连 | ✅ `gkxlumen-display` 不直连库，不直连 Python，不写 nGQL，不打 `/v1/policy/**` |
| D12 | ✅ 不调用 `demo-*`。不嵌算法中台页。不把 `policyData.js` 迁进接口 |
| D14 | ✅ 231 不灌文件，不新建桶，不写对象存储，前端不直连 RustFS。响应不内嵌写死的 PDF、Word、Excel |
| D16 / D18 | ✅ 五叶只点名 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。建表灌数不在本单。无行则空。接口不直接返回 mock，不用 501 充当功能。230 请求不插入 |
| D9 | ✅ 不新造 `metric_id`。229 沿用 `M_POLICY_DS_11_POLICY_EVAL_015`。不改 D4。不把 mock 写成已上线。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿保持 blocked |
| 可观测 | ✅ trace 沿既有展示链，display 往 element 带 traceId。本分册不新设计观测点 |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、种类分发、空态、偏离和内部委托。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-PLAN-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 PLAN-ARCH 第 2 节 |
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

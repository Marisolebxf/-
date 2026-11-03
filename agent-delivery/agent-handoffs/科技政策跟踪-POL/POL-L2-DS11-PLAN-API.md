# POL-L2-DS11-PLAN-API · 政策分析评价 · 推荐方案报告交互展示 · 后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| 说明 | 认领已完成，状态保持 in_progress。本单只写接口设计分册。不改注册表，不标 done |

## 范围

政策分析评价 · 二级「推荐方案报告交互展示」。SRS 序号 227–231。用户故事 `US-DS-POL-05`。

本分册是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不写实现代码，不写 OpenAPI 字段表、DTO、枚举闭包、格式名。不新开资源。

浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 不直连 Python，不直连库。五叶都不进 `gkxlumen-topic-async-service`，不加 `policy_scheme`，不调用 `polan.text.simulate`。DoD「不复用 `/topic/v1/policy`」指浏览器不改打专题政策 URL。不把 `/topic/v1/policy` 或 `/v1/policy/**` 写成对外入口。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单。

| 序号 | 落点 | 是不是 Job |
|---|---|---|
| 227 | `POST /display/v1/policy/evaluation/jobs`。种类为方案对照。element 只读 `gapfill_policy_eval_scheme` 的方案对照行。请求内不重算。对不上或少于两行则对比空 | 否。同步 |
| 228 | 同一条 `POST evaluation/jobs`。种类为参数模拟。同一张表按方案和参数档拣行。请求内不重算。对不上则该块空 | 否。同步 |
| 229 | 同一条 `POST evaluation/jobs`。种类为路径与风险。同一张表按方案拣行。请求内不重算。对不上则该块空 | 否。同步 |
| 230 | `GET /display/v1/policy/evaluation/shells`。只读同一张表的意见行。请求不插入新意见。无行则列表空 | 否。同步 |
| 231 | 同一条 `GET evaluation/shells`。只读同一张表的正文行和意见行。从当次读到的行生成文件。不灌导出文件。没有正文行则导出空 | 否。同步 |

正文行就是方案对照行。230、231 不读参数模拟行，不读路径与风险行。五叶无行或对不上则该块空，不写死 mock，不用 501 充当画面。序号 219–226 不进本分册。

## 与架构的对应

上游 `sdd/l2/POL-L2-DS11-PLAN-ARCH.md` 按本单派令已签收。会签页 `sdd/l2/会签/POL-L2-DS11-PLAN-SIGNOFF-ARCH.md` 同意。本分册按该稿写路径和委托，不改架构稿，不改会签页。

- 227 对应架构 §5.1：`POST evaluation/jobs`，种类为方案对照，element 只读 `gapfill_policy_eval_scheme`。少于两行则对比空。同步，不是 Job
- 228 对应架构 §5.2：同一条 `jobs`，种类为参数模拟，按方案和参数档拣行。请求内不重算。对不上则该块空。不调用 `polan.text.simulate`
- 229 对应架构 §5.3：同一条 `jobs`，种类为路径与风险。`metric_id` 沿用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。不读图。对不上则该块空
- 230 对应架构 §5.4：`GET evaluation/shells`，只读意见行。请求不插入新意见
- 231 对应架构 §5.5：同一条 `shells`，读正文行和意见行，从当次读到的行生成文件。不灌导出文件。不单独占种类
- 会签页：五叶不进异步任务，不加 `policy_scheme`。浏览器只打 `/display/v1/policy/**`。display 不直连 Python，不直连库
- 219–226 不进本分册。`counts` 上的短板条数和机遇条数不读、不改
- 契约输入清单里上述资源行只作路径对照。清单里的 Job 和 501 列不覆盖签收读法：对不上或无行则空
- 指标分册把五叶三档保持为 501。那是指标身份。接口不返回 501，无行则空。本分册不改指标分册

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-PLAN-API.md`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 调用链 | 浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 委托 `gkxlumen-element` 只读 `gapfill_policy_eval_scheme`。五叶不进 `gkxlumen-topic-async-service` |
| 不直连 Python | `gkxlumen-display` 不直连 Python，不直连库，不打 `/v1/policy/**`，不调用 `polan.text.simulate`。Java 不生成方案，不按弹性公式现算，不写 nGQL |
| D12 | 不调用 `demo-*` 服务。不把展示原型的本地方案数组迁进接口。算法中台效果推演页不是这五叶 |
| D14 | 231 不灌导出文件，不写对象存储，前端不直连 RustFS |
| D18 | 五叶只读一张 gapfill 表。接口不直接返回写死 mock。对不上或无行则该块空。不用 501 充当这五叶的画面 |
| 不改 D4 | 不新造 `metric_id`。229 沿用 `M_POLICY_DS_11_POLICY_EVAL_015`，D4 保持 mock。不加 `policy_scheme` |

## ponytail

ponytail: off

定义任务。未用 YAGNI 删掉调用链、空态、element 只读、五叶不进异步任务，以及与 219–226、推演键、501 的边界。

## 会签态

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-PLAN-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用 PLAN-ARCH 第 2 节（227–229 走 element 读 `jobs`，230–231 走 element 读 `shells`，都不进异步任务） |
| 会签态 | 架构图源文件无 frontmatter，记 `draft`。架构会签页已同意。本接口分册未会签 |
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
- 未改 PLAN-ARCH、会签页及任何兄弟分册
- 未调 task-registry，未改 `task-registry.yaml`，未改任务状态
- 未写业务代码，未另建 API-POL，未新开资源

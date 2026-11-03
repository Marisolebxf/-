# POL-L2-DS10-TREND-API · 科创政策全景政策动向后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 任务已是 in_progress。本单只写接口设计。不改注册表，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、空列表与 501 的差别、204 的内部委托，以及缺项表只读这条边界。

## Headroom

| 字段 | 值 |
|---|---|
| headroom | `skip` |
| 说明 | 定义文档，本单未调用 headroom |

## 范围

科创政策全景 · 二级「政策动向跟踪」。只覆盖 SRS 序号 203–206，用户故事 `US-DS-POL-02`。

浏览器只打 `/display/v1/policy/**`。本分册只写路径、方法、同步还是读表、空态。

| 序号 | 公开资源 | 读法 | 空态 |
|---|---|---|---|
| 203 | `GET /display/v1/policy/panorama/ingest` | 同步。display → `gkxlumen-element` → 已有 ADS。不抓取。详情复用已有 `{id}/detail` | 无入库行则空列表 |
| 204 | `GET /display/v1/policy/panorama/subscriptions` | display 只委托 `gkxlumen-topic-policy`。不手写订阅，不建缺项表，不灌假订阅。不是收藏，不进 `jobs`。实现单 `E-E7-POLICY-M1-L11` / `L12` / `L13`，本分册不认领 | 没有订阅则空列表 |
| 205 趋势；206 时间、地域 | `GET /display/v1/policy/panorama/stats` | 同步。读已有 `M_POLICY_TIMESERIES` 与 `M_POLICY_NATIONAL_DIST` 所在表。不另建查询。不往 ADS 写 mock 点，不改灌 `gapfill_policy_qry_stat` | 无行则图空，不造 0 |
| 206 主题分布 | 仍是 `stats` 上的一维 | element 读 `gapfill_policy_theme_dist`。display 不生成主题桶 | 无行则该维空 |
| 205 热点、影响、深度报告 | `POST /display/v1/policy/panorama/jobs` | 读表。不进 Python，不进 `gkxlumen-topic-async-service`。element 读 `gapfill_policy_trend_hotspot`、`gapfill_policy_trend_impact`、`gapfill_policy_trend_report` | 无行则该块空 |

读失败只让对应块空，不清空已经返回的时序、地域和入库列表。切筛选不自动起任务。

本分册是 `BE-POL-CONTRACT-01` 的输入。不另冻结第二份 API-POL。不写 OpenAPI 字段闭包、响应体、枚举、DTO。不写实现代码。

## 偏离

原 DoD「501 空态」按已签收架构解释：空是空列表或空图，不是 501。禁止用 501 充当功能，禁止接口直接返回 mock。

原 DoD「不复用 `/topic/v1/policy`」按已签收架构解释：浏览器不改打专题 URL，仍只打 `/display/v1/policy/**`。`stats` 沿用检索叶已写的内部委托，本分册不另建查询。204 的内部委托不把 `E-E7-POLICY-M1-L06` 改成展示联调单。

## 产物路径

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-TREND-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-TREND-API.md`

## 问题清单

- 204 的门面实现在 `E-E7-POLICY-M1-L11` / `L12` / `L13`。本分册不认领，不冻结子路径。
- 四张缺项表的列在 `POL-L2-DS10-TREND-DATA`，灌数在 `POL-L2-DS10-TREND-GAPFILL-L01`。本分册不执行。表无行时对应块空。
- QPOL-07 未闭合。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。D4 仍是 mock。本分册不改口径，不改绿。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS10-TREND-API.md`
- 新增本 handoff

## 测试结果

定义文档，无运行测试，无业务代码。分册路径、方法、同步或读表、空态与已签收架构稿第 2、4、7 节及说明书第 11.1 节动向一行一致。未把 501 写成这几块的功能。

## 遗留风险

门面入口未接上时，展示侧不得用手写订阅顶上，也不得改判 501；订阅能力仍等 L11–L13。缺项表在灌数之前，热点、影响、深度报告和主题分布是空块。时序和地域在闸门解开前，读到的仍是 mock 行，D4 不因此改绿。

## CI/CD

- 分支：未提交
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无。定义文档，父会话收口后再提交

## 可观测性

- OTEL_SERVICE_NAME：沿既有 `gkxlumen-display` 展示链，本分册不新服务名
- traceId（dev 抽样）：无。本单无请求
- Tempo / Loki：无本次抽样
- `stats`、`ingest`、缺项表读取和 204 的委托沿既有链带 traceId。不新设计观测点

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-TREND-API.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-TREND-API.md`

## 验收证据

两份文档已落盘。203 的同步读表、204 的委托与空列表、205/206 的 `stats` 读已有表、主题维读缺项表、热点三项经 `jobs` 读缺项表，以及读失败只空对应块，都写在接口分册。定义单，无业务代码，无 PR。未 commit，未 push。不标 done。不写会签结论。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本分册不写算法。热点、影响、深度报告不进 Python；mock 行由既有灌数单写入缺项表，Java 只读 |
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。203 经 element 读已有 ADS。204 只在服务内部委托专题门面。`jobs` 这三项不进 `gkxlumen-topic-async-service` |
| 图谱 | ✅ 本分册不读图，不写 nGQL |
| 可观测 | ✅ trace 沿既有展示链。不新设计观测点 |
| CI/CD | ✅ 定义文档未提交。未 force。父会话收口 |
| D12 | ✅ 不调用 demo 服务，不把 demo 门面写成契约 |
| D9 | ✅ 不新造 metric_id，不改 D4，不把 mock 写成已上线，不闭合 QPOL-07 |
| D14 | ✅ 深度报告正文在 `gapfill_policy_trend_report` 的表行里。本分册不写对象存储 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

无控制台分项。按同级定义单 `estimated_tokens` 8000、api-agent 80/20、B 档 `$3/$15` 回填：`8000×0.80×3/1e6 + 8000×0.20×15/1e6 = 0.043`，记 `0.04`。父会话写入注册表。本单不改注册表。

## 未做

- 不写实现代码，不改 Java、Python、前端仓
- 不灌数，不建表，不执行 `POL-L2-DS10-TREND-GAPFILL-L01`
- 不改 D4，不新造 `metric_id`
- 不认领 `E-E7-POLICY-M1-L11` / `L12` / `L13`
- 不把 `E-E7-POLICY-M1-L06` 改成展示联调单
- 不另冻结第二份 API-POL
- 不改架构稿、说明书、WBS、契约输入清单
- 未 commit，未 push，未改注册表，未标 done

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-TREND-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用架构稿：203 读 element/ADS；204 委托专题门面；205 趋势与 206 时间、地域读已有统计表；205 三项与 206 主题读 gapfill |
| 会签态 | 图源无 frontmatter。架构稿已由 `human:淮政玮` 于 2026-11-03 按说明书第 11 节签收。本分册不另填绿 |
| 说明 | 图在 `sdd/l2/POL-L2-DS10-TREND-ARCH.md` 第 2 节。本分册只补每条资源的方法、同步或读表、空态 |

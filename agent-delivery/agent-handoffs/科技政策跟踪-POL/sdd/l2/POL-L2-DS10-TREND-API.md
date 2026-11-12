# POL-L2-DS10-TREND-API · 科创政策全景 · 政策动向跟踪 · 后台接口设计

- 任务：`POL-L2-DS10-TREND-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-02`
- 上游：`sdd/l2/POL-L2-DS10-TREND-ARCH.md`（2026-11-03 `human:淮政玮` 按说明书第 11 节签收，本分册以它为准，不改）、说明书第 11 节、SRS `科创政策全景.md` 序号 203–206、`sdd/契约输入清单.md` 全景里的 `stats` / `ingest` / `jobs` / `subscriptions`
- 签收：2026-11-03 human:淮政玮 签收。空是空列表或空图，接口不直接返回 mock。

本分册只定科创政策全景二级「政策动向跟踪」的后台接口。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。

这里只写路径、方法、同步还是读表、空态。不写 OpenAPI 字段闭包、响应体、枚举、DTO。不写实现代码。

## 偏离

本二级 DoD 里的「501 空态」按已签收架构解释：空是空列表或空图，不是 501。无行则对应块空，不造 0。禁止用 501 充当这几块功能，禁止接口直接返回 mock。

「不复用 `/topic/v1/policy`」指浏览器不改打专题 URL。浏览器仍只打 `/display/v1/policy/**`。`stats` 沿用检索叶已经写明的内部委托，本分册不另建一条统计查询。204 由 `gkxlumen-display` 内部把 `subscriptions` 委托给 `gkxlumen-topic-policy`。这次内部委托不把 `E-E7-POLICY-M1-L06` 改成展示联调单。

## 1. 公开资源

浏览器经网关打 `gkxlumen-display`。前缀 `/display/v1/policy/`。不另开路径，不另开页。

| 序号 | 公开资源 | 读法 | 空态 |
|---|---|---|---|
| 203 | `GET /display/v1/policy/panorama/ingest` | 同步。display → `gkxlumen-element` → 已有 ADS | 无入库行则空列表。不抓取 |
| 204 | `GET /display/v1/policy/panorama/subscriptions` | display 只委托 `gkxlumen-topic-policy` | 没有订阅则空列表。不手写，不建缺项表，不灌假订阅 |
| 205 趋势；206 时间、地域 | `GET /display/v1/policy/panorama/stats` | 同步。读已有 `M_POLICY_TIMESERIES` 与 `M_POLICY_NATIONAL_DIST` 所在表。不另建查询 | 无行则图空，不造 0 |
| 206 主题分布 | 仍是上面这条 `stats` 上的一维 | element 读 `gapfill_policy_theme_dist`。display 不生成主题桶 | 无行则该维空 |
| 205 热点、影响、深度报告 | `POST /display/v1/policy/panorama/jobs` | 读表。不进 Python，不进 `gkxlumen-topic-async-service`。element 读三张缺项表 | 无行则该块空 |

读失败只让对应块空，不清空已经返回的时序、地域和入库列表。切筛选不自动起任务。

`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。trace 沿既有展示链。`stats`、`ingest`、缺项表读取和 204 的委托在 display 往下游带 traceId。本分册不新设计观测点。

## 2. 203 · `GET /display/v1/policy/panorama/ingest`

同步。链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → 已有 ADS。读第 6 项已经落入 ADS 的入库列表。不委托专题政策门面。

不在本页发起抓取，不把 `ingest` 改成 Job，不在展示侧建来源站点清单。来源监控没有 `metric_id`，本分册不新造。

空态：无入库行则列表空。这不是 501。

打开一条详情时复用全景已有的 `GET /display/v1/policy/panorama/{id}/detail`。本分册不新开详情资源，不重写这条 detail。无正文则详情空。

**2026-11-07 变更（`POL-L2-DS10-SRCMON-SYNTH-L01`）**：

- `ingest` 每行新增 `is_mock`（0/1）。LLM 合成行为 1，前端评审态挂 MockBadge。其余列不变。
- `POST /display/v1/policy/panorama/sync-history`（立即同步）立即返回同步历史，最新一行 `status='running'`、`fetched=10`。合成在后台进行。已有一条在跑时不新开，`honesty.note='已有同步在进行'`。
- `GET /display/v1/policy/panorama/sync-history`：`status` 取 `running`/`success`/`partial`/`failed`。`note` 写明「LLM 合成，未抓取外站；产业补码 X 条，条款结构化 Y 条」或失败原因。前端每 4 秒轮询，直到没有 `running` 行，再重读 `ingest`。
- 中台（demo-ui-system-test）政策 Mock 页走 demo 网关 `/policy/v1/policy/mock/synth`：`POST {count}` 发起，`GET` 查 `{running,last,total}`，`DELETE` 删除全部合成行。这三条只在中台用，不进展示前端。

## 3. 204 · `GET /display/v1/policy/panorama/subscriptions`

display 只委托 `gkxlumen-topic-policy`。保存、修改、取消、读取和外发都在这次委托里。展示不保存订阅关系，不跑定时，不发系统通知、邮件或短信，不把订阅写进 `gkxlumen-element` 或 ADS。

公开资源只有这一条 GET。本分册不另开展示路径，不冻结门面子路径。浏览器不改打 `/topic/v1/policy`。

不是序号 201 的收藏，不读 `favorites`。不进 `jobs`。页面 localStorage 和「立即推送」不是这条资源。

不建缺项表，不灌假订阅。说明书第 11 节写明订阅条件不灌假记录。实现单是 `E-E7-POLICY-M1-L11`、`L12`、`L13`，监管都是 `human:淮政玮`。本分册不认领。

空态：该用户没有订阅则空列表。外发通道还没有时，推送记录为空列表。display 不返回手写订阅来顶上，也不改判 501。不因这条读失败清空时序、地域和入库列表。

## 4. 205 趋势与 206 时间、地域、主题 · `GET /display/v1/policy/panorama/stats`

同步。浏览器仍打这一条已有 `stats`。内部委托以 `POL-L2-DS10-QRY-ARCH` 为准。本分册不另建一条统计查询，不改这条资源上留给检索、部门件数、标杆比对和行业覆盖的其余挂接。

| 叶子 | 读哪张已有表 | 空态 |
|---|---|---|
| 205 趋势 | `M_POLICY_TIMESERIES` 所在表 | 无点则图空 |
| 206 时间轴、趋势 | 同一条时序 | 无点则图空 |
| 206 地域热力 | `M_POLICY_NATIONAL_DIST` 所在表 | 无省行则图空 |

两条指标类型都是 STAT，D1 aligned，D4 mock。对齐前数值仍是 mock。接口只读表，不在返回里造点，不往 ADS 写 mock 点，也不把这些点改灌进检索的 `gapfill_policy_qry_stat`。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本分册不把闸门写成已解开，不把 D4 改绿。连续性仍是 QPOL-07，本分册不改口径。D2 为 provisional 时保留「待核验」。

重点领域（科创发展、人才引进、资金扶持）是 `stats` 上的筛选条件，不是三条新指标。本分册不冻结取值。

206 主题分布仍是 `stats` 上的一维。没有已挂的 `metric_id`。这一维由 `gkxlumen-element` 读 `gkxlumenx_gapfill.gapfill_policy_theme_dist`。display 不生成主题桶，也不借用类型分布冒充主题。无行则该维空，不造 0。主题读失败只让这一维空，不清空已经返回的时序和地域。

## 5. 205 热点、影响、深度报告 · `POST /display/v1/policy/panorama/jobs`

读表。这三项没有模型，不进 Python，不进 `gkxlumen-topic-async-service`。display 委托 `gkxlumen-element` 按种类读表，原样返回行。display 不组装报告。Java 不识别热点，不写影响，不生成报告。

| 结果 | 表 |
|---|---|
| 热点识别 | `gkxlumenx_gapfill.gapfill_policy_trend_hotspot` |
| 政策影响评估 | `gkxlumenx_gapfill.gapfill_policy_trend_impact` |
| 深度分析报告 | `gkxlumenx_gapfill.gapfill_policy_trend_report` |

三张表与说明书第 11.1 节动向一行相同。列由 `POL-L2-DS10-TREND-DATA` 定。灌数由 `POL-L2-DS10-TREND-GAPFILL-L01` 执行。本分册不写列，不灌数，不新造 `metric_id`。深度报告正文在 `gapfill_policy_trend_report` 的行里，不写对象存储。

用户点了其中一种才查表。切领域、切筛选不自动起任务，也不自动查另一域。无行则该块空，不造 0，不在接口里填一份报告。读失败只让该块空，不清空已经返回的时序、地域和入库列表。

**导出（2026-11-12 KEYFIELD-FDE）**：影响评估 / 深度分析报告在 FE 弹窗读到行之后，可另走已有 `POST /display/v1/situation/report/generate`（及 download）产出 PDF/Word。本分册不新开 panorama 专用导出 URL。jobs 响应仍不内嵌写死 PDF。无行不产文件。

同一条 `jobs` 上的实施效果、匹配、力度属于其他叶子。本分册不展开，也不改挂 `M_POLICY_FOCUS_INDEX`、`M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_SIMULATE`，以及序号 211、217 的报告资源。

## 6. 空态对照

| 资源 | 无数据 | 本分册的空 |
|---|---|---|
| `ingest` | 无入库行 | 空列表。不抓取。详情无正文则详情空 |
| `subscriptions` | 该用户没有订阅；外发通道还没有 | 空列表。不手写订阅，不灌假订阅 |
| `stats` 时序、地域 | 无点、无省行 | 对应图空，不造 0，不往 ADS 写 mock 点 |
| `stats` 主题分布 | `gapfill_policy_theme_dist` 无行 | 该维空。display 不生成主题桶 |
| `jobs` 热点、影响、深度报告 | 对应缺项表无行 | 该块空 |

上表的空都不是 501。读失败只让对应块空。

## 7. 明确不做

- 不另建 API-POL，不写 OpenAPI 字段闭包、响应体、枚举、DTO。交给 `BE-POL-CONTRACT-01`。
- 不写实现代码。不改 Java、Python、前端仓。
- 不认领 `E-E7-POLICY-M1-L11` / `L12` / `L13`。不把 `E-E7-POLICY-M1-L06` 改成展示联调单。
- 不灌数，不建表，不改 D4，不新造 `metric_id`，不闭合 QPOL-07，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不把时序和地域点改灌进 `gapfill_policy_qry_stat`，不往 ADS 写 mock 点。
- 不把 204 写成缺项表或假订阅。不把 203 写成抓取。不把热点、影响、深度报告写进 Python 或异步任务服务。
- 浏览器不改打 `/topic/v1/policy`。
- 序号 197–202、207–218 不在本分册。`search`、`rank`、`favorites`、`share`、`feedback`、`assessment-report`、`version-diff`、`benchmark-report` 不在本二级重写。`{id}/detail` 只被 203 打开一条时复用。
- 不改架构稿、说明书、WBS、契约输入清单、调用链、指标分册、数据分册。
- 不把任务标成 done。

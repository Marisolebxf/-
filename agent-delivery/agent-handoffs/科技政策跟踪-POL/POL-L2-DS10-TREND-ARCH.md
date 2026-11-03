# POL-L2-DS10-TREND-ARCH · 科创政策全景政策动向架构

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock_until | `2026-11-04T04:00:30.744Z` |
| 说明 | 2026-11-03 human:淮政玮按说明书第 11 节再次签收 |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、缺项表读法、第 6 项只读边界和与 197–202、207–218 的分界。

## 范围

科创政策全景 · 二级「政策动向跟踪」。只覆盖 SRS 序号 203–206，用户故事 `US-DS-POL-02`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 203 | 政策来源监控与更新 | 同步读 `ingest`。第 6 项已有结果。不重开 GDF |
| 204 | 政策订阅服务 | 展示只委托 `gkxlumen-topic-policy`。不手写订阅列表。任务 `E-E7-POLICY-M1-L11` / `L12` / `L13` |
| 205 | 重点领域政策分析 | 趋势读已有时序表。热点、影响、深度报告读三张 `gapfill_` 表 |
| 206 | 政策动态可视化展示 | 时间轴和趋势读时序表。地域热力读全国分布表。主题分布读 `gapfill_policy_theme_dist` |

浏览器只打 `/display/v1/policy/**`。203 走 `gkxlumen-element` → ADS。205 的趋势、206 的时间与地域读已有统计表。204 由 display 委托专题门面，展示不返回手写订阅。localStorage 不是订阅服务。热点、影响、深度报告和主题分布由 element 读缺项表。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-TREND-ARCH.md`

## 与相邻叶子的边界

本叶不写 197–202 和 207–218 的流程。点名排除 `search`、`rank`、`favorites`、`share`、`feedback`、`assessment-report`、`version-diff`、`benchmark-report`。`{id}/detail` 只在打开一条入库政策时复用，不在本叶重写。

`jobs` 接到 205 的热点、影响、深度报告时只读缺项表，不进 Python。实施效果、匹配、力度不在本叶展开。

## 未做事项

- 未写 OpenAPI 字段表、请求体、响应体、枚举。留给 `POL-L2-DS10-TREND-API`
- 未新造 `metric_id`，未改 D4，未闭合 QPOL-07，未把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开
- 未改 `FE-POL-01B`，未新建前端单，未重开 GDF
- 浏览器未改打 `/topic/v1/policy`。未把 `E-E7-POLICY-M1-L06` 写成展示前端联调单
- 未改说明书、WBS、调研分册
- 订阅与外发交给 `E-E7-POLICY-M1-L11`、`L12`、`L13`，监管都是 `human:淮政玮`。本单不认领这三张。热点、影响、深度报告和主题分布不新注册模型，改读 `gapfill_` 表
- 四张缺项表要灌的 mock 写在架构稿第 7.3 节。灌数执行单 `POL-L2-DS10-TREND-GAPFILL-L01` 交给 data-agent，本单不执行

## 偏离

原 DoD 写「不消费 `/topic/v1/policy`」。签收口径：浏览器和展示对外 URL 仍只走 `/display/v1/policy/**`。`stats` 沿用检索叶已经写明的内部委托。204 的 `subscriptions` 由 `gkxlumen-display` 内部委托 `gkxlumen-topic-policy`，订阅与外发的实现不在展示服务。这不把 `E-E7-POLICY-M1-L06` 改成展示联调单。

签收条件以说明书第 11 节为准。204 走专题门面，不灌假订阅。时序和地域热力读已有表，不另建缺项表。热点、影响、深度报告和主题分布只建第 11.1 节那四张 `gapfill_` 表，Python 灌 mock，接口读表。接口不直接返回 mock，也不用 501 充当这几块。

## 验收证据

架构稿与本 handoff 已落盘。2026-11-03 human:淮政玮按说明书第 11 节再次签收。四张表、灌数内容和 `POL-L2-DS10-TREND-GAPFILL-L01` 与第 11.1 节动向一行一致。定义单，无业务 PR。随 `gkx-orchestration` 的 `origin/dev` 提交。

| 序号 | 签收链路 | 结论 |
|---|---|---|
| 203 | element 读已有 ADS 入库列表。无行则空列表 | 符合。读已有表 |
| 204 | display 只委托 `gkxlumen-topic-policy`。不手写订阅。门面内部由 L11–L13 实现，本叶不建缺项表 | 符合。判定做得到，不走 501，不手写 mock |
| 205 趋势 | `stats` 读 `M_POLICY_TIMESERIES` 所在表 | 符合。读已有表。D4 仍是 mock，接口不另造点 |
| 205 热点、影响、深度报告 | element 读 `gapfill_policy_trend_hotspot`、`gapfill_policy_trend_impact`、`gapfill_policy_trend_report`。Python 灌 mock | 符合。没有模型，只走缺项表 |
| 206 时间、地域 | 读时序表和 `M_POLICY_NATIONAL_DIST` 所在表 | 符合。读已有表 |
| 206 主题分布 | element 读 `gapfill_policy_theme_dist` | 符合。没有指标，只走缺项表 |

要灌的 mock 在架构稿第 7.3 节。热点表灌三个领域的热点名称和一句说明。影响表灌领域、对象、方向和一句结论。报告表灌标题、领域和正文，正文在行里。主题表灌主题名和件数。不灌分数、文件和类型分布。执行单 `POL-L2-DS10-TREND-GAPFILL-L01`，本单不灌数。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本叶不写算法。热点、影响、深度报告没有模型，不进 Python；mock 行由 Python 灌进缺项表，Java 只读 |
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。204 只在服务内部委托专题门面 |
| 图谱 | ✅ 本叶不读图，不写 nGQL |
| 可观测 | ✅ 沿既有展示链 trace，不新设计观测点 |
| CI/CD | ✅ 定义文档随 `origin/dev` 提交，未 force |
| D12 | ✅ 不调用 demo 服务 |
| D9 | ✅ 不新造 metric_id，不改 D4，不闭合 QPOL-07 |
| D14 | ✅ 深度报告正文在缺项表行里。本叶不写对象存储 |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-TREND-ARCH-SEQ` |
| 图 diff | 203 读 element/ADS。204 委托专题门面。205 趋势与 206 时间、地域读已有统计表。205 三项与 206 主题读 gapfill。禁止边：浏览器改打专题 URL、接口直接返回 mock、用 501 充当这几块、热点改挂焦点指数、主题分布新造指标 |
| 会签态 | 2026-11-03 human:淮政玮按说明书第 11 节再次签收。图源无 frontmatter，不另填绿 |
| 说明 | 图在架构稿第 2 节 |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 8000、architect 80/20、B 档 `$3/$15` 回填：`8000×0.80×3/1e6 + 8000×0.20×15/1e6 = 0.043`，记 `0.04`。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS10-TREND-ARCH.md`
- 新增本 handoff

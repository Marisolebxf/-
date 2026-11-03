# POL-L2-DS10-TREND-ARCH · 科创政策全景政策动向架构

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock_until | `2026-11-04T04:00:30.744Z` |
| 说明 | 2026-11-03 human:淮政玮签收。订阅与外发仍未接通 |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、501 空态、第 6 项只读边界和与 197–202、207–218 的分界。

## 范围

科创政策全景 · 二级「政策动向跟踪」。只覆盖 SRS 序号 203–206，用户故事 `US-DS-POL-02`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 203 | 政策来源监控与更新 | 同步读 `ingest`。第 6 项已有结果。不重开 GDF |
| 204 | 政策订阅服务 | 当前 `subscriptions` 501。接通后展示只委托 `gkxlumen-topic-policy`，实现不在展示服务。任务 `E-E7-POLICY-M1-L11` / `L12` / `L13` |
| 205 | 重点领域政策分析 | 趋势读 `stats` 上的 `M_POLICY_TIMESERIES`。热点、影响、深度报告当前走 `jobs` 501。接通后仍是这一条 Job，见架构稿第 7.2 节 |
| 206 | 政策动态可视化展示 | 时间轴和趋势读时序。地域热力读 `M_POLICY_NATIONAL_DIST`。主题分布不新造指标 |

浏览器只打 `/display/v1/policy/**`。203 走 `gkxlumen-element` → ADS。205、206 的统计读已有 `stats`，不另建查询。204 当前在 display 直接 501。接通后展示只委托 `gkxlumen-topic-policy`，订阅与外发的实现不在展示服务。localStorage 不是订阅服务。三项报告的接通方案仍在架构稿第 7.2 节。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-TREND-ARCH.md`

## 与相邻叶子的边界

本叶不写 197–202 和 207–218 的流程。点名排除 `search`、`rank`、`favorites`、`share`、`feedback`、`assessment-report`、`version-diff`、`benchmark-report`。`{id}/detail` 只在打开一条入库政策时复用，不在本叶重写。

`jobs` 只承接 205 的三项未见模型。实施效果、匹配、力度不在本叶展开。

## 未做事项

- 未写 OpenAPI 字段表、请求体、响应体、枚举。留给 `POL-L2-DS10-TREND-API`
- 未新造 `metric_id`，未改 D4，未闭合 QPOL-07，未把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开
- 未改 `FE-POL-01B`，未新建前端单，未重开 GDF
- 浏览器未改打 `/topic/v1/policy`。未把 `E-E7-POLICY-M1-L06` 写成展示前端联调单
- 未改说明书、WBS、调研分册
- 第 7 节是接通方案，不是已经接通。订阅与外发交给 `E-E7-POLICY-M1-L11`、`L12`、`L13`，监管都是 `human:淮政玮`。本单不认领这三张。未注册热点、影响、深度报告模型

## 偏离

原 DoD 写「不消费 `/topic/v1/policy`」。签收口径：浏览器和展示对外 URL 仍只走 `/display/v1/policy/**`。`stats` 沿用检索叶已经写明的内部委托。204 的 `subscriptions` 接通后也由 `gkxlumen-display` 内部委托 `gkxlumen-topic-policy`，订阅与外发的实现不在展示服务。这不把 `E-E7-POLICY-M1-L06` 改成展示联调单。入口未接上时，204 仍是 501。

## 验收证据

架构稿与本 handoff 已落盘。2026-11-03 human:淮政玮签收。定义单，无业务 PR。随 `gkx-orchestration` 的 `origin/dev` 提交。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本叶不写算法。热点、影响、深度报告接通后走 Python `/internal/*`，Java 不识别、不生成 |
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。204 只在服务内部委托专题门面 |
| 图谱 | ✅ 本叶不读图，不写 nGQL |
| 可观测 | ✅ 沿既有展示链 trace，不新设计观测点 |
| CI/CD | ✅ 定义文档随 `origin/dev` 提交，未 force |
| D12 | ✅ 不调用 demo 服务 |
| D9 | ✅ 不新造 metric_id，不改 D4，不闭合 QPOL-07 |
| D14 | ✅ 本叶不写对象存储。报告目录只写在预计实现里 |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-TREND-ARCH-SEQ` |
| 图 diff | 第 2 节是当前路径：203 读 element/ADS；205 趋势与 206 读已有 stats；205 三项未注册则 501；204 直接 501。第 7 节接通后：204 由 display 委托 gkxlumen-topic-policy，业务不在展示服务；三项报告仍走同一条 Job 进 Python。禁止边：浏览器改打专题 URL、展示服务自建订阅表或外发、热点改挂焦点指数、主题分布新造指标 |
| 会签态 | 2026-11-03 human:淮政玮签收本单。图源无 frontmatter，不另填绿 |
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

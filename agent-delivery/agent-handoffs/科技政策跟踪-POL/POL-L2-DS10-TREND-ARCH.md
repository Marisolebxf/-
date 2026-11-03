# POL-L2-DS10-TREND-ARCH · 科创政策全景政策动向架构

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock_until | `2026-11-04T04:00:30.744Z` |
| 说明 | 只写政策动向跟踪的实现架构。不标 done，不会签 |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、501 空态、第 6 项只读边界和与 197–202、207–218 的分界。

## 范围

科创政策全景 · 二级「政策动向跟踪」。只覆盖 SRS 序号 203–206，用户故事 `US-DS-POL-02`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 203 | 政策来源监控与更新 | 同步读 `ingest`。第 6 项已有结果。不重开 GDF |
| 204 | 政策订阅服务 | `subscriptions`，501 |
| 205 | 重点领域政策分析 | 趋势读 `stats` 上的 `M_POLICY_TIMESERIES`。热点、影响、深度报告走 `jobs`，501 |
| 206 | 政策动态可视化展示 | 时间轴和趋势读时序。地域热力读 `M_POLICY_NATIONAL_DIST`。主题分布不新造指标 |

浏览器只打 `/display/v1/policy/**`。203 走 `gkxlumen-element` → ADS。205、206 的统计读已有 `stats`，不另建查询，不新开专题委托。204 在 display 直接 501。localStorage 不是订阅服务。

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
- 未把本单标 done。会签不在本单

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-TREND-ARCH-SEQ` |
| 图 diff | 203 由 display 读 element/ADS；205 趋势与 206 读已有 stats；205 三项报告进异步 Job，未注册则 501；204 在 display 进入 501。禁止边：浏览器改打专题 URL、本叶新开抓取、订阅写成已有外发、主题分布新造指标 |
| 会签态 | 本叶新图。源文件无 frontmatter，记 `draft`。不自填绿 |
| 说明 | 图在架构稿第 2 节 |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |

## 修改内容

- 新增 `sdd/l2/POL-L2-DS10-TREND-ARCH.md`
- 新增本 handoff

# POL-L2-DS10-QRY-ARCH · 科创政策全景多维检索架构

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 只写多维检索查询的实现架构。2026-11-03 首次签收。同日按说明书第 11 节再次签收 |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、501 空态和与 203–218 的边界。

## 范围

科创政策全景 · 二级「多维检索查询」。只覆盖 SRS 序号 197–202，用户故事 `US-DS-POL-01`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 197 | 多维度检索条件设置 | 同步，委托专题政策门面。智能检索先 `query-intent` 再 `search`（`sdd/l2/POL-L2-DS10-QRY-INTENT.md`） |
| 198 | 高级检索功能 | 同步，委托专题政策门面 |
| 199 | 检索结果智能排序 | 读 `gapfill_policy_qry_rank`。普通三列仍走 search |
| 200 | 检索结果筛选与分类 | 同步。没有正式行时读缺项表 |
| 201 | 检索历史与收藏 | 门面用户记录。不灌假收藏 |
| 202 | 检索结果导出与分享 | 导出当次目录。不灌假文件 |

197、198、200 读已有 `stats`、`search`、`{id}/detail`。浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 内部委托 `gkxlumen-topic-policy`。有正式行读 ADS / DWD；没有正式行时 Python 读 `gapfill_policy_qry_doc`、`gapfill_policy_qry_stat`。接口不写死数。D4 仍是 mock。

199 读 `rank`，Python 只读名次表，不返回 `smartScore`。201、202 委托同一门面，不建缺项表。没有记录或当次目录为空则空，不灌假数据。

展示不自建这三套能力。本叶不改门面代码，不把缺项行写成已上线。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-QRY-ARCH.md`

## 与 203–218 的边界

本叶不写 203–218 的流程。点名排除 `panorama/jobs`、`ingest`、`subscriptions`、`feedback`、`assessment-report`、`version-diff`、`benchmark-report`。

| 序号 | 边界 |
|---|---|
| 203 | 入库列表走 `ingest`。不重开 GDF |
| 204 | 订阅走 `subscriptions`。不是收藏 |
| 205 | 趋势另叶复用时序。热点、影响、深度报告走 `jobs` |
| 206 | 动态可视化另叶。本叶不实现 |
| 207 | 页内并列查看另叶。深度对比不在本五条 |
| 208 | 只消费已有子图。本叶不读图，不走 `E-E7-POLICY-M1-L06` |
| 209 | 另叶读 `ads.policy_effect` |
| 210 | 另叶读缺项表 |
| 211 | 另叶读缺项表。不是 202 |
| 212 | 另叶读 `ads.policy_match`。不改去打 `/topic/v1/policy` |
| 213 | 新旧对比另叶 |
| 214 | 详情对比的力度另叶 |
| 215 | 部门件数另叶，复用政策总数 |
| 216 | 标杆力度另叶。本叶不把支持力度写成检索结果 |
| 217 | 对标报告另叶。与 `share` 分开 |
| 218 | 对标可视化另叶 |

`stats` 上的 `M_POLICY_INDUSTRY_COVERAGE`、`M_POLICY_SUPPORT_STRENGTH` 不改挂到 197–202。

## 未做事项

- 未写 OpenAPI 字段表、请求体、响应体、枚举。留给 `POL-L2-DS10-QRY-API`
- 未新造 `metric_id`，未改 D4，未把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开
- 未改 `FE-POL-01A`，未新建前端单，未重开 GDF
- 浏览器未改打 `/topic/v1/policy`。内部委托含 stats / search / detail，以及 rank、favorites、share。未把 `E-E7-POLICY-M1-L06` 写成展示前端联调单
- 未改说明书、WBS、注册表、调研分册
- 2026-11-03 human:淮政玮首次签收。同日按说明书第 11 节再次签收

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-QRY-ARCH-SEQ` |
| 图 diff | 197/198/200 委托门面，正式行读已有表，否则读两张 qry 缺项表；199 只读名次表；201/202 委托门面且不灌假记录。禁止边：浏览器改打专题 URL、display 直连 Python、接口直接返回 mock、`L06` 作前端联调单 |
| 会签态 | 2026-11-03 human:淮政玮首次签收。同日按说明书第 11 节再次签收。源文件无 frontmatter |
| 说明 | 图在架构稿第 2 节 |

## 范围与实现

见上文「范围」。DoD：架构与流程落在 `sdd/l2/POL-L2-DS10-QRY-ARCH.md`。浏览器只打 `/display/v1/policy/**`。

## 偏离

原 DoD 写「不消费 `/topic/v1/policy`」。签收口径：浏览器和展示对外 URL 仍只走 `/display/v1/policy/**`。本二级由 `gkxlumen-display` 内部委托 `gkxlumen-topic-policy`。这是 A1 的本二级例外，不改 `ARCH-DISPLAY-01` 的全局 A1。再次签收对照说明书第 11.1 节：197、198、200 没有正式行时读两张缺项表；199 只读名次表；201、202 不灌假记录。接口不直接返回 mock。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-QRY-ARCH.md`
- 本 handoff

## 验收证据

架构稿与本 handoff 已落盘。2026-11-03 human:淮政玮首次签收，同日按说明书第 11 节再次签收。定义单，无业务 PR。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本叶不写算法。排序模型落在门面转 `/internal/policy`，Java 不打分 |
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。展示内部委托专题门面，不直连 Python |
| 图谱 | ✅ 本叶不读图，不写 nGQL |
| 可观测 | ✅ 沿既有展示链 trace，不新设计观测点 |
| CI/CD | ✅ 定义文档随 `origin/dev` 提交，未 force |
| D12 | ✅ 不调用 demo 服务 |
| D9 | ✅ 不新造 metric_id，不改 D4 |
| D14 | ✅ 本叶不写对象存储。导出目录只写在预计实现里 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.04 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 8000、architect 80/20、B 档 `$3/$15` 回填：`8000×0.80×3/1e6 + 8000×0.20×15/1e6 = 0.043`，记 `0.04`。

## 修改内容

- `sdd/l2/POL-L2-DS10-QRY-ARCH.md`
- 本 handoff

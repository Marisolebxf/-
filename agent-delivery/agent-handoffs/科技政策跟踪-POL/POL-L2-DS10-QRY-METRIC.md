ponytail: off

# POL-L2-DS10-QRY-METRIC · 科创政策全景多维检索指标设计

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 定义单。只写 197–202 的指标挂接。不写代码，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过已有 metric_id、501 空态和 D4=mock。

## 范围与实现

科创政策全景 · 二级「多维检索查询」。只覆盖 SRS 序号 197–202，用户故事 `US-DS-POL-01`。判定只沿用说明书第 2 节和调研三档。

| 序号 | 叶子 | 指标 |
|---|---|---|
| 197 | 多维度检索条件设置 | 可接统计读面。`M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`、`M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST`。D4 仍是 mock |
| 198 | 高级检索功能 | 可接统计读面。`M_POLICY_TIMESERIES`、`M_POLICY_NATIONAL_DIST`、`M_POLICY_LEVEL_DIST`、`M_POLICY_TYPE_DIST`、`M_POLICY_VALIDITY_RATE`。D4 仍是 mock |
| 199 | 检索结果智能排序 | 不是指标。排序模型未注册，501 空态。不写公式，不写 smartScore |
| 200 | 检索结果筛选与分类 | 可接统计读面。`M_POLICY_TYPE_DIST`、`M_POLICY_NATIONAL_DIST`。D4 仍是 mock |
| 201 | 检索历史与收藏 | 不是指标。501 空态 |
| 202 | 检索结果导出与分享 | 不是指标。501 空态 |

去重后本二级只用上述 7 个已有 `metric_id`，类型都是 STAT。八件套来自 2026-11-03 的 `metric-get`。布尔组合、二次筛选、普通三列排序（发布时间、效力级别、浏览量）没有独立 `metric_id`。

`M_POLICY_INDUSTRY_COVERAGE`、`M_POLICY_SUPPORT_STRENGTH` 不改挂到 197–202。

读面沿 `POL-L2-DS10-QRY-ARCH`：197、198、200 走已有 `stats` / `search` / `{id}/detail`；199、201、202 当前 501。本叶不改这条路径，不写算法实现。

## 偏离

无新偏离。序号与三档以说明书第 2 节为准。

`M_POLICY_TOTAL_COUNT` 的需求来源页是序号 215，`M_POLICY_TIMESERIES` 的需求来源页含 205、206。本叶不改挂，仍按说明书把总数用在 197、时序用在 198。`M_POLICY_VALIDITY_RATE` 的 `srs_refs` 为空，仍留在 198，不新造 id。

`metric-query` 关键词「排序」命中 `M_POLICY_DS_11_POLICY_EVAL_015`（评价页序号 229）。该条不是检索排序模型，本二级不挂。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-QRY-METRIC.md`
- 本 handoff

未改指标 seed、矩阵、说明书、调研分册、架构稿、`task-registry.yaml`。未写代码。

## 验收证据

- `metric-get` 七条均 `found.seed=true`、`found.matrix=true`，D4 均为 `mock`，`algorithm_type` 均为 STAT。
- `metric-query`：智能排序、相关性、收藏、检索历史、导出、分享均为 0 条。未查到本二级的排序模型、收藏指标、导出指标。
- 指标设计稿与本 handoff 已落盘。定义单，无业务 PR，无 pipeline。
- 文档随本次提交进入 `origin/dev`。状态进入 `integration`。会签未完成，不标 done。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不写算法实现。已有 STAT 仍由 Python 计算，Java 不打分 |
| 调用链 | ✅ 沿架构稿。浏览器只打 `/display/v1/policy/**`。本单不改链，展示不直连 Python |
| 图谱 | ✅ 本二级不读图，不写 nGQL |
| 可观测 | ✅ 不新设计观测点，沿既有展示链 |
| D9 | ✅ 只用已注册 metric_id。八件套与 D1–D4 分开写。D4 保持 mock。199/201/202 不新造 id |
| D12 | ✅ 不把展示调用链改去 demo 服务。注册表里的 demo 计算文件只作索引，本单不改、不调用 |
| D17 | ✅ 不改唐绍祖锁定的合规算法。本单不写算法实现 |
| D14 | ✅ 本单不写对象存储 |
| CI/CD | ✅ 定义文档随 `origin/dev` 提交，未 force |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.05 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 8000、algorithm 75/25、B 档 `$3/$15` 回填：`8000×0.75×3/1e6 + 8000×0.25×15/1e6 = 0.048`，记 `0.05`。

## 修改内容

- `sdd/l2/POL-L2-DS10-QRY-METRIC.md`
- 本 handoff

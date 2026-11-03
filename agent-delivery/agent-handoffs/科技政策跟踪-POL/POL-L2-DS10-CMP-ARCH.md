# POL-L2-DS10-CMP-ARCH · 科创政策全景政策重点比对架构

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-11-03 按可实现标准写完。未会签，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、缺项表、力度评估迁移和与 197–212、核增研报的分界。

## 范围

科创政策全景 · 二级「政策重点比对」。只覆盖 SRS 序号 213–218，用户故事 `US-DS-POL-04`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 213 | 政策新旧对比 | 读 `gapfill_policy_version_diff` |
| 214 | 政策详情对比 | 正文走已有门面。力度读 `ads.policy_intensity`。条件与材料读 `gapfill_policy_detail_compare` |
| 215 | 部门政策对比 | 已有 `M_POLICY_TOTAL_COUNT` 与目录。不新造部门指标 |
| 216 | 标杆比对功能 | 同一次力度计算读 `M_POLICY_SUPPORT_STRENGTH`。不新建表 |
| 217 | 对标报告生成与导出 | 读 `gapfill_policy_benchmark_report`。不灌假文件 |
| 218 | 对标结果可视化展示 | 读 `ads.policy_intensity`。不建可视化缺项表 |

浏览器只打 `/display/v1/policy/**`。展示不直连库，不打开算法中台，不打 `/v1/policy/**`。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-CMP-ARCH.md`

## 与相邻叶子的边界

本叶不写 197–212 的流程。点名排除 `rank`、`favorites`、`share`、`feedback`、`assessment-report`。217 不是序号 211，也不是核增研报 614–618。

## 架构合规

| 项 | 结果 |
|---|---|
| 调用链 | 浏览器 → 网关 → `gkxlumen-display`。正文委托 `gkxlumen-topic-policy`。力度走 Python `/internal/policy`。缺项表由 Python 查询 |
| 算法只在 Python | 力度沿用 `polan.eval.intensity.run`。Java 不打分 |
| D12 | 不直连 demo 服务，不把 demo 路径写成对外入口 |
| D18 / 说明书第 11 节 | 做不到的只建缺项表并读表。接口不直接返回 mock |
| 指标 | 不新造 `metric_id`，不改 D4 |
| GDF / 图 | 不重开。215 不新造部门指标 |

## 验收

- 架构稿已落盘，含同步读面、Job、缺项表和跨项只消费。
- 六叶输入条件在架构稿第 3 节。数据来源和现成接口在第 3.1 节。展示原型的选项是本地常量，不迁。部门名单和版本时点现没有接口。
- 灌数单 `POL-L2-DS10-CMP-GAPFILL-L01` 本叶不执行。218 不建 `gapfill_policy_benchmark_viz`，以本架构第 9 节为准。
- 未会签。不标 done。

## 开放项

- `policy_intensity` 这个 `sub_type` 尚未挂到 `/internal/policy/jobs/execute`。本叶不改代码。
- 缺项表的列由 `POL-L2-DS10-CMP-DATA` 定。

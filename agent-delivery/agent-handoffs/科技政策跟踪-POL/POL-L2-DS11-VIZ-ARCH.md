# POL-L2-DS11-VIZ-ARCH · 政策分析评价可视化架构

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 架构稿已落盘。会签未完成。未签收。 |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、缺项表、第 7 项只消费和与 223–231、全景时序、核增研报的分界。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-VIZ-ARCH-SEQ` |
| 图 diff | 本叶新图。浏览器到网关到 `gkxlumen-display`。219、220 进 `gkxlumen-element` 读缺项表，不进异步任务。221 只消费第 7 项子图。222 读壳表 |
| 会签态 | `draft`。源文件无 frontmatter，不自填 approved |

## 范围

政策分析评价 · 二级「政策分析报告可视化呈现」。只覆盖 SRS 序号 219–222，用户故事 `US-DS-POL-05`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 219 | 多维指标趋势图 | 读 `gapfill_policy_eval_trend`。不建任务 |
| 220 | 分区/群体对比分析图 | 读 `gapfill_policy_eval_partition`。不建任务 |
| 221 | 多维结构关联图 | 只消费第 7 项已有子图。不建表，不新开资源 |
| 222 | 报告模板定制与批量导出 | 读 `gapfill_policy_eval_shell` 的模板选用。不灌文件，不灌假日志 |

浏览器只打 `/display/v1/policy/**`。不增加第 4 条路径。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-ARCH.md`

## 与相邻叶子的边界

本叶不写 223–231。不读 `evaluation/counts`。`jobs` 上的焦点、效能、摘要、实施路径仍走异步，本叶只把趋势和分区从这条 POST 里拆成同步读表。222 只定 `shells` 上的模板段。壳表的建立和灌数属于 `POL-L2-DS11-READ-GAPFILL-L01`。

## 架构合规

| 项 | 结果 |
|---|---|
| 调用链 | 浏览器 → 网关 → `gkxlumen-display`。219、220、222 由 `gkxlumen-element` 只读缺项表。221 不新开查图 |
| 算法只在 Python | 本叶没有可迁移的趋势或分区模型。Java 不补曲线 |
| D12 | 不直连 demo 服务，不把 `/v1/policy/**` 写成对外入口 |
| D18 / 说明书第 11.2 节 | 219、220 建表灌 mock 后由接口读表。221 不建表。222 读已定壳表 |
| 指标 | 不新造 `metric_id`，不改 D4，不改挂全景时序和全景分布 |
| GDF / 图 | 不重开。221 不写 nGQL |

## 验收

- 架构稿已落盘，含同步读表、不建任务的 `jobs` 分流、501 不再充当画面、221 跨项只消费。
- 四叶输入条件在架构稿第 3 节。数据来源在第 3.1 节。
- 灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` 本叶不执行。221 不建表。222 不进这张灌数单。
- 会签未完成。未签收。

## 开放项

- 展示仓还没有评价页控制器。本叶不改代码。
- 缺项表的列由 `POL-L2-DS11-VIZ-DATA` 定。壳表的列由解读二级的数据分册定。
- `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。221 在子图读不到时为空。

## CI/CD

定义单，无业务仓提交，无 Pipeline。

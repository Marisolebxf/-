# POL-DISPLAY-SURVEY-DS11-L01 · 政策分析评价存量调研

- 日期：2026-11-03
- 执行：`agent:arch-agent`
- 监管人：`human:淮政玮`
- 状态：分册已写。未改注册表，未 commit，未 push。

## 范围

只覆盖 DS-11 政策分析评价。用户故事 `US-DS-POL-05`。SRS 序号 219–231。对照任务 `FE-POL-02A`（`pending_test`）。

不写政策效果推演、政策布局推荐、核增四页。不写接口字段表，不改业务仓，不改 WBS，不改其他分册。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/survey/DS-11.md`

## 三档计数

判定表 17 行。

| 判定 | 行数 |
|---|---|
| 可接统计读面 | 2 |
| 501 | 9 |
| 跨项索引 | 1 |
| 未见 | 5 |

可接统计读面的 2 行是短板条数、机遇条数。类型为 STAT，D4=`mock`，数值是 mock。第一批 STAT 脚本不含这两条。

501 的 9 行覆盖趋势、分区对比、焦点指数、分主题结论、智能摘要、多方案对比、参数模拟、实施路径、效果评分。效果评分与焦点指数、摘要、实施路径已有 `metric_id`，类型不是 STAT/COMPUTE，D4 仍是 mock。

跨项索引 1 行：序号 221 结构关联，真图归第 7 项，只索引 `E-E7-POLICY-M1-L02`（done）与 `GDF-POLICY-GRAPH-EXT-L01`（backlog）。

## 未见清单

- 序号 219、220、221、222、224、225、227、228、230、231 与分析报告份数：无本叶专属 `metric_id`。
- 序号 221 不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。
- 力度与支持力度的需求来源在科创政策全景，不改挂本叶。
- `M_POLICY_TEXT_PARSE` 需求来源为空，不在本叶展开。
- 布局推荐与 `M_POLICY_SIMULATE` 不写入本叶。线框和 `FE-POL-02A` 上的布局建议卡因此未展开。
- 评价大屏未见独立任务。小屏仅见 `FE-DISPLAY-SMALL-BATCH-B`（backlog）。
- 摘要、实施路径、参数模拟、多方案：未见展示侧已注册模型任务。
- `M_POLICY_DS_07_POLICY_GUARD_001`、`M_POLICY_DS_07_POLICY_GUARD_008` 不派给本叶。

## ponytail

ponytail: off

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |

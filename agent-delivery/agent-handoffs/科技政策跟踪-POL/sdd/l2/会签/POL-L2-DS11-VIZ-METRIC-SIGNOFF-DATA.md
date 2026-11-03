# POL-L2-DS11-VIZ-METRIC-SIGNOFF-DATA · 政策分析评价 · 政策分析报告可视化呈现 · 数据会签（METRIC 分册）

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-VIZ-METRIC`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-VIZ-ARCH` 第 5、9 节；`POL-L2-DS11-VIZ-DATA`；`sdd/指标与501.md` 219–222 行（只转述，不改）
- 范围：SRS 219–222 的指标挂接与 D4 口径核对。八件套内容、D1–D3 维度不在本页补核
- 结论：**同意会签**

本页只从数据角色核对 METRIC 分册有没有把灌入行写成真实接入。不改 METRIC 分册，不改 `指标与501.md`，不改注册表，不改 D4。

## 核对表

| 口径 | METRIC 分册原文落点 | 判定 |
|---|---|---|
| 灌入行不写成真实接入 | 第 1 节「缺项表里灌入的行仍是 mock。本叶不把 mock 写成已上线」。第 4 节「不把缺项写成已上线，不把 D4 升成 live」。第 8 节同 | 一致 |
| D4 仍 mock | 第 1 节「D4 仍是 `mock`」。第 4 节四叶均「没有可改的 D4」。第 7 节点名不挂表里各号 D4 只转述不改 | 一致 |
| 不新造 `metric_id`，挂接 0 条 | 第 1 节「本二级挂接 0 条已有 `metric_id`」。第 2 节四叶均不挂。第 8 节「不新注册指标」 | 一致。与 DATA 分册三张表 `metric_id` 留空一致 |
| 判定列不改 | 219、220、222 仍 501，221 仍跨项索引。第 1 节「本叶不改那两份文件，也不把调研判定列改写成另一档」 | 一致 |
| 不把 501 当画面 | 第 5 节「有行读表，无行则空。221 无子图则空」；架构第 5、9 节同口径 | 一致 |
| 点名不挂的号不进缺项表 | 第 7 节：`M_POLICY_TIMESERIES`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`、全景分布、`M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`、`M_POLICY_SIMULATE` 均不挂、不改 D4 | 一致。DATA 分册同名单（第 2、3、4 节及第 7 节跨项表）也写明不抄进三张表 |
| 写表位置核对只读不改 | 第 5.4、5.5 节只读 `effect.py`、`simulate.py` 的 `run()`；不调用、不改公式、不改删除范围 | 一致 |
| 白名单不加键 | 第 5.6 节 `PolicyAnalysisTypes` 不增删键，219、220、222 不进异步 | 一致。与 API 分册第 8.1 节口径一致 |
| `metric_id` 留空行上的名字不当注册号 | 第 2 节：219 的 `metric_name`、220 的对象与投向、222 的模板名「不是 `metric_id`，不登记成指标」 | 一致。与 DATA 分册列定义（`metric_name` 是行上名称、`metric_id` 留空）一致 |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。

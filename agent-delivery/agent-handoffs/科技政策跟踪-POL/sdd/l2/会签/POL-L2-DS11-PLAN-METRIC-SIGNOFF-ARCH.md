# POL-L2-DS11-PLAN-METRIC-SIGNOFF-ARCH · 政策分析评价 · 推荐方案报告交互展示 · 指标分册架构会签

- 角色：`agent:arch-agent`（主会话代执，子智能体连续限流后由 coordinator 会话按架构基准直核）
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-METRIC`
- 监管：`human:淮政玮`
- 对照：已签收 `POL-L2-DS11-PLAN-ARCH`（注册表 done）。本页只核分册是否落在架构基准内，不重新设计，不改分册，不改架构稿，不改 task-registry，不改代码
- 范围：SRS 序号 227–231 的指标挂接

## 结论

同意会签

分册挂接收敛为 1 条已有 `M_POLICY_DS_11_POLICY_EVAL_015`（仅 229，D4 保持 mock），其余四叶 `metric_id` 留空不新注册，不改 D4，不改注册表，不调用 `polan.text.simulate.run`，与架构第 9 节行级规定逐条对上。

## 核对

| 项 | 分册写法 | 对架构判定 |
|---|---|---|
| 仅 229 挂已有 015 | 第 2 节挂接表只有 `M_POLICY_DS_11_POLICY_EVAL_015`（GRAPH，D4=mock，挂在 229）；「这一条之外，本二级不新造 `metric_id`」 | 一致。与架构第 9 节「路径与风险行的 `metric_id` 用已有 015」一致 |
| 其余四叶留空 | 第 1、6 节：227 不挂 `M_POLICY_LAYOUT_REC_COUNT`/`M_POLICY_DEEP_171_1`；228 不挂 `M_POLICY_SIMULATE`；230/231 无指标，行上留空；不把 015 指进这四叶 | 一致。与架构「其余三种没有已挂指标，`metric_id` 留空，不新注册」逐句对上 |
| 不迁 `polan.text.simulate.run` | 第 3、5 节核对了 `simulate.py`：`run()` 只做省级力度情景，行上 `metric_id` 固定 `M_POLICY_SIMULATE`，不产出 015；本叶不调用、不改函数、不改 `cfg_model_registry.yaml` | 一致。与架构「不迁推演函数、229 不读 `ads.policy_simulate`」一致；注册表并列表不当成产出证据的判定正确 |
| D16 行级口径 | 第 6 节：灌数单对无号叶 `metric_id` 留空、路径行写 015、`fill_method` 用 `manual`、`gap_item` 写序号和叶子名 | 一致。与架构第 9 节 D16 五列原文一致 |
| D4 不改、mock 不洗白 | 第 4 节：D4 只转述 `指标与501` 229 行 mock，不升 live；缺项行仍是 mock；`GDF-POLICY-MOCK-GATE-L01` 仍 blocked | 一致。与架构口径一致，不把 mock 写成已上线 |
| 三档不改 | 第 1 节：227/228/230/231 维持 501 判定、230/231 不升第四档；采用架构读面（读缺项表无行则空）但不回改 `指标与501` | 一致。调研判定与展示读面分层处理正确 |
| 效能得分不越界 | 第 1、7 节：`evaluation/counts` 短板/机遇条数不在本二级，不读不改 | 一致。与架构第 6 节一致 |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。同意会签不是签收。

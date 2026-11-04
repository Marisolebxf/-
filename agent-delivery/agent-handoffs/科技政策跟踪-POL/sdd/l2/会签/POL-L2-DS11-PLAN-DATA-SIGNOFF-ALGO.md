# POL-L2-DS11-PLAN-DATA-SIGNOFF-ALGO · 政策分析评价 · 推荐方案报告交互展示 · 数据落点算法会签

- 角色：agent:algorithm-agent（监管 human:淮政玮）
- 日期：2026-11-03
- 对象：`sdd/l2/POL-L2-DS11-PLAN-DATA.md`（只读会签，不改分册）
- 监管：human:淮政玮
- 对照：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md` 第 9 节（已签收架构）；代码实读 `repos/lumen-algo-py/vendor/entan-py/polan/text/simulate.py`、`repos/lumen-algo-py/vendor/entan-py/conf/cfg_model_registry.yaml`（均只读）
- 范围：SRS 227–231 五叶的数据落点核对。格式沿同目录 VIZ 侧算法会签；会签环境未见 metric-registry MCP，本文不做指标注册查询

## 结论

同意会签

## 核对

| 项 | 分册写法 | 对算法判定 |
|---|---|---|
| `metric_id` 列规则 | 第 2 节列清单：「路径与风险行固定 `M_POLICY_DS_11_POLICY_EVAL_015`。其余三种留空，写 NULL，不写空字符串」 | ✅ 与 API/METRIC 两册一致且更严（NULL 而非空串）。015 的固定值与代码事实相容：`simulate.py` 无 015 产出，行值只能来自灌数单，不存在「查表即上线」的口子 |
| D16 行级列齐备 | 第 2 节：`metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`，外加 `is_mock=1` 每行必填 | ✅ 与架构稿第 9 节逐列对齐；`is_mock=1` 保证缺项行不被读成已上线，D4=mock 有行级支撑 |
| 228 不灌推演 | 第 4 节、第 8 节表（不灌：省级力度情景、弹性公式现算、采纳时新插入的行）、第 10 节「不把推演情景、弹性曲线、`ads.policy_simulate` 的行灌进本表」 | ✅ 与 `simulate.py` 产出结构对不上号：该表行粒度是方案 × 参数档，推演行是省 × 情景（`scenario_id`/`scope_code`/`curve`），无一列可映射；封死复制路径正确 |
| 229 固定 015、不改 D4、不读图、不改推演函数 | 第 5 节、第 9 节边界表：「现有推演函数不产出这条指标，本叶不改那个函数」 | ✅ 「不产出」与代码实读一致（`run()` 行上 `metric_id` 固定 `M_POLICY_SIMULATE`，无 015）；表行与 nGQL 无关 |
| 唯一新表与四种 `row_kind`、231 不占种类 | 第 1、2 节：仅 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`，四值无第五值；231 不另建行、不设文件列 | ✅ 与架构稿第 9 节一致；不拆四张表、不建文件表，无越界 |
| 灌数单唯一写者 | 第 8 节：`POL-L2-DS11-PLAN-GAPFILL-L01` 建表与灌数，查询请求不灌数、空表返回空，Java 与前端不建表不灌数 | ✅ D18 口径闭合：mock 只经灌数单落表，接口只读；「本单不认领、不执行」边界清楚 |
| 跨项消费边界 | 第 9 节表：`ads.policy_simulate`、`M_POLICY_SIMULATE`、`polan.text.simulate.run` 归推演键，与本表零交互；`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` 不写入方案对照 | ✅ 与注册表侧事实一致：`POLICY_SIMULATE` 的 `ads_table` 是 `ads.policy_simulate`，与 `gkxlumenx_gapfill` 无关；三册边界互认 |

### 算法侧补充

- `fill_method` 固定 `manual` 故不设 `fill_model` 列，与「政策只在方法为 llm 时要求模型名」的注册表惯例一致，避免了无意义的空列。
- 229 的 `metric_id` 固定值是「登记身份」而非「产出凭证」：注册表把 015 并列在 `POLICY_SIMULATE.metric_ids` 下，但 handler 不写它——本分册第 5 节的表述没有把两者混淆。

## 签收边界

- 本页只做算法角色会签。未改分册、未改代码、未碰 task-registry MCP、未 commit/push。
- 不把 `POL-L2-DS11-PLAN-DATA` 标 done 或 ready_to_sign；签收由 human:淮政玮 做。

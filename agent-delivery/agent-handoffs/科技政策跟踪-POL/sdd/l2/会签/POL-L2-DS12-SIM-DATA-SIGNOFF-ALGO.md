# POL-L2-DS12-SIM-DATA-SIGNOFF-ALGO · 政策效果推演 · 科技政策推演 · 数据落点 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-DATA.md`（2026-11-05。本页不改它）
- 对照：`lumen-algo-py/vendor/entan-py` 的 `polan/text/parse.py`、`polan/text/simulate.py`、`polan/clause_job.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_TEXT_PARSE`、`POLICY_SIMULATE`；`PolicyAnalysisTypes.java` 白名单。读法对照 `POL-L2-DS12-SIM-ARCH.md` 第 5、7、9 节与 `POL-L2-DS12-SIM-METRIC.md`。判定引自 `sdd/指标与501.md` §3
- 监管：`human:淮政玮`
- 强度：ponytail off
- 范围：SRS 235–242 的列与行上身份。只读核对。不改分册，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-05 指标身份只取 `指标与501.md`。不读 seed YAML，不编 D1–D3。注册表与函数不一致只记观察，不要求本页改注册表。

`polan.text.parse.run` 从 `dwd.policy_base_info` 做规则截取，写出标题、摘要、结构化要素和自动标签，插入前 `conn.truncate` 清空整张 `ads.policy_text_parse`。每一行的 `metric_id` 固定为字面量 `M_POLICY_TEXT_PARSE`。函数不写推演曲线，不写重点项、影响对象、路径环节、解读段落，插入行里也没有 `M_POLICY_SIMULATE`。

`polan/clause_job.py` 的 `_write_default` 在已有解析行上 `UPDATE` 同一行的 `structured_elements`，把 `clauses` 与 `clause_meta` 写进该 JSON。这条 `UPDATE` 不改 `metric_id`。找不到行时才插入，插入行的 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。条款写入本身不 TRUNCATE。文件注明灌数重灌仍会清空该表。

`polan.text.simulate.run` 只读 `ads.policy_intensity` 中 `scope_type=province` 且力度指数非空的行，取力度前 12 省。三条情景按 `simulated = baseline * (1 + boost * elasticity)` 写出基线、推演值、变化率和逐年曲线，`TRUNCATE` 后写入 `ads.policy_simulate`。行上 `metric_id` 固定为 `M_POLICY_SIMULATE`。函数不写 `gkxlumenx_gapfill` 的结果表或意见表。

`PolicyAnalysisTypes` 的规范键含 `policy_text_parse`，注释为展示智能摘要（226）。没有推演键，也没有重点可视化、影响范围、路径预测、解读报告键。数据分册不把 `parse.run` 或 `simulate.run` 加进该白名单。

`POLICY_TEXT_PARSE` 的 `ext.is_mock` 为 true，`ext.ads_table` 为 `ads.policy_text_parse`。501 把 `M_POLICY_TEXT_PARSE`、`M_POLICY_SIMULATE`、`M_POLICY_RELATION_DEGREE` 的 D4 都写成 `mock`。数据分册不改这些 D4。

| 序号 | 数据分册 | 代码 | 判定 |
|---|---|---|---|
| 235 | `gapfill_policy_sim_result` 的 `row_kind=多维评估`。行上 `metric_id` 留空，写 NULL。不挂 `M_POLICY_SIMULATE`，不挂 `M_POLICY_DEEP_168_1`。`is_mock=1`。D4 仍是 mock | `simulate.run` 只写 `ads.policy_simulate` 的省级力度情景，不写这张缺项表 | 同意 |
| 236 | `gapfill_policy_sim_stakeholder` 的 `row_kind=参与意见`。行上 `metric_id` 留空，写 NULL。不把 `M_POLICY_SIMULATE` 写入本表。`is_mock=1`。请求不插入 | 无意见采集函数。`simulate.run` 不写参与意见 | 同意 |
| 237 | 只读 `gkxlumenx_ads.policy_text_parse`。不加列，不灌，不把解析行写进两张缺项表。行上已有 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`，本单不改。展示请求不调用 `polan.text.parse.run`。D4 保持 mock | `parse.run` 会清空整表后再插入，行上只有 `M_POLICY_TEXT_PARSE`。条款 `UPDATE` 不改该列 | 同意 |
| 238 | 与 235 同一张结果表，`row_kind=重点`。`metric_id` 留空。不挂 `M_POLICY_FOCUS_INDEX`。不把 237 的解析标签写进标题或明细。`is_mock=1` | 未见重点可视化函数 | 同意 |
| 239 | 同一张结果表，`row_kind=影响范围`。`metric_id` 留空。不挂 `M_POLICY_SIMULATE`。不把 234 的空间预测行抄进本种类。`is_mock=1` | `simulate.run` 不写影响范围 | 同意 |
| 240 | 不设表，不设列。不把 `M_POLICY_RELATION_DEGREE` 写进结果表或意见表。不写 nGQL | 本单不新建查图函数 | 同意 |
| 241 | 同一张结果表，`row_kind=路径环节`。`metric_id` 留空。不挂 `M_POLICY_LAYOUT_REC_COUNT`，不挂 `M_POLICY_DS_11_POLICY_EVAL_015`。`is_mock=1` | 未见路径预测函数。`simulate.run` 不写路径环节，也不写 015 | 同意 |
| 242 | 同一张结果表，`row_kind=解读段落`。内容只在 `body_text`。`metric_id` 留空。不把 226 的 `summary` 抄进正文。不设文件路径。`is_mock=1` | 未见解读报告函数。`parse.run` 的摘要不是这四段 | 同意 |

结果表五种行与意见表参与意见行的 `metric_id` 都是可空列，约束写明留空、写 NULL、不写空字符串。第 12 节写明 `M_POLICY_SIMULATE` 只挂 232–234，不写入本单六种业务行。两张表都要求 `is_mock=1`，并写明据此避免把缺项行读成已上线。D4 保持 mock。`GDF-POLICY-MOCK-GATE-L01` 仍写 blocked，不写成已解开。

237 不建文本解析用的 gapfill 表，不改 `policy_text_parse` 已有列，不把 `M_POLICY_TEXT_PARSE` 改成别的号，也不把该号抄进两张缺项表。第 9 节写明展示请求不调用 `polan.text.parse.run`，因为该函数会清空整张解析表。第 11 节把灌数单 DoD 里的「文本解析」收成不灌、不写 `gkxlumenx_ads.policy_text_parse`、不在两张 gapfill 表里加文本解析行。

观察（不构成不同意，也不要求改注册表或改分册）：

- 架构稿第 1.4 节把条款隔离的语义写成「不含 `clauses` 键的行」，判别写法交给本数据分册。条款代码是更新同一条解析行，不是另插一行。数据分册据此规定：含有 `clauses` 的行仍读标题、摘要、标签和其余要素，返回前从 `structured_elements` 去掉 `clauses` 与 `clause_meta`。这不调用 `parse.run`，也不改行上已有的 `M_POLICY_TEXT_PARSE`。
- `POLICY_TEXT_PARSE` 的 `metric_ids` 同时列 `M_POLICY_TEXT_PARSE` 与 `M_POLICY_DS_11_POLICY_EVAL_012`。`parse.run` 只写前一个号。012 留在评价页 226。本数据分册不挂 012，不改注册表。
- `POLICY_SIMULATE` 的 `metric_ids` 同时列 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015`。`simulate.run` 只写前一个号，且只写入 `ads.policy_simulate`。本数据分册不把这两个号写进结果表或意见表。

未发现结果表或意见表行上写入 `M_POLICY_SIMULATE`。未发现 237 改写解析表上已有的 `M_POLICY_TEXT_PARSE`。未发现把 `is_mock=1` 的缺项行写成已上线，或把 D4 改出 mock。未发现展示请求或本单执行路径调用 `polan.text.parse.run`。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改数据分册，不改架构稿，不改指标分册，不改算法代码，不改模型注册表。

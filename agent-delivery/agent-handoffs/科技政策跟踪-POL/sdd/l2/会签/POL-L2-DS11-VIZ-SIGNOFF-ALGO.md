# POL-L2-DS11-VIZ-SIGNOFF-ALGO · 政策分析评价 · 政策分析报告可视化呈现 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-VIZ-ARCH.md`（2026-11-03。本页不改它）
- 对照：`lumen-algo-py/vendor/entan-py` 的 `polan/eval/effect.py`、`polan/eval/layout.py`、`polan/eval/focus.py`、`polan/text/simulate.py`、`polan/text/parse.py`、`polan/job.py`、`polan/basic/indicators.py`、`polan/timeseries_board.py`、`polan/regional_board.py`、`conf/cfg_model_registry.yaml`；`PolicyAnalysisTypes.java` 白名单。判定引自 `sdd/指标与501.md` 219–222。边界对照 `POL-L2-DS11-READ-ARCH.md` 与说明书第 11.2 节
- 监管：`human:淮政玮`
- 范围：SRS 219–222。只读核对。不改已有文件，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

不同意会签。阻塞只在序号 222。

点名 `POL-L2-DS11-VIZ-ARCH.md` 第 5.4 节、第 8 节签收表的 222 行、第 9 节表的 222 行。这三处把模板选用行的灌数写成 `POL-L2-DS11-READ-GAPFILL-L01`，并写「灌什么由解读二级定」。`POL-L2-DS11-READ-ARCH.md` 第 7 节末段与第 8 节表写明：壳表只服务 224、225，该灌数单只灌解读条目和多媒体条目，不灌模板，序号 222 的模板选用不在解读叶灌入。可视化自己的 `POL-L2-DS11-VIZ-GAPFILL-L01` 只灌趋势点和分区对照。

222 在注册表里没有导出模型，`polan/eval/` 也没有导出函数。两张已点名的灌数单都不写模板选用行。模板区因此一直空，导出也空。这是用 501 的空态充当这一叶，和第 7 节「不允许用 501 充当四叶的画面」对不上。

219、220、221 的指标挂接不是不同意的理由。

## 核对

2026-11-03 指标身份只取 `指标与501.md`。不读 seed YAML，不编 D1–D3。注册表与函数不一致只记观察，不要求本页改注册表。

| 序号 | 指标分册 | 代码 | 架构稿 |
|---|---|---|---|
| 219 | 未见。判定 501。不借用 `M_POLICY_TIMESERIES` | 无趋势模型。`effect.run` 把 `M_POLICY_EFFECT_SCORE` 写入 `ads.policy_effect`（`scope_type=region_effect`），把 `M_POLICY_IMPLEMENTATION_EFFECT` 写入 `ads.policy_metric_timeseries`（每个区域一行，`stat_date` 为运行当天）。`indicators.py` 把 `M_POLICY_TIMESERIES` 写入 `ads.policy_timeseries`。`policy_timeseries` 走 `timeseries_board`，是产业结果板，不写这条 ADS | 不改挂这三条，也不把落地实效当成趋势图。只要趋势时不建任务、不转发 `gkxlumen-topic-async-service`、不调 Python。读 `gapfill_policy_eval_trend`，无行则图空 |
| 220 | 未见。判定 501。不挂全景分布类 STAT | 无分区效果模型。`policy_regional` 走 `regional_board`，按产业 VID 归经济区。级别、类型、全国分布在 `indicators.py`，指标是 `M_POLICY_LEVEL_DIST`、`M_POLICY_TYPE_DIST`、`M_POLICY_NATIONAL_DIST` | 不挂这些分布。读 `gapfill_policy_eval_partition`，无行则图空 |
| 221 | 未见。判定跨项索引。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` | `eval` 无共词模块。`focus.run` 把关联度留在焦点行，行上 `metric_id` 为 `M_POLICY_FOCUS_INDEX/M_POLICY_RELATION_DEGREE`。注册表 `POLICY_RE` 另挂 `M_POLICY_RELATION_DEGREE` | 只消费第 7 项已有子图。不把共词网络写成新算法，不新造图指标，不调用上述函数 |
| 222 | 未见。判定 501。无指标，无导出模型 | 注册表无导出模型。`PolicyAnalysisTypes` 白名单无导出键 | 读 `gapfill_policy_eval_shell` 的模板选用。不走 `report/jobs`，不走全景 `benchmark-report`。写入方见结论，此行阻塞 |

`PolicyAnalysisTypes` 的规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`。没有趋势图、分区对比、导出。219、220 不进入这六键。`polan.text.simulate.run` 只写省级力度情景，`metric_id` 固定 `M_POLICY_SIMULATE`，本叶不调用。

观察（不构成不同意，也不要求改注册表）：

- 第 5.1 节把 `M_POLICY_IMPLEMENTATION_EFFECT` 与 `M_POLICY_EFFECT_SCORE` 都写成写入 `ads.policy_effect`。`effect.run` 只把效果分写入该表；落地实效写入 `ads.policy_metric_timeseries`。注册表 `POLICY_EFFECT` 的 `ads_table` 只写了 `ads.policy_effect`。两处都不挂 219，本叶不调用 `effect.run`。
- 第 2 节写「实施路径仍走异步管道」。白名单没有路径键。`simulate.run` 不产出路径与风险。方案稿不把序号 229 送进这条管道。本叶第 6 节已把 229 排除。本页不据此要求调用 `simulate.run`。

219、220 的缺项表行是灌入的 mock，D4 仍是 `mock`。不新造 `metric_id`。221 仍是跨项索引。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。222 要有会写入模板选用行、且不拿 224、225 解读条目充当的灌数归属，才有条件再看这份会签。

## 第二轮（2026-11-03 返工后）

### 结论

同意会签。

第一轮只因序号 222 没有写入方。返工后模板选用读 `gapfill_policy_eval_template`，灌数单是 `POL-L2-DS11-VIZ-GAPFILL-L01`，不读 `gapfill_policy_eval_shell`，不用 224、225 的解读条目或多媒体条目充当。222 不再阻塞。

第 5.1 节已写成：`M_POLICY_EFFECT_SCORE` 写入 `ads.policy_effect`，`M_POLICY_IMPLEMENTATION_EFFECT` 写入 `ads.policy_metric_timeseries`，两条都不挂 219，本叶不调用 `effect.run`。`polan/eval/effect.py` 的 `run()` 与这句一致。

### 核对

| 序号 | 架构稿 | 代码 | 判定 |
|---|---|---|---|
| 219 | 第 5.1 节：效果分写入 `ads.policy_effect`，落地实效写入 `ads.policy_metric_timeseries`。都不挂本叶。不调用 `effect.run`。趋势读 `gapfill_policy_eval_trend`，灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` | `effect.py` 把 `M_POLICY_EFFECT_SCORE` 插入 `ads.policy_effect`（`scope_type=region_effect`），把 `M_POLICY_IMPLEMENTATION_EFFECT` 插入 `ads.policy_metric_timeseries` | 同意 |
| 220 | 读 `gapfill_policy_eval_partition`。不挂全景分布。同一张灌数单 | 本叶不调用分区效果函数 | 同意 |
| 221 | 只消费第 7 项已有子图。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。不把共词写成新算法 | 本叶不新开导出或图计算 | 同意 |
| 222 | 第 2 节、第 5.4 节、第 8 节、第 9 节：建 `gapfill_policy_eval_template`，灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` 写入模板选用行。`shells` 只读这张表。不读壳表，不用 224、225 充当。不走 `report/jobs`，不走 `benchmark-report` | `PolicyAnalysisTypes` 白名单无导出键。本叶不要求调用导出函数 | 同意。不再阻塞 |

`PolicyAnalysisTypes` 仍在 `lumen-svc-platform` 的 `gkxlumen-topic-async-service`。规范键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`、`policy_focus_ads`、`policy_text_parse`。没有趋势图、分区对比、模板导出。219、220、222 不进入这些键。

未发现架构稿要求调用并不产出本叶结果的函数。第 5.1 节与 `effect.py` 一致，第一轮那条「两指标都写入 `ads.policy_effect`」的句子已经改掉。不要求改注册表。

### 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改架构稿，不改算法代码，不改模型注册表。

## 第三轮（2026-11-03 晚）

- 角色：`agent:algorithm-agent`
- 对象：`POL-L2-DS11-VIZ-ARCH.md` 当前全文。本轮重读，不沿用第二轮结论
- 对照：`sdd/指标与501.md` 第 2 节 219–222；`lumen-algo-py/vendor/entan-py/api/policy_routes.py` 的 `_MODEL_TABLE`；`polan/eval/` 目录；`polan/eval/effect.py` 的 `run()`
- 本轮不改架构稿，不改代码，不改 task-registry

### 结论

同意会签。

219 不改挂 `M_POLICY_TIMESERIES`，也不把 `M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT` 当成趋势图。第 5.1 节的落表与 `effect.py` 一致。220 不挂全景分布。221 不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`，不把共词网络写成新算法。222 读 `gapfill_policy_eval_template`，不走 `report/jobs`，不走 `benchmark-report`，缺项表没有被写成已有真算法。不新造 `metric_id`，不改 D4。

### 核对

| 序号 | 指标分册第 2 节 | 代码 | 架构稿 | 判定 |
|---|---|---|---|---|
| 219 | 未见。判定 501。不借用 `M_POLICY_TIMESERIES` | `_MODEL_TABLE` 无趋势键。`polan/eval/` 无趋势图模块。`effect.run` 把 `M_POLICY_EFFECT_SCORE` 插入 `ads.policy_effect`（`scope_type=region_effect`），把 `M_POLICY_IMPLEMENTATION_EFFECT` 插入 `ads.policy_metric_timeseries`（每个区域一行，`stat_date` 为运行当天）。这是效果行，不是多维趋势图 | 第 5.1 节按这两张表写落表。两条都不挂本叶，不调用 `effect.run`。趋势只读 `gapfill_policy_eval_trend`。第 6 节排除全景时序和效果分 | 同意。落表与 `effect.py` 一致 |
| 220 | 未见。判定 501。不挂全景分布类 STAT | `_MODEL_TABLE` 无分区键。`polan/eval/` 无分区对比模块 | 只读 `gapfill_policy_eval_partition`。第 5.2、第 6、第 9 节不挂全国分布、类型分布、级别分布 | 同意 |
| 221 | 未见。判定跨项索引。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` | `polan/eval/` 无共词模块。`_MODEL_TABLE` 无图计算键 | 第 5.3 节只消费第 7 项已有子图。不挂上述两个 id。不把共词网络写成新算法，不新造图指标 | 同意 |
| 222 | 未见。判定 501。无指标，无导出模型，与核增研报无关 | `_MODEL_TABLE` 无导出键。`polan/eval/` 无导出模块 | 第 5.4 节读 `gapfill_policy_eval_template`，灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01`。写明没有导出模型。不走 `report/jobs`，不走 `benchmark-report`。不读壳表，不用 224、225 充当 | 同意。缺项表是新建 mock 读面，不是已有真算法 |

`_MODEL_TABLE` 的键只有 `focus`、`opportunity`、`intensity`、`effect`、`gap`、`layout`、`guide`、`guard`。`effect` 只读 `policy_effect` 且 `scope_type=region_effect`，对不上 219 的趋势图。

`polan/eval/` 现有模块是 `focus`、`intensity`、`effect`、`gap`、`opportunity`、`layout`、`focus_one`、`ds_composite`。没有趋势图模块，没有分区对比模块。`effect.py`、`intensity.py` 写入 `policy_metric_timeseries` 的是指标行，本叶不拿来当 219、220 的图。

观察（不构成不同意）：第 3.1 节 219 行把 `effect.run` 收成「写入 `ads.policy_effect` 和效果分」，没有点名 `policy_metric_timeseries`。规范落表在第 5.1 节，与 `effect.py` 第 58–81 行的两次 `insert` 一致。本叶不调用 `effect.run`。

219、220、222 在指标分册仍是 501、无专属 `metric_id`。架构保留这个判定，不新造 `metric_id`，不改 D4。缺项行是灌入的 mock，无行则空。

### 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。

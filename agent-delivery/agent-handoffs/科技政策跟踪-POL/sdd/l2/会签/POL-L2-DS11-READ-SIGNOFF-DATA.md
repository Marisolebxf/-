# POL-L2-DS11-READ-SIGNOFF-DATA · 政策分析评价 · 结果解读报告多维展示 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-READ-ARCH`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-READ-ARCH` 第 8 节；`科技政策跟踪-系统详细设计说明书.md` 第 11.2 节「评价 · 解读 222–226」；`lumen-algo-py/vendor/entan-py` 的 `polan.eval.focus`、`polan.eval.gap`、`polan.text.parse`、`polan.eval.opportunity`、`polan.common.db` SCHEMA
- 范围：SRS 223–226
- 结论：**同意会签**

本页只核对架构第 8 节的数据落点是否与说明书第 11.2 节、以及已有计算的落表一致。下游 DATA 分册还没有，本页不等它，也不定字段级 DDL。不改架构稿，不改任务状态，不建库，不灌数。

## 核对

| 口径 | 架构第 8 节 | 代码落表 | 判定 |
|---|---|---|---|
| 223 短板只读已有 `ads.policy_effect`（`scope_type=region_gap`），不建 `ads.policy_gap`，不加列 | 新建：否。要落的是区域、`shortboard_cnt`、分项原因。行上已有 `is_mock` 与 `QPOL-02`。不新开灌数单 | `gap.run` 写入 `{ads}.policy_effect`，`scope_type=region_gap`。计数用已有列 `shortboard_cnt`，分项在已有 `ext.reasons`，`ext.is_mock=true`，`ext.pending=QPOL-02`。行上 `metric_id` 仍是 `M_POLICY_SHORTBOARD_COUNT`。SCHEMA 没有 `policy_gap`。`GET /v1/policy/analysis/gap` 只查这张表、这个范围，不调用 `gap.run` | 一致 |
| 223 焦点只读已有 `ads.policy_focus`（`policy_id` 非空），不建 `gapfill_policy_eval_focus`。`focus.run` 不删 `policy_id` 为空的机遇行 | 新建：否。要落的是 `focus_score`、标题、一句说明。`metric_id` 仍是 `M_POLICY_FOCUS_INDEX/M_POLICY_RELATION_DEGREE`。Job 调用已有 `focus.run`，不改删除范围 | `focus.run` 写入 `{ads}.policy_focus`：`focus_score`，`ext.title`，`ext.explanation`。删除条件是 `WHERE policy_id IS NOT NULL`。机遇行由 `opportunity.run` 写成 `policy_id IS NULL`，只被 `WHERE policy_id IS NULL` 那条删除清掉。中台 focus 读面是同一条件 | 一致 |
| 226 只读已有 `ads.policy_text_parse.summary`，不建 `gapfill_policy_eval_summary`。请求不调用 `parse.run` | 新建：否。展示 Job 只查询。解析批次仍是已有 `parse.run`，不在请求里调用 | SCHEMA 已有 `summary`。`parse.run` 用规则截取写入该列，行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`，然后 `truncate` 整张表。条款结构化写在同一张表的 `structured_elements`，条款批次声明不 TRUNCATE，并写明灌数重灌会清空该表。请求只查、不调用 `parse.run` | 一致 |
| 224、225 只新建 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。不写 ODS、DWD、ADS、供应方库。不灌视频、PDF、模板。序号 222 的模板选用不由本叶灌 | 新建：是，只这一张。解读条目：专题或指标名、一句结论、一句应用建议。多媒体条目：标题、一句说明。不灌视频、PDF、模板。序号 222 不在本叶灌入 | 这四叶的已有计算里没有分主题解读，也没有多媒体。没有表、也没有算法，退路只在 `gkxlumenx_gapfill` | 一致 |
| shell 行的 `metric_id` 留空，不新注册。`fill_method` 用 `manual`。查询不插入。无行则空 | 每一行带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。没有已挂指标的，`metric_id` 留空。`fill_method` 用 `manual`。`gap_item` 写序号和叶子名。查询请求不灌数。表里没有行则空 | 本页不新注册指标。223、226 沿用行上已有 `metric_id`，不改挂。shell 不设 `fill_model` | 一致 |
| 说明书 11.2 把 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`、`gapfill_policy_eval_shell` 写在一行。架构收窄成只建 shell | 焦点和摘要已有 ADS 和计算，不建前两张。shell 保留，并且只服务 224、225 | 符合第 11 节「已经有 ADS 表、也有可调用计算的，不新建表」。焦点名称和一句说明已在 `policy_focus.ext`。摘要已在 `policy_text_parse.summary`。短板已在 `policy_effect`。三张缺项表里只有 shell 没有对应的 ADS 和计算 | 同意收窄 |

## 库表名

| 序号 | 架构 | 代码 |
|---|---|---|
| 223 短板 | `ads.policy_effect`（`scope_type=region_gap`） | `{ads}.policy_effect`。无 `policy_gap` |
| 223 焦点 | `ads.policy_focus`（`policy_id` 非空） | `{ads}.policy_focus`。机遇行 `policy_id` 为空，不在本读面 |
| 224、225 | `gkxlumenx_gapfill.gapfill_policy_eval_shell` | 新建，只在 `gkxlumenx_gapfill` |
| 226 | `ads.policy_text_parse` | `{ads}.policy_text_parse`，读已有列 `summary` |

223、226 的表名是 `policy_effect`、`policy_focus`、`policy_text_parse`。代码 SCHEMA 的默认库是 `demo_gkxlumenx_ads`。架构写作 `ads.<表名>`，指的是这一组已有表。不把这三张表再放到 `gkxlumenx_gapfill`，也不往 ODS、DWD、ADS、供应方库加表或加列。

shell 的 `metric_id` 留空，不新注册。`fill_method=manual`。列的其余字段留给 `POL-L2-DS11-READ-DATA`，本页不定 DDL。

## 灌数单

`POL-L2-DS11-READ-GAPFILL-L01` 只灌 shell 的解读条目和多媒体条目。本页不执行。223、226 不新开灌数单。要补批次时仍走已有 `gap.run`、`focus.run`、`parse.run`，由后续 DATA 排。展示请求不调用 `parse.run`。

本页不把任务标 done，签收仍由 human:淮政玮 做。

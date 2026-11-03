# POL-L2-DS11-READ-DATA-SIGNOFF · 政策分析评价 · 结果解读报告多维展示 · 数据分册会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`sdd/l2/POL-L2-DS11-READ-DATA.md`
- 监管：`human:淮政玮`
- 对照：已签收 `sdd/l2/POL-L2-DS11-READ-ARCH.md` 第 4、7、8 节；`storage/POLICY/stores/mysql/ads.md` 的 `policy_effect`、`policy_focus`、`policy_text_parse`；说明书第 11.2 节「评价 · 解读 223–226」
- 范围：SRS 223–226
- 结论：**同意**

本页只核数据分册是否落在已签收架构内。不改数据分册正文，不改说明书，不改任务状态，不建库，不灌数。

## 核对

| 口径 | 数据分册 | 已签收架构 | 判定 |
|---|---|---|---|
| 只新建 `gkxlumenx_gapfill.gapfill_policy_eval_shell` | 第 1、5、9 节。只这一张。建表由灌数单落地，本单不执行 | 第 8 节：224、225 新建这一张。第 7 节收窄后只留 shell | 一致 |
| 只灌 224 解读条目（专题或指标名、一句结论、一句应用建议）和 225 标题加一句说明 | 第 5 节。`entry_kind` 与 `gap_item` 成对。`POL-L2-DS11-READ-GAPFILL-L01` 只灌这两类 | 第 8 节同一内容。灌数单只灌这两类行 | 一致 |
| 不灌视频、PDF、模板选用 | 第 5、7、8、9 节。不设视频、PDF、对象键、模板号。序号 222 不写入 shell | 第 4.3、7、8 节。模板选用不在本叶灌入 | 一致 |
| 不建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary` | 第 1、4、6、9 节 | 第 7、8 节。焦点和摘要已有 ADS，不建这两张 | 一致 |
| 223 短板读 `ads.policy_effect`（`scope_type=region_gap`） | 第 3 节。`shortboard_cnt`、`scope_code`、`scope_name`、`ext.reasons`。`counts` 不调用 `gap.run`。无行则空，不造 0 | 第 8 节。不建 `ads.policy_gap`。不新开灌数单 | 一致 |
| 223 焦点读 `ads.policy_focus`（`policy_id` 非空） | 第 4 节。`focus_score`、`ext.title`、`ext.explanation`。`policy_id` 为空的行不返回。无行则空 | 第 8 节。Job 调用已有 `focus.run` 后再读。不改删除范围 | 一致 |
| 226 读 `ads.policy_text_parse.summary` | 第 6 节。返回列只取 `summary`。展示请求不调用 `parse.run`。无行则空。`summary` 为空不补句 | 第 8 节。不把改稿和推送记录灌进去 | 一致 |
| 不写 ODS、DWD、ADS，不加已有 ADS 列，不写供应方库 | 第 1、9 节。本单和灌数单不往三张已有表插入 shell 行。已有 `run()` 仍按原路径，本单不改 | 第 6、8 节。不加 ODS、DWD、ADS 表 | 一致 |
| 不改 D4，不新造 `metric_id` | 全文。D4 保持 mock。shell 无专属号，`metric_id` 留空；解读行只许填写已经登记的号。223、226 沿用行上已有号 | 第 8 节。没有已挂指标的留空。`fill_method=manual` | 一致 |
| 无行则空 | 第 1–6、9 节。查询不插入。接口不直接返回写死的 mock | 第 3、7 节。表里没有行就返回空 | 一致 |

shell 行带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。`fill_method` 固定 `manual`，不设 `fill_model`。`is_mock` 固定为 1。生产配置不读 `gkxlumenx_gapfill`。

已有列与 `ads.md` 及现有 `run()` 对齐：`policy_effect.shortboard_cnt` 与 `ext.reasons` 由 `polan.eval.gap.run` 写入；`policy_focus.focus_score`、`ext.title`、`ext.explanation` 由 `polan.eval.focus.run` 写入，删除条件是 `policy_id IS NOT NULL`；`policy_text_parse.summary` 已有，`polan.text.parse.run` 规则截取后清空整表。数据分册不加列，不改这些函数。

签收仍由 human:淮政玮 做。

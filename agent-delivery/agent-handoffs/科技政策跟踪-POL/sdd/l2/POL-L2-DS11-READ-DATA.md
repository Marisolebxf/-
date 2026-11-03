# POL-L2-DS11-READ-DATA · 政策分析评价 · 结果解读报告多维展示 · 数据落点

- 任务：`POL-L2-DS11-READ-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游架构：`POL-L2-DS11-READ-ARCH`（2026-11-03 human:淮政玮签收，第 8 节）。本单只写数据落点，不改那份架构，不改图。

本叶只定政策分析评价二级「结果解读报告多维展示」的数据落点。SRS 序号 **223–226**。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-READ-ARCH.md` 第 8 节、同目录已签收会签页、`storage/POLICY/stores/mysql/ads.md` 里已登记的 `policy_effect`、`policy_focus`、`policy_text_parse`。写入核对只读 `lumen-algo-py/vendor/entan-py` 的 `polan.eval.gap.run`、`polan.eval.focus.run`、`polan.text.parse.run`。指标沿用已有 `metric_id`。不新造 `metric_id`，不改 D4。

## 1. 范围

四叶都在政策分析评价里完成。浏览器只打 `/display/v1/policy/**`。查询只读表。查询请求不灌数。表里没有行就返回空。接口不直接返回写死的 mock。

| 序号 | 叶子 | 库 | 表 | 本单 |
|---|---|---|---|---|
| 223 短板 | 热点问题分析看板 · 短板条数 | 已有政策 ADS | `policy_effect`，只取 `scope_type=region_gap` | 不加列，不建 `ads.policy_gap`，不新开灌数 |
| 223 焦点 | 热点问题分析看板 · 焦点指数 | 同一已有 ADS | `policy_focus`，只取 `policy_id` 非空 | 不加列，不建 `gapfill_policy_eval_focus` |
| 224 | 分主题分指标互动解读 | `gkxlumenx_gapfill` | `gapfill_policy_eval_shell` 的解读行 | 本单定列。建表与灌数在灌数单 |
| 225 | 多媒体辅助解读 | 同一张缺项表 | `gapfill_policy_eval_shell` 的多媒体行 | 与 224 同一张表，不另建 |
| 226 | 智能摘要与结论推送 | 同一已有 ADS | `policy_text_parse`，只读已有 `summary` | 不加列，不建 `gapfill_policy_eval_summary` |

223 短板、223 焦点、226 的 D4 仍是 `mock`。224、225 没有专属指标，行是以后灌入的 mock，D4 不因缺项表而改绿。`QPOL-02` 未闭合。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本叶不把 mock 写成已上线，也不把该闸门写成已解开。

三张已有表的物理库是这三份 `run()` 正在写的 `{ads}`。`polan.common.db` 的默认库，以及 `ads.md` 的登记名，都是 `demo_gkxlumenx_ads`。架构写作 `ads.<表名>`，指的就是这一组已有表。本叶不把它们复制到 `gkxlumenx_ads` 或 `gkxlumenx_gapfill`，也不把行写入 `gkxlumenx_ods`、`gkxlumenx_dwd`、供应方库。查询读 `run()` 写入的同一张表。

本叶唯一新建的表是 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。本单只定列，不建库，不插入。

## 2. 223 短板条数

不另建表，不加列，不建 `ads.policy_gap`。`polan.eval.gap.run` 已把区域短板写入 `policy_effect`，`scope_type` 固定 `region_gap`。`GET /display/v1/policy/evaluation/counts` 由 `gkxlumen-element` 只读这些行的 `shortboard_cnt`。这次读取不调用 `gap.run`。

粒度：一行是一个区域。`scope_code`、`scope_name` 用 `run()` 已有的省级代码和名称。计数在已有列 `shortboard_cnt`。分项原因在已有 `ext`，不拆成新列。

`run()` 现写的分项在 `ext.reasons`。每一项有 `dim`。产业覆盖盲区另有 `count` 与 `detail`。政策失效占比偏高、平均政策力度不足另有 `value` 与 `threshold`。`ext.explanation` 是同一行上已有的一句说明。`ext.is_mock` 为真，`ext.pending` 为 `QPOL-02`，`ext.model` 为 `gap`。本叶不改公式，不改权重，不新增 `is_mock` 列。

| 已有位置 | 本叶怎么读 |
|---|---|
| `policy_effect.scope_type` | 只取 `region_gap`。不读 `region_effect`、`region_layout`、`ds_guide`、`ds_guard` |
| `policy_effect.scope_code`、`scope_name` | 区域代码和名称 |
| `policy_effect.shortboard_cnt` | 该区域短板条数 |
| `policy_effect.ext` | JSON。原因在 `reasons`。`is_mock` 为真，`pending` 为 `QPOL-02` |
| `policy_effect.metric_id` | 行上已有 `M_POLICY_SHORTBOARD_COUNT`。不改挂 |
| `policy_effect.calc_batch_id` | 保持 `run()` 现有写法 |
| `policy_effect.effect_score`、`layout_rec_cnt`、`impl_effect` | `gap.run` 现写空。本叶不填，也不把它们当成短板条数 |

无行则计数空，不造 0，不在接口里写死条数。D4 保持 mock。这张区域短板表不是序号 224 的解读条目，也不是序号 226 的摘要。

本单不新开灌数。要补批次时只跑已有 `polan.eval.gap.run`。本单不执行。`gap.run` 的删除范围维持现状：只删 `scope_type=region_gap` 的行。不把 `GDF-POLICY-MDC-STAT-L01` 写成已覆盖本指标。

## 3. 223 焦点指数

不另建表，不加列，不建 `gapfill_policy_eval_focus`。焦点名称和一句说明已经在 `policy_focus.ext`。

粒度：一行是一条政策。本叶只取 `policy_id` 非空的行。`policy_id` 为空的行是机遇汇总，由 `polan.eval.opportunity.run` 写入，指标是 `M_POLICY_OPPORTUNITY_COUNT`。机遇没有 223–226 的序号，不进本读面。

`polan.eval.focus.run` 的删除语句是 `DELETE FROM {ads}.policy_focus WHERE policy_id IS NOT NULL`，然后只插入政策粒度行。这个删除不扩到 `policy_id` 为空的机遇行。机遇行只由 `opportunity.run` 自己的 `WHERE policy_id IS NULL` 清掉。本叶不改这两条删除范围。

看板上要读的是 `focus_score`，以及 `ext` 里已有的 `title`、`explanation`。这就是说明书第 11.2 节写的「焦点问题名称和一句说明」，落在已有表上。

| 已有位置 | 本叶怎么读 |
|---|---|
| `policy_focus.policy_id` | 只取非空。空值行不进焦点看板 |
| `policy_focus.focus_score` | 焦点指数。只来自表上的查询结果 |
| `policy_focus.ext.title` | 焦点名称。`focus.run` 现写政策标题 |
| `policy_focus.ext.explanation` | 一句说明 |
| `policy_focus.ext` | 同一 JSON 里已有 `is_mock` 为真，`pending` 为 `QPOL-02/03`，`model` 为 `focus`。本叶不改这些键 |
| `policy_focus.metric_id` | 行上已有 `M_POLICY_FOCUS_INDEX/M_POLICY_RELATION_DEGREE`。不改挂，不拆成新指标 |
| `policy_focus.relation_degree` | 同一行已有。本叶不把它改挂到 223，也不为此读图 |
| `policy_focus.opportunity_cnt` | 政策粒度行上 `focus.run` 现写空。本叶不填，也不把机遇计数读进焦点块 |
| `policy_focus.region_code`、`calc_batch_id` | 保持 `run()` 现有写法 |

展示 Job 的种类是已签收架构定的 `policy_focus_ads`：调用已有 `polan.eval.focus.run`，再读上述行。本单不执行 `focus.run`，不改公式，不改权重。带 items 的既有 `policy_focus` 作业保持原样，不把 harness 的返回当成这张表的另一套写入。

无行则焦点块空，不造 0，不返回写死的指数。D4 保持 mock。

## 4. 224、225 解读条目与多媒体条目

库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_shell`。这是本单唯一要定的新表。224 与 225 共用这一张。不拆成两张表。

一行是一条解读，或一条多媒体说明。一行不是一个视频，不是一段动画，不是一个图形文件，不是一份 PDF，不是一份模板。序号 222 的模板选用不写入这张表。

`entry_kind` 只有两个值：

| 值 | 序号 | 这一行放什么 |
|---|---|---|
| `解读` | 224 | 专题或指标名、一句结论、一句应用建议 |
| `多媒体` | 225 | 标题、一句说明 |

点选专题或指标，只在已经返回的 `解读` 行里筛选。不另起计算，不新开路径。`GET /display/v1/policy/evaluation/shells` 由 `gkxlumen-element` 只读这张表。`gkxlumen-display` 不直连库。不写入 ODS、DWD、ADS、供应方库。不写对象存储，前端不直连 RustFS。

下列是必要列。建表语句由灌数单 `POL-L2-DS11-READ-GAPFILL-L01` 落地。本单不执行该单，也不在这里给出可执行脚本。这张列清单不是可执行 SQL。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `entry_kind` | varchar(16) | 否 | `解读` 或 `多媒体` |
| `topic_or_metric` | varchar(256) | 是 | `解读` 行必填：专题或指标名。`多媒体` 行空 |
| `conclusion_text` | text | 是 | `解读` 行必填：一句结论。`多媒体` 行空 |
| `suggestion_text` | text | 是 | `解读` 行必填：一句应用建议。`多媒体` 行空 |
| `title` | varchar(256) | 是 | `多媒体` 行必填：标题。`解读` 行空 |
| `caption` | text | 是 | `多媒体` 行必填：一句说明。`解读` 行空 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 没有已挂指标则留空。条目若指向已经存在的指标，只写那个已有 `metric_id`。不新注册 |
| `gap_item` | varchar(128) | 否 | `解读` 行固定 `224 分主题分指标互动解读`。`多媒体` 行固定 `225 多媒体辅助解读`。不写序号 222 |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

`fill_method` 固定 `manual`，因此不设 `fill_model`。政策只在方法为 `llm` 时要求模型名。

`metric_id` 留空是 224、225 的常态。这两叶没有专属指标。不允许为了填满该列，把 `M_POLICY_FOCUS_INDEX`、`M_POLICY_SHORTBOARD_COUNT`、`M_POLICY_DS_11_POLICY_EVAL_012` 或 `M_POLICY_TEXT_PARSE` 抄到壳表上。抄已有指标只发生在这一行本来就在指向那个已注册指标的时候。

不设视频地址、动画地址、图形文件、对象键、PDF、模板编号、模板正文。不灌这些内容。序号 222 的模板表不在本叶，本叶不往壳表写模板行。

不把 226 的 `summary` 复制成解读行。不把 223 的 `ext.title`、`ext.explanation` 复制成解读行或多媒体行。

表空则对应块空。查询不插入行。

## 5. 226 智能摘要与结论推送

不另建表，不加列，不建 `gapfill_policy_eval_summary`。摘要已经在 `policy_text_parse.summary`。

粒度：一行是一条政策的解析结果。展示只读 `summary`。展示挂接用已有 `M_POLICY_DS_11_POLICY_EVAL_012`，这是该列的读面身份。行上的 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。本叶不改这个 `metric_id`，也不把规则截取改成大模型。

`polan.text.parse.run` 用规则截取写入 `summary`：取摘要或正文，压成一行，超过 80 字则截断并加省略号。写入前对整张 `{ads}.policy_text_parse` 做清空，再插入解析行。条款结构化写在同一张表的 `structured_elements` 上。条款批次自己不清空这张表，并写明解析重灌会把该表清空。因此展示请求不调用 `parse.run`。一次展示查询若调用它，会把条款行一起清掉。

| 已有位置 | 本叶怎么读 |
|---|---|
| `policy_text_parse.summary` | 智能摘要。只来自表上的查询结果 |
| `policy_text_parse.policy_id`、`title` | 这条摘要属于哪条政策。名称用表上已有标题 |
| `policy_text_parse.metric_id` | 行上已有 `M_POLICY_TEXT_PARSE`。不改成 `M_POLICY_DS_11_POLICY_EVAL_012` |
| `policy_text_parse.structured_elements` | 条款等结构化内容在此。本叶不把条款当成摘要，也不在展示请求里重写它 |
| `policy_text_parse.auto_tags`、`model_version`、`calc_batch_id` | 保持 `parse.run` 现有写法。本叶不补 |

展示 Job 的种类是已签收架构定的 `policy_text_parse`：只查询。不在这次请求里调用 `parse.run`，不调用大模型。本单不执行 `parse.run`。

可编辑和推送没有登记的用户表，也没有发信通道。本叶不建编辑表，不把改过的句子写回 ADS，不灌假通知，不把推送记录灌进 `policy_text_parse`。用户当时在页面上改字，不构成本条的落表。

无行则摘要空，不造段落，不返回写死的句子。D4 保持 mock。序号 242 的推演解读、核增研报 `report/jobs`、`focus-one` 不写入这张表，也不充当这条摘要。

## 6. 灌数单

灌数单 `POL-L2-DS11-READ-GAPFILL-L01` 依赖本单和已签收架构。执行人仍是 `data-agent`，监管仍是 `human:淮政玮`。本单只点名，不认领，不执行，不建库，不插入行，不改那张任务的注册字段。

该单当前仍是 `backlog`。它的旧 DoD 写的是三张缺项表，并要灌入焦点说明、摘要结论、模板与解读条目：

- 在 `gkxlumenx_gapfill` 建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`、`gapfill_policy_eval_shell`
- 独立脚本灌入焦点说明、摘要结论、模板与解读条目
- 不灌短板条数，不灌 PDF

本分册按 2026-11-03 已签收架构把范围收窄成只有 shell。收窄后的灌数范围：

| 旧 DoD | 本分册 |
|---|---|
| 建 `gapfill_policy_eval_focus` | 不建。焦点说明已在 `policy_focus.ext` |
| 建 `gapfill_policy_eval_summary` | 不建。摘要已在 `policy_text_parse.summary` |
| 建 `gapfill_policy_eval_shell` | 保留。只建这一张，列按第 4 节 |
| 灌焦点说明 | 不灌进缺项表。焦点仍由已有 `polan.eval.focus.run` 写入 `policy_focus` |
| 灌摘要结论 | 不灌进缺项表。展示请求不调用 `parse.run` |
| 灌模板 | 不灌。序号 222 不写入壳表 |
| 灌解读条目 | 保留。只灌第 4 节的 `解读` 行和 `多媒体` 行 |
| 不灌短板条数，不灌 PDF | 保持。短板不进壳表。本单也不新开短板灌数单 |

查询请求不调用这张灌数单，也不调用 `gap.run`、`focus.run`、`parse.run`。空表返回空。

223 短板要补批次时，只跑已有 `polan.eval.gap.run`，不新开灌数单。223 焦点的展示 Job 在实现时调用已有 `polan.eval.focus.run` 再查询。226 的展示 Job 只查询。这三件事都不是本单的执行内容。

## 7. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| `M_POLICY_OPPORTUNITY_COUNT` | 无 223–226 的序号。`policy_id` 为空的 `policy_focus` 行留给机遇读面。本叶不改 `counts` 上的机遇读法，不扩大 `focus.run` 的删除范围 |
| 219–221 | 趋势、分区、结构关联。不读壳表，不把短板行改成趋势行 |
| 222 | 报告模板与批量导出。不写入 `gapfill_policy_eval_shell`。本叶不改可视化分册里的模板表 |
| 227–231 | 方案、参数模拟、实施路径、意见与归档。不读壳表。`M_POLICY_DS_11_POLICY_EVAL_015` 不挂本叶 |
| `M_POLICY_EFFECT_SCORE` | 在效果行上，不是 223 的 `region_gap` 读面。本叶不改它的读法 |
| `policy_focus` 的 harness 路径 | 带 items 的既有焦点作业。展示看板的落表仍是 `focus.run` 写入的 `policy_id` 非空行 |
| `compare/jobs`、`report/jobs`、`simulation/jobs` | 核增对比、研报、推演。不写入本叶三张已有表，也不写入壳表 |
| `M_POLICY_RELATION_DEGREE` | 仍在焦点行的 `relation_degree` 与行上已有 `metric_id` 里。本叶不改挂，不读图 |
| `M_POLICY_DEEP_169_1` | 仍是 MODEL。不在短板这条同步链上计算，不为此加列 |
| `GET /v1/policy/analysis/gap`、`/focus`，`/v1/policy/text/parse` | 算法中台自己的读面，与本叶读同一张已有表。展示不改打这些 URL |
| `focus-one` | 不写 ADS。不充当 223 的焦点行，也不充当 226 的摘要 |

## 8. 明确不做

- 不写可执行 SQL，不建库，不灌数，不跑 `gap.run`、`focus.run`、`parse.run`。
- 不重开 GDF，不写 nGQL，不加 ODS、DWD、ADS 表，不加已有 ADS 列。
- 不建 `ads.policy_gap`。不建 `gapfill_policy_eval_focus`。不建 `gapfill_policy_eval_summary`。
- 不新造 `metric_id`，不改 D4，不把缺项行或已有 mock 行写成已上线。
- 不把壳表的行写入 ODS、DWD、ADS、供应方库。
- 不灌视频、动画、图形文件、PDF、模板。序号 222 不写入壳表。
- 不把用户改稿和推送记录写入 `policy_text_parse`。不建编辑表、通知表。
- 不把 `focus.run` 的删除扩到 `policy_id` 为空的机遇行。
- 不在展示请求里调用 `parse.run`。该函数会清空整张 `policy_text_parse`，条款行也在这张表上。
- 查询不插入。列清单不是可执行 SQL。
- 不改说明书、WBS、`指标与501.md`、可视化分册、方案分册、架构稿、`ads.md`、注册表里的灌数单。
- 不认领 `POL-L2-DS11-READ-GAPFILL-L01`。
- 不把本单标成 done 或 ready_to_sign。

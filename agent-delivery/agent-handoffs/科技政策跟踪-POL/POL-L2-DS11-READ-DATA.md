ponytail: off

# POL-L2-DS11-READ-DATA · 政策分析评价结果解读报告多维展示数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链和空表返回空。

## 范围

政策分析评价 · 二级「结果解读报告多维展示」。SRS 序号 223–226，用户故事 `US-DS-POL-05`。上游是已签收的 `POL-L2-DS11-READ-ARCH` 第 8 节。数据落点写在 `sdd/l2/POL-L2-DS11-READ-DATA.md`。

| 序号 | 叶子 | 落点 |
|---|---|---|
| 223 短板 | 热点问题分析看板 · 短板条数 | 已有 `policy_effect`，`scope_type=region_gap`，列 `shortboard_cnt`，原因在 `ext` |
| 223 焦点 | 热点问题分析看板 · 焦点指数 | 已有 `policy_focus`，只取 `policy_id` 非空。`focus_score`，`ext.title`，`ext.explanation` |
| 224 | 分主题分指标互动解读 | `gkxlumenx_gapfill.gapfill_policy_eval_shell` 的解读行 |
| 225 | 多媒体辅助解读 | 同一张壳表的多媒体行 |
| 226 | 智能摘要与结论推送 | 已有 `policy_text_parse.summary` |

## 表与粒度

223 短板一行一个区域。物理库是 `polan.eval.gap.run` 正在写的 `{ads}`，`ads.md` 与代码默认都是 `demo_gkxlumenx_ads`。不加列，不建 `ads.policy_gap`。`counts` 只读 `shortboard_cnt` 与 `ext.reasons`。行上 `metric_id` 仍是 `M_POLICY_SHORTBOARD_COUNT`，`ext.is_mock` 为真，`ext.pending` 为 `QPOL-02`。本单不新开灌数。要补批次只跑已有 `polan.eval.gap.run`，本单不执行。无行则计数空，不造 0。

223 焦点一行一条政策，只取 `policy_id` 非空。`focus.run` 的删除只删 `policy_id` 非空，不扩到机遇行。不建 `gapfill_policy_eval_focus`。行上 `metric_id` 仍是 `M_POLICY_FOCUS_INDEX/M_POLICY_RELATION_DEGREE`。本单不执行 `focus.run`，不改公式。无行则焦点块空。

224、225 共用唯一新表 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。本单只定列，不建库，不灌数。解读行：专题或指标名、一句结论、一句应用建议，`gap_item` 为 `224 分主题分指标互动解读`。多媒体行：标题、一句说明，`gap_item` 为 `225 多媒体辅助解读`。每行带 `metric_id`（没有已挂指标则留空）、`gap_item`、`fill_method=manual`、`gapfill_batch_id`、`generated_at`，以及 `is_mock=1`。不设 `fill_model`。不灌视频、动画、PDF、模板。序号 222 不写入这张表。查询不插入。列清单不是可执行 SQL。

226 一行一条政策的解析结果，只读已有 `summary`。行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。展示读面用已有 `M_POLICY_DS_11_POLICY_EVAL_012`。不建 `gapfill_policy_eval_summary`。展示请求不调用 `polan.text.parse.run`，因为它会清空整张 `policy_text_parse`，条款行也在这张表的 `structured_elements` 上。不灌用户改稿和推送记录。无行则摘要空。

壳表只写 `gkxlumenx_gapfill`。三张已有表不复制到 `gkxlumenx_ads` 或 `gkxlumenx_gapfill`。不写 ODS、DWD、供应方库。D4 保持 mock。

## 灌数单

只点名，本单不认领，不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS11-READ-GAPFILL-L01` | 按本单第 4 节建 `gapfill_policy_eval_shell` 并只灌解读行和多媒体行。依赖本单。旧 DoD 里的另两张缺项表按已签收架构取消 |

该单旧 DoD 写了三张缺项表：`gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`、`gapfill_policy_eval_shell`，并要灌焦点说明、摘要结论、模板与解读条目。本分册收窄成只有 shell。焦点说明留在 `policy_focus.ext`。摘要留在 `policy_text_parse.summary`。模板不灌，序号 222 不进壳表。本单不改那张灌数单的注册字段。

223 短板不新开灌数单。展示请求不调用 `parse.run`。

## 不重开 GDF

不重开 GDF。不写 nGQL。不加已有 ADS 列。不新造 `metric_id`。不把 D4 从 mock 改绿。

## 偏离

无实现偏离。三张已有表的库名沿用 `ads.md` 已登记的 `demo_gkxlumenx_ads`，与已有 `run()` 同一张表。

灌数单注册表里的旧 DoD 仍写三张缺项表。本单不改那张任务。执行时以本分册和已签收架构为准，只建 shell。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-READ-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml`，未 commit，未 push。未改说明书、WBS、`指标与501.md`、可视化分册、方案分册、架构稿。未认领 `POL-L2-DS11-READ-GAPFILL-L01`。

## 验收证据

- 223–226 的库表与已签收架构第 8 节一致。短板、焦点、摘要的列与 `polan.eval.gap.run`、`polan.eval.focus.run`、`polan.text.parse.run` 的实际写入一致。
- 壳表的 D16 列按本单写明：`metric_id` 无已挂指标则留空，`fill_method=manual`，`gap_item` 带序号和叶子名。
- 明确不建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`。
- 灌数单只出现在点名表。本单没有建库、没有插入、没有调用 `run()`。
- 定义任务，未跑业务 CI，未部署。待签收。不标 done，不标 ready_to_sign。

## 架构合规自检

- ✅ 调用链：223 短板与 224、225 由 `gkxlumen-element` 只读；223 焦点与 226 走已有展示 Job。展示不直连库，不直连 Python。
- ✅ Java 不写算法。本单不改已有 `run()`。
- ✅ 不写 nGQL。焦点关联度不为此读图。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造 0。
- ✅ D14：壳表不写视频、动画、PDF，不新建桶，不写对象键。
- ✅ D16：224、225 只在 `gkxlumenx_gapfill`，行上带规定列。不写 ODS、DWD、ADS、供应方库。焦点和摘要已有 ADS，不另建缺项表。
- ✅ D18：223、226 读已有表。224、225 的 mock 先落壳表再被查询。查询不直接返回 mock。
- ✅ 不重开 GDF。

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-READ-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 8 节 |
| 会签态 | `draft`。源文件无 frontmatter，沿架构稿记 draft。不自填绿 |
| 说明 | 数据落点不替代该图。本单待签收 |

## 问题清单

- `POL-L2-DS11-READ-GAPFILL-L01` 的注册 DoD 仍写三张缺项表。执行该单时以本分册为准，只建 shell。本单不改那张任务。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS11-READ-DATA.md`
- 新增本 handoff

## 测试结果

- 只读核对 `polan/eval/gap.py`、`polan/eval/focus.py`、`polan/text/parse.py` 的写入列、删除条件和 `parse.run` 的整表清空。
- 只读核对 `ads.md` 里三张表的已有列。未跑业务测试，未建库。

## 遗留风险

- 灌数单旧 DoD 与本分册不一致，直到该单按本分册执行。本单不认领它。
- `parse.run` 若在展示请求之外被整表重跑，会清空条款行。展示查询路径不调用它。

## CI/CD

- 分支：未提交
- commit：无
- pipeline URL / ID：无。定义任务，`cicd: skip`
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：未部署。未执行 `run()`

## 可观测性

- OTEL_SERVICE_NAME：本叶不新设计观测点。trace 沿既有展示链
- traceId（dev 抽样）：无。未发请求
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-READ-DATA.md`

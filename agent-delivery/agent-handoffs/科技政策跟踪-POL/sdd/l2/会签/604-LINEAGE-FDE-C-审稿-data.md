# 604 · 波次 C · data-agent 审稿

- 身份：`agent:data-agent`
- 日期：2026-11-16
- 总单：`POL-L2-PC1-LINEAGE-FDE-L01`
- 被审：说明书「#### 604」、`sdd/l2/POL-L2-PC1-LINEAGE-ARCH.md` 2026-11-16 补段、`会签/604-LINEAGE-FDE-B-读法方案.md`
- 范围：只审溯源、查证、复核是否越出已有索引行。已签收的 `gkxlumenx_gapfill.gapfill_policy_lineage_index` 读面不重新判成停机
- 本稿只记异议，不改说明书、ARCH、API、指标、数据稿、用例、代码、task-registry

## 逐条核对

1. 界面值与库列（库 `gkxlumenx_gapfill`，表 `gapfill_policy_lineage_index`）。三个动作都读同一次 `GET /display/v1/policy/governance/lineage-index` 已返回的行，不另开读口。

| 界面值 | 落点 | 说明 |
|---|---|---|
| 政策原文 | `gkxlumenx_gapfill.gapfill_policy_lineage_index.policy_title` | 行上必有。全文不在本表，本波不另读 ADS / DWD |
| 条款内容 | 同表 `clause_no`、`clause_excerpt` | 两列均 NOT NULL。条款结论行自带摘录，不必再联原文条款行 |
| 分析结论 | 同表 `conclusion_title`、`conclusion_text` | 只在 `link_kind=条款结论` 有值。`原文条款` 行这两列是 NULL |
| 洞察标识 | 同表 `conclusion_key` 的页面别名 | 没有 `insight_id` 列。`原文条款` 行此列为 NULL。不是 `gapfill_policy_report_trace` 的键 |
| 路径「原文 → 条款 → 结论」 | 无列 | 页面用上面几列拼接 |
| 已复核、复核说明 | 不落库 | 只在当次页面。重开即无。不写本表，不新增列 |

2. 已签收灌数有行，本审不重连库、不把读面判成停机。`POL-L2-PC1-LINEAGE-GAPFILL-L01`（2026-11-08）写入 10 行：`原文条款` 5、`条款结论` 5；政策 `18318861` / `18319069` / `18319394`。合规用例对 `18319069` 期望 4 行。其后治理按钮同表另有 `BTN-governance` 行（B07 记 4 行），行种类仍是这两类。未选：提示先选择政策，三个按钮不出现在空行上。已选但对不上：表空，写「这条政策还没有关联索引」，不出现数字 0，不造行。
3. 三个动作不需要新表、新列、新同步。表仍在 `gkxlumenx_gapfill`（D16 缺项库，已签收）。结论行 `is_mock=1` 是已签收的 D18 灌数，本波不改 D4、不新造 `metric_id`。复核不是新同步。
4. 本波没有写 ODS / DWD / ADS / 供应方库的路径。element 对这张表只 SELECT。复核不写回本表。

## 异议

[data] D-C1 · 三个动作若挂在每一行上，原文条款行没有结论和标识可画 · 说明书 604 状态「有行」要求每行看见分析结论以及「溯源」「查证」「复核」；604-2 弹层要列出分析结论并写出到「结论」的路径；604-3 要看见分析结论或洞察标识。B 读法规定只用被点那一行，不新接口。已签收行里 `link_kind=原文条款` 的 `conclusion_key`、`conclusion_title`、`conclusion_text` 均为 NULL（灌数脚本 `real_rows()`；按钮脚本 `_lineage_rows` 的原文条款行也不带这三列）。条款结论行才自带标题、摘录和结论，可在本行画完。按「每行都有三个按钮」去画，只能空着、现编结论，或把同政策另一行 / 617 表拼进来，后两种都越出这一行 · 三个按钮以及「必须看见结论、洞察标识、路径到结论」只挂 `link_kind=条款结论` 且 `conclusion_key` 非空的行。原文条款行结论列保持空白，不出现三个按钮，不从邻行拼结论。不新增列，不读 `gapfill_policy_report_trace`。

[data] D-C2 · 「洞察标识」不是本表的列，不能到 617 表去补 · 说明书 604-3、ARCH 2026-11-16 补段写「分析结论或洞察标识」。本表没有洞察列；唯一可当标识的是本行 `conclusion_key`。`gapfill_policy_report_trace` 是 617 的表，ARCH §5.2 与 B 读法都写明不共用、不打开 617。现行页把 `conclusion_key` 显示成关联洞察并离开本页，那是被本波拿掉的跳转，不是本行多出来的一列 · 查证只标出被点那一行已有的 `conclusion_title` / `conclusion_text`，标识只用该行 `conclusion_key`。`conclusion_key` 为空则不提供查证。不 SELECT `gapfill_policy_report_trace`，不把这个键说成研报洞察主键。

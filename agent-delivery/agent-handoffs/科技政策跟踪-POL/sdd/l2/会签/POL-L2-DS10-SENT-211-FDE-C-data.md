# POL-L2-DS10-SENT-211-FDE · 波次 B · data-agent 审稿

- 身份：`agent:data-agent`
- 日期：2026-11-14
- 被审：`sdd/简报/2026-11-14-211-FDE-B-arch.md`（`744209a4`）
- 对照：`sdd/l2/POL-L2-DS10-SENT-DATA.md` 第 6 节；展示表 DDL `lumen-algo-py/scripts/mysql/gapfill_policy_assessment.sql`；中台写库 `demo-algo-ent-analysis/polan/assessment_report_job.py`（只读，核对源行怎么落）
- 本稿只记这一版仍然成立的问题。不改读法稿，不改代码，不认领任务

已拍板、本稿不复议：列表一个「下载」只下 PDF。查看弹窗保留「导出 Word」和「导出 PDF」。

## 已采纳，不再列为异议

1. 抄入只读 `demo_gkxlumenx_ads.gapfill_policy_assessment_report`。`scope_text` 原样带走。对不上那两行手工种子就插入新行，不用政策标题改它们。
2. 目标表里同一 `scope_text` 已经有多行：停下来交给人拣，不自动收成一行。
3. 插入带 `metric_id`、`gap_item`、`gapfill_batch_id`，这两列从源行原样抄，不带 `policy_id`。

## 结论

有异议 3 条。下面三条按这一版核对过，无异议。

## 核对过、无异议

1. **八段用现有列就够。** 标题「政策效果评估报告」是固定文案，不入库。其余七段对应 `scope_text`、`generated_at`、`achievement_text`、`social_impact`、`problem_text`、`suggestion_text`、`report_body`。第 6 节都有，没有评分列。`policy_id` 不是其中一段，展示表也不加这列。

2. **失败不删，两行手工种子不会被这条读法删掉。** 抄失败或一条成功行都没有：不 `DELETE`。两行种子范围不同，正文以「缺项演示」开头，`fill_method=manual`，批次 `POL-L2-DS10-SENT-MOCK-211`。中台按政策生成时 `scope_text` 是政策标题，对不上这两句，按这一版插入新行，不改这两行。全景按钮只删 `gapfill_batch_id=BTN-panorama`，不会删这个灌数批次。有成功行后，前端不列出仍是 `manual` 或以「缺项演示」开头的行，种子从列表消失，行还在表里。没有成功行时，表里现有行仍显示。

3. **展示库和演示库是分开的。** 展示只读 `gkxlumenx_gapfill.gapfill_policy_assessment_report`，不读 demo 库。中台写在 `demo_gkxlumenx_ads` 的同名表，写语句拒绝 `gkxlumenx_*`。抄入只进这张缺项表，不写 `gkxlumenx` 业务库，不写 `gkxlumenx_ads`。`is_mock` 保持 1。211 没有已挂指标，D4 不因这次抄入改绿。

## 异议

### D1 · 成功行仍少「五段去掉空白后都非空」

- **问题**：这一版的成功行仍是两条：`fill_method=llm`，五段都不以「缺项演示」开头。空字符串和只含空白的段都不以这四个字开头。开头有空白再写「缺项演示」也会被放过。中台是先去掉空白，空段不算成功，五段都非空才写。
- **影响到哪**：抄入和展示前端用的是同一句成功行。这种行会被抄进 `gkxlumenx_gapfill`，并出现在报告列表里，空段显示成「暂无」。按钮上的「模板句」「大模型」和灌数行的 `manual` 仍被排除，这一条不说它们。
- **建议改法**：成功行三条一起满足：`fill_method` 去空白后等于 `llm`；五段各自去掉空白后都非空；去掉空白后都不以「缺项演示」开头。

### D2 · 源表同一范围、不同 id 的成功行，这一次抄入会落成两行或盖掉先写的那行

- **问题**：目标侧同一 `scope_text` 已有多行则停，这一点已经写上。源表只按 `id` 去重，同一 `scope_text`、不同 `id` 的两条成功行都会进入抄入。中台按 `policy_id` 各写一行，标题相同就是这种行。读法没有写这两条在同一次抄入里的顺序。若都按抄入前的目标表判断，目标当时是 0 行，两条都会插入。若插入第一条之后再看目标，目标变成 1 行，第二条会走「只更新」，先写入的正文被盖掉。
- **影响到哪**：第一次抄入要么在展示表留下两行相同范围，列表两行都显示；要么只留下后写的那一行，另一份正文没有了。下一轮才可能因为目标已有多行而停下来。两行手工种子范围不同，不受这一条影响。
- **建议改法**：同一次抄入里，源表相同 `scope_text` 的成功行超过一条时，这一范围停下来交给人拣，不插入，也不更新。`scope_text` 仍原样比较，不去空白、不改成种子那两句。目标侧已经有多行的规则保持不变。

### D3 · 只更新那一行时，批次号和 gap_item 仍不改

- **问题**：插入会带上 `metric_id`、`gap_item`、`gapfill_batch_id`。同一 `scope_text` 只有一行时，仍只更新五段正文、`generated_at`、`fill_method`。本表没有 `fill_model`，`fill_method=llm` 之后只能靠 `gapfill_batch_id` 看出是哪一次生成。中台写成功时批次是 `POL-RPT-CACHE-ASSESS-MENU`，`gap_item` 是 `211 政策效果评估报告`，`metric_id` 空。
- **影响到哪**：对上的那一行若是手工种子，五段换成生成正文，`fill_method` 变成 `llm`，批次仍是 `POL-L2-DS10-SENT-MOCK-211`。生成行和灌数行分不开。政策标题对不上那两句种子时走插入，插入路径没有这个问题；对得上、或再次抄入已经插入的那一行时，批次停在旧值。
- **建议改法**：更新这一行时，除五段、`generated_at`、`fill_method=llm` 外，把 `metric_id`、`gap_item`、`gapfill_batch_id`、`is_mock` 也按源行写入。不改 `scope_text`，不改 `id`，不带 `policy_id`，不加 `fill_model`。

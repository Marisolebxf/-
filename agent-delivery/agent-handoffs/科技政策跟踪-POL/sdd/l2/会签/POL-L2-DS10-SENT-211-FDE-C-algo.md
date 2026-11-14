# POL-L2-DS10-SENT-211-FDE · 波次 C · algorithm-agent 审读法

- 身份：`agent:algorithm-agent`
- 日期：2026-11-14
- 被审：`sdd/简报/2026-11-14-211-FDE-B-arch.md` 的抄入读法
- 对照：`demo-algo-ent-analysis/polan/assessment_report_job.py` 的写入库、表、成功条件、`scope_text` 是否落库改写
- 不改生成代码，不认领任务
- 列表一个「下载」只下 PDF、弹窗保留 Word 与 PDF，本签不重开

结论：有异议。中台已经写成的成功行可以抄，但按 `scope_text` 对不齐展示表现有的两行；按稿里点名的插入列去插，目标表的非空列不够。

## 核过

1. 成功写入的库和表是 `demo_gkxlumenx_ads.gapfill_policy_assessment_report`。写语句只允许 UPDATE / INSERT 这张表，失败不 DELETE。展示表仍是 `gkxlumenx_gapfill.gapfill_policy_assessment_report`，生成路径不写它。
2. 中台菜单带 `policy_id` 才生成（`api/policy_assessment_report_routes.py` 有 `policy_id` 就走 `run_for_policy`）。成功时 `fill_method` 写成 `llm`，`is_mock` 写成 `1`。五段列名是 `achievement_text`、`social_impact`、`problem_text`、`suggestion_text`、`report_body`，与读法一致。`_five` 拒空串、拒以「缺项演示」开头、拒纯分数。失败不 UPDATE、不 INSERT。种子行 `fill_method` 为 `manual` 且正文以「缺项演示」开头，按读法的两条不会被当成成功行抄走。
3. 已有行的 UPDATE 语句不含 `scope_text`。`_apply_update` 见到产出里带 `scope_text` 直接拒绝。重新生成不会改库里的 `scope_text`。

## 异议

### 1. `scope_text` 不能当和展示种子行对齐的键

问题：没有该 `policy_id` 的行时，`_write_policy` 插入的 `scope_text` 是 DWD `policy_base_info.title`（去掉首尾空白后的政策标题），不是展示种子里的长句。展示种子两行是「广东省科技企业研发支持条款，2024年至2025年。这是报告里的评估范围，不是区域代码。」和深圳市同结构的那一句（`lumen-algo-py/scripts/mysql/gapfill_policy_assessment.sql`）。插入之后的 UPDATE 不再改 `scope_text`，所以库内键稳定，稳定成的是标题，不是那两句。表上只有主键 `id`，没有 `scope_text` 唯一约束；两条政策标题相同就会有两行相同的 `scope_text`。另外接口返回前会把内存里的 `scope_text` 设成当前标题，库内仍是首次写入的标题；DWD 标题后来改了，接口和表不一致。

影响：按 `scope_text` 全等去对展示表，中台已生成行对不上现有两行，抄入会再插一行，不会改那两行的五段。列表在出现成功行后只显示新行，评估范围变成政策标题。标题相同时「更新这一行、不插第二行」无法决定留哪一份报告。若按接口返回值抄，会把库内没改过的 `scope_text` 写成新标题。

建议：抄入只读 `demo_gkxlumenx_ads` 的表，不读生成接口的返回。`scope_text` 原样带走，不要截断，不要改回种子长句。目标里没有相同 `scope_text` 就插入，不要拿标题去改那两行种子。源表用 `id` 去重；目标侧同一 `scope_text` 已经有多行时停下来交给人挑，不要自动收成一行。

### 2. 点名的插入列抄不进目标表

问题：目标表 `gap_item`、`gapfill_batch_id` 是 NOT NULL 且没有默认值，也没有 `policy_id`。读法写的插入内容是五段、`generated_at`、`fill_method=llm`、`is_mock=1`，加上 `scope_text`。源成功行另有 `policy_id`，以及 `gap_item='211 政策效果评估报告'`、`gapfill_batch_id='POL-RPT-CACHE-ASSESS-MENU'`、`metric_id` 空。

影响：只插点名的列，INSERT 会因缺非空列失败，已生成行留在 demo 库。把 `policy_id` 一起抄，目标表没有这列，同样失败。

建议：插入时从源行带上 `scope_text`、五段、`generated_at`、`fill_method`、`is_mock`、`metric_id`、`gap_item`、`gapfill_batch_id`，不带 `policy_id`，不加评分列。`is_mock` 保持源行的 `1`，不要写成 `0`。更新已有同范围行时仍只改五段、`generated_at`、`fill_method`，不改 `scope_text`。

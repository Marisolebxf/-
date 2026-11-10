# POL-L2-PC1-CLEAN-FDE-B2 · data-agent 审稿

- 身份：`agent:data-agent`
- 日期：2026-11-10
- 被审稿：`sdd/l2/会签/POL-L2-PC1-CLEAN-FDE-B2-读法方案.md`
- 口径：说明书「#### 602」、`sdd/602-选择政策-线框.md`
- 本稿不改方案、说明书、代码，不代人选定。

有条件支持方案第 4.1 款。

条件：候选只读 `{ods}` 两表里真实存在的列，分源返回；六条规则仍按无加工事实留空；本波不建表、不写库。4.2、4.3 本次不支持。

## 逐条核对

1. 候选列表能落到列。国内 `{ods}.dwd_policy_base`：标题 `title`，文号 `publish_code`，发文部门 `ministry`，发布日期 `publish_date`，政策 ID `id`。海外 `{ods}.dwd_global_policy_base`：标题 `title`，发布机构 `organ`，发布日期 `publish_date`，政策 ID `id`。结构真源 `agent-delivery/data/data-design/storage/POLICY/sources/ods-ddl.md`。两表 `id` 各自主键，列表必须带来源。批次名、已选条数、规则名、作用范围、开关在 4.1 是当次勾选或页上固定文案，没有事实列。本批判定条数、命中、脱敏样例、更新时间、状态没有事实列。
2. 供应库 `gkx` 2026-11-09 快照两表各 20,000 行，但方案不读 `gkx`，这 20,000 不能当成 `{ods}` 的行。正式 `gkxlumenx_ods` 到 2026-11-02 仍是待贴源、未回签。演示管线写国内 `dwd_policy_base`，海外 `dwd_global_policy_base` 书面是零写入。没有行的那一源显示「这一源还没有贴源数据」。六条没有事实行时，命中和批次状态留空，不写成功，不造 0。
3. 4.1 不需要新表、新列、新同步，不触 D16，不触 D18。准确性若以后改成演示数，才另建一张 D18 的 ADS 表。
4. 4.1 的候选路由只读。去重合并、格式标准化不改贴源行。不写 `{ods}`、不写 DWD、不写 ADS、不写供应库 `gkx`。

## 异议

[data-agent] D1 · 海外搜索和作用范围套用了国内才有的列 · 方案 §3.1 写智能搜索「按标题、文号或发文部门」覆盖两表；线框去重范围含文号、效力级别，格式标准化含「PDF 转文本」，噪声过滤含「扫描件乱码、重复附件」，准确性含「与原文对不上」。`ods-ddl.md`：海外无 `publish_code`、`ministry`、`rank`；两表都无 PDF 转写列、乱码标记、附件重复标记、原文核对结论列。`appendix_name` / `appendix_link` 只是附件名和链接，`content` 是正文。国内 `rank` 样例是 `["国家级"]` 这种字符串（`GKX数据源表及行数报告-20261109-1026.MD` 国内政策库字段表） · 数据稿按表写条件：国内搜索 `title`、`publish_code`、`ministry`；海外搜索只对 `title`。`organ` 只作发布机构，`report_number` 只作报告编号。上述没有列的作用范围保持页上固定文案。4.1 不拿这些列计算命中。

[data-agent] D2 · 「非历史」过滤和「现在有没有行」还不能按方案那句直接执行 · 方案 §3.1 写贴源行带 `is_deleted`、`is_history`，当前行等于未删除且非历史，结构以 `ods-ddl.md` 为准。2026-11-09 供应库快照写明活库没有 `is_history`（国内还没有 `t_id`，海外还没有 `t_id`、`doc_type`；同报告字段差集）。`GDF-POLICY-WORKPACK-v2/04` 规定应用侧谓词是 `is_deleted = 0` 且 `IFNULL(is_history, 0) = 0`，`NULL` 当当前；源表缺列要登记例外，不能在 SQL 里补条件把行丢掉。正式库：`pipeline-ods-to-dwd.md` 写本管线对 `gkxlumenx_ods` 零写入，派单包 README（v2.0.8，2026-11-02）仍待 GDF 预填，未回签不得宣称闭环。演示库：`pipeline-demo-mock.md` §1 第 3 点与 §8 写明 mockgen 零写入 `dwd_global_policy_base`。方案 §5.1 把演示海外说成「可能很少」，并且没重查行数 · 列在时用 `is_deleted = 0 AND IFNULL(is_history, 0) = 0`。列不在时只滤 `is_deleted = 0`，缺列走「读取失败」，空表走「这一源还没有贴源数据」。两句分开。供应库的 20,000 行不填 `{ods}` 候选。波次 C 连上选定库后再记各源行数。

[data-agent] D3 · 4.2 的新表还没到该建的时候，准确性演示数不能和命中事实放一起 · 方案 §4.1 写现在不另造表把空白填上；§4.2 / §5.3 / §5.5 把新 ADS 表留给尚未裁定的选项。D16 的 `gapfill_` 只进 `gkxlumenx_gapfill`，不能拿来装这六条。D18 的演示行单独一张 ADS 表，由 Python 写入，Java 只读 · 维持 4.1：本波数据稿不建表、不加列、不加同步。人若改选演示数，表名放到那时的数据稿，并带 MockBadge。人若改选命中事实表，表落 ADS，不进 ODS / DWD / 供应方库。

[data-agent] D4 · 只读还没写成库范围，清洗文案容易被做成改行 · 方案 §2、§4.1 写 Python 只读 `{ods}`、不读 `gkx`，判定文案不改贴源行。`sources/inventory.md` 与 `pipeline-ods-to-dwd.md` 禁止写正式 `gkxlumenx_*` 和供应库 `gkx`。贴源 `updated_time` 是行的技术更新时间，不是本批清洗的更新时间；`{dwd}.script_state` 的 `status` / `tried_at` 属于 C1/C2，键是 `policy_base_info.policy_id`（`stores/mysql/dwd.md` 的 `script_state`） · 候选路由只允许 SELECT。禁止对 `{ods}`、DWD、ADS、`gkx` 做 INSERT / UPDATE / DELETE。批次「更新时间」在无事实时留空，不改用贴源 `updated_time` 或 `script_state.tried_at`。

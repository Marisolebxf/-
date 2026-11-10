# 602 · 波次 C · data-agent 审稿

- 身份：`agent:data-agent`
- 日期：2026-11-10
- 被审稿：`sdd/l2/POL-L2-PC1-CLEAN-ARCH.md`、`sdd/l2/POL-L2-PC1-CLEAN-API.md`、`sdd/l2/POL-L2-PC1-CLEAN-METRIC.md`
- 不审：`POL-L2-PC1-CLEAN-DATA.md`、Storage
- 对照：说明书「#### 602」、`会签/POL-L2-PC1-CLEAN-FDE-B2-读法方案.md` 文末裁定清单与第 4.1 节、`审稿硬清单.md` data-agent 四问
- 本稿只记异议，不改四单、说明书、线框、Storage、代码

已知且不另立缺陷：候选和执行不复用 `governance/results`；六条正式事实表不建；准确性表名 `policy_accuracy_demo` 是这一波数据稿的草稿名，ARCH / API 写「见 DATA 稿」与此相符。

## 逐条核对

1. 候选列表能落到列。国内 `{ods}.dwd_policy_base`：`id`、`title`、`publish_code`、`ministry`、`publish_date`。海外 `{ods}.dwd_global_policy_base`：`id`、`title`、`organ`、`publish_date`。结构以 `storage/POLICY/sources/ods-ddl.md` 为准。API 把业务键写成贴源 `id`，不是 `policy_base_info.policy_id`。批次名和条数等于这一次勾选，没有事实列。六条正式事实表不建，五条判定留在这次响应里，与裁定第 5 条一致。页眉 `M_POLICY_TOTAL_COUNT` 经 metric-get 核对：STAT，D4=`mock`，本叶不改口径、不走候选读口，不替代本批条数。准确性演示数不注册、不写公式。
2. 没有行时的文案，ARCH §3 和 API §5 已分开：该源零行是「这一源还没有贴源数据」；有数据但 ID 对不上是「该 ID 不在贴源」；搜不到是「这次没搜到」；读不出来是「读取失败」。不造 0。供应库 `gkx.dwd_policy_base` 的 20,000 行是页眉指标注册表上的底数，不是 `{ods}` 的行，ARCH 也没有拿它填候选。
3. 本叶新表只有准确性这一张 D18 的 ADS 演示表。不进 ODS、DWD、供应方库，不是 `gapfill_`，不和六条正式事实表合并。不另做目录同步。点「执行」这次不写库；演示行由 Python 在点击之外写入，Java 只读。与裁定第 3、5 条一致。
4. ARCH §4、§8 与 API §1、§4 写明：五条只 SELECT 上述两表，禁止对 `{ods}`、DWD、ADS、`gkx`、`script_state` 做写入。点击路径不改贴源原文。准确性写入只指向那张演示表，不写进五条结果。

## 异议

[data-agent] D-C1 · 智能搜索仍用同一句「标题、文号或发文部门」覆盖国内和海外，海外没有这两列 · ARCH §3（约第 94 行）、API §2 搜索词（约第 43 行）把文号、发文部门写成两源共用。`ods-ddl.md`：海外无 `publish_code`、`ministry`；`organ` 是发布机构，`report_number` 是报告编号。上一轮数据审稿 D1 与数据任务已定为国内搜 `title`、`publish_code`、`ministry`，海外只搜 `title`。按现在这句去 SELECT，海外会打到不存在的列，整块变成「读取失败」，而不是「这次没搜到」 · 候选搜索按源落列。海外只对 `title`。`organ` 只出现在列表上，不参与搜索。没有的列不要 SELECT。

[data-agent] D-C2 · 准确性只写了「读失败」，没写表在但这一条没有演示行时界面显示什么，也没写按哪一列去对行 · ARCH §5、API §3 准确性那一行：启用时 element 只读演示表，失败则「读取失败」。说明书 602-7 要求看得出是演示的数，且没点执行前不出现命中。勾选是多条「来源 + 贴源 id」。稿里没有读键。空结果若改写成读取失败、无加工事实、0，或拿别的行的数顶上，都和「不造 0、不得写成已经按原文核过」冲突。清单第 2 问要的就是没有行时显示什么 · 按本次勾选的来源和贴源 `id` 读数据稿里的 `policy_accuracy_demo`。对上的行才把演示说明放进该条，并标明演示。表不存在或查询失败走读取失败。表在但这一条没有行：这一条不出现演示命中，不造 0，不写成无加工事实，也不写成已经核过。

[data-agent] D-C3 · 可判定时的更新时间、脱敏失败样例仍然没有列 · 说明书批次明细要看见更新时间和脱敏失败样例（602-7）。API §3 只在「无加工事实」写更新时间留空；可判定时只写命中条数和状态。读法方案第 4.1 节：无事实时不用贴源 `updated_time`，也不用 `script_state.tried_at`。两表 `updated_time` 是技术更新时间。噪声、一致性没有可判定列，样例不能从 `content`、`appendix_name`、`appendix_link` 现造。没有六条事实表，这两项也落不到新列 · 成功、部分、失败同样不回填 `updated_time`。脱敏样例只在这一条作用范围确有列、且判定出失败时，从该列脱敏后放进这次响应；缺列则样例与命中一样留空。

[data-agent] D-C4 · 「这一源有没有行」还没写成当前行，海外表现状也不是空表 · 读法方案 §3.1 要求未删除、非历史。ARCH §3、API §5 的「一条行都没有」没有这句。`ods-ddl.md` 两表都有 `is_deleted`、`is_history`。不过滤时，历史行会进勾选，删光的源也不会走空源文案。`etl/pipeline-demo-mock.md` §4 E1：mockgen 只写国内表，国际表未建未灌。表不存在是读取失败，不是「这一源还没有贴源数据」。裁定第 1 条的空源文案只适用于表在且当前行计数为 0 · 列在时用 `is_deleted = 0 AND IFNULL(is_history, 0) = 0`；`is_history` 不在时只滤 `is_deleted = 0`。缺列走读取失败，不要把行滤掉。海外未建表保持读取失败。供应库那 20,000 行不填 `{ods}`。

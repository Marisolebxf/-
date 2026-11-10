# POL-L2-PC1-CLEAN-FDE-B2 · data-agent 再审

- 身份：`agent:data-agent`
- 日期：2026-11-10
- 被审稿：`sdd/l2/会签/POL-L2-PC1-CLEAN-FDE-B2-读法方案.md`（2026-11-10，「点执行才跑」）
- 口径：说明书「#### 602」、`sdd/602-选择政策-线框.md`
- 范围：第 4 节，以及第 2 节里点「执行」之后的时序。上一轮搜索列分源、空态不造 0、不复用政策主表检索、公开路径与 `results` 拆开，本轮不重写。
- 本稿不改方案、说明书、代码，不代人选定。

有条件支持第 4.1 款。

条件：现算只读 `{ods}` 两表里已经有的列，分源 SELECT，不改源行，不写库。没有对应列的规则，命中为 null，状态不写成功，不造 0。现在没有六条实现、也没有事实行，所以现在整批仍是这个空。本轮不建表。4.2、4.3 本轮不支持。

## 第 2 节时序

点「执行」之前不发本批，不写库。点「执行」之后读还是算，图上写明见第 4 节、尚未选定。时序没有把作业落表写成已经发生。这一节无单独异议。

## 逐条核对

1. 点「执行」之后，界面上的批次名、这次条数、规则名、作用范围、开关，来自当次勾选和页上固定文案，没有事实列。本批判定、命中、脱敏样例、更新时间、状态，也没有事实列。4.1 若现算，输入只能来自贴源已有列，结构真源 `agent-delivery/data/data-design/storage/POLICY/sources/ods-ddl.md`。国内 `{ods}.dwd_policy_base` 有 `title`、`publish_code`、`rank`、`publish_date`、`ministry`、`content`、`appendix_name`、`appendix_link`。海外 `{ods}.dwd_global_policy_base` 有 `title`、`publish_date`、`organ`、`content`、`appendix_name`、`appendix_link`、`report_number`，没有 `publish_code`、`ministry`、`rank`。两表都没有 PDF 转写列、扫描件乱码标记、附件重复标记、原文核对结论列。`appendix_name` / `appendix_link` 只是附件名和链接，`content` 是正文，`report_number` 是报告编号。方案 §4.1 写「做判定」，没有把这些列写进这一款。
2. 六条规则没有事实表，也没有事实行。2026-11-10 复核：`lumen-algo-py` 没有这六条的政策实现；`agent-delivery/data` 没有这六条的事实表。`{dwd}.script_state` 的 `job` 只记 c1 / c2，主键 `(job, policy_id)` 对的是 `policy_base_info.policy_id`（`stores/mysql/dwd.md`）。点过「执行」之后仍然没有加工事实：命中 null，状态不写成功，不造 0。和说明书「无加工事实」同一句。
3. 4.1 不需要新表、新列、新同步，不触 D16，不触 D18。4.2 要在跑完后回写批次明细，就必须有一张新表：ADS，Python 写入，Java 只读；不进 ODS、DWD、供应库 `gkx`；不用 `script_state`；不拿 `gapfill_` 装这六条。方案把表名留给第 5.5 节，并写明未裁定时 4.2 不能落地成库。第 5.5 节「先不建」配的是 4.1，「只建命中事实表」才改用 4.2 或 4.3。所以 4.2 要新表；本轮不选 4.2，也不落表名。准确性若以后改成演示数，仍单独一张 D18 的 ADS 表，不和命中表放一起。
4. 4.1 写了去重合并、格式标准化不改贴源行，也写了不新建正式事实表、不读 `script_state`、不读政策主表、Java 不读贴源。没有把六条现算写成只允许 SELECT。贴源 `updated_time` 是行的技术更新时间，不是本批更新时间。

## 4.2

要新表才能回写。不建表就没有批次明细、命中、更新时间、状态的列；在途若写进 `script_state`，会和 C1/C2 混表。本轮不支持。

## 4.3

和「现在没有六条规则的加工事实」不矛盾。现在没有这张表、没有这些行，点了只能得到空命中，状态不写成功，不造 0。方案已经写了「点了也只得到空命中」「未建表时这一款没有读口」。点击不现算，也不在这次请求里写入，所以这次点击不会变出六条事实。本轮不支持。不单列异议。

## 异议

[data-agent] R2-D1 · 4.1 现算没有落到库.表.列，缺列时的返回也没写成一句 · 方案 §4.1 只写按当时勾选和当时启用的规则「做判定」；风险只写去重对贴源全表比对会超时。海外没有 `publish_code`、`rank` 写在 §4.2，没有写在推荐款 §4.1。`ods-ddl.md`：国内去重能读到的列是 `dwd_policy_base.title`、`publish_code`、`rank`；海外去重能读到的列只有 `dwd_global_policy_base.title`。格式标准化能读到的日期列是两表的 `publish_date`，文号只有国内 `publish_code`。完整性里「缺发布日期」能看两表 `publish_date` 是否空，「缺发文机关」只能看国内 `ministry`；海外 `organ` 是发布机构，不是发文机关列。一致性要的「效力级别与发文主体对不上」没有对照表；海外没有 `rank`。噪声过滤、PDF 转文本、准确性原文核对，两表都没有对应列 · 4.1 分源只 SELECT 上面这些已有列，国内和海外的去重不要合成一把。没有对应列的那一条作用范围不参与命中：该规则命中为 null，状态不写成功，不造 0。缺列走「无加工事实」，不走「读取失败」。「读取失败」只留给查询本身失败。

[data-agent] R2-D2 · 4.1 没有把六条现算锁成只读 · 方案 §4.1 只写去重合并、格式标准化不改贴源行。噪声过滤、格式标准化若被做成改行或删行，就会写 `{ods}`。§4.1 同时写「不新建正式事实表」，批次结果只应留在这次响应里 · 六条判定只允许 SELECT `{ods}.dwd_policy_base` 与 `{ods}.dwd_global_policy_base`。禁止对 `{ods}`、DWD、ADS、供应库 `gkx` 做 INSERT / UPDATE / DELETE。不写 `script_state`。无事实时批次「更新时间」留空，不用贴源 `updated_time`，也不用 `script_state.tried_at`。

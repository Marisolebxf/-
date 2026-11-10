# POL-L2-PC1-CLEAN-DATA · 政策数据治理 · 系统引用政策源数据清洗 · 后台数据架构设计

- 任务：`POL-L2-PC1-CLEAN-DATA`
- 日期：2026-11-10
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`
- 强度：ponytail off
- 上游：`POL-L2-PC1-CLEAN-ARCH.md`、`会签/POL-L2-PC1-CLEAN-FDE-B2-读法方案.md` 第 4.1 节与文末裁定清单、`会签/POL-L2-PC1-CLEAN-FDE-B2-审稿-data.md` D1–D4、`data/data-design/storage/POLICY/sources/ods-ddl.md`
- SRS：**602**

波次 C 数据稿。候选和五条判定改读演示贴源两表。准确性只登记一张演示表。正式事实表不建。

## 1. 谁读哪两张贴源表

候选，以及去重合并、格式标准化、噪声过滤、完整性校验、一致性校验这五条，只读演示贴源。库名写 `{ods}`，指向演示贴源，不写成正式库名。

| 源 | 表 | 谁读 |
|---|---|---|
| 国内 | `{ods}.dwd_policy_base` | Python 只 SELECT |
| 海外 | `{ods}.dwd_global_policy_base` | Python 只 SELECT |

两表分源读，不合成一把。Java 不读贴源，只转发。不读供应方库 `gkx`。不读 `policy_base_info`。不读 `script_state`。不改贴源行。不对 `{ods}`、DWD、`gkx` 写入。这一次候选和五条的 SELECT 不写 ADS。演示表的写入留在点击之外。

结构以 `ods-ddl.md` 为准。两表都有 `id`、`title`、`publish_date`、`content`、`appendix_name`、`appendix_link`、`is_deleted`、`is_history`、`updated_time`。国内另有 `publish_code`、`ministry`、`rank`。海外另有 `organ`、`report_number`，没有 `publish_code`、`ministry`、`rank`。两表都没有 PDF 转写列、乱码标记、附件重复标记、原文核对结论列。`content` 是正文。`appendix_name`、`appendix_link` 只是附件名和链接。

候选列表能落到的列：国内 `title`、`publish_code`、`ministry`、`publish_date`、`id`；海外 `title`、`organ`、`publish_date`、`id`。列表必须带来源。批次名、已选条数、规则名、作用范围、开关是当次勾选或页上固定文案，没有事实列。

表在且按第 3 节滤完的当前行为 0，界面写「这一源还没有贴源数据」。表不存在是读取失败。供应方库里的行数不填 `{ods}` 候选。本叶不连库，不记现网行数。

## 2. 搜索列（审稿 D1）

国内搜索只用 `title`、`publish_code`、`ministry`。海外搜索只用 `title`。按政策 ID 精确查只用各表自己的 `id`。

海外没有的文号、发文部门、效力级别不拿来算命中。`organ` 只作发布机构。`report_number` 只作报告编号。贴源没有对应列的作用范围保持页上固定文案，不拿来算命中。

## 3. 当前行怎么滤（审稿 D2）

列在时，当前行是 `is_deleted = 0 AND IFNULL(is_history, 0) = 0`。`is_history` 不在时，只滤 `is_deleted = 0`。缺列不是把行滤掉。

`ods-ddl.md` 里两张表目前都写了这两列。表不存在是读取失败。表在且当前行为 0，才是「这一源还没有贴源数据」。

## 4. 五条判定，不建正式事实表

不建六条正式事实表。点「执行」之后，五条由 Python 在这一次请求里只 SELECT 第 1 节两张贴源表，国内和海外分源。结果留在这次响应里，不落库。

能用来算的列与读法方案第 4.1 节相同，只使用 `ods-ddl.md` 里已有的列：

| 规则 | 能用来算的列 | 没有的列 |
|---|---|---|
| 去重合并 | 国内 `title`、`publish_code`、`rank`；海外只有 `title` | 海外文号、效力级别不参与命中 |
| 格式标准化 | 两表 `publish_date`；文号只有国内 `publish_code` | 「PDF 转文本」没有列，不参与命中 |
| 噪声过滤 | 无 | 命中为 null。附件名和链接不算重复标记 |
| 完整性校验 | 「缺发布日期」看两表 `publish_date` 是否空；「缺发文机关」只看国内 `ministry` | 海外 `organ` 不拿来当发文机关算命中 |
| 一致性校验 | 无 | 没有效力级别与发文主体的对照；海外没有 `rank`。命中为 null |

没有对应列时，样例与命中都留空，状态不写成功，不造 0，走无加工事实。不从正文 `content` 或附件名 `appendix_name`、`appendix_link` 现造样例。缺列不把行滤掉，也不走读取失败。转发失败或超时才标明读取失败，不返回 0。

去重合并的判定文案是「应合并」，格式标准化是「待标准化」。两句都表示不改贴源行。

没有事实时，批次更新时间留空。有判定时，更新时间也不是贴源 `updated_time`，不用 `script_state.tried_at`。

## 5. 准确性演示表

准确性不参加第 4 节的现算。单独一张 D18 的 ADS 演示表，表名 `policy_accuracy_demo`。

| 项 | 定法 |
|---|---|
| 库 | 演示 ADS `demo_gkxlumenx_ads` |
| 状态 | draft。本叶只登记，不写可执行建表语句，不连库 |
| 不进 | ODS、DWD、供应方库 `gkx`。不是 `gapfill_`。不和 ADS 里那 16 张已落地真算表混用 |
| 谁写 | 写入留在点击之外。Python 另行写入演示行，不在这一次 SELECT 里现造 |
| 谁读 | 点「执行」且当时准确性启用时，Java 只读这张表。display 不直连库。不读九张指标表 |
| 界面 | 标明演示。演示条数不是注册指标，不占 D4，不写成质量分 |

列：

| 列 | 含义 |
|---|---|
| 来源 | 国内或海外，对应第 1 节两张贴源表之一 |
| 贴源 id | 该贴源表自己的 `id` |
| 演示命中说明 | 演示用的命中说明 |
| 演示条数 | 这一行上看得出是演示的数。不是注册指标 |
| 写入批次标记 | 前缀 `demo_`，能看出是演示 |

不设「已按原文核过」这一列，演示命中说明里也不写这句话。

按来源和贴源 id 对行。对上的行才带出演示条数和演示命中说明，并标明演示。读失败或表不存在时，准确性这一块标明读取失败，不用写死的数顶上。表在但没有对上的行：不造数，不用固定写死的演示数，不返回 0，不写成已经核过。没点「执行」之前不出现命中。

登记位置：`data/data-design/storage/POLICY/stores/mysql/ads.md` 的「准确性演示」一节，状态 draft。

## 6. 明确不做

不建六条正式事实表。不重开 GDF。不改 `ods-ddl.md`。不改那 16 张真算表的列。不写可执行 SQL，不连库灌数。不把 `policy_base_info` 或 `script_state` 当成 602 的清洗结果。页眉库级计数不在本叶改读法。

# POL-L2-DS10-TREND-205-FDE · 波次 C2 · 审稿 · data-agent

- 日期：2026-11-15
- 身份：`agent:data-agent`
- 被审：`sdd/l2/POL-L2-DS10-TREND-DATA.md` 第 8 节；`sdd/l2/POL-L2-DS10-TREND-ARCH.md` 第 7.6 节；说明书「#### 205 重点领域政策分析（2026-11-15）」卡面读法表
- 对照：`storage/POLICY/stores/mysql/dwd.md` 的 `policy_base_info`、`policy_industry_rel`（只读 CREATE，确认没有评分列）
- 口径：`.cursor/skills/gkx-fde-design-change/审稿硬清单.md` data-agent 四问
- 本稿只记审稿。不改 DATA，不改 ARCH，不改说明书，不改旧会签，不写代码，不 commit，不连库

本稿不把 `dwd.md` 里 2026-10-26 的行数写成今天的现网行数。结果表按第 8 节尚未建，现无行。

## 硬清单（四问）

1. **每个界面值落到哪库.表.列**

| 界面值 | 稿里写的落点 | 源列（dwd.md 已有） | 结论 |
|---|---|---|---|
| 卡名 | 草稿 `ads_policy_keyfield_card.domain_name` | 无。四个名字是固定词，不从来源表读 | 表未建。无行时名字仍按说明书留在卡上 |
| 政策条数 | 同表 `policy_count`。没有政策则不插入行 | 件数来自 `demo_gkxlumenx_dwd.policy_base_info` 的 `title`、`abstract`、`keywords`、`content`。稿未写 `is_deleted`、`is_history` | 结果列是新列。无行时只写了「不写 0」，没有写界面上的字。见 C2-2 |
| 热度 | 同表 `heat_label`。不足两年为空 | `policy_base_info.publish_date`（另有 `publish_year`，稿点名的是 `publish_date`） | 空列对应「暂时看不了热度」，这一格对得上 |
| 对标区域 | 同表 `region_text` | `province`、`country`、`region`。CREATE 里还有 `city`、`district`、`geo_region`，稿未点名 | 无地区时说明书有一句空态，DATA 未写这句是否进 `region_text`。见 C2-2 |
| 平均评分 | 同表 `avg_score`，可空 | **没有。** `policy_base_info`、`policy_industry_rel` 的 CREATE 都没有评分列 | 仍放进「统计」。见 C2-1 |
| 关键焦点 | 同表 `focus_text` | 无来源列。模型写入，最多三个 | 模型不可用则整次不写。无合格行只写「空态」，没有单独一句界面文案 |
| 两句说明 | 深度正文前两句 | 正文列表未定表名。现列在 `gkxlumenx_gapfill.gapfill_policy_trend_report.body`，第 8 节说缺项库不再是归宿 | 没有库.表.列。见 C2-2 |
| 政策全景 | 同表 `panorama_text`。没有关联时记空态句 | `demo_gkxlumenx_dwd.policy_industry_rel` 的 `policy_id`、`industry_name`、`is_deleted` | 空态句没有写成说明书那句「这一领域还没有产业全景」 |
| 影响评估 | 「仍用现在的列」：`domain_name`、`impact_object`、`impact_direction`、`conclusion` | 现列在 `gkxlumenx_gapfill.gapfill_policy_trend_impact`。ADS 表名留到建表批准时再定 | 没有库.表.列。见 C2-2 |
| 深度分析报告 | 「仍用现在的列」：`domain_name`、`title`、`body` | 现列在 `gkxlumenx_gapfill.gapfill_policy_trend_report`。ADS 表名同样未定 | 没有库.表.列。见 C2-2 |
| 热点 | 不进这张卡的加工。仍读 `gkxlumenx_gapfill.gapfill_policy_trend_hotspot` 的 `domain_name`、`hotspot_name`、`brief` | 缺项表已有列 | 这一项对得上。无行时说明书写「这一领域还没有热点」 |
| 整页趋势 | 不贴到四张卡。仍读已有 `M_POLICY_TIMESERIES` | 不在第 8 节新表里 | 本波不改这条。无行则图空，稿已写不造 0 |

2. **现在有没有行；没有行时界面显示什么**

- 草稿 `ads_policy_keyfield_card` 与影响、深度的 ADS 表都还没建。正式库 `gkxlumenx_ads` 本波不建。演示库同名表留到实现波再写。所以这三处结果现在没有行。
- 说明书写：接到正式 ADS 之前，展示页仍是现在的样子。DATA 第 8 节写：没有合格行则空态。这两句不是同一件事。目标空态（评分、区域、两句、全景、影响、深度）还没绑到「表不存在」这一种没有行。
- 热度这一格写清了：`heat_label` 空，界面「暂时看不了热度」。热点写清了：「这一领域还没有热点」。
- 一份集合一件政策都没有：ARCH 写不写新行、旧行保留。若上一轮留下合格行，界面继续显示旧条数，不是「不写 0」。见 C2-3。

3. **新表落哪个库，是否触 D16 / D18**

- 新表名只定了卡面草稿 `ads_policy_keyfield_card`。实现波建在 `demo_gkxlumenx_ads`。批准后再落 `gkxlumenx_ads`。不进 `gkxlumenx_gapfill`，表名不是 `gapfill_`，**不是 D16**。
- 平均评分无法从已有列真算。若为此新建 ADS 表来装这个数，才触及 **D18**。D18 要求稿里写明表名、灌数方、读取接口，写入的是 mock 行，D4 仍是 mock，不能写成统计出来的平均分。影响表、深度表的表名未定，D18 的表名不齐。见 C2-1、C2-3。
- 条数、热度、区域、全景可以从已有列算出，焦点、影响、深度是模型正文。这几项不应和评分捆成同一步「统计」。

4. **写 ODS / DWD / 正式 ADS / 供应方库**

- 第 7.6 节写明：写库只允许 `demo_gkxlumenx_ads`；不写 `gkxlumenx_*`；取材读演示 DWD，不加列。按这三句，**本波不写** ODS、DWD、正式 ADS、供应方库。
- 留下的入口：批准后把草稿落进 `gkxlumenx_ads`；第 7.3 节仍写缺项三张表生成成功后把 `fill_method` 改成 `llm`。见 C2-3。

## 异议

有异议 3 条。

[data] C2-1 · 问题：平均评分没有源列，稿仍把它当成能统计出来的数。DATA 第 8 节把早先「评分无列」和上一版读法一起作废，并在 `ads_policy_keyfield_card` 留可空列 `avg_score`，写「没有可汇总的评分就空，不写 0」。这句话的另一面是：有可汇总的评分就写入数字。说明书流程图把「评分」和条数、热度、区域放在同一步统计；第 7.6 节也是「统计并准备卡面」，评分列留着。`dwd.md` 的 `policy_base_info`（`id` 至 `updated_time`）和 `policy_industry_rel`（`id`、`policy_id`、`industry_name`、`industry_link_code`、`is_deleted`、`create_time`、`update_time`）都没有评分列。没有源列，就不存在可汇总的评分。禁止用标题摘要、种子分、焦点指数、实施效果或推演来填，只挡住假来源，没有取消「这一格是统计结果」。 · 依据：`POL-L2-DS10-TREND-DATA.md` 第 188–200 行；`POL-L2-DS10-TREND-ARCH.md` 第 7.6 节约第 321–324 行；说明书「#### 205」约第 74、90、110 行；`dwd.md` 第 32–81 行、第 93–106 行；硬清单 data-agent 第 1 问。 · 建议：`avg_score` 退出统计。这一列不写入任何数字，演示 ADS 和以后的正式 ADS 都不写。有行、无行、无表，这一格都只显示「还没有可汇总的评分」，不写 0，不写 89.2。不给 `policy_base_info` 加评分列。

[data] C2-2 · 问题：影响评估、深度分析报告、卡上两句说明没有库.表.列。第 8 节只给卡面草稿定了表名；影响和深度「仍用现在的列含义」，正式表名留到建表批准时再定。两句说明取深度正文前两句，正文表跟着没有名字。现有 `gkxlumenx_gapfill.gapfill_policy_trend_impact`、`gapfill_policy_trend_report` 被写成不再是这份结果的归宿，又没有新的库.表.列接上。没有这张表时，说明书写展示页仍是现在的样子，DATA 只写「没有合格行则空态」。政策条数无行时只写「不写 0」。对标区域无地区、全景无关联，说明书有固定句子，DATA 没有把这两句定成 `region_text`、`panorama_text` 的内容。 · 依据：`POL-L2-DS10-TREND-DATA.md` 第 192–208 行（对照同文第 5.3、5.4 节现列）；`POL-L2-DS10-TREND-ARCH.md` 第 7.6 节约第 326–332 行；说明书「#### 205」约第 94、107–114、120、136、163、172 行；硬清单 data-agent 第 1、2 问。 · 建议：表名写死之前，这三项只走说明书已写的空态：「这一领域还没有影响评估」「这一领域还没有深度分析报告」「这一领域还没有汇总到政策举措」。不读缺项表现行当中台新结果，也不把缺项行迁进 ADS。政策条数没有合格行时不写 0，并写明界面上的字，不用空白代替。`region_text` 无地区时存「这一领域还没有可汇总的区域」。`panorama_text` 无关联时存「这一领域还没有产业全景」。

[data] C2-3 · 问题：新表不是 D16，评分又够不上 D18 的真算替代，正式 ADS 仍有被写进去的入口。`ads_policy_keyfield_card` 不在 `gkxlumenx_gapfill`，也不是 `gapfill_` 前缀，不能算 D16 缺项表。本波不建 `gkxlumenx_ads`，实现波只在 `demo_gkxlumenx_ads` 建同名表，这一点本身不写正式 ADS。但第 8 节写「等建表批准后再落 `gkxlumenx_ads`」。平均评分无法真算，不能借这次批准写成正式 ADS 里的统计列。D18 只接受新建 ADS、由 Python 灌 mock 行、接口只读该表，且稿里要写明表名、灌数方、读取接口；影响表和深度表的表名现在没有，读取接口第 8 节也没有点名。另一处抢写：第 7.3 节仍写 205 三张缺项表生成成功后把 `fill_method` 改成 `llm`，和第 7.6 节「不把结果灌进缺项库」不是同一归宿。零命中「不写、旧行保留」时，旧的合格行会继续显示上一轮条数。 · 依据：`POL-L2-DS10-TREND-DATA.md` 第 186–190、206–208 行；`POL-L2-DS10-TREND-ARCH.md` 第 7.6 节约第 310、316–317、323、332 行，第 7.3 节约第 336–340 行；`architecture-baseline.md` D16、D18；硬清单 data-agent 第 3、4 问。 · 建议：本波保持不写 ODS、DWD、`gkxlumenx_ads`、供应方库，不加来源列。卡面若只建在演示库，写明库 `demo_gkxlumenx_ads`、表名、Python 写入、展示本波不读。`avg_score` 不作为 mock 数字灌入，批准落正式 ADS 时也不带数字过去。第 7.3 节「三张缺项表改为 `fill_method=llm`」标明不适用于卡面、影响、深度。零命中且没有合格行时，不沿用上一轮条数。

## 核对过、本条不另立异议

1. **两张来源表没有评分列。** `policy_base_info` 的 CREATE 从 `id` 到 `updated_time`，`policy_industry_rel` 的 CREATE 从 `id` 到 `update_time`，都没有评分、分值或评价列。DATA 第 190 行和 ARCH 第 7.6 节「主表没有评分列」这半句是对的。异议只针对仍把平均评分放进统计、并留可写入的 `avg_score`。
2. **热点仍在缺项库。** `gkxlumenx_gapfill.gapfill_policy_trend_hotspot` 的 `domain_name`、`hotspot_name`、`brief` 不动。无行时「这一领域还没有热点」。不进四张卡的加工，不改挂焦点指数。
3. **热度的空规则写清了。** `heat_label` 不足两年为空，界面「暂时看不了热度」，不读整页时序来填。
4. **本波写库句子本身排除了 ODS、DWD、正式 ADS、供应方库。** 写库只允许 `demo_gkxlumenx_ads`，取材不加列。C2-3 异议的是批准后的正式库入口和缺项表 `fill_method` 抢写，不是这句边界没写。

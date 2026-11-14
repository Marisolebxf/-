# POL-L2-DS10-TREND-205-FDE · 波次 C · data-agent 审稿

- 身份：`agent:data-agent`
- 日期：2026-11-15
- 被审：说明书「#### 205 重点领域政策分析（2026-11-15）」；`sdd/简报/2026-11-15-205-FDE-B-读法.md`
- 对照：`sdd/l2/POL-L2-DS10-TREND-DATA.md`（只读）；`storage/POLICY/stores/mysql/ads.md` 的 `policy_timeseries`；`storage/POLICY/stores/mysql/dwd.md` 的 `policy_category_rel`；正式库建表种子 `lumen-algo-py/scripts/mysql/gapfill_policy_trend.sql`；中台写库 `demo-algo-ent-analysis/polan/trend_hotspot_job.py`（只读，核对成功行怎么判）
- 本稿只审稿。不改说明书，不改读法，不改四单，不改代码，不 commit，不连库改数
- 硬清单：`gkx-fde-design-change/审稿硬清单.md` data-agent 四条

展示迁到正式库之前，热点、影响、深度报告仍只读 `gkxlumenx_gapfill` 已有三张表。本稿不建议新建正式表，不加列，不把演示库行抄进 `gkxlumenx_ads` / `gkxlumenx_dwd` / `gkxlumenx_ods`。

## 落点对照

| 界面值 | 已有库.表.列 | 没有合格行时界面写什么 | 本波要不要新表新列 |
|---|---|---|---|
| 趋势 | `gkxlumenx_ads.policy_timeseries` 的 `period_type`、`period_key`、`publish_count`。`metric_id` 仍是 `M_POLICY_TIMESERIES` | 图空，不补 0 | 不要。表上没有领域列，见 D3 |
| 热度 | 上表同一条年行的 `publish_count` 比较出来的标签。没有热度列 | 「暂时看不了热度」；热度单独失败写「热度暂时看不了，可稍后重试」 | 不要。见 D3 |
| 举措两句 | 四单和已登记表都没有这一列 | 「这一领域还没有汇总到政策举措」；只出一句时，空的那句写「还没有」 | 不要。见 D1。没有列之前，两句位置固定走这句空态 |
| 政策条数、平均评分、对标区域、关键焦点 | 没有列。`publish_count` 是整页年发布量 | 读法只写了没有举措时政策条数、平均评分、对标区域写「—」 | 不要。见 D2 |
| 热点 | `gkxlumenx_gapfill.gapfill_policy_trend_hotspot` 的 `domain_name`、`hotspot_name`、`brief` | 「这一领域还没有热点」 | 不要。见 D5 |
| 影响 | `gkxlumenx_gapfill.gapfill_policy_trend_impact` 的 `domain_name`、`impact_object`、`impact_direction`、`conclusion` | 「这一领域还没有影响评估」；无完整结论不导出 | 不要。见 D5 |
| 深度报告 | `gkxlumenx_gapfill.gapfill_policy_trend_report` 的 `domain_name`、`title`、`body` | 「这一领域还没有深度分析报告」；无正文不导出 | 不要。见 D5 |
| 政策全景 | 读法写「沿用全景已有政策列表」，没有点名列。类别列的取值对不上四张卡名 | 「这一领域还没有政策全景」 | 不要。见 D4 |

本稿不连库，不把仓库种子或 2026-10-26 的行数写成今天的现网行数。种子脚本里，科创发展、人才引进、资金扶持各有以「缺项演示」开头、`fill_method=manual` 的热点、影响、报告行；技术发展方向没有种子行。按读法，这些种子行不算已生成结果，四张卡的热点、影响、报告都走上表空态。中台生成写在 `demo_gkxlumenx_ads` 的同名表，本波展示不读。

## 新表、新列、写库

- 不需要新表、新列、新同步。缺口用空态文案盖住。
- 三张缺项表仍在 `gkxlumenx_gapfill`，不进 ODS、DWD、正式 ADS、供应方库。这是 D16 缺项表，D4 保持 mock。
- 本波读法不写这四个库。中台已有的写库停在 `demo_gkxlumenx_ads`，不在本波接到展示打开。不要为了让展示看见生成结果而新建正式表，或把三张表迁进 `gkxlumenx_ads`。

## 异议

有异议 5 条。

### [data] D1 · 两句举措没有库.表.列

- **问题**：205-2 要在卡上原来的两句说明位置，读出这一领域已经汇总好的两句举措。`POL-L2-DS10-TREND-DATA` 没有举措表，也没有举措列。读法同时写明本波不新建、不加列，不读三张缺项表的 `brief` / `conclusion` / `body`，不读前端种子 `impact` / `prediction`。两句因此没有可落的库.表.列。
- **依据**：说明书 100–107 行；读法 28–34 行；DATA 第 5 节只定热点、影响、报告、主题分布；硬清单 data-agent 第 1 条。
- **建议**：补上已有列之前，这个位置固定写「这一领域还没有汇总到政策举措」。只汇总出一句的规则先悬着。不把热点说明、影响结论、报告正文挪来当两句，不读 `keyFieldPolicyAnalysis`。不新建正式表，不加列。

### [data] D2 · 政策条数、平均评分、对标区域、关键焦点没有列

- **问题**：205-1 要求每张卡仍看见政策条数、平均评分、对标区域、关键焦点。读法只规定没有两句举措时，政策条数、平均评分、对标区域写「—」，关键焦点留在原标签位。已经有两句时，这四项仍然没有库.表.列。种子里的 `totalPolicies`、`avgScore`、`topRegions`、`keyFocus` 被读法排除。`policy_timeseries.publish_count` 是整页某年的发布量，不能当成这一领域的政策条数。
- **依据**：说明书 69、95、105 行；读法 32–34 行；DATA 第 4 节；`lumen-ui-science-pc/src/mock/modules/policySeed.ts` 1304–1357 行。
- **建议**：这四项本波一律写「—」，有没有举措都一样。关键焦点标签留着，名称不改，内容不填热点名。不写 0，不编地区。不加列。

### [data] D3 · 领域名筛不了时序，热度也没有可复算的列规则

- **问题**：热度没有自己的列，只能从 `gkxlumenx_ads.policy_timeseries` 的 `publish_count` 看走向。这张表的列是 `period_type`、`period_key`、`publish_count`、`growth_rate`、`continuity_rate`，没有领域列。说明书第 83 行把领域名写成看这一条时序时的筛选；读法第 38 行写四张卡的热度都对上整页这一条。两条并立时，后波会去给时序加领域列。DATA 已写明第一批 `growth_rate`、`continuity_rate` 留空，不能拿它们当热度。只有一个有点数的年份时，往上、走平、往下比不出来，读法没有写这一格显示什么。
- **依据**：说明书 83、109–116 行；读法 36–40 行；DATA 第 4 节第 70 行；`ads.md` 157–170 行。
- **建议**：四张卡共用整页这一条年行，领域名不进这张表的筛选。热度只比较已有点的 `publish_count`：后一点更高写「热度上升」，相等写「热度稳定」，更低写「热度下降」。少于两个有 `publish_count` 的点时写「暂时看不了热度」，不补 0。不读留空的 `growth_rate`。不加列，不建分领域时序表。无点时图空，热度写「暂时看不了热度」。

### [data] D4 · 政策全景没有对上已有列

- **问题**：205-6 的全景要按这一张卡的领域列出已经汇总的政策。读法只写沿用全景已有政策列表，没有库.表.列。已登记的类别列 `policy_category_rel.category` 取值是科创政策、行业政策、园区政策、招商政策、人才政策、财税政策、知识产权，对不上科创发展、人才引进、资金扶持、技术发展方向。检索用数范围是 `gkxlumenx_dwd.policy_base_info` 的国内当前行，没有「各国政府」列。种子 `searchKeyword`（科创 / 人才 / 研发 / 人工智能）被读法排除，不能拿来顶领域条件。
- **依据**：说明书 136–140 行；读法 54–58 行；`POL-L2-DS10-QRY-DATA` 第 39、41、67–72 行；`dwd.md` 149–155 行；`policySeed.ts` 1307–1348 行。
- **建议**：本波不新建正式表、不加列。四个领域名对不上已有条件列时，全景写「这一领域还没有政策全景」。不把「科创政策」或关键词「科创」当成「科创发展」。不用 `demo_gkxlumenx_dwd` 的行填正式全景。

### [data] D5 · 合格行只看「缺项演示」前缀，和中台成功行不一致

- **问题**：热点、影响、深度报告的列可以落到上表。读法把合格行定成正文不以「缺项演示」开头，没有同时要求 `fill_method` 为 `llm`，也没有先去掉空白。中台成功行是 `fill_method` 去空白后等于 `llm`，正文字段去空白后非空且不以「缺项演示」开头；热点还要同一领域凑满 2 条才算成功，领域闭集只有科创发展、人才引进、资金扶持。正式库种子给这三个领域写的是 `fill_method=manual`、正文以「缺项演示」开头；技术发展方向没有种子行。只卡前缀时，手工改掉开头四个字的 `manual` 行会显示成已生成。展示若去读 `demo_gkxlumenx_ads`，就离开了「迁移前仍读正式库」。
- **依据**：读法 16–18、42–62 行；DATA 5.1–5.4 与第 6 节（三个领域、`fill_method` 固定 `manual`）；`gapfill_policy_trend.sql` 第 5–65 行；`trend_hotspot_job.py` 第 17–18、53–66 行；硬清单第 2、3 条。
- **建议**：合格行三条一起满足：`fill_method` 去空白后等于 `llm`；`brief` / `conclusion` / `body` 各自去掉空白后非空；去掉空白后都不以「缺项演示」开头。热点同一 `domain_name` 合格行少于 2 条时，这一领域写「这一领域还没有热点」。没有合格行时走读法已写的空态。展示继续只读 `gkxlumenx_gapfill` 这三张表，不读 `demo_gkxlumenx_ads`，不抄行，不新建正式表，不加列，不改主键。

## 核对过、无异议

1. **热点、影响、深度报告的业务列已经在 DATA 第 5.2–5.4 节。** 热点是 `domain_name`、`hotspot_name`、`brief`；影响是 `domain_name`、`impact_object`、`impact_direction`、`conclusion`；深度报告是 `title`、`domain_name`、`body`。不改挂焦点指数、实施效果、推演、序号 211、序号 217。
2. **三张卡各自的空态文案已经写在说明书和读法里。** 没有热点、没有影响评估、没有深度分析报告、读失败可重试、失败不删旧行、业务界面不出现库名表名。技术发展方向没有合格行时走各自空态，不为它建表，也不为它建指标。
3. **本波不写 ODS、DWD、正式 ADS、供应方库。** 缺项表留在 `gkxlumenx_gapfill`。演示库写入已有中台作业，展示打开不接那张库。D4 不因这次读法改绿。

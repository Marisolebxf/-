# POL-L2-DS12-EST-DATA · 政策效果推演 · 效果预估 · 数据落点

- 任务：`POL-L2-DS12-EST-DATA`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-06`
- 上游架构：`sdd/l2/POL-L2-DS12-EST-ARCH.md` 第 9 节。该稿文件头写明待架构、算法、数据、产品四角色会签，不标 done。2026-11-05 只改了第 5.4、5.5 节的库.表写法，读法未改。本单按第 9 节定列，不改那份架构，不改图。
- 对照：同目录 `POL-L2-DS12-SIM-ARCH.md` 第 7、9 节，只读。235、236 的交叉只写在第 1 节末句。

2026-11-07 修订（`human:淮政玮`）：未出台仿真增加列 `target_industry`。行上必填，是产业级联回显全文。已有两行分别写 `新一代信息技术`（研发补助那一行）、`生物产业`（人才引进那一行）。查询只在请求带了该字段时等值。不写入 `industry_text`。新出台预测行、区域空间行此列留空。同一组政策类型、覆盖范围、支持力度、实施时间、目标产业只留一行。修复单 `POL-L2-DS12-INDUSTRY-EQ-FIX-L01`。

本叶只定政策效果推演二级「效果预估」里 SRS 序号 **232–234** 的数据落点。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本。

上游只引用，不改写：`POL-L2-DS12-EST-ARCH` 第 9 节，以及第 5.1–5.3 节的行内容。不新造 `metric_id`，不改 D4。

## 1. 范围

三叶都在政策效果推演的效果预估里完成。浏览器只打 `/display/v1/policy/**`。查询只读表。查询请求不灌数。表里没有行、或条件对不上，该区返回空。空态是空。不把空表写成 501，接口也不直接返回写死的预测。真模型种类在未注册时如何返回，仍以架构稿为准；那一条不落在本表。本单不改 `sdd/指标与501.md`。

本二级的三类预测不读已有 ADS，也不读已经落库的推演结果。`ads.policy_simulate` 继续只服务中台读面，行不复制进本表。`ads.policy_text_parse` 的解析行不进入本表。仓库里没有已落库的未出台仿真、新出台预测或区域空间结果可以复用。三叶只读将由灌数单新建的这一张缺项表。表还没建、或建了但没有对得上的行时，对应块返回空。

233 的政策标识与全景检索目录的 `policy_id` 是同一业务键。那份目录不是本表。本单不读目录正文来填预测值，也不新建政策列表读面。

| 序号 | 叶子 | 库 | 表 | 本单 |
|---|---|---|---|---|
| 232 | 未出台政策仿真模拟 | `gkxlumenx_gapfill` | `gapfill_policy_sim_forecast` 的未出台仿真行 | 本单定列。建表与灌数在灌数单 |
| 233 | 新出台政策效果预测 | 同一库 | 同一张表的新出台预测行 | 与 232 同一张表，不另建 |
| 234 | 区域经济发展空间模拟 | 同一库 | 同一张表的区域空间行 | 与 232 同一张表，不另建 |

三叶行上的 `metric_id` 都用已有推演键 `M_POLICY_SIMULATE`。该指标的 D4 保持 `mock`。不因此新注册，也不把 D4 改绿。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本叶不把 mock 写成已上线，也不把该闸门写成已解开。

本叶唯一新建的表是库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`。库只允许 `gkxlumenx_gapfill`。表名以 `gapfill_` 开头。本单只定列，不建库，不插入。不写 `gkxlumenx_ods`、`gkxlumenx_dwd`、`gkxlumenx_ads`，不写供应方库。

`gkxlumen-display` 不直连库。`gkxlumen-element` 按种类只读这张表。232、233、234 都走 `POST /display/v1/policy/simulation/jobs`。Java 不生成方案，不按弹性公式现算，不插入行。

235 的列归 `POL-L2-DS12-SIM-DATA` 的库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_result`，236 的列归同一单的库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_stakeholder`；读路径见 `POL-L2-DS12-EST-ARCH` §5.4/§5.5，灌数见 `POL-L2-DS12-SIM-GAPFILL-L01`。

## 2. 唯一新表

库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_forecast`。232、233、234 共用这一张。不拆成三张表。235、236 不写入本表。

一行是一组未出台参数档，或挂在一条已有政策上的一条预测，或挂在一个区域和一个政策类型上的一条空间结果。一行不是一份地图文件，不是一条用户模拟历史，不是一条文本解析记录，不是中台 `ads.policy_simulate` 上的一条省级力度情景。

`row_kind` 只有三个值：

| 值 | 序号 | 这一行放什么 |
|---|---|---|
| `未出台仿真` | 232 | 一组参数档：政策类型、覆盖范围、支持力度、实施时间、目标产业，以及经济效益、社会影响、创新促进的预测值与变化率、逐年趋势、一句解释 |
| `新出台预测` | 233 | 挂在一条已有政策上：短期与长期效果、经济增长、产业发展、科技创新影响、时间变化趋势、空间分布特征、相似政策依据说明 |
| `区域空间` | 234 | 挂在一个区域 × 一个政策类型上：GDP 增长、产业结构变化、就业率变化、空间分布 |

没有第四个值。与 SIM 组两张表的种类不是同一列。那两张表的行不写入本表，本表的行不写入那两张表。

下列是必要列。建表语句由灌数单 `POL-L2-DS12-EST-GAPFILL-L01` 落地。本单不执行该单，也不在这里给出可执行脚本。这张列清单不是可执行 SQL。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `row_kind` | varchar(16) | 否 | `未出台仿真`、`新出台预测`、`区域空间` 三者之一 |
| `policy_type` | varchar(256) | 是 | 未出台仿真行、区域空间行必填：政策类型。新出台预测行留空 |
| `coverage_scope` | varchar(256) | 是 | 未出台仿真行必填：覆盖范围。其余行留空 |
| `support_intensity` | varchar(256) | 是 | 未出台仿真行必填：支持力度。其余行留空 |
| `implement_time` | varchar(256) | 是 | 未出台仿真行必填：实施时间，展示原文。与 `generated_at` 不是同一列。其余行留空 |
| `target_industry` | varchar(256) | 是 | 未出台仿真行必填：目标产业，级联回显全文。其余行留空。不是 `industry_text` |
| `econ_text` | text | 是 | 未出台仿真行必填：经济效益的预测值与变化率。其余行留空 |
| `social_text` | text | 是 | 未出台仿真行必填：社会影响的预测值与变化率。其余行留空 |
| `innovation_text` | text | 是 | 未出台仿真行必填：创新促进的预测值与变化率。其余行留空 |
| `yearly_trend` | text | 是 | 未出台仿真行必填：逐年趋势，若干组年份和数值。其余行留空 |
| `explain_text` | text | 是 | 未出台仿真行必填：一句解释。其余行留空 |
| `policy_id` | varchar(100) | 是 | 新出台预测行必填。与全景检索目录的政策 `policy_id` 同一业务键。不建外键。其余行留空 |
| `policy_title` | varchar(256) | 是 | 新出台预测行必填：政策名称，只供展示。不复制政策正文。其余行留空 |
| `short_effect_text` | text | 是 | 新出台预测行必填：短期效果说明句。其余行留空 |
| `medium_effect_text` | text | 是 | 新出台预测行可选：中期效果说明句。其余行留空 |
| `long_effect_text` | text | 是 | 新出台预测行必填：长期效果说明句。其余行留空 |
| `growth_text` | text | 是 | 新出台预测行必填：经济增长影响说明句（卡下脚注）。其余行留空 |
| `industry_text` | text | 是 | 新出台预测行必填：产业发展**柱图**「名+分」串（如 `人工智能95、生物医药88`）。不兼作卡内产业发展 KPI。其余行留空 |
| `tech_effect_text` | text | 是 | 新出台预测行必填：科技创新影响说明句（卡下脚注）。其余行留空 |
| `time_trend_text` | text | 是 | 新出台预测行必填：时间变化趋势。格式 `2026-06月45/85、…`（值/置信度百分数）；无置信度时可写旧式无斜杠。其余行留空 |
| `space_feature_text` | text | 是 | 新出台预测行必填：空间分布特征。其余行留空 |
| `similar_basis_text` | text | 是 | 新出台预测行可保留一句总述。界面列表以 `similar_items` 为准。其余行留空 |
| `similar_items` | text | 是 | 新出台预测行必填（COVER-FDE）：相似政策列表 `名称|匹配|效果；…`，至少 2 条。其余行留空 |
| `term_kpi_text` | text | 是 | 新出台预测行必填（COVER-FDE）：短中长期三维 KPI `短期|gdp|产业|科创；中期|…；长期|…`。其余行留空 |
| `auto_tags` | varchar(512) | 是 | 新出台预测行可选：关键词标签串。其余行留空 |
| `region_name` | varchar(256) | 是 | 区域空间行必填：用户所选区域的名称。其余行留空 |
| `gdp_text` | text | 是 | 区域空间行必填：GDP 增长，展示原文。其余行留空 |
| `industry_change_text` | text | 是 | 区域空间行必填：产业结构变化，展示原文。其余行留空 |
| `employment_text` | text | 是 | 区域空间行必填：就业率变化，展示原文。其余行留空 |
| `spatial_items` | text | 是 | 区域空间行必填：空间分布，若干组更细区域名和数值。其余行留空 |
| `is_mock` | tinyint | 否 | 每行必须为 1。D4 仍是 mock |
| `metric_id` | varchar(64) | 否 | 三种行都固定 `M_POLICY_SIMULATE`。不写空，不写别的指标 |
| `gap_item` | varchar(128) | 否 | 序号加叶子名。见下表 |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间。由灌数单填写，本单不生成 |

种类用不到的列留空，写 NULL，不写空字符串。

`gap_item` 按种类固定：

| `row_kind` | `gap_item` |
|---|---|
| `未出台仿真` | `232 未出台政策仿真模拟` |
| `新出台预测` | `233 新出台政策效果预测` |
| `区域空间` | `234 区域经济发展空间模拟` |

`fill_method` 固定 `manual`，因此不设 `fill_model`。政策只在方法为 `llm` 时要求模型名。

D16 行级列就是 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。外加 `is_mock=1`，避免把缺项行读成已上线。谁写这张表：灌数单里的 Python 脚本。Java 与前端不建表、不灌数。谁读：仅功能验收链路上的 `gkxlumen-element`。生产配置不读 `gkxlumenx_gapfill`。本叶不把读到的行写入 ADS，因此不产生 `gapfill_` 前缀的 `calc_batch_id`。

拣行只用 `row_kind`，再加上该种类的条件列。未出台仿真再加用户本次提交了的 `policy_type`、`coverage_scope`、`support_intensity`、`implement_time`、`target_industry`。新出台预测再加 `policy_id`。区域空间再加 `region_name`，政策类型提交了再加 `policy_type`，不加 `target_industry`。条件对不上的行不返回。查询不插入行来凑数。

灌数时的不重复，由灌数单照下面三条保管，本单不建库：

- 未出台仿真：同一组 `policy_type`、`coverage_scope`、`support_intensity`、`implement_time`、`target_industry` 只留一行。
- 新出台预测：同一 `policy_id` 只留一行。
- 区域空间：同一 `region_name` 加同一 `policy_type` 只留一行。

## 3. 232 未出台仿真

粒度：一行一组参数档。政策类型在 `policy_type`。覆盖范围在 `coverage_scope`。支持力度在 `support_intensity`。实施时间在 `implement_time`。目标产业在 `target_industry`。经济效益在 `econ_text`。社会影响在 `social_text`。创新促进在 `innovation_text`。逐年趋势在 `yearly_trend`。一句解释在 `explain_text`。

`econ_text`、`social_text`、`innovation_text` 各是一段文字，内容是该方面的预测值与变化率。基线到推演后的对照写在这两段里。不另设 baseline、simulated、delta 三个数值列，也不把这三方面收成闭集以外的滑块。`yearly_trend` 是若干组「年份、数值」，组数不固定，供前端画曲线。不单列年份。`explain_text` 是一句可解释说明。查询原样返回这五列。请求内不调用 `polan.text.simulate.run`，不按弹性公式现算。

五列参数档在行上都要有值。它们是展示原文，不是资金、人才、平台三个滑块，也不是中台那三条固定情景的原文。`target_industry` 是级联回显全文：只选集群时就是集群名，选到更深节点时用 ` / ` 连接。已灌两行：研发补助那一行是 `新一代信息技术`，人才引进那一行是 `生物产业`。多选回显含 `、` 或「等 N 项」时整串参与等值，不拆成多行 OR。

`metric_id` 固定为已有 `M_POLICY_SIMULATE`。不新注册，不改这条指标的 D4，不把读到的行写成已上线。不挂 `M_POLICY_LAYOUT_REC_COUNT`，不挂 `M_POLICY_DEEP_171_1`，不挂 `M_POLICY_EFFECT_SCORE`，不挂 `M_POLICY_INTENSITY_SCORE`。

`jobs` 的未出台仿真只读 `row_kind=未出台仿真`。政策类型、覆盖范围、支持力度、实施时间、目标产业五类至少提交一类。用户提交了的参数必须与行上对应列相等。用户没提交的参数不参与过滤。五类都没提交则该区空，不返回全部未出台仿真行。提交了但对不上任何行则该次模拟空，不补默认档。对得上的多行一并返回，供前端并排比较。服务端不建对比槽，不存用户自己的模拟历史。无行则该区空。

## 4. 233 新出台预测

粒度：一行挂在一条已有政策上。政策标识在 `policy_id`。政策名称在 `policy_title`。短期/中期/长期说明句在 `short_effect_text` / `medium_effect_text` / `long_effect_text`。卡内三维数值在 `term_kpi_text`。经济增长/科技创新说明句在 `growth_text` / `tech_effect_text`。产业发展柱图分在 `industry_text`。时间变化趋势在 `time_trend_text`（可带置信度）。空间分布特征在 `space_feature_text`。相似政策列表在 `similar_items`；`similar_basis_text` 可作一句总述。关键词在 `auto_tags`。

`similar_items` 是列表原文串，至少两条。`term_kpi_text` 固定三期。查询原样返回。不调 `parse/jobs`，不调 `policy_text_parse` 通道，不读 `ads.policy_text_parse` 来顶替预测行。2026-11-12 `POL-L2-DS12-EST-233-COVER-FDE-L01` 增列与趋势置信度格式。

需规没有定义「新出台」按颁布日期还是按状态。本单的临时默认：行上不设是否新出台，不设颁布日期截断。`policy_id` 必须对得上全景检索目录里已有政策的同一业务键。哪几条政策挂预测行，由灌数单在能对上的政策里选取。查询只按 `policy_id` 拣 `row_kind=新出台预测`，不在查询里判断颁布日期。用户以政策文本选定一条政策时，先落到目录里的 `policy_id` 再拣行。本表不存政策正文，不按正文全文匹配。没有 `policy_id` 则该区空，不返回全部预测行。对不上则该区空。甲方确认「新出台」口径之前保持这个默认。本单不改客户决策清单。

`metric_id` 固定为已有 `M_POLICY_SIMULATE`。不新注册，不改 D4。不把解析键 `M_POLICY_TEXT_PARSE` 写进行上。

`jobs` 的新出台预测只读 `row_kind=新出台预测`。政策必选。无行则该区空，不返回解析结果顶替。

## 5. 234 区域空间

粒度：一行挂在一个区域名称 × 一个政策类型上。区域名称在 `region_name`。政策类型在 `policy_type`。GDP 增长在 `gdp_text`。产业结构变化在 `industry_change_text`。就业率变化在 `employment_text`。空间分布在 `spatial_items`。

区域粒度按本单定为：`region_name` 是用户所选区域的一段名称。不拆成省、市、区三列编码，不建区划字典。同一政策类型下区域名称不重复。`spatial_items` 是若干组「更细区域名、数值」，组数不固定，写在这一行上。热力图、三维地图用这些组，渲染在前端。服务端只返回行。不存地图文件，不设对象键，不设文件字节列。不造名为「全国」的兜底行。

`gdp_text`、`industry_change_text`、`employment_text` 是已灌入的展示原文。查询原样返回。Java 不现算增长率。

`metric_id` 固定为已有 `M_POLICY_SIMULATE`。不新注册，不改 D4。不把这三列挂到别的指标上。

`jobs` 的区域空间只读 `row_kind=区域空间`。区域必选。未选区域则空间结果空，不返回全部区域行。政策类型提交了则必须与 `policy_type` 相等；没提交则只按 `region_name` 拣。类型对不上则空间结果空。无行则该区空。

## 6. 灌数单

灌数单 `POL-L2-DS12-EST-GAPFILL-L01` 依赖本单和 `POL-L2-DS12-EST-ARCH`。执行人是 `data-agent`，监管是 `human:淮政玮`。本单只点名，不认领，不执行，不建库，不插入行，不改那张任务的注册字段。

该单当前仍是 `backlog`。它的 DoD 已经指向这一张表：在 `gkxlumenx_gapfill` 建 `gapfill_policy_sim_forecast`，独立脚本灌入未出台、新出台、区域空间三类预测结果行，不挂布局推荐，不改 D4，不新造 `metric_id`。执行时列按第 2 节，行按第 3 至第 5 节。

灌数单要灌的最少内容，沿架构第 9 节，本单仍不执行：

| 种类 | 灌数单以后要灌 | 不灌 |
|---|---|---|
| 未出台仿真 | 若干参数档行。每行含四类参数档、经济效益、社会影响、创新促进的预测值与变化率、逐年趋势、一句解释 | 中台三条情景原文、弹性现算、用户模拟历史、布局推荐条数 |
| 新出台预测 | 挂在已有政策上的预测行。含短长期效果、三类影响、时间趋势、空间特征、相似政策依据说明 | 独立文本解析行、顶替用的解析结果、政策正文、布局推荐条数 |
| 区域空间 | 挂在区域 × 政策类型上的行。含 GDP、产业结构、就业率变化、空间分布数据 | 全国通用兜底行、地图文件、布局推荐条数 |

三种业务行都带第 2 节的 D16 列，`fill_method=manual`，`is_mock=1`，`metric_id` 固定 `M_POLICY_SIMULATE`。

查询请求不调用这张灌数单。空表返回空。本单不写示例行。235、236 的灌数不在本单，见第 1 节末句。

## 7. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| `ads.policy_simulate`、`M_POLICY_SIMULATE` 的中台读面、`polan.text.simulate.run`、`/v1/policy/simulate` | 中台省级力度情景留在原地。不复制进本表。本表三叶行上的 `metric_id` 只用这条已有推演键，不改 D4，不改 `run()` |
| `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` | 布局推荐键。不写入本表，不灌条数 |
| `M_POLICY_EFFECT_SCORE`、`M_POLICY_INTENSITY_SCORE` | 效能得分留评价页，力度分留全景。不挂本表 |
| `M_POLICY_TEXT_PARSE`、`parse/jobs`、`parse/clauses`、`ads.policy_text_parse` | 233 不调。解析行不复制进本表，也不顶替预测行 |
| `evaluation/jobs` 序号 228 | 评价键的参数模拟。不共用本表，不把本页参数档写成评价方案 |
| `report/jobs` | 核增研报。不写入本表 |
| 全景检索目录 | 只提供 233 的 `policy_id` 业务键。本单不读它的正文来填预测，不新建政策列表 |
| 235、236 | 见第 1 节末句。本表不放这两类行，本文不写那两张表的列 |
| `GDF-POLICY-MOCK-GATE-L01` | 仍是 blocked。本单不把它写成已解开 |

## 8. 明确不做

- 不写可执行 SQL，不建库，不灌数，不跑推演函数。
- 不重开 GDF，不写 nGQL，不加 ODS、DWD、ADS 表，不写供应方库。
- 不把本表拆成三张。不把 235、236 写进本表，也不在本文展开那两张表的列。
- 不新造 `metric_id`，不改 D4，不把缺项行写成已上线。
- 不把中台三条情景、弹性曲线、`ads.policy_simulate` 的行灌进本表。
- 不灌文本解析行，不把 `ads.policy_text_parse` 复制进本表。
- 不灌地图文件，不写对象存储，不设文件列，不造全国兜底行。
- 不把用户模拟历史、页面上的新意见写回本表。
- 查询不插入。空态是空，不写成 501。列清单不是可执行 SQL。
- 不改架构稿、调研分册、`指标与501.md`、说明书、WBS、注册表。
- 不认领 `POL-L2-DS12-EST-GAPFILL-L01`，不认领 `POL-L2-DS12-SIM-GAPFILL-L01`。
- 不把本单标成 done 或 ready_to_sign。

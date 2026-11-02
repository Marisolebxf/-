# M_SCIUI_P10_022 科技人员流动动态 —— 指标信息 MD

> **类型**：简单统计类｜ **域**：时空演进 New·要素总览·人员流动（`SpaceTimeEvolutionNewPage.jsx:1089`）｜ **UI 挂载**：科技信息展示系统 → 创新载体孵化载体 New（时空演进页）→ 要素卡「科技人员流动动态」（人）+ KpiTile Q0205
> **数据支持度**：**完全转换支持**｜ **公式定义人**：无（净流入口径 UI 标签与 mock 计算式不一致；库口径=入-出一步转换）｜ **口径归属**：UI 挂载件（SRS 无同名指标；上位叶=时空演进展示·序号 507 族）
> **复现脚本**：`code/M_SCIUI_P10_022.py`（薄壳实算，共享探针 `code/_shared_s308_laneb_probe.py`）｜ **产物**：`code/M_SCIUI_P10_022_out.json`
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（无现成净流入结果面）；直接数据=无；依赖结构=完全（jiuxin 流动三件套：yearly_flow 51,489 行/event 298,384 行/geo 面 inbound-outbound 列）；依赖数据=完全（2018-2025 八年净流入+跨域事件实算）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全转换支持。**（久新流动三件套一步转换：净流入 = inbound − outbound（同行两列）；跨域事件三标志现成——中国 2018-2025 净流入 +115→+21 八年实算）。

### 批次通用纪律摘要（S3-08 批共用）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除/相减 | 净流入=同表同行两列相减（share_basis 注记） |
| B4 | 负结论带探针 | dev/gkx 流动面缺失留证（absence_probe） |
| B5 | 确定性 | 年份 sorted；守恒断言全零校验 |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳实算脚本重跑产出 |
| B8 | 回执不复收 | 实算读数可重跑复验 |
| B9 | 单位/日期陷阱 | 2026 不完整年截断；单位人 |
| B10 | 口径裁定保守交付 | 净流入（区域切）vs 毛存量（mock 式）双口径披露，触发器写死 §1.6 |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成净流入面吗？ | 无直出面 | 需 inbound−outbound 一步转换（geo 面两列现成） |
| 流动事件面数据量够吗？ | 够 | event 298,384 行（2000-2025）+ yearly_flow 51,489 行 |
| 区域切得动吗？ | 切得动 | COUNTRY/PROVINCE/CITY 三级全有（geo 面 171,736 行） |

## 摘要

「科技人员流动动态」是时空演进 New 页「全球要素总览」四联卡的第四卡（`SpaceTimeEvolutionNewPage.jsx:1089`）：stat 绑 `kpis.talent`（人），desc「全球科研人员净流入」，点击下钻 `ste-b-talent` 可视化区块（P10_023）；页首另有 KpiTile「科研人员净流入（Q0205）」（`:681`）。数据侧判定：**完全转换支持**——久新流动三件套承载：①`ads_geo_yearly_metrics`（171,736 行）含 `inbound_talent_count`/`outbound_talent_count` 现成列，净流入=同行两列相减（中国 2018-2025：+115/+95/+155/+158/+96/+28/−5/+21 人）；②`ads_talent_mobility_event`（298,384 行，30 列）含跨域三标志（2024 年：事件 33,461 起，其中国家级跨域 419/省级 669/市级 817）；③`ads_talent_mobility_yearly_flow`（51,489 行，LOCATION/INSTITUTION/DISCIPLINE 三维）。口径修正点：mock 计算式为毛存量外推（26 城 base.talent 求和）而 UI 标签写「净流入」——切真时按库净流入口径并修正 desc（COUNTRY 全集合计逐年=0 守恒，「全球净流入」无意义，须按区域切）。gkx 学者履历面（21,316 学者/57,117 工作经历）为备选路径，精度低于事件面。

- 需求判定：**UI 挂载件**（SRS 无同名；上位叶=序号 507 族 + bid_desc 500「科技人员流动等实时动态数据」）。
- 复现状态：薄壳实算已跑通；净流入/跨域事件序列落产物。
- 档位结论：**完全转换支持**（三面齐备一步转换）。
- 关键事实：中国 2024 净流入 −5 人（2024 净流出国 Top：香港/美国/西班牙）——存量大国亦有净流出年。
- 升档路径：久新建区域净流入物化视图 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 时空演进展示（New 页族）→「全球要素总览」四联 ElementCard 第四卡「科技人员流动动态」（`SpaceTimeEvolutionNewPage.jsx:1089`，icon=IconUserGroup，color=#00B42A）。卡组另三卡：学术论文/专利交易（P10_001）/科技资金。`kpis.talent` 由 `getGlobalTotals`→`aggregateStats` 毛存量外推（`mockData.js:244-253` talent 按 growth×0.8 外推）。`:681` 页首 KpiTile `label=科研人员净流入（${year}）value=kpis.talent metricId=Q0205`。点击 `scrollToBlock('ste-b-talent')` 下钻 P10_023 可视化区块。

### 1.2 为什么需要本指标

人员净流入是区域科研吸引力的净读数：净流入持续为正=人才磁极形成，负值年提示竞争力预警（SRS 507 需规原文「辅助团队建设和全球人才战略引导」）；它是「要素总览」四卡的人才维锚点，与论文/专利/资金三卡构成要素全景。

### 1.3 需求文档是否给出定义方法

**三份说明书未给出该指标的计算方法。**「科技人员流动动态」卡片名未在需求文档出现；上位语义（507 需规+bid_desc 500）只给功能行为（跟踪流动、识别趋势、展示热点），无净流入公式（入-出的区域层级/期间）、无人员口径（学者/工程师/学生）。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①OECD/欧盟人才流动指标（Migration of scientists：国家间净流动率，履历法）；②美国 NSF Survey of Doctorate Recipients（职业流动调查，问卷法）；③Nature Index 人才流动（机构间转移计数，署名法）。久新事件面（from/to institution/location 双 ID+跨域三标志）与①③的方法原料同构——履历法已在库内物化（event 表即履历时序差分结果），权威方法可直接落地。完整版见附录 C。

### 1.5 引用来源

1. OECD. Handbook on Measuring the Mobility of Scientists（科学家流动测量手册）. https://www.oecd.org/sti/sci-tech/
2. NSF. Survey of Doctorate Recipients（博士职业流动调查）. https://www.nsf.gov/statistics/srvydoctoratework/
3. Nature Index. Talent flow（机构间人才转移口径）. https://www.nature.com/nature-index/

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **口径 A（区域净流入，已实现）**：净流入 = inbound_talent_count − outbound_talent_count（geo 面同行两列，COUNTRY 级按区域切）。
- **口径 B（跨域事件量，已实现）**：年度跨域事件数 = COUNT(event) 分 is_cross_country/province/city 三标志。
- **口径 C（毛存量，mock 式）**：Σ talent_count 外推——与「净流入」标签不一致，弃用但披露。
- **降档触发器**：若 UI 强约束「全球净流入」单值（全集守恒恒=0 无意义）→ 须先修 desc 为区域读数，否则口径不可交付。
- **升档触发器**：久新建区域净流入物化视图（年份×层级预聚合）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/科技时空演进展示.md` |
| 所属四级功能 | 1.1.1.1.4.6 科技成果展示（域）|
| 所属页面 | 时空演进 New（创新载体孵化载体 New 页族）|
| 本件叶 | 要素总览卡「科技人员流动动态」+KpiTile Q0205（UI 挂载件；上位叶=序号 507 族）|
| 相近叶 | P10_023 可视化区块（同根下钻位）/P10_001 专利交易卡（同卡组）；序号 510 科学家协作网络（同域邻叶）|
| UI 容器 | `SpaceTimeEvolutionNewPage.jsx:1082-1094` ElementCard |

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径 A（区域净流入，已实现）**：入−出两列相减，按 COUNTRY 级区域切（本件判档依据）。
- **口径 B（跨域事件量，已实现）**：event 表三标志年度计数（佐证面）。
- **口径 C（毛存量，mock 式）**：披露弃用——与「净流入」标签语义不符。
- **裁定**：A/B 结构+数据均足；C 仅作 ui_demo_fallback 对照。

### 2.2 探针读数实测

```sql
SELECT statistics_year, inbound_talent_count - outbound_talent_count
FROM ads_geo_yearly_metrics
WHERE location_level='COUNTRY' AND location_id='loc_B56D...';  -- 中国
SELECT event_year, COUNT(*), SUM(is_cross_country), SUM(is_cross_province), SUM(is_cross_city)
FROM ads_talent_mobility_event WHERE event_year BETWEEN 2018 AND 2025
GROUP BY event_year;
```

实读：中国净流入 2018-2025 = +115/+95/+155/+158/+96/+28/−5/+21 人（2021 峰值 +158，2024 转负 −5）；跨域事件 2018=25,493 起（国家 636/省 926/市 1,090）、2024=33,461 起（国家 419/省 669/市 817）。COUNTRY 全集合计逐年=0（守恒断言通过）。

### 2.3 读数落盘与同基核对

净流入序列落 `derived[0]`——同表同行两列相减（B3 同基注记）；跨域事件四元组落 `derived[1]`；守恒校验面落 `derived[2]`（全零序列，证明「全球净流入」须按区域切）。

### 2.4 稳健性与口径敏感性

2026 为不完整年（geo 面 talent 流动 0 行）截断；2025 净流入 +21 偏低（收录滞后）；location_id 硬编码改为 name 解析时注意中国大陆/香港分行（本件中国行不含香港——香港 2024 净流入 +19 另行）；assignment_confidence 列（事件面）提示部分事件为推断归属，正式口径可加置信度过滤。

### 2.5 基期年份可用性

`base_years_used`=2018-2025 八年；`missing`=[]；基期建议 2018；事件面全序列 2000-2025 二十六年更长可用。note 详附录 B。

### 2.6 需求符合性预评

卡片 stat 可切真（口径 A 区域净流入序列）；desc「全球科研人员净流入」须修正为区域读数（守恒约束）；KpiTile Q0205 同步切真；专业主题维（507 需规「各专业主题下」）需 DISCIPLINE 维（5,753 行）下钻，主体卡无此约束。

### 2.7 复现代码结果展示

复现入口 `python3 code/M_SCIUI_P10_022.py`（薄壳直连久新实算：geo 面净流入+event 三标志+守恒断言）；产物 `code/M_SCIUI_P10_022_out.json`；关键读数：`derived[0]` 八年净流入、`derived[1]` 跨域事件、`derived[2]` 守恒校验。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | 流动三件套 51,489/298,384/171,736 行 | facts.jiuxin_*_rows |
| 2 | 中国净流入 +115→+21（2024 −5） | derived[0] |
| 3 | 跨域事件 2018=25,493 / 2024=33,461 | derived[1] |
| 4 | 全集守恒逐年=0 | derived[2] |
| 5 | dev/gkx 无流动事件面 | absence_probe[0]/[1] |
| 6 | 判档 完全转换支持 | support_judgment |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 净流入列（入/出） | jiuxin `ads_geo_yearly_metrics` | **有**（inbound/outbound_talent_count 现成） |
| 流动事件底表 | jiuxin `ads_talent_mobility_event` | **有**（298,384 行，30 列含三跨域标志） |
| 年度流量面 | jiuxin `ads_talent_mobility_yearly_flow` | **有**（51,489 行三维） |
| 区域字典 | jiuxin `ads_location` | **有**（22,229 行） |
| 净流入现成结果面 | 三源 | **无**（一步转换——判转换支持的依据） |
| dev 流动面 | dev | **无**（scholar 名录+链上列，无事件面） |
| gkx 履历面 | gkx `dwd_scholar_work_experience` 等 | **备选**（57,117 行，精度低于事件面） |

### 3.2 现场复核清单

UI 链实读：`SpaceTimeEvolutionNewPage.jsx:1089` ElementCard stat 绑 `kpis.talent`、`:681` KpiTile Q0205、`mockData.js:244-253` 外推式。久新实连复核（本件脚本）：geo 面净流入八年序列+守恒断言；event 面三标志年度合计；yearly_flow 维度分布 LOCATION 28,672/INSTITUTION 17,064/DISCIPLINE 5,753。dev/gkx 词族见 absence_probe。

## 四、数据缺失情况

### 4.1 缺口清单

①净流入物化视图未建（现算，判「转换」不判「直接」）；②2026 不完整年（talent 流动 0 行）；③专业主题维（DISCIPLINE 粒度到领域非 UI 六主题）映射未做；④人员类型维（学者/工程师）无区分（event 面全员口径）。

### 4.2 修复建议与影响面

短期：卡片+KpiTile 切口径 A 真数（八年序列现成）+desc 修正。中期：久新建区域净流入物化视图 → 完全直接支持（联动 P10_023/025 三件）。远期：DISCIPLINE→UI 主题映射 + 人员类型维扩展。同族联动：P10_023（可视化）/P10_025（主体路径）共用三面，一次物化三件升档。

### 4.3 影响面

要素总览四卡中本卡与 P10_001 同批可切真；「净流入」语义修正后数据链完整；P10_023 热点三标签同步受益。

## 参考文献

1. OECD. Handbook on Measuring the Mobility of Scientists. https://www.oecd.org/sti/sci-tech/
2. NSF. Survey of Doctorate Recipients. https://www.nsf.gov/statistics/srvydoctoratework/
3. Nature Index. Talent flow. https://www.nature.com/nature-index/

# 附件

## 附录 A 原始需求原文摘录

- SRS《科技时空演进展示.md》序号 507（excel_row 510）：「支持主动跟踪各专业主题下的科技人员流动，智能识别跨区和跨领域流动趋势，展示人才聚集、迁徙热点及高成长区。用户可导出流动趋势报告，辅助团队建设和全球人才战略引导。」
- bid_desc（excel_row 500，序号 497）：「支持按时间要素对论文发布、专利交易、资金与研发进度、科技人员流动等实时动态数据，进行分布展示与流动展示。」
- 检索记录：`rg 科技人员流动动态` 三份说明书 → 卡片名 0 命中（507 族功能覆盖；挂点 :1089 实查定位）。
- mock 参照：`getCityStats` talent 外推（毛存量语义）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_022_out.json`）

metric_id/batch=S3-08/ui_evidence（2 条组件行号）/requirement_trace（named_in_srs=false + SRS 锚 507 族）/facts（ui_mount/ui_kpis_source/ui_mock_note/jiuxin_flow_table/jiuxin_flow_rows=51489/jiuxin_flow_year_span/jiuxin_flow_dimensions/jiuxin_event_table/jiuxin_event_rows=298384/jiuxin_event_columns_30/jiuxin_geo_table/gkx_talent_tables/gkx_talent_note/dev_talent_word_hits/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）/derived[0]（中国净流入八年）/derived[1]（跨域事件四元组）/derived[2]（守恒校验全零）/absence_probe（三源三条）/support_judgment=完全转换支持/notes（5 条）/base_years 三键/ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：OECD 流动测量（履历法）→ NSF SDR（问卷法）→ Nature Index 人才流（署名法）——事件面即履历法物化结果。数据矩阵：净流入列现成；事件面 298,384 行；流量面 51,489 行；物化视图无（转换点）。分期方案：一期切真（口径 A+desc 修正）、二期物化视图（完全直接，三件联升）、三期主题映射+人员类型。风险登记：全集守恒陷阱（全球净流入恒 0）、中国/香港分行口径、assignment_confidence 推断归属。总判：完全转换支持（三面齐备；desc 修正是前置动作）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_022.py` | 退出码 0，落 `_out.json` |
| 实算复核 | derived[0] 2024=−5 / derived[2] 全零 | 重跑一致 |
| 判档一致 | MD 文首「完全转换支持」= out.json `support_judgment` | 一致 |
| 负证据 | dev/gkx 流动面缺失两条 | 逐一可复验 |
| mock 披露 | 毛存量外推仅 §1.1 语义描述 | 不参与支持度结论 |

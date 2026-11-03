# 区域论文数（M_SCIUI_INNOV_011）

> **类型**：COUNT（区域聚合计数，双池口径 A geo 年度截面 / 口径 B topic_country 全窗）｜ **域**：科技发展态势·全球创新监测·载体排行对比维度（主）+ 创新载体孵化载体双页（跨页挂载）｜ **UI 挂载**：全球创新监测页（`carrierRankingCompareModel.js:25` 对比维度选择器『论文数』）+ 孵化载体 Workbench（`InnovationEcosystemWorkbench.jsx:1391` 载体表格列）+ 孵化载体 New 页（`InnovationEcosystemNewPage.jsx:1229` 载体列）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 推导叶（`cfg_metric` 无条目；指标名三份说明书 0 命中）
> **复现脚本**：`code/M_SCIUI_INNOV_011.py`｜ **产物**：`code/M_SCIUI_INNOV_011_out.json`
> **四判定摘要**：直接结构 = 否（gkx dwd_zh_paper 32 列无任何地理列——结构级缺失；dev 论文表 0 张）；直接数据 = 否；依赖结构 = 是（久新 ads_geo_yearly_metrics 171,736 行 paper_count + paper_fractional_count 双列 / ads_topic_country_snapshot 209,517 行双窗双计数列）；依赖数据 = 部分（两池国别聚合全量可用，但 UI 语义是载体粒度、承载池是国家粒度——粒度错配须分卡）
> **数据源口径**：本件支持度按「开发库 gkxlumenx_*（禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin（47.93.119.170:29030 只读）」三源评估（20261101 三源铁律）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** gkx 侧是全批论文面的**结构级缺失**典型：`dwd_zh_paper` 100,900 行（官方共享快照原值）32 列逐一核对**无任何地理归属列**（countr/region/area/prov 四关键字 0 命中，本件 absence_probe 留证）——与 001 件 dwd_patent「有列但采样 100% CN」的数据级塌缩不同，论文侧连受理局类地理列都不存在，国别聚合无从起算。dev 库 SHOW TABLES LIKE '%paper%' 0 张（官方快照同值）。但久新侧两池齐备：口径 A（`ads_geo_yearly_metrics` COUNTRY 级 2025 截面）中国 533,316 / 美国 153,305 / 英国 55,966，Top12 合计占全球 75.7825%；口径 B（`ads_topic_country_snapshot` 2015-2025 全窗）中国整计数 2,096,489、分数计数 1,739,786.18（较整计数折让 17.03%——跨国合著重复计入的实证）。压档主因：①UI 挂载是**载体粒度**（mock papers 200-2,200 对应单机构千级），承载池是国家粒度——回填须两级分卡；②口径 B 全窗量级（11 年累计）与 UI 柱状图的年度预期不可直比，统计窗必须声明。判**部分支持**。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | Top12 占比分子分母同表同年 2025 截面 |
| B4 | 负结论带探针 | gkx 32 列核对 + dev 0 表双探针留证 |
| B5 | 确定性 | 榜单 ORDER BY paper_count DESC；两池口径分列 |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑 |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | 2025 截面（2026 残年不用）；整计数/分数计数双列标注 |
| B10 | 口径裁定保守交付 | 双池双计数四口径并列 + 统计窗声明 |
| B11 | 多本账互推 | geo 池 171,736 与 002/004 件同表同值；topic 池 209,517 与 016/017 件同表同值 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 国别论文聚合能直查吗？ | 能（久新两池） | 口径 A/B 双榜单实跑 |
| gkx 侧论文能按区域聚合吗？ | 不能（32 列无地理列） | `gkx_dwd_zh_paper_geo_columns=[]` |
| UI 载体粒度能回填吗？ | 不能即期回填（粒度错配） | mock 200-2,200 vs 国家 53 万+ |

## 摘要

「区域论文数」是全球创新监测页载体排行对比维度选择器的**第 3 项**（`carrierRankingCompareModel.js:25`，与专利数/项目数并列），跨页挂孵化载体两页的载体表格列。三源探测揭示论文面的双侧反差：gkx `dwd_zh_paper`（100,900 行）**结构级缺失**——32 列无任何地理列，国别聚合无从起算（专利侧 001 件至少有 country_code 列只是数据塌缩，论文侧连列都没有）；dev 库论文表 0 张；而久新两池全量齐备——口径 A（geo 池 2025 截面）中国 533,316 / 美国 153,305 / 英国 55,966 居前三，Top12 合计 976,076 占全球 1,287,996 的 75.7825%；口径 B（topic_country 池 2015-2025 全窗）中国整计数 2,096,489（全球 3,850,794），但**分数计数仅 1,739,786.18（折让 17.03%）**——跨国合著论文在整计数下对两国各计 1 次的重复计入得到实证（OECD/Scopus 口径警示 R1/R2）。语义核验：同一快照 topic 粒度全球论文 5,527,507 vs 各国行合计 3,850,794——69.65% 的论文产于有排名的主题池内。判**部分支持**：国家粒度即期可交，但 UI 挂载是载体粒度（mock 200-2,200 量级）、gkx 侧结构缺失、统计窗双池不可直比三因叠加。

- 需求判定：**UI 推导叶**（指标名三份说明书 0 命中；最近锚为全球创新监测.md seq 67『专利数量、论文引用率、投资金额』举例级提及）。
- 复现状态：脚本已跑通；双池 Top12 榜 + 分数计数对照 + 整计数重复计入实证 + gkx 32 列核对 + dev 0 表双负结论全部落产物。
- 档位结论：**部分支持**（gkx 结构级缺失 + 载体/国家粒度错配 + 双池统计窗不可直比）。
- 关键事实：整计数 vs 分数计数的 17.03% 折让（中国全窗）是本件最有价值的口径发现——柱状图回填必须声明计数制式。
- 升档路径：上游若出 `ads_institution_yearly_metrics` 载体级论文列的 UI 挂载卡（表已在 816,120 行）→ 载体粒度可交 → 升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**全球创新监测**/创新载体排行榜对比维度（主挂载）+ 跨页两处（孵化载体 / 孵化载体 New）。挂载点实查：

- `src/pages/global-innovation/tabs/carrierRankingCompareModel.js:25`：`compareMetricOptions { key: 'papers', label: '论文数' }`——载体对比维度选择器第 3 项（score/patents/papers/projects/rank 五选一），对比视图柱状图的 Y 轴语义。
- `src/pages/achievement-preview/modules/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1391`：载体表格列 `{ title: '论文数', dataIndex: 'papers', width: 90 }`——孵化载体页的载体明细列。
- `src/pages/achievement-preview-new/innovation-ecosystem-new/InnovationEcosystemNewPage.jsx:1229`：New 版生态页同构载体列。

三处语义同为**载体粒度计数**（单机构千级量级），mock `mockData.js:82` `papers = Math.floor(Math.random()*2000)+200`（随机 200-2,200，演示值，不参与支持度结论）。本报告以久新国家粒度两池作数据侧最近似承载，粒度错配在 §4 披露。

### 1.2 为什么需要本指标

论文数是创新产出的**第一计数指标**：与专利数（技术产出）构成「科学-技术」双翼，是排行榜、对比图、趋势线的通用燃料。本指标承担三职：①**对比维度**（载体排行对比图的柱高）；②**明细列**（孵化载体表格的量化列）；③**分母基座**（论文引用率、篇均引用等派生指标的分子来源）。数据侧本件是 001 件（区域专利数）的**姊妹对照件**：专利侧 gkx 有列但数据塌缩（采样 100% CN），论文侧 gkx 连列都没有——两件合起来完整展示了「结构级缺失 vs 数据级缺失」的降档谱系，对批内所有论文类指标（021 论文热度值等）的 gkx 侧预期有直接指导意义。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「区域论文数/论文数」作为指标名三份说明书 0 命中。全球创新监测.md 两处最近锚：seq 67『将全球创新数据按照关键数据指标进行分类，如专利数量、论文引用率、投资金额』——论文以**引用率**形态被举例（本件的计数形态是其分子）；seq 18『将全球创新成果（专利、论文）、创新资讯……按照创新价值进行自动分类』——论文作为成果类型枚举。两处均无计数口径（整计数/分数计数）、统计窗、区域归属轴的定义。本报告的双池双计数构造即填补该留白的保守方案。

### 1.4 类似指标权威方法可行性分析概要

区域论文计数的权威口径之争集中在**计数制式**与**归属轴**两点。**OECD Compendium**（R1）：官方口径用整计数（whole counting）——每个作者机构所在国各计 1 次，但明言「fractional counts can be aggregated up while whole counts cannot」；**NSF NCSES**（R2）：国家产出主口径用**分数计数**（fractional counting，按合作国作者数分摊），国际协作分析才用整计数——2023 年 Scopus 数据中国整计数 1,003,473 vs 美国整计数 568,973（分数计数下差距收窄）；**科学计量学派**（Waltman 等，R3）：分位归一与领域归一场景下推荐分数计数，「counting method 必须声明，不同计数制的排名不可互比」。方法族对照：

| 方法族 | 计数制式 | 归属轴 | 三源承载 | 匹配度 |
|---|---|---|---|---|
| OECD 整计数（R1） | whole | 作者机构国 | 久新两池 paper_count 列 | **高（上游默认）** |
| NSF 分数计数（R2） | fractional | 作者机构国 | 久新两池 paper_fractional_count 列 | **高（对照列现成）** |
| SCImago 国别文档数（R4） | whole | 通讯/机构国 | 久新 geo 池最近似 | 中（年度截面参照系） |

结论：权威两制式在上游两池均有承载列——本件双列并列交付即合规；正式版建议柱状图主口径用分数计数（R2 范式）、整计数作上界参考。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:25`（对比维度）；`…/InnovationEcosystemWorkbench.jsx:1391`（载体列）；`…/InnovationEcosystemNewPage.jsx:1229`（New 版载体列）；`…/mockData.js:82`（mock 生成器）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` seq 67（指标分类举例）、seq 18（成果类型枚举）。
- 数据：`code/_snapshots/_shared_probe_s3_01_out.json`（gkx dwd_zh_paper 100,900、dev 论文表 0 张）；`code/_snapshots/_probe_lane5_s3_01_out.json`（geo/topic_country 两池 DESC+COUNT+样例）。

### 1.6 推测原意与推测定义

**推测定义（双池双计数，均须披露口径假设）**：

- **口径 A（geo 池年度截面·柱状图主推）**：`papers(country, year) = paper_count`，取 `ads_geo_yearly_metrics` COUNTRY 级 2025 年行。实测 Top5：China 533,316 / United States 153,305 / United Kingdom 55,966 / Germany 42,453 / Australia 33,517（产物 `jiuxin_country_paper_2025_top12`）；同年全球 222 国合计 1,287,996。
- **口径 B（topic_country 池全窗·总量口径）**：`papers(country) = SUM(paper_count)`（2015-2025 分析窗），对照列 `SUM(paper_fractional_count)`。实测中国整计数 2,096,489 / 分数 1,739,786.18；美国 779,205 / 491,131.85（产物 `jiuxin_topic_country_allwindow_top12`）。
- **UI 载体粒度**（挂载语义）：单机构论文数百至千级（mock 200-2,200），对应 `ads_institution_yearly_metrics`（816,120 行，lane 共享探针登记值）的机构级 paper 列——回填需另立载体卡（本件不展开）。

**降档/升档触发器（B10 模板）**：若甲方接受「国家粒度=区域论文数」→ 口径 A 即期交付（仍部分支持，载体粒度披露）；若 UI 侧增加机构级挂载点并接 `ads_institution_yearly_metrics` → 载体粒度可交 → 升完全转换支持；若上游出城市级年度论文列（geo 池 CITY 级 paper_count 已在）→ 城市卡可交 → 维持完全转换支持另立工程。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md`（主）+ 跨页两挂载 |
| 所属四级功能 | 全球创新监测（33 叶） |
| 本件挂载视图 | 载体排行对比维度（主）+ 孵化载体表格列 ×2 |
| 需求叶对应 | 无同名叶；最近 seq 67/seq 18 举例级 |
| 批内相邻件 | M_SCIUI_INNOV_001（区域专利数——结构/数据缺失谱系姊妹）；M_SCIUI_INNOV_016（趋势对标——同 topic_country 池消费双窗列）；M_SCIUI_INNOV_017（领域排名——同池 output_rank） |
| 跨模块参照 | 孵化载体（:1391/:1229 挂载语境） |

本件与 001 构成「论文-专利」双翼对照：两件同挂载体对比维度选择器（papers 第 3 项、patents 第 2 项）、同判部分支持、但缺失形态互补（本件 gkx 结构级、001 件 gkx 数据级）——批内「区域计数三姊妹」（001 专利/011 论文/013 五维）的降档因各不相同，判档谱系由此三件确立。

## 二、计算过程

### 2.1 装载与规模校验

久新 `ads_geo_yearly_metrics` 171,736 行（`facts.jiuxin_geo_yearly_metrics_rows`，共享探针快照原值断言通过）；`ads_topic_country_snapshot` 209,517 行（`facts.jiuxin_topic_country_rows`）= 4,467 topics × 224 countries（官方快照 #2/#3 原值，4,467 topics × 224 countries 见 lane 共享探针 #2/#44）。双计数列（paper_count / paper_fractional_count）两池齐备——权威两制式的承载列一次取齐。

### 2.2 gkx 侧结构级缺失（absence_probe 主证据）

```sql
SHOW COLUMNS FROM gkx.dwd_zh_paper
```

32 列逐一核对，countr/region/area/prov 四关键字 0 命中（`facts.gkx_dwd_zh_paper_geo_columns=[]`）——gkx 论文面**无国别聚合起算点**。行数 100,900（官方快照原值，不重跑）。与 001 件 dwd_patent 的 32 列中含 country_code（采样 100% CN）对照：专利是「有列无区分度」，论文是「列不存在」——后者更不可修复，属上游建模缺失。

### 2.3 dev 侧负结论

`SHOW TABLES LIKE '%paper%'` → 0 张（`facts.dev_paper_tables=[]`，与官方共享快照同值零漂移）——开发库论文面完全空载。

### 2.4 口径 A：geo 池 2025 截面 Top12

```sql
SELECT l.name_en, m.paper_count, m.paper_fractional_count
FROM ads_geo_yearly_metrics m LEFT JOIN ads_location l ON l.location_id=m.location_id
WHERE m.location_level='COUNTRY' AND m.statistics_year=2025
ORDER BY m.paper_count DESC LIMIT 12
```

Top12 见产物 `jiuxin_country_paper_2025_top12`；全球合计 1,287,996（`jiuxin_country_paper_2025_global_sum`）、222 国（`jiuxin_country_paper_2025_country_count`）。派生比 1：Top12 合计 976,076 / 1,287,996 = **75.7825%**（`derived.jiuxin_2025_top12_share_pct`，分子分母同表同年 B3）；派生比 2：中国单国 533,316 / 1,287,996 = **41.4067%**（`derived.jiuxin_2025_cn_share_pct`）。

### 2.5 口径 B：topic_country 池全窗 Top12（双计数并列）

```sql
SELECT country_name_en, SUM(paper_count), SUM(paper_fractional_count)
FROM ads_topic_country_snapshot GROUP BY country_name_en
ORDER BY SUM(paper_count) DESC LIMIT 12
```

中国 2,096,489 / 1,739,786.18、美国 779,205 / 491,131.85……（`jiuxin_topic_country_allwindow_top12`）。窗口字段实查：analysis 2015-2025 / baseline 2020-2022 / recent 2023-2025（`jiuxin_topic_country_window`）。

### 2.6 整计数重复计入实证（口径核验）

同一快照内：topic 粒度全球论文合计 5,527,507（每 topic 取 `global_paper_count` 去重加总）vs 各国行 paper_count 总和 3,850,794——**落池率 69.65%**（3,850,794/5,527,507，复算式，分子分母均产物键 `jiuxin_topic_country_country_rows_sum` / `jiuxin_topic_country_distinct_topic_global_sum`）；中国一档整计数 2,096,489 vs 分数计数 1,739,786.18（折让 17.03%）——跨国合著的重复计入在两列间得到直接实证（R1「whole counts cannot be aggregated」的数据面佐证）。

### 2.7 复现代码结果展示

| 产物键 | 值（节选） |
|---|---|
| `jiuxin_country_paper_2025_top12[0..2]` | China 533,316/446,217.99；United States 153,305/89,584.30；United Kingdom 55,966/22,930.88 |
| `jiuxin_2025_top12_share_pct` | 75.7825 |
| `jiuxin_2025_cn_share_pct` | 41.4067 |
| `jiuxin_topic_country_allwindow_top12[0..1]` | China 2,096,489/1,739,786.18；United States 779,205/491,131.85 |
| `gkx_dwd_zh_paper_geo_columns` | []（结构级缺失） |

### 2.8 分步证据对照表

| 步骤 | SQL/操作 | 产物键 | 结果 |
|---|---|---|---|
| S1 规模断言 | COUNT 两池 | `jiuxin_geo_yearly_metrics_rows`/`jiuxin_topic_country_rows` | 171,736 / 209,517 与共享快照零漂移 |
| S2 gkx 列核对 | SHOW COLUMNS | `gkx_dwd_zh_paper_geo_columns` | [] |
| S3 dev 探测 | SHOW TABLES | `dev_paper_tables` | [] |
| S4 口径 A | COUNTRY 2025 Top12 | `jiuxin_country_paper_2025_top12` | China 居首 |
| S5 口径 B | 全窗 SUM 双列 | `jiuxin_topic_country_allwindow_top12` | 双计数并列 |
| S6 语义核验 | topic 全球 vs 国合计 | `jiuxin_topic_country_distinct_topic_global_sum` | 69.65% 落池率 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 源表 | 行数 | 库别 | 状态 |
|---|---|---|---|---|
| D1 国别年度论文 | ads_geo_yearly_metrics | 171,736 | jiuxin | **全量（口径 A 主承载）** |
| D2 国别全窗论文 | ads_topic_country_snapshot | 209,517 | jiuxin | **全量（口径 B 主承载）** |
| D3 地理维表 | ads_location | 224 国+ | jiuxin | 全量（name_en/name_zh 双名） |
| D4 gkx 论文底表 | dwd_zh_paper | 100,900 | gkx | 结构缺失（无地理列） |
| D5 dev 论文面 | — | 0 表 | dev | 空载 |

### 3.2 D1/D2 主承载明细

geo 池 COUNTRY 级 2025 年 222 行全量（Top12 榜即期可交）；topic 池 224 国 × 4,467 topics 全覆盖（PARTIAL 覆盖状态行在窗，coverage_status 列可过滤）。两池均带分数计数对照列——柱状图回填的计数制式声明有数据基础。

### 3.3 D4 gkx 结构级缺失面

32 列全清单落 absence_probe（`SHOW COLUMNS` 原样留证）——修复需上游重建地理解析管线，非本批工程能内解决。

### 3.4 D5 dev 空载面

官方共享快照「dev 论文表探测」0 行（本件断言同值）——开发库论文侧 0 承载。

### 3.5 现场复核清单

- `SELECT COUNT(*) FROM ads_geo_yearly_metrics` → 171,736
- `SELECT SUM(paper_count) FROM ads_geo_yearly_metrics WHERE location_level='COUNTRY' AND statistics_year=2025` → 1,287,996
- `SELECT SUM(paper_count) FROM ads_topic_country_snapshot WHERE country_name_en='China'` → 2,096,489

## 四、数据缺失情况

### 4.1 载体粒度承载缺位（粒度错配，主降档因）

UI 三处挂载均为**载体粒度**（mock 200-2,200），三源无现成「载体论文数」结果面——`ads_institution_yearly_metrics`（816,120 行）有机构级论文列但机构→载体（enterprise/institution 双类型）映射链未建。**修复建议**：孵化载体两页改挂机构级卡（接 ads_institution_yearly_metrics），全球创新监测页保持国家粒度（口径 A/B 直给）。**影响面**：孵化载体双页的论文列回填延期至映射链建立。

### 4.2 gkx 地理列缺失（结构级）

论文面无 country/region 列（§2.2）——gkx 侧国别聚合永久不可行（除非上游重建）。**修复建议**：gkx 侧放弃论文地理聚合，论文侧统一走久新池。**影响面**：批内所有论文类指标的 gkx 侧预期统一记「结构缺失」。

### 4.3 计数制式与统计窗未声明（口径风险）

UI 无计数制式/统计窗字段；整计数（口径 B 中国 2,096,489）与分数计数（1,739,786.18）差 17.03%、年度截面（口径 A 中国 533,316）与全窗累计（2,096,489）差近 4 倍。**修复建议**：柱状图卡片强制带「计数制式 + 统计窗」双标签（UI 侧加字段）。**影响面**：不加标签则跨卡对比必然误导。

## 参考文献

1. OECD Compendium of Bibliometric Science Indicators[EB/OL]. OECD. https://one.oecd.org/document/DSTI/EAS/STP/NESTI(2016)8/FINAL/en/pdf （R1，whole/fractional counting 官方口径与聚合性警示，2026-11-01 WebSearch 核验可达）
2. Discovery: R&D Activity and Research Publications, NCSES NSF[EB/OL]. NSF. https://ncses.nsf.gov/pubs/nsb20257/publication-output-by-geography-and-scientific-field （R2，分数计数主口径 + 整计数对照范式，2026-11-01 WebSearch 核验可达）
3. SCImago Journal & Country Rank Help[EB/OL]. SCImago. https://www.scimagojr.com/help.php （R4，国别科学产出指标定义（documents/citable documents），2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

**「区域论文数/论文数」未作为指标名出现在三份说明书。** 检索记录（2026-11-01）：

| 检索词 | 范围 | 命中 |
|---|---|---|
| 论文数 | 全球创新监测.md | 0 |
| 论文 | 全球创新监测.md | seq 18（成果类型枚举）/ seq 67（引用率举例） |
| papers | UI 源码 | carrierRankingCompareModel.js:25 等 4 处（本件挂载） |

最近语义原文：
- seq 67：『将全球创新数据按照关键数据指标进行分类，如专利数量、论文引用率、投资金额，用户可选择查看不同类别的数据指标。』
- seq 18：『支持将全球创新成果（专利、论文）、创新资讯（创新基金、创新研究课题）、创新机构、企业动态按照创新价值进行自动分类……』

### A.2 检索记录逐行

（检索工具：ripgrep 于 SRS 目录与 repos/demo-ui-science/src；时间 2026-11-01；命中行号已实查 ±10 行上下文。）

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_011_out.json`（20261101 实跑：双池 Top12 / 双派生比 / 整计数实证 / gkx 32 列 / dev 0 表在案）。
- 本 lane 共享探针：`code/_snapshots/_probe_lane5_s3_01_out.json`（两池 DESC+COUNT+样例 #2-#8）。
- 官方共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（dwd_zh_paper 100,900 / dev 论文表 0 张）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INNOV_011_out.json`，20261101 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `jiuxin_geo_yearly_metrics_rows` | 计数 | 171,736 | §2.1 |
| `jiuxin_country_paper_2025_top12` | 榜单 | 12 国双计数 | §2.4/§2.7 |
| `jiuxin_country_paper_2025_global_sum` | 计数 | 1,287,996 | §2.4 |
| `jiuxin_country_paper_2025_country_count` | 计数 | 222 | §2.4 |
| `jiuxin_topic_country_rows` | 计数 | 209,517 | §2.1 |
| `jiuxin_topic_country_window` | 窗口 | analysis 2015-2025 等 | §2.5 |
| `jiuxin_topic_country_allwindow_top12` | 聚合 | 12 国双计数 | §2.5/§2.7 |
| `jiuxin_topic_country_distinct_topic_global_sum` | 计数 | 5,527,507 | §2.6 |
| `jiuxin_topic_country_country_rows_sum` | 计数 | 3,850,794 | §2.6 |
| `gkx_dwd_zh_paper_rows` | 计数 | 100,900 | §2.2 |
| `gkx_dwd_zh_paper_column_count` | 计数 | 32 | §2.2 |
| `gkx_dwd_zh_paper_geo_columns` | 负结论 | [] | §2.2/§〇 |
| `dev_paper_tables` | 负结论 | [] | §2.3 |
| `derived.jiuxin_2025_top12_share_pct` | 派生比 | 75.7825 | §2.4 |
| `derived.jiuxin_2025_cn_share_pct` | 派生比 | 41.4067 | §2.4 |
| `absence_probe` | 探针 | gkx 32 列 + dev 0 表 | §2.2/§2.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

### B.3 共享快照消费（B11 零漂移）

本件消费：官方快照 `dims.gkx[0]`（dwd_zh_paper 100,900）作为 `gkx_dwd_zh_paper_rows` 登记值（不重跑）；`dims.dev` 论文表探测 0 行与 `dev_paper_tables=[]` 断言一致；lane5 探针 #5（geo 171,736）/#2（topic 209,517）作为两池规模登记值。全部引用原值零漂移。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 计数制式 | 三源承载 | 贴合度 |
|---|---|---|---|
| OECD 整计数（R1） | whole | 久新两池 paper_count | **高（上游默认）** |
| NSF 分数计数（R2） | fractional | 久新两池 paper_fractional_count | **高（对照列现成）** |
| SCImago 年度文档数（R4） | whole | geo 池年度截面 | 中高（参照系） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| geo 池 COUNTRY 2025 | 222 行 | 双计数列 | 无（国家粒度） |
| topic 池全窗 | 209,517 | 双计数+双窗 | PARTIAL 行需过滤 |
| gkx dwd_zh_paper | 100,900 | 无地理列 | 结构缺失 |
| dev 论文面 | 0 表 | — | 空载 |
| 载体粒度承载 | 无结果面 | — | 映射链未建 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 国家榜回填对比维度 + 口径 B 全窗榜（双计数标签） | 甲方接受国家粒度 |
| v2 | 机构级卡接 ads_institution_yearly_metrics | 机构→载体映射链 |
| v3 | 城市级年度卡 | geo 池 CITY 级消费另立件 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 整/分计数混读（17.03% 折让） | **高** | 卡片双标签（制式+窗口） |
| 全窗 vs 单年混读（4 倍差） | 高 | 统计窗字段强制 |
| 载体粒度误回填国家数 | 中 | 两级分卡 |
| PARTIAL 行混入 | 低 | coverage_status 过滤 |

### C.5 总判

**部分支持**：国家粒度双池全量（即期可交），但 gkx 结构级缺失 + 载体粒度承载缺位 + 双池统计窗不可直比三因叠加。升档第一杠杆（机构→载体映射链）与触发器写死 §1.6，按 B10 保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_011.py` | 退出码 0，落 `_out.json` |
| 数据入口 | gkx 经 `_gkxdb.py`；jiuxin 直连只读 | demo_* 直接 raise |
| 口径 A 复算 | Top12 SUM/全球 SUM | 976,076/1,287,996=75.7825% |
| 口径 B 折让复算 | (整-分)/整 | (2,096,489-1,739,786.18)/2,096,489≈17.03% |
| 判档一致 | MD 文首 vs 产物 `support_judgment` | 部分支持 |
| mock 残留检查 | `rg "papers: Math.floor" repos/demo-ui-science/src` | 正式版替换后无 mock |

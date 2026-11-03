# 区域专利数（M_SCIUI_INNOV_001）

> **类型**：COUNT（分区计数，载体/区域双口径）｜ **域**：科技发展态势·全球创新监测·创新载体排行榜/创新成果综合展示｜ **UI 挂载**：全球创新监测页载体对比维度选择器（carrierRankingCompareModel.js:24「专利数」）+ 孵化载体 New 页企业详情（IncubationCarrierNewPage.jsx:962「专利数 N 件」）+ 创新生态工作台载体表格列（InnovationEcosystemWorkbench.jsx:1397）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 推导叶（筛选记录 row_01 35），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_INNOV_001.py`｜ **产物**：`code/M_SCIUI_INNOV_001_out.json`
> **四判定摘要**：直接结构 = 否（三源无「区域专利数」现成结果面）；直接数据 = 否；依赖结构 = 是（久新 ads_patent_analysis_institution 7,270 行机构×国别×专利数）；依赖数据 = 部分（受让人-机构解析覆盖率 1.93% + gkx 专利地域列 100% CN 无区分度）
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

**本件判定：部分支持。** 「区域专利数」看似最简单的计数指标，三源探测后呈现罕见的「双源伪支持」格局：gkx `dwd_patent` 有 2,939,895 行且有 `country`/`country_code` 列——结构上是支持的，但 20 万行采样显示 country_code **100% 是 CN**（country 文本列采样：China 193,750 / WO 6,175 / Hong Kong 66），该库实质是「向中国受理局递交的专利公开文本池」，地域列是受理局维度，没有区域对比的区分度——**列存在但数据无区分度**，是数据级缺失；开发库专利 4 表 3 表 0 行、org_rel 969 行纯关系无计数值。唯一真承载在久新：`ads_patent_analysis_institution`（7,270 行，机构→国别→专利数，ALL 期）可同时出载体榜（口径 A）与国别榜（口径 B），但其 coverage 表自证受让人-机构解析覆盖率仅 **1.93%**（covered 33,807 / eligible 1,752,444），读数系统性偏小一个量级。结构与量都在、两处口径钳制（解析覆盖率 + 受理局≠属地），判部分支持。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 两个派生比分子分母同出 patent_analysis_institution ALL 期 |
| B4 | 负结论带探针 | gkx 采样分布 / dev 逐表行数 / coverage 自证三件留证 |
| B5 | 确定性 | 榜单按 rank / patents 降序；GROUP BY 去重 |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑 |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | patent_share DECIMAL 直读；20 万采样 note 标注 |
| B10 | 口径裁定保守交付 | 载体 A / 国别 B 双口径 + 降档升档触发器写死（§1.6） |
| B11 | 多本账互推 | gkx 2,939,895 引官方快照；jurisdiction 675 与 024 件零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| gkx 专利地域列可用吗？ | 不可用（无区分度） | 20 万采样 country_code 100% CN |
| 久新机构专利榜可信吗？ | 结构可信、量级偏小 | coverage 1.93%（33,807/1,752,444） |
| 「区域」语义闭合吗？ | 不闭合（受理局 vs 属地 vs 机构归属国三义并存） | R1/R2 权威口径为发明人居住国，三源无对齐 |

## 摘要

「区域专利数」挂在全球创新监测页的三个位置：载体对比维度选择器（与论文数/项目数并列的切换维度）、孵化载体企业详情的「专利数 N 件」、生态工作台表格列——三处语义其实都是**载体（机构）专利数**，「区域」只是聚合视角。三源探测呈现双伪支持：gkx 专利 293.9 万行有地域列但采样 100% CN（受理局维度，无区域对比力）；开发库专利 4 表基本空载。真承载是久新 `ads_patent_analysis_institution`（7,270 行，机构×国别×专利数，附 coverage 质量自证）：口径 A 载体榜 Top10（Roche 5,621 / 南京工业大学 2,039 / Purdue 1,941…），口径 B 国别榜（US 49,165 / CH 29,010 / CN 17,285…，Top12 占 92.74%）；参照系受理局榜 US 932,277（53.20%）/ EP 289,891 / CN 273,396。降档根因：受让人-机构解析覆盖率 1.93% 使机构/国别榜系统性偏小；受理局与属地两种「区域」语义未裁定。判**部分支持**。脚本已跑通，正文与产物数字逐一对应。

- 需求判定：**UI 推导叶**（「区域专利数」指标名三份说明书未出现；最近语义为全球创新监测.md seq 67「如专利数量、论文引用率、投资金额」举例级提及）。
- 复现状态：脚本已跑通；载体 Top10 / 国别聚合 Top12 / 受理局榜 / coverage 质量面落产物。
- 档位结论：**部分支持**（解析覆盖率 1.93% + 区域语义未裁定双因）。
- 关键事实：gkx 专利地域列是「有列无区分度」的典型——结构探针会误判为支持，必须数据分布探针纠偏。
- 升档路径：久新提升受让人-机构解析覆盖率（当前 1.93%）→ 机构/国别榜量级修复 → 可升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**全球创新监测**/创新载体排行榜 + 创新成果综合展示（SRS seq 56–88 域）。本件三个挂载点实查：

- `pages/global-innovation/tabs/carrierRankingCompareModel.js:24`：`compareMetricOptions` 第 2 项 `{ key: 'patents', label: '专利数' }`——载体对比视图的指标切换器（创新能力指数/专利数/论文数/项目数/当前排名五选一），同文件 `:3` `metricLabels.patents='专利数'`、`:88` 专利维度 indicators `['专利数量','授权占比','高价值专利','近三年增长']`——前端作者为专利维预留了四个子指标槽位，即预期正式版专利数不只是裸计数。
- `pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:962`：企业详情 Descriptions 行 `{ label: '专利数', value: `${selectedEnterprise.patents} 件` }`——单载体读数形态。
- `pages/achievement-preview/modules/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1397`：载体表格列 `{ title: '专利数', dataIndex: 'patents', width: 90 }`——列表形态。

mock：`pages/global-innovation/mockData.js:81` `patents: Math.floor(Math.random() * 5000) + 500`——每载体随机 500-5,500 件，**随机种子生成，演示值，不参与支持度结论**；但该分布的量级设定（千级）与口径 B 国别榜首（US 49,165）同数量级、与口径 A 载体榜首（Roche 5,621）吻合，说明前端量级预期与久新承载天然对齐。

三处挂载的主语都是「载体」（企业/机构），没有一处 UI 直接说「按行政区统计专利」——「区域专利数」的「区域」来自筛选记录对 l3（专利数＞柱状图＞专利数）的归类。本报告按双口径处理：载体维（UI 语义同构）与国别维（「区域」语义的最近似）。

### 1.2 为什么需要本指标

专利数是创新载体排行榜的第一性读数：`carrierRankingMethodConfig` 把「专利产出」设为综合创新力指数四维之首（权重 35%，`formula: '创新力指数 = 专利产出 × 35% + 论文影响 × 25% + 项目转化 × 25% + 成果活跃 × 15%'`），专利数既是独立对比维度、又是复合指数的最大权重输入。国别聚合视角则服务「哪个国家/地区创新产出多」的全球对标叙事（与 WIPO 世界知识产权指标的国别 origin 榜同构，R2）。

数据侧本件是全批最有教育意义的伪支持案例：**结构探针（有 country 列）与数据探针（采样分布）会得出相反结论**。gkx 293.9 万行专利从任何「有没有地域列」的 schema 审查看都是强支持，但数据分布揭示它是 CN 受理局单一来源池——如果只做结构探针就判「完全直接支持」，回填后柱状图会是一根 CN 独柱。这正是 B4 纪律要求负结论带数据探针、B11 要求与快照数字互推的原因。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「区域专利数/专利数」作为指标名未出现在三份说明书。语义最近两处：全球创新监测.md seq 67「数据指标分类展示」——『将全球创新数据按照关键数据指标进行分类，如专利数量、论文引用率、投资金额，用户可选择查看不同类别的数据指标』（举例级提及，无定义）；科技创新评估.md seq 140「专利数量统计分析」——『收集并统计特定领域内专利申请和授权的数量，用户可按时间范围、技术类别、地域、申请人等维度查看专利数量分布情况』（给了维度枚举：时间/技术类别/地域/申请人——这是全批最接近「区域专利数」口径的需求原文，但它属于科技创新评估模块非本页）。主需求文档 :505 为 seq 67 同文复述。

### 1.4 类似指标权威方法可行性分析概要

专利国别统计的权威口径有三层。OECD MSTI/Triadic：以**三方专利族**（EPO+JPO+USPTO 同时申请）计数，按**发明人居住国**归属（多国发明人分数计数），按**最早优先权日**定时点——三重设计共同压制「本土优势」偏差（R1）；WIPO 世界知识产权指标：按 **origin**（第一申请人/受让人居住地）分 resident/abroad 两口径，绝对计数（区域局申请算一次）（R2）；我国国家知识产权局年报则按受理局与国内省份双口径发布。方法族对照：

| 方法族 | 归属轴 | 时点轴 | 数据要求 | 与三源匹配 |
|---|---|---|---|---|
| OECD 三方族（R1） | 发明人居住国（分数） | 优先权日 | 三局族标识+发明人国别 | **无（三源无发明人国别结构化列）** |
| WIPO origin（R2） | 第一申请人居住地 | 申请日 | 申请人国别 | **部分（久新 institution 榜=受让人机构归属国，语义最近）** |
| 受理局口径（国知局双口径之一） | 受理局 | 申请/公开日 | jurisdiction_code | **有（gkx/jiuxin 均有，但非「区域创新」语义）** |
| 载体归属口径（UI 语义） | 机构（受让人） | ALL 期 | 机构-专利关系 | **有（jiuxin patent_analysis_institution，覆盖率 1.93%）** |

结论：权威口径的发明人居住国轴三源无结构化承载；最近似可算是久新受让人机构归属国（WIPO origin 族），但解析覆盖率钳制量级。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:24`（对比维度）、`:82-89`（专利维四子指标槽位）；`…/incubation-carrier-new/IncubationCarrierNewPage.jsx:962`；`…/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1397`；mock `pages/global-innovation/mockData.js:81`。
- SRS：`…/科技发展态势/全球创新监测.md` seq 67（excel_row 70）举例提及；`…/科技创新评估.md` seq 140（excel_row 143）维度枚举（跨模块最近定义）。
- 主需求文档：《科技信息展示系统和科技专题服务系统.md》:505（seq 67 复述）。
- 数据：`code/_snapshots/_probe_lane5_s3_01_out.json`（本 lane 探针：institution/jurisdiction/coverage 三表 DESC+分布+采样）。

### 1.6 推测原意与推测定义

**推测定义（B10 双口径并列，均须披露口径假设）**：

- **口径 A（载体维·UI 同构）**：`patents(carrier) = patent_count`，取久新 `ads_patent_analysis_institution` ALL 期机构榜。实测 Top3：Roche (Switzerland) 5,621（族 3,768）/ Nanjing Tech University 2,039 / Purdue Research Foundation 1,941。
- **口径 B（国别维·区域语义）**：`patents(country) = Σ_{inst∈country} patent_count`，同表按 country_code 聚合。实测 Top3：US 49,165（313 机构）/ CH 29,010（21）/ CN 17,285（206）；Top12 合计占全表 92.74%（derived.jiuxin_top12_country_share_pct）。
- 口径 C（发明人居住国·OECD 权威）：三源无发明人国别结构化列，**不可构建**，仅作谱系参照。

**降档/升档触发器（B10 模板）**：若甲方接受「受让人机构归属国=区域」语义（WIPO origin 族）→ 仍部分支持但语义闭合（覆盖率随行披露）；若久新解析覆盖率从 1.93% 提升（受让人→平台机构映射扩充）→ 量级修复，可升**完全转换支持**；若甲方要求发明人居住国口径 → 三源无承载，维持部分支持不升档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` |
| 所属四级功能 | 全球创新监测（33 叶，seq 56–88） |
| 本件挂载视图 | 创新载体排行榜对比维度（seq 73–76 域）+ 成果综合展示 |
| 需求叶对应 | 无同名叶；最近 seq 67 数据指标分类展示（举例提及） |
| 批内相邻件 | M_SCIUI_INNOV_011（区域论文数——同构姊妹件，论文侧）；M_SCIUI_INNOV_002（趋势演进——专利维年度序列）；M_SCIUI_INNOV_010（区域投资额——同「区域聚合」模式） |
| 跨模块参照 | 科技创新评估.md seq 140 专利数量统计分析（唯一给出维度枚举的需求原文） |

本件与 011（区域论文数）、010（区域投资额）是「区域聚合三姊妹」：同一个「按区域汇总」的产品模式套三种产出物。本件的独特性在于伪支持陷阱最深（gkx 结构假象），011 的论文侧 gkx 同样只有中文池（100,900 行）——三姊妹的 gkx 侧结论可以互推：**要素底表的地域维要么缺失要么单一化，区域聚合的可靠承载只在久新分析层**。

## 二、计算过程

### 2.1 装载与规模校验

久新 Doris 只读连接。主承载 `ads_patent_analysis_institution` 7,270 行（facts.jiuxin_patent_analysis_institution_rows），period_key 全表仅 'ALL' 一期（本 lane 探针），即当前无分年期机构榜——年度趋势须走 002 件的 jurisdiction 序列。质量自证表 `ads_patent_analysis_coverage` INSTITUTION 行：eligible 1,752,444 / covered 33,807 / coverage_rate **0.019291**（facts.jiuxin_institution_coverage，limitation_note 自述『Only confirmed assignee-to-platform institution relations are counted』）。

### 2.2 gkx 侧伪支持纠偏（数据分布探针）

gkx `dwd_patent` 2,939,895 行（官方共享快照原值引用）。20 万行采样协议（无索引大表纪律，note 标注采样）：

```sql
-- 采样分布（B4：结构探针必须配数据探针）
SELECT country_code, COUNT(*) c FROM (SELECT country_code FROM gkx.dwd_patent LIMIT 200000) t
WHERE country_code IS NOT NULL AND country_code != '' GROUP BY country_code ORDER BY c DESC LIMIT 12;
-- → CN 200000（100%）
SELECT country, COUNT(*) c FROM (SELECT country FROM gkx.dwd_patent LIMIT 200000) t
WHERE country IS NOT NULL AND country != '' GROUP BY country ORDER BY c DESC LIMIT 10;
-- → China 193,750 / WO 6,175 / Hong Kong 66 / Japan 9
```

结论：地域列存在但分布塌缩为 CN 单值——受理局维度不承载「区域对比」。gkx 侧判定：**表数据直接支持 = 否**（数据级缺失，非结构级）。

### 2.3 口径 A：载体维 Top10

```sql
SELECT institution_name_en, institution_type_id, country_code, patent_count, family_count, institution_rank
FROM ads_patent_analysis_institution WHERE period_key='ALL' AND institution_rank<=10
GROUP BY institution_name_en, institution_type_id, country_code, patent_count, family_count, institution_rank
ORDER BY institution_rank;
-- → Roche(CH,company) 5,621/3,768 · Nanjing Tech(CN,education) 2,039/1,916
--   Purdue Research Foundation(US,nonprofit) 1,941/1,197 · RIKEN(JP) 1,546 · Battelle(US) 1,141 …
```

Top1 Roche 占全表 3.30%（derived.jiuxin_top1_institution_share_pct）。类型分布健康（company/education/nonprofit/facility/healthcare 混合），且名称带国别后缀（Roche (Switzerland)）说明上游做过机构消歧——榜单结构可直接回填 UI 对比维度。

### 2.4 口径 B：国别聚合 Top12

```sql
SELECT country_code, COUNT(DISTINCT institution_id) insts, SUM(patent_count) patents
FROM ads_patent_analysis_institution WHERE period_key='ALL'
GROUP BY country_code ORDER BY patents DESC LIMIT 12;
-- → US 313/49,165 · CH 21/29,010 · CN 206/17,285 · FR 136/11,955 · JP 60/11,550
--   DE 148/10,190 · (null) 65/8,960 · TW 22/4,865 · NL 16/4,790 · CA 46/4,520 · GB 44/3,970 · BE 20/1,865
```

Top12 合计 158,700，占全表 170,505 的 **92.74%**（derived.jiuxin_top12_country_share_pct，分子分母同表同口径）。注意 CH 以 21 个机构贡献 29,010 件（Roche 单机构 5,621 占 CH 近两成）——小机构数高产出国的量级受单巨头钳制，国别榜应同时披露机构数。

### 2.5 参照系：受理局榜（维度对照）

`ads_patent_analysis_jurisdiction` ALL 期：US 932,277（share 53.20%）/ EP 289,891（16.54%）/ CN 273,396（15.60%）/ WO 256,880（14.66%）。该榜与口径 B 的量级差（US 93 万 vs 4.9 万）即「受理局受理量 vs 受让人机构已解析量」的解析缺口可视化——两个榜都真，但语义完全不同，UI 回填时若混用会出现「美国专利数 4.9 万」与「USPTO 受理 93 万」同屏打架。此参照系是本件口径教育的核心证据。

### 2.6 三源负结论探针

- **开发库**（facts.dev_patent_table_rows）：`enterprise_chain_patent`=0、`enterprise_patent_detail`=0、`enterprise_patent_history`=0、`enterprise_patent_org_rel`=969（纯关系表，无专利计数值列）——四表无一可出「专利数」读数。
- **gkx**（§2.2 采样分布）：结构有列、数据无区分度，判数据级不支持区域对比。
- **久新**：承载成立；补充登记 `ads_institution_patent`（100,358 行）陷阱——它是每机构 Top20 代表性专利明细（selection_method=RELATION_GRANT_SCIENCE_CITATION_YEAR，selection_reason 明示 Top20 截断），直接 COUNT 会把所有机构截断在 20，**不能当机构专利总数用**（facts 键外 ctx_refs 登记）。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INNOV_001.py`（久新直连 + gkx 经 `_gkxdb.py`，零 demo_*；采样子查询协议）。运行 `python3 code/M_SCIUI_INNOV_001.py`。
- 产物：`code/M_SCIUI_INNOV_001_out.json`。正文数字与产物键逐一对应：`jiuxin_patent_analysis_institution_rows=7270`（§2.1）、`jiuxin_institution_patent_top10` 十行（§2.3）、`jiuxin_country_patent_agg_top12` + `jiuxin_country_agg_top12_total=158700` / `jiuxin_institution_patent_total_all=170505`（§2.4）、`jiuxin_jurisdiction_all_top` 四行（§2.5）、`jiuxin_institution_coverage`（§2.1）、`gkx_patent_country_code_sample_top=[["CN",200000]]`（§2.2）、`dev_patent_table_rows` 四表（§2.6）、derived 两比（92.7392 / 3.2967）。
- 结果解读：两个可用读数（载体榜直接回填对比维度；国别榜供「区域」叙事）+ 一个教育性负结论（gkx 伪支持）+ 一组量级警示（覆盖率 1.93%、受理局/属地双榜并存）。
- 对照需求功能要求的评审：载体对比维度——满足（Top10 结构与 mock 量级对齐）；「区域」柱状图——部分满足（国别榜可用，语义须从受理局纠偏为归属国并披露覆盖率）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 机构榜行数 | `jiuxin_patent_analysis_institution_rows` | 7,270（仅 ALL 期） |
| 质量 | 受让人解析覆盖率 | `jiuxin_institution_coverage` | 1.93%（33,807/1,752,444） |
| 口径 A | 载体 Top1 | `jiuxin_institution_patent_top10[0]` | Roche 5,621（族 3,768） |
| 口径 A | Top1 集中度 | `derived.jiuxin_top1_institution_share_pct` | 3.2967% |
| 口径 B | 国别 Top3 | `jiuxin_country_patent_agg_top12` | US 49,165 / CH 29,010 / CN 17,285 |
| 口径 B | Top12 占比 | `derived.jiuxin_top12_country_share_pct` | 92.7392%（158,700/170,505） |
| 参照 | 受理局 Top1 | `jiuxin_jurisdiction_all_top[0]` | US 932,277（53.20%） |
| 纠偏 | gkx 采样分布 | `gkx_patent_country_code_sample_top` | CN 200,000/200,000 |
| 负结论 | dev 专利 4 表 | `dev_patent_table_rows` | 0/0/0/969 |
| 陷阱 | institution_patent 明细 | notes/ctx_refs | Top20 截断，禁当总数 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 机构×专利计数 | jiuxin_warehouse | `ads_patent_analysis_institution`（patent_count/family_count/rank） | 7,270 | 直查 | **有**（主承载） |
| D2 | 机构国别归属 | jiuxin_warehouse | 同表 country_code（+institution_profile 83,745 行可 JOIN） | 7,270 内含 | 直查 | 有 |
| D3 | 解析覆盖率质量面 | jiuxin_warehouse | `ads_patent_analysis_coverage` INSTITUTION 行 | 35 行域表 | 直查 | 有（自证 1.93%） |
| D4 | 专利地域维（gkx） | gkx | `dwd_patent.country/country_code` | 2,939,895（采样 100% CN） | **无区分度** | **缺**（数据级） |
| D5 | 开发库专利计数 | dev | `enterprise_*patent*` 4 表 | 0/0/0/969 | 空载 | 缺 |
| D6 | 发明人居住国 | 三源 | —（无结构化列） | — | **不存在** | 缺（权威口径锚点） |

`support_judgment="部分支持"` 与产物一致（闸 6）。

### 3.2 D1/D2 主承载明细

`ads_patent_analysis_institution` 是分析层成品表：每行=机构×期（ALL），带 patent_count（专利数）、family_count（族数）、patent_share、institution_rank、growth_rate（ALL 期多为空）、resolution_coverage_rate。机构类型覆盖五类（company/education/nonprofit/facility/healthcare），国别覆盖 Top12+长尾——与 UI 载体语义（企业/机构两型）兼容。它是三源唯一同时满足「载体维 + 区域维 + 计数值」三条件的表。

### 3.3 D3 覆盖率质量面（主降档因）

coverage 表 INSTITUTION 域自证：eligible（分析域内合格专利）1,752,444，covered（已解析到平台机构）33,807，rate 0.019291。对照 INVENTOR 域 95.09%、IPC 域 99.81%——受让人→机构是全链路最弱的解析环节（limitation_note 直言只计「confirmed assignee-to-platform」关系）。这意味着口径 A/B 的读数是「已解析子集」的排序，排序结构可信（大机构先被解析），绝对量级偏小约一个量级——回填 UI 时卡片必须带「已解析子集」注记。

### 3.4 D4 gkx 数据级缺失（伪支持纠偏）

见 §2.2。补充判档语言：这属于四缺失情形中的「**表存在、列存在、数据无区分度**」——比「列不存在」更隐蔽，因为 schema 审查会放行。本件把该情形单列为判档依据，供批内 011/010（论文/投资区域聚合）直接复用结论：gkx 要素底表做不了区域对比，不必再逐件踩坑。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 机构榜 | 7,270 行仅 ALL 期；Top10 结构完整 |
| 覆盖率 | 1.93%（33,807/1,752,444）三行快照一致 |
| 国别聚合 | Top12=158,700 / 全表 170,505 → 92.74% |
| 受理局参照 | US 932,277 与 024 件 jurisdiction 榜零漂移 |
| gkx 采样 | country_code 100% CN（20 万样本） |
| dev 专利表 | 0/0/0/969 |
| 脚本形态 | 单进程顺序查询，零 demo_*，采样 note 在案 |

## 四、数据缺失情况

### 4.1 发明人居住国缺失（结构级，权威口径锚点）

OECD/WIPO 权威口径的归属轴（发明人居住国 R1 / 第一申请人居住地 R2）在 gkx `dwd_patent` 无结构化列（inventors/assignees 是 variant JSON 非国别列），久新 profile 的 inventors 同为 variant。四缺失情形归属：**列不存在**。修复动作：上游把 variant JSON 里的 inventor/assignee 国别抽平为国别列，或对齐外部专利族库。影响面：本件 + 全批所有专利国别类指标（002 趋势的属地版、017 领域排名专利维）。

### 4.2 受让人-机构解析覆盖率 1.93%（数据级，量级钳制）

见 §3.3。这不是结构缺口而是解析工程进度：covered 33,807 vs eligible 1,752,444，约 54 倍提升空间。修复与影响：上游扩充 confirmed assignee 映射 → 机构/国别榜量级向受理局榜方向修复（不会到 93 万，因为 eligible 域小于受理局全量）；属可工程闭合缺口，是本件升档的第一杠杆。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| UI 卡片带「已解析子集」注记 | 产品决策 | 本件即期 | 零成本止血 |
| 受让人→机构映射扩充（1.93%→提升） | 上游工程 | 本件 + 017 | 升档第一杠杆 |
| inventor/assignee 国别抽平列 | 结构工程 | 本件 + 002 + 全批专利国别类 | 对齐 WIPO origin 口径 |
| 双榜语义分离展示（受理局 vs 归属国） | 产品决策 | 本件 + 002 | 消除同屏打架 |

四条路径的档位后果：注记+双榜分离 → 仍部分支持但误读风险消除；映射扩充达标 → 可升**完全转换支持**；国别列落地 → 权威口径可建（同升）。推荐组合：即期注记 + 双榜分离，中期推映射扩充。

## 参考文献

1. Triadic Patent Families Methodology[EB/OL]. OECD. https://www.oecd.org/content/dam/oecd/en/publications/reports/2004/03/triadic-patent-families-methodology_g17a156f/443844125004.pdf （R1，2026-11-01 WebSearch 核验可达）
2. About the WIPO IP Statistics Data Center[EB/OL]. WIPO. https://www.wipo.int/en/web/ip-statistics/about （R2，2026-11-01 WebSearch 核验可达）
3. World Intellectual Property Indicators 2025[EB/OL]. WIPO. https://www.wipo.int/edocs/pubdocs/en/wipo-pub-941-2025-en-world-intellectual-property-indicators-2025.pdf （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

「区域专利数/专利数」未作为指标名出现在三份说明书，无直接原文。语义最近两段：

SRS《02-科技信息展示系统/科技发展态势/全球创新监测.md》seq 67（excel_row 70）：

> 将全球创新数据按照关键数据指标进行分类，如专利数量、论文引用率、投资金额，用户可选择查看不同类别的数据指标。

SRS《02-科技信息展示系统/科技发展态势/科技创新评估.md》seq 140（excel_row 143，跨模块最近定义）：

> 收集并统计特定领域内专利申请和授权的数量，用户可按时间范围、技术类别、地域、申请人等维度查看专利数量分布情况，系统提供柱状图、折线图等可视化形式展示专利数量的变化趋势。

UI 组件 `carrierRankingCompareModel.js:24`（本件挂载点之一）：

> `{ key: 'patents', label: '专利数' }`（compareMetricOptions 第 2 项）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 区域专利数 | 三份说明书 + 主需求文档 | 0 |
| 专利数 | 全球创新监测.md | 1（seq 67 举例） |
| 专利数量 | 全球创新监测.md / 科技创新评估.md | 1 + 1（seq 140 维度枚举） |
| 专利数量 | 科技信息展示系统和科技专题服务系统.md | 6（:33/:505/:817/:835/:895 等功能叙述） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_001_out.json`（20261101 实跑：载体 Top10 / 国别 Top12 / 受理局榜 / coverage / gkx 采样 / dev 行数在案）。
- 本 lane 共享探针：`code/_snapshots/_probe_lane5_s3_01_out.json`（patent_analysis_institution/jurisdiction/coverage DESC+COUNT+样例、dwd_patent 采样两分布、institution_patent 陷阱表）。
- 官方共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（dwd_patent 2,939,895、dev 专利 4 表名）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INNOV_001_out.json`，20261101 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INNOV_001 | 文首 |
| `ui_evidence` | 证据 | 4 条组件行号（含 mock 生成器） | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.jiuxin_patent_analysis_institution_rows` | 计数 | 7,270 | §2.1 |
| `facts.jiuxin_institution_patent_top10` | 榜单 | 10 机构（含 type/country/族数/rank） | §2.3/口径 A |
| `facts.jiuxin_country_patent_agg_top12` | 聚合 | 12 国（机构数+专利数） | §2.4/口径 B |
| `facts.jiuxin_country_agg_top12_total` | 计数 | 158,700 | §2.4 |
| `facts.jiuxin_institution_patent_total_all` | 计数 | 170,505 | §2.4/derived 分母 |
| `facts.jiuxin_jurisdiction_all_top` | 参照 | 4 受理局 | §2.5 |
| `facts.jiuxin_institution_coverage` | 质量 | eligible/covered/rate | §2.1/§3.3 |
| `facts.gkx_patent_country_code_sample_top` | 采样 | [["CN",200000]] | §2.2/§3.4 |
| `facts.dev_patent_table_rows` | 计数 | 0/0/0/969 | §2.6 |
| `derived.jiuxin_top12_country_share_pct` | 派生比 | 92.7392 | §2.4 |
| `derived.jiuxin_top1_institution_share_pct` | 派生比 | 3.2967 | §2.3 |
| `absence_probe` | 探针 | gkx 采样分布 1 条 | §2.2/§3.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `notes` | 披露 | 覆盖率/语义/陷阱 5 条 | §〇/§4 |

### B.3 共享快照消费（B11 零漂移）

本件消费：官方快照 `dims.gkx[2]`（dwd_patent 2,939,895）作为 facts.gkx_dwd_patent_rows 登记值（不重跑，正文 §2.2/§3.4 引用原值）；本 lane 探针 jurisdiction ALL 榜与 024 件年序列同源（US 932,277 与 1990-2025 序列 SUM 口径互恰）；dev 专利 4 表名复用官方快照 `dims.dev[5]` 表清单、行数本件补测。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 归属轴 | 三源承载 | 贴合度 |
|---|---|---|---|
| OECD 三方族（R1） | 发明人居住国（分数计数） | 无结构化列 | 高（不可行） |
| WIPO origin（R2/R3） | 第一申请人/受让人居住地 | 久新受让人机构归属国（最近似） | **中高（即期口径 B）** |
| 受理局口径 | jurisdiction | gkx/jiuxin 均有 | 中（非区域创新语义，留作参照系） |
| 载体归属（UI 语义） | 机构 | 久新 patent_analysis_institution | **高（即期口径 A，覆盖率 1.93% 随行）** |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| patent_analysis_institution | 7,270 | 带族数/share/rank | 仅 ALL 期无年度 |
| coverage INSTITUTION | 1.93% | 自证透明 | 解析工程进度 |
| gkx dwd_patent 地域列 | 采样 100% CN | 无区分度 | 数据级塌缩 |
| dev 专利 4 表 | 3 空 1 关系 | — | 空载 |
| 发明人国别列 | 不存在 | — | 结构缺失 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 载体榜回填对比维度 + 口径 B 国别榜（覆盖率注记） | 甲方接受 origin 族语义 |
| v2 | 映射扩充后量级修复 + 年度机构榜（上游出 YEAR 期） | 解析工程 |
| v3 | 发明人国别列 + WIPO origin 完整对齐 | 结构工程 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 受理局榜与归属国榜同屏打架 | **高** | 双榜分离展示+维度标签 |
| 1.93% 覆盖率读数被当全量 | 高 | 卡片「已解析子集」注记 |
| institution_patent 明细被 COUNT 当总数 | 中 | 表级使用警示（Top20 截断） |
| CH 单巨头（Roche）钳制国别榜 | 低 | 国别行带机构数 |

### C.5 总判

**部分支持**：唯一真承载（久新机构榜）结构量双达标，但受让人解析覆盖率 1.93% 钳制量级、权威归属轴（发明人国别）三源无列、gkx 侧数据级塌缩三因叠加。升档第一杠杆（映射扩充）与触发器写死 §1.6，按 B10 保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_001.py` | 退出码 0，落 `_out.json` |
| 数据入口 | gkx 经 `_gkxdb.py`；jiuxin 直连只读 | demo_* 直接 raise |
| 采样协议 | dwd_patent LIMIT 200000 子查询 | note「采样，非全表」在案 |
| 口径 B 复算 | Σ(country) vs 全表 | 158,700/170,505=92.74% |
| 覆盖率对账 | 产物 coverage.rate vs 表值 | 0.019291 |
| 判档一致 | MD 文首 vs 产物 `support_judgment` | 部分支持 |
| mock 残留检查 | `rg "patents: Math.floor" repos/demo-ui-science/src` | 正式版替换后无 mock |

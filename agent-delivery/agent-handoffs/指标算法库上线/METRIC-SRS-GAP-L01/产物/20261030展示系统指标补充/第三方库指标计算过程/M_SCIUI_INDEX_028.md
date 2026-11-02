# 科技影响力指数（M_SCIUI_INDEX_028）

> **类型**：需业务建模类（组合指数）｜ **域**：科技发展态势·科技指数·科技影响力指数（tech-index 数据层指标树四分项之一）｜ **UI 挂载**：科技指数数据集页 → 指标树「科技影响力指数」节点（weight 24）+ 对象详情「指标拆解」行
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 拆件叶（`_phase3_471_export.json` row_01 220）+ 组合语义真源=主需求文档 :923（**裁定 NEW**：组合指数，候选仅科学影响力单维）
> **复现脚本**：`code/M_SCIUI_INDEX_028.py`｜ **产物**：`code/M_SCIUI_INDEX_028_out.json`
> **四判定摘要**：直接结构 = 否（三源无「科学+技术组合」指数现成面）；直接数据 = 否；依赖结构 = 部分（科学单维 citation_score 现役、技术侧仅专利明细原料、通用指数承载表 0 行）；依赖数据 = 部分（单维覆盖 100%，组合技术分列与传播/对标子维缺位）
> **数据源口径**：三源评估——开发库 `gkxlumenx_*`（10.50.11.76:3306）+ 三方库 `gkx`（183.240.141.251:3318 只读）+ 久新库 `jiuxin_warehouse`（47.93.119.170:29030 只读）。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 派单裁定 NEW 成立：需求文档 :923（1.1.1.1.4.1.7.3 产业发展潜力指标展示）明文「以及**科学影响力、技术影响力等科技影响力指标**，构建产业发展潜力评估体系」——「科学+技术等」的列举式定义把本件锚定为**组合语义**。按此口径盘点三源：现役承载只有**科学影响力单维**——久新 `ads_institution_technology_power.citation_score` 64,698 行全覆盖（facts `jiuxin_citation_score_coverage`：nonnull 64,698/64,698=100.0%，min 3.1964/max 100.0/avg 50.0）；**技术影响力分列缺位**（power 四分项 paper/citation/talent/topic 全学术族，专利侧只有明细原料 `ads_technology_patent` 172,644 行/`ads_institution_patent` 100,358 行无评分面）；通用指数承载表 `ads_geo_yearly_index` 实测 **0 行**（facts `jiuxin_geo_yearly_index_rows`——本批现场复核）；gkx `dwd_scholar` 学者级影响力三列（citation_nums/h_index 全非空 21,316、reference_nums 0 非空，facts `gkx_scholar_influence_cols`）；dev `svc_tech_power_score` 黑名单 0 行。组合所需的「技术分合成+传播强度/区域带动/全球对标子维」三源均无现成分列，判部分支持。

### 批次通用纪律摘要（S3-02 批 Lane 4，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 两覆盖度派生分子分母同表同层 |
| B4 | 负结论带探针 | 组合面/子维 absence 三源留证（§3.3） |
| B5 | 确定性 | 覆盖度 GROUP BY 聚合；Top5 双键排序 |
| B6 | 闸门自身被闸 | 本批不自跑闸门 |
| B7 | 产物只由脚本产出 | 改脚本→重跑 |
| B8 | 回执不复收 | 派单方硬复验 |
| B9 | 单位/日期陷阱 | fwci decimal 保持；快照日期字符串化 |
| B10 | 口径裁定保守交付 | 单维先行/组合立项双口径+触发器（§1.6） |
| B11 | 多本账互推 | 64,698/816,120/21,316 与姊妹件零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 组合指数现成面存在吗？ | 不存在 | geo_yearly_index 0 行 + power 无技术分列（facts） |
| 科学单维可读吗？ | 可（100% 覆盖） | `jiuxin_citation_score_coverage` |
| 技术分可现算吗？ | 不可即期（明细在、评分面无） | 专利明细行数在案无 score 列 |

## 摘要

「科技影响力指数」是科技指数数据层（techIndex.js）指标树四分项之一（weight 24，描述「引用影响、传播强度、区域带动和全球对标」），对象详情「指标拆解」行直读 influence 分。派单裁定其语义为组合指数——需求 :923「科学影响力、技术影响力等科技影响力指标」的列举式定义是组合语义真源。三源盘点结论：现役承载只有科学单维（久新 citation_score 机构级 100% 覆盖、fwci 篇均族 2026 年 21,651/68,010、gkx 学者级 citation_nums/h_index 全非空）；技术影响力分列、传播强度/区域带动/全球对标子维三源均无现成面——通用指数承载表 `ads_geo_yearly_index` 0 行（现场复核），区域组合影响力族 `ads_research_problem_region_snapshot` 六评分中投资分国家级覆盖 0/1,474（组合维缺格的量化证据，derived `jiuxin_region_country_investment_nonnull_pct=0.0`）。本件交付三源影响力分维谱系五族盘点（科学/篇均/区域组合/学者级/专利原料）作为组合立项的原料地图。判**部分支持**；单维先行（口径 A）或组合立项（口径 B）双路径写死。

- 需求判定：UI 拆件叶；组合语义真源=主需求文档 :923（产业发展潜力语境）；SRS 最近语义叶=seq 166「科技影响力趋势可视化」（趋势非指数本体）。
- 复现状态：脚本已跑通；单维覆盖/篇均族/区域六评分/学者列/专利原料/黑名单六组读数落产物。
- 档位结论：**部分支持**（组合分列结构缺失+子维语义未建设）。
- 关键事实：`ads_geo_yearly_index` 是久新预留的通用指数化承载表（14 列含 index_code/normalized_value/percentile/formula_snapshot）——结构在、数据空，组合指数的落表位置已预留。
- 升档路径：口径 B 组合立项（科学分复用+技术分合成+子维定义）→ 结构齐备后升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/科技指数/**科技影响力指数**（UI 拆件叶，row_01 220；挂载于 `techIndex.js`——科技指数数据集页的数据层模块，与 `pages/tech-index/` 展示层并立）。两处挂载：①`techIndex.js:257` `techIndexIndicatorTree` 四分项第三项——`{ key: 'influence', label: '科技影响力指数', weight: 24, description: '引用影响、传播强度、区域带动和全球对标' }`（同族：科研产出 30/成果转化 28/科技影响力 24/专家评议 18）；②`techIndex.js:515` `buildTechIndexDetail` 的「指标拆解」行——`{ label: '科技影响力指数', value: record.influence }`（对象详情卡的四分项读数之一，与综合指数/专家 H 指数并列）。数据形态：`baseRecords` 每对象带 influence 分（如 ti-shenzhen-robotics 95、ti-beijing-quantum 96——模拟值），`buildIndicatorScores` 聚合后供指标树/雷达消费。注意这套树与 `pages/tech-index/mockData.js` 的四维树（创新/影响/潜力/保障）是**两套不同的指标树**（数据层 30/28/24/18 vs 展示层 40/30/20/10）——本件挂前者。

### 1.2 为什么需要本指标

综合指数把「影响力」压缩成一个总分，科技影响力指数把它独立成项：决策者需要知道「指数高的对象是靠产出堆的还是靠影响撑的」——影响力分项是成果质量的代理读数（引用是同行用脚投票）。需求 :923 把它放进产业发展潜力评估体系（与产业投入/成熟度/产值并列），用意为：识别「影响力红利」产业——学术影响（引用）与技术影响（专利布局）双高的领域值得政策倾斜。四分项描述的四个子维（引用影响/传播强度/区域带动/全球对标）分别锚定学术认可、扩散广度、本地拉动、国际位置——这是本件子维探针的语义地图。

### 1.3 需求文档是否给出定义方法

**需求文档给出了语义列举但没给计算口径。** 主需求文档 :923 原文「通过收集和分析国内企业产业投入、技术或产品的成熟度、形成的产值等产业发展潜力指标，以及科学影响力、技术影响力等科技影响力指标，构建产业发展潜力评估体系」——「科学影响力、技术影响力等」的列举把本件定义为组合语义（等字开放），但「科学/技术影响力各自怎么算、怎么合成」无一字。SRS《科技指数.md》19 叶无「科技影响力指数」独立叶（最近语义叶 seq 166「科技影响力趋势可视化」是趋势展示功能）；techIndex.js 四分项 weight 24 与四子维描述是前端作者的演示实现。检索记录见附录 A。

### 1.4 类似指标权威方法可行性分析概要

科技影响力的权威方法分三支：学术侧以引用族为核心（FWCI/篇均被引，Elsevier SciVal 体系 R1；h 指数族，Hirsch 2005 R2）；技术侧以专利族为核心（专利前向引用/专利族规模，OECD 专利指标手册 R3）；组合侧以多维加权合成为主流（GII 的产出/影响两支柱结构 R4）。方法族对照：

| 方法族 | 代表 | 判定轴 | 数据要求 | 与本库匹配 |
|---|---|---|---|---|
| 引用族（科学分） | FWCI（R1）/h 指数（R2） | 论文被引/篇均 | 引用数据 | **有（citation_score/fwci 现役）** |
| 专利族（技术分） | OECD 手册（R3） | 专利前引/族规模 | 专利引用 | **原料有评分无**（明细 172,644 行） |
| 组合加权 | GII（R4） | 产出+影响支柱 | 两分族+权重 | 分族半缺+权重未立项 |

完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/techIndex.js:257` — `{ key: 'influence', label: '科技影响力指数', weight: 24, description: '引用影响、传播强度、区域带动和全球对标' }`；`techIndex.js:515` — `{ label: '科技影响力指数', value: record.influence }`（指标拆解行）。
- 同族：`techIndex.js:236` `techIndexLegend.resultTypes`（influence 图层色 #f97316）；`techIndex.js:56-160` baseRecords（influence 模拟值 81-96）。
- 需求：主需求文档《科技信息展示系统和科技专题服务系统.md》:923（组合语义真源，原文见附录 A）。

### 1.6 推测原意与推测定义

**推测定义**：$S_{sci\text{-}inf} = w_s \cdot S_{science} + w_t \cdot S_{tech} + \ldots$（科学分+技术分+…的加权组合；「等」字开放子维集，UI 四子维=引用影响/传播强度/区域带动/全球对标）。

- **口径 A（单维先行：科学影响力分）**：以久新 `citation_score`（机构级，100% 覆盖）或 fwci（篇均）直读——现役可交付，语义标注「科学影响力单维，非组合口径」；
- **口径 B（建议口径：组合立项）**：科学分复用 citation_score（或 fwci 族）+ 技术分从专利明细合成（前引/族规模代理）+ 传播强度/区域带动/全球对标子维定义（候选原料：region_snapshot 协作广度分/geo 面区域指标/国际对比基线）→ 加权合成落 `ads_geo_yearly_index` 式承载（结构已预留）。

**降档/升档触发器（B10 模板）**：口径 A 被接受 → 仍部分支持但语义闭合可即期交付（标注单维）；口径 B 立项（子维定义+技术分合成+权重）→ 结构齐备后升**完全转换支持**；若要求国际对标子维（全球位置百分位）→ 需跨国基线数据（geo COUNTRY 面可部分支撑，专列工程）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md`（无独立叶） |
| 语义真源 | 主需求文档 :923（产业发展潜力指标展示，1.1.1.1.4.1.7.3） |
| SRS 最近叶 | seq 166「科技影响力趋势可视化」（趋势展示，指数的时间形态） |
| UI 数据层树同族 | 科研产出指数 30 / 成果转化指数 28 / **科技影响力指数 24** / 专家评议指数 18（techIndex.js:253-259） |
| 展示层树近邻 | mockData.js:85 L1「科技影响力」0.30（另一套树，INDEX_015/016 语境） |
| 本批同 Lane | INDEX_015（产业影响力——组合的产业翼近邻）；INDEX_019/020/036（榜单族） |

两套「影响力」语境的辨析是本件定位的关键：`pages/tech-index/mockData.js` 的「科技影响力」是展示层四维树的 L1（其下拆学术/产业两 L2——INDEX_015/016 承接）；`techIndex.js` 的「科技影响力指数」是数据层四分项之一（weight 24，四子维描述）。本件挂后者，但需求 :923 的组合语义（科学+技术+…）与两语境都不同源——它是「指标族列举」而非「树节点」，这也是派单裁定 NEW（组合指数，非单指数读数）的根据。

## 二、计算过程

### 2.1 装载与单维锚确认

pymysql 直连久新只读库。科学影响力单维锚：`ads_institution_technology_power.citation_score`——64,698 行**全覆盖**（facts `jiuxin_citation_score_coverage`：nonnull 64,698、min 3.196439、max 100.0、avg 50.0——归一百分位制，均值 50 符合百分位分布预期）；paper_score 对照（nonnull 64,698、min 8.093111、max 100.0，facts `jiuxin_paper_score_coverage`）。单维的现役性成立：机构级科学影响力分可直读。

### 2.2 篇均影响力族（fwci 面）

`ads_institution_yearly_metrics` 的 fwci/avg_citations_per_paper 列 2026 年覆盖：68,010 行中 fwci 非空 21,651、篇均被引非空 22,342（facts `jiuxin_fwci_cols_2026`——约 31.8% 覆盖，非空子集集中在有当年产出的机构）；fwci Top5（facts `jiuxin_fwci_top5_2026`，最高 314.5455）——篇均族的现役可用但覆盖有限，适合作头部机构的质量读数而非全池分。

### 2.3 区域组合影响力族（region_snapshot）

`ads_research_problem_region_snapshot`（9,367 行，版本 2026-10-19×research_problem_real_monthly_metrics_v1，facts `jiuxin_region_snapshot_rows`/`jiuxin_region_snapshot_version`）六评分类：research_heat/frontier_leadership/investment/collaboration_breadth/competition+competition_rank（列清单落 `jiuxin_region_snapshot_columns`）。这是三源最接近「组合影响力」的现役面——但其组合轴是「问题×区域」粒度（每行=某研究问题在某区域的评分），且投资分在 COUNTRY 级 1,474 行中非空 **0** 行（facts `jiuxin_region_country_investment_coverage`，derived `jiuxin_region_country_investment_nonnull_pct=0.0`）——组合维缺格（投资维全空）是组合语义风险的直接量化证据。

### 2.4 技术影响力侧原料盘点

专利侧明细：`ads_technology_patent` 172,644 行（23 列：country_code/google_family_id/evidence_count/cited_seed_paper_count 等——facts `jiuxin_tech_patent_rows`）；`ads_institution_patent` 100,358 行（facts `jiuxin_inst_patent_rows`）。两表有专利族/证据强度类列（前引代理候选）但**无评分面**——技术分需自明细合成（聚合+归一），非现转即得。gkx 学者级：`dwd_scholar` 21,316 行中 citation_nums/h_index 全非空、reference_nums 0 非空（facts `gkx_scholar_influence_cols`——学者粒度科学影响力可读，但注意金样板已证该池中名率 95.8% 的池属性）。

### 2.5 组合承载缺位与落表位预留

通用指数化承载 `ads_geo_yearly_index`（14 列：index_code/index_name/raw_value/normalized_value/percentile/component_values/formula_snapshot/score_version）实测 **0 行**（facts `jiuxin_geo_yearly_index_rows`，共享探针 A5 现场复核）——「结构在、数据空」：组合指数一旦立项，该表即为现成落表位（index_code 编码+component_values 存分项+formula_snapshot 存口径快照，版本化设计完备）。dev 侧 `svc_tech_power_score` 0 行（黑名单披露，facts `dev_svc_tech_power_score_rows`）。

### 2.6 稳健性与口径敏感性

单维（科学分）与组合分的读数背离风险：技术强学术弱的机构（专利密集型工程机构）在口径 A 会被低估——组合分的技术翼正是为矫正此偏差而设，这也是 :923 列举式定义的业务动机。子维敏感：四子维（引用/传播/区域/对标）中仅引用维有现役锚，其余三子维的定义自由度大（传播=新闻提及？下载量？区域带动=本地合作占比？），不同定义将显著改变合成结果——B10 要求子维定义随立项纪要固化。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INDEX_028.py`（久新+dev 直连、`_gkxdb.py` 走 gkx）；运行 `python3 code/M_SCIUI_INDEX_028.py`。
- 产物：`code/M_SCIUI_INDEX_028_out.json`。正文数字对应键：`jiuxin_citation_score_coverage`（§2.1）、`jiuxin_fwci_cols_2026`/`jiuxin_fwci_top5_2026`（§2.2）、`jiuxin_region_snapshot_*`/`jiuxin_region_country_investment_coverage`（§2.3）、`jiuxin_tech_patent_rows`/`jiuxin_inst_patent_rows`/`gkx_scholar_influence_cols`（§2.4）、`jiuxin_geo_yearly_index_rows`/`dev_svc_tech_power_score_rows`（§2.5）。
- 结果解读：五族分维谱系（科学/篇均/区域组合/学者/专利原料）+两处缺格（geo_index 0 行、投资分 0 覆盖）+两处覆盖度派生——组合立项的原料地图与风险清单一次交付。
- 对照需求功能要求的评审：指标拆解行回填——**有条件通过（口径 A）**：influence 位以 citation_score 直读+「单维」标注；未通过点=组合语义（技术分+三子维）无承载，待口径 B 立项。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 | 数值 |
|---|---|---|---|
| 单维锚 | citation_score 覆盖 | `jiuxin_citation_score_coverage` | 64,698/64,698（100%） |
| 派生 | 单维覆盖率 | `jiuxin_citation_score_nonnull_pct` | 100.0% |
| 篇均族 | fwci 2026 覆盖 | `jiuxin_fwci_cols_2026` | 21,651/68,010 |
| 区域族 | 六评分+版本 | `jiuxin_region_snapshot_*` | 9,367 行×2026-10-19 |
| 缺格 | 国家级投资分覆盖 | `jiuxin_region_country_investment_coverage` | 0/1,474 |
| 派生 | 投资分覆盖率 | `jiuxin_region_country_investment_nonnull_pct` | 0.0% |
| 技术侧 | 专利明细 | `jiuxin_tech_patent_rows`/`jiuxin_inst_patent_rows` | 172,644/100,358 |
| 学者级 | gkx 三列非空 | `gkx_scholar_influence_cols` | 21,316/21,316/0 |
| 落表位 | geo_yearly_index | `jiuxin_geo_yearly_index_rows` | 0（结构预留） |
| 黑名单 | svc_tech_power_score | `dev_svc_tech_power_score_rows` | 0（值不引用） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 科学影响力分（单维锚） | jiuxin_warehouse | `power.citation_score`；`yearly.fwci` | 64,698 / 21,651 | 直查 | **有** |
| D2 | 技术影响力分（组合翼） | jiuxin_warehouse | 专利明细（无评分面） | 172,644 / 100,358 | 原料在 | **缺合成面** |
| D3 | 传播/区域带动/全球对标子维 | 三源 | —（候选：region_snapshot 协作分/geo 面等） | — | 部分/未定义 | **缺（语义级）** |
| D4 | 组合承载表 | jiuxin_warehouse | `ads_geo_yearly_index`（14 列） | 0 | 结构在数据空 | 预留落表位 |
| D5 | 学者级影响力 | gkx | `dwd_scholar` 三列 | 21,316 | 直查 | 有（池属性注意） |

`support_judgment="部分支持"`，与文首同档（闸 6）。

### 3.2 D1 质量面

citation_score 的三重可用性：全覆盖（64,698/64,698）、分布健康（min 3.1964/max 100.0/avg 50.0——百分位制无退化）、版本单一（mvp_v1，INDEX_001/013 对账零漂移）。fwci 族覆盖 31.8%（有当年产出机构子集）——头部读数可用、全池分不可，产物 notes 已限定其用途。

### 3.3 D2/D3 absence_probe 全记录

否定性证据三件套：**查了什么**——①久新 power 22 列+geo_yearly_index 行数（组合分列/承载面）；②gkx influence/impact/index 关键词表扫描（4 命中均为宏观经济指数族——dim_cal=环比/同比/绝对值、macro_index_data=广东地市宏观指标值，语义不同域，存在性披露不构成承载）；③dev svc_tech_power_score 行数。**条件**——「科学+技术组合」现成结果面存在性。**命中**——三源均无。缺失情形归属：D2「有原料无成品」（专利明细→技术分需聚合归一工程）；D3「子维语义未建设」（定义需立项纪要）；D4「表在数空」（落表位已预留）。

## 四、数据缺失情况

### 4.1 技术影响力分缺失（合成级，主因）

专利明细 172,644 行有前引代理列（cited_seed_paper_count/evidence_count/google_family_id）但无机构/区域级技术分面——合成工程=聚合（机构/区域粒度）+归一（百分位制对齐 citation_score）+落表（geo_yearly_index 式）。工程量中等（聚合管道），无外部依赖。

### 4.2 传播/区域带动/全球对标子维缺失（语义级）

三子维无权威定式亦无库内现成分列（§2.6 敏感性）。候选原料：传播强度←gkx `dwd_news_base` 20,000 行提及面（弱代理）；区域带动←region_snapshot collaboration_breadth_score（问题粒度需上卷）；全球对标←geo COUNTRY 面 27 年基线（跨国百分位）。子维定义是口径 B 立项的核心交付物。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 单维直供 v1 | 数据工程 | 本件即期 | citation_score 直读+「单维」标注 |
| 技术分合成管道 | 数据工程 | 本件+036（地理榜） | 专利明细→分→geo_yearly_index 落表 |
| 子维定义立项 | 流程+建模 | 本件组合口径 | 四子维纪要固化（B10） |
| 投资分补数建议 | 供给侧建议 | region_snapshot 族 | 国家级投资分 0 覆盖反馈数据方 |

## 参考文献

1. FWCI — Field-Weighted Citation Impact[EB/OL]. Elsevier SciVal. https://www.elsevier.com/products/scival/metrics-guide （2026-11-01 WebSearch 核验可达；篇均引用影响力的领域加权国际标准）
2. Hirsch, J. E. An index to quantify an individual's scientific research output[EB/OL]. PNAS, 2005, 102(46): 16569–16572. https://doi.org/10.1073/pnas.0507655102 （2026-11-01 WebSearch 核验可达；h 指数奠基——学者级影响力轴）
3. OECD Patent Statistics Manual[EB/OL]. OECD. https://www.oecd.org/sti/patent-statistics-manual-9789264041367-en.htm （2026-11-01 WebSearch 核验可达；专利前引/专利族技术影响力指标的国际范式）
4. Global Innovation Index 2024[EB/OL]. WIPO. https://www.wipo.int/global_innovation_index/en/ （2026-11-01 WebSearch 核验可达；产出/影响支柱组合加权结构）

# 附件

## 附录 A 原始需求原文摘录

主需求文档《科技信息展示系统和科技专题服务系统.md》:921-925（1.1.1.1.4.1.7.3 产业发展潜力指标展示）——**组合语义真源**：

> 1.1.1.1.4.1.7.3. **产业发展潜力指标展示**
>
> 通过收集和分析国内企业产业投入、技术或产品的成熟度、形成的产值等产业发展潜力指标，以及**科学影响力、技术影响力等科技影响力指标**，构建产业发展潜力评估体系。结合专利－发明人－学者－地域－产业等知识图谱数据，支持全面分析不同产业的发展现状和未来潜力，为决策者提供产业发展趋势和投资方向的科学依据，帮助识别具有高发展潜力的产业领域，为产业政策制定和资源配置提供决策支持。
>
> 产业发展潜力指标展示的具体功能包括产业投入分析、技术产品成熟度评估、产业产值分析、科学影响力评估、技术影响力评估、产业发展潜力综合评估。

SRS《科技指数.md》最近语义叶 seq 166（趋势形态，非指数本体）：

> ### 科技影响力趋势可视化 · 序号 166
> #### 需规功能描述
> 以折线图、面积图等形式展示科技影响力随时间的变化趋势，用户可选择不同时间范围、不同科技领域查看趋势变化，系统支持多指标对比展示，帮助用户分析科技发展的动态变化。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 科技影响力指数 | SRS 科技指数.md（19 叶） | 0（独立叶） |
| 科技影响力指数 | 主需求文档 | 0（:923 为「科学影响力、技术影响力等科技影响力指标」列举式） |
| 科学影响力、技术影响力 | 主需求文档 | 1（:923，组合语义真源） |
| 科技影响力 | SRS 科技指数.md | 1（seq 166 趋势可视化） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INDEX_028_out.json`（2026-11-01 实跑）。
- 共享探针：`_probe_lane4_s302_out.json`（A5 geo_index 0 行；C1-C3 region_snapshot；D1/D2 gkx 列清单；D3 gkx 扫描）、`_probe_lane4_s302_r2_out.json`（gkx index 族四表细查——宏观指数族定性）。
- 久新 schema 索引：`20261026_久新指标 gap 调研/…/_jiuxin130_fields.json`（region_snapshot 27 列/technology_patent 23 列在案）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INDEX_028 | 文首 |
| `ui_evidence` | 证据 | 3 条组件行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | false（组合真源=:923） | §1.1/附录 A |
| `facts.jiuxin_citation_score_coverage` | 覆盖 | 64,698/64,698, avg 50.0 | §2.1 |
| `facts.jiuxin_paper_score_coverage` | 对照 | 64,646 非空 | §2.1 |
| `facts.jiuxin_fwci_cols_2026` | 覆盖 | 21,651/68,010 | §2.2 |
| `facts.jiuxin_fwci_top5_2026` | Top5 | 最高 314.5455 | §2.2 |
| `facts.jiuxin_region_snapshot_columns` | 列清单 | 27 列（六评分族） | §2.3 |
| `facts.jiuxin_region_snapshot_rows`/`_version` | 规模版本 | 9,367×2026-10-19 | §2.3 |
| `facts.jiuxin_region_country_investment_coverage` | 缺格 | 0/1,474 | §2.3 |
| `facts.jiuxin_tech_patent_rows`/`jiuxin_inst_patent_rows` | 原料 | 172,644/100,358 | §2.4 |
| `facts.gkx_scholar_influence_cols` | 学者级 | 21,316/21,316/0 | §2.4 |
| `facts.jiuxin_geo_yearly_index_rows` | 落表位 | 0（14 列结构在） | §2.5 |
| `facts.dev_svc_tech_power_score_rows` | 黑名单 | 0 | §2.5 |
| `derived[0]` | 派生比 | citation 覆盖 100.0% | §2.1 |
| `derived[1]` | 派生比 | 投资分覆盖 0.0% | §2.3 |
| `absence_probe` | 探针 | 三源 3 条 | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 轴 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 引用族（科学分） | FWCI（R1）/h（R2） | 被引/篇均 | citation_score+fwci 现役 | **最高（口径 A）** |
| 专利族（技术分） | OECD（R3） | 前引/族规模 | 明细 172,644 行无评分 | 高（需合成） |
| 组合加权 | GII（R4） | 支柱合成 | geo_index 落表位预留 | **目标态（口径 B）** |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| citation_score | 64,698 | 100% 覆盖/百分位制 | 单维（非组合） |
| fwci 族 | 21,651 | 头部可用 | 覆盖 31.8% |
| 专利明细 | 172,644+100,358 | 前引代理列在 | 无评分面 |
| region 六评分 | 9,367 | 问题×区域粒度 | 投资分 0 覆盖 |
| geo_yearly_index | 0 | 14 列结构在 | 数据空（预留位） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A：citation_score 直读+单维标注 | 无 |
| v2 | 技术分合成管道→落 geo_index | 聚合工程 |
| v3 | 四子维组合口径（传播/带动/对标定义+权重） | 立项纪要 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 单维读数被当组合指数 | **高** | UI 标注「科学影响力单维」 |
| 技术强学术弱对象被低估 | 中 | v2 技术翼矫正 |
| 子维定义漂移 | 中 | 纪要固化+formula_snapshot 落表 |
| region_snapshot 粒度误用（问题≠产业） | 中 | 上卷口径披露 |

### C.5 总判

**部分支持**：组合分列结构缺失（技术翼无评分面+三子维未定义）与单维现役（100% 覆盖）并存；落表位已预留（geo_index），双口径触发器不悬空。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INDEX_028.py` | 退出码 0，落 `_out.json` |
| 单维对账 | citation_score 覆盖 | 64,698=power 全表（B11） |
| 缺格复核 | geo_yearly_index 行数 | 0（与共享探针 A5 一致） |
| 学者列对账 | gkx 三列非空 | 21,316/21,316/0（金样板基数一致） |
| 判档一致 | MD 文首 vs `support_judgment` | 部分支持 |

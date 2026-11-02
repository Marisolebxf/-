# 学者环境适应性评估得分（M_SCIUI_TALENTIR_004）

> **类型**：需业务建模类（评分口径三源未立项）｜ **域**：科技信息展示系统·人才引进推荐评估·学者适配度分析｜ **UI 挂载**：科技信息展示系统 → 人才引进推荐评估 → 能力映射清单（talentRecommendSpec.js:22「学者适应性评估」L6 项）→ `DifficultyTab` mock 消费 `difficultyEstimate.factors`/`overall`
> **数据支持度**：**部分支持**｜ **公式定义人**：无（需求给功能行为「综合国籍、语言能力、教育经历、文化背景等多维信息，对学者的工作环境适应性进行量化分析」，不给算式）｜ **口径归属**：需求明列叶（主需求 1.1.1.1.4.3.4.2.1），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TALENTIR_004.py`｜ **产物**：`code/M_SCIUI_TALENTIR_004_out.json`
> **四判定摘要**：直接结构 = 无（三源无适应性评分结果面，capability 模型四维无适应性维）；直接数据 = 无（同左）；依赖结构 = 部分（地理/流动/教育经历三维结构在，语言/文化两维结构缺）；依赖数据 = 部分（地理代理 38.47% 覆盖、跨国经历 0、跨国流动事件 8,748 在案）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 需求四维（国籍/语言能力/教育经历/文化背景）逐一对照三源：**教育经历维结构+数据双在**——久新 `ads_talent_experience` 140,887 行覆盖 49,279 人才（其中教育段 56,302 行）；**地理/流动维数据在但代理语义弱**——`ads_talent_profile.country_name` 覆盖 38.47%（38,467/100,000，schema 文档明示是机构所在地代理非已核验居住地），`ads_talent_experience` 跨国经历人才 0（0.0%，分母=经历表 49,279 人才池），`ads_talent_mobility_event` 跨国事件 8,748 在案（跨文化流动经历是适应性文献的常用代理）；**语言维只能弱代理**——`ads_paper_profile.language` 面存在（Top8：en 3,828,053/de 19,799/fr 12,188/es 9,980/ja 8,302…）但论文语言≠个人语言能力，本件不派生；**文化背景维零承载**——三源无文化评分面。评分结果面三源未立项：capability 模型唯一在册公式四维=科研毅力/创新/学科匹配/政治倾向，无适应性维（§3.3）。`scholar_environment_adaptability_score = null`（B10 不写伪分）。

### 批次通用纪律摘要（S3-03 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 跨国经历占比分母=经历表人才池非 profile 全池（note 写死口径差异） |
| B4 | 负结论带探针 | 语言/文化零承载的四源探针（§3.3） |
| B5 | 确定性 | Top8 按计数降序、词族扫描固定顺序 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | 覆盖率为百分数；经历表无日期运算 |
| B10 | 口径裁定保守交付 | 不写伪分；derived 留 null + mock 登记披露；升档触发器写死 |
| B11 | 多本账互推 | 久新 100,000/140,887 与族内件零漂移；gkx 27 列与 CHINESE_RATIO 探针一致 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有适应性评分现成结果面吗？ | 无 | 表名词族 0 命中 + capability 模型四维无适应性维（§2.5/§3.3） |
| 依赖四维有几维结构+数据双在？ | 一维（教育经历） | 140,887 行/49,279 人（§2.4） |
| 缺的维（语言/文化）能代理吗？ | 语言弱代理（不派生）；文化零承载 | 论文语言≠个人语言能力（§2.6） |

## 摘要

「学者环境适应性评估得分」是学者适配度分析的第三功能叶（主需求 1.1.1.1.4.3.4.2.1）：综合国籍、语言能力、教育经历、文化背景等多维信息，对学者到岗后的工作环境适应性进行量化分析。UI 侧它是能力映射清单的 L6 登记项（`talentRecommendSpec.js:22`），实际数字消费在 `DifficultyTab`——mock 生成器 `data.js:1385` 产出 `difficultyEstimate.factors`（气候/生活成本/文化适应难度）与 `overall` 常量演示值。数据侧三源均无适应性评分结果面：gkx 学者面 27 列无国籍/语言列（结构级缺失）；dev talent 词族 0 命中；久新 capability 模型四维（毅力/创新/学科匹配/政治倾向）无适应性维。但依赖侧三维有数据：教育经历面 140,887 行（教育段 56,302）、地理代理 country_name 覆盖 38.47%、跨国流动事件 8,748。判**部分支持**：一维双在、一维弱代理、两维缺——评分口径选型待裁定（参照 POLCMP_008 写法）。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**需求明列叶**（主需求 :2369/:2371-2373），功能行为在、算式无。
- 复现状态：脚本已跑通；四维承载探针 + 三维代理读数全落产物。
- 档位结论：**部分支持**（评分面未立项 + 依赖三维数据在）。
- 关键事实：`ads_talent_experience` 140,887 行、49,279 人才，跨国经历 0 人——经历表的 country 字段实质未回填为多国值，地理代理只能靠 profile.country_name 单点常驻国。
- 升档路径：甲方裁定适应性口径=地理/流动/教育三维代理合成 → 完全转换支持；引入语言能力数据源 → 四维闭合。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技人才态势/**人才引进推荐评估·学者适配度分析/学者适应性评估**（主需求 1.1.1.1.4.3.4.2.1）。UI 实际容器是人才引进推荐评估页的难度评估 Tab（`DifficultyTab`）与推荐说明侧栏：`talentRecommendSpec.js` 是能力映射清单数据结构，第 22 行登记 `{ id: 'fit', label: '学者适应性评估', ... }` 为 L6 项（第 15 行起结构定义），`DifficultyTab` 从 `talent` 对象读取 `difficultyEstimate.factors`（气候/生活成本/文化适应三因子）与 `difficultyEstimate.overall`（综合难度常量）渲染——这些值全部由 mock 生成器 `data.js:1385` 按固定区间 random 产出。与 S3-02 的 POLCMP_016/022 同型：**结构在、mock 值不写伪分**（B10 纪律——derived 留 null + mock 登记披露）。

### 1.2 为什么需要本指标

学者引进的场景痛点是「到岗失败」：学术能力评分再高，若学者无法适应目标城市的生活成本、文化环境、语言要求，引进投入照样沉没。需求把适应性评估放在适配度分析（与贡献度分析并列的第二分析面）：贡献度回答「他能产出什么」，**适配度回答「他能不能落地」**。官方对应物是科技人才评价改革试点方案（R1）的「分类评价」思想——不同岗位类型的适配要求不同；国际口径上 OECD 人才流动指标（R2）把跨国流动经历作为人才适应性的标准观测维。本件的调研重心因此是「需求四维（国籍/语言/教育/文化）在三源有没有可观测的落点」：有落点的维可进评分，无落点的维只能披露为缺口。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**主需求 :2371-2373 给出的是功能行为：「综合国籍、语言能力、教育经历、文化背景等多维信息，对学者的工作环境适应性进行量化分析，帮助用人单位了解学者到岗后的工作环境适应难度，提前提供针对性支持」——四维点名了，但每维的观测源、标准化、权重、合成算式一个字都没有。核增需求与算法库两份真源检索 0 命中（附录 A.2）。UI mock 的 factors/overall 是演示值，不构成口径证据。

### 1.4 类似指标权威方法可行性分析概要

「环境适应性评估」的权威方法锚分层：其一，科技人才评价改革试点方案（R1，国科发才〔2022〕255 号）不直接给适应性公式，但给出「按岗位类型分类评价」框架——引才适配评估应按引进岗位类型差异化，这与需求「帮助用人单位了解适应难度」的场景一致。其二，OECD 人才流动指标体系（R2）把「跨国流动经历」作为人才适应性的核心观测——有跨国工作/学习经历的学者适应性风险更低，这与久新 `ads_talent_mobility_event` 的跨国事件面（8,748）直接可映射。其三，跨文化适应研究经典 ACSS 框架（R3）把适应分为心理适应/社会文化适应/学术适应三面——社会文化适应面（语言/日常/文化距离）与需求四维高度同构，学术适应面（教育经历/科研环境）在库内有直接落点（experience 面）。方法族对照：

| 方法族 | 代表 | 维度结构 | 数据要求 | 与三源匹配 |
|---|---|---|---|---|
| OECD 流动口径 | R2 | 跨国流动经历/迁移率 | 流动事件/迁移记录 | **有**（mobility_event 298,384 行，跨国 8,748） |
| ACSS 跨文化适应 | R3 | 心理/社会文化/学术适应 | 量表数据（库内无） | 部分（学术适应→experience 可映射） |
| 分类评价试点 | R1 | 岗位类型×适配要求 | 分类画像 | 部分（career_stage 在） |
| 前端演示模型 | UI difficultyEstimate | 气候/生活成本/文化适应 | mock 常量 | 结构披露（不作源） |

结论：无单一权威公式可直接落地，但地理/流动/教育三维的代理读数全部有数据面；语言/文化两维零承载。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/talent-trend/talentRecommendSpec.js:22` — `{ id: 'fit', label: '学者适应性评估' }`（L6 能力映射项）；第 15 行起结构定义；mock 消费 `data.js:1385`（`difficultyEstimate.factors`/`overall`）；`DifficultyTab` 渲染容器。
- 主需求：`科技信息展示系统和科技专题服务系统.md` :2369/:2371-2373（1.1.1.1.4.3.4.2.1），原文见附录 A。
- 权威方法：R1 国科发才〔2022〕255 号（科技部官网）；R2 OECD 人才流动指标（OECD Handbook）；R3 Mak et al. 1997 跨文化适应量表。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**：

$$S_{adapt} = \sum_{d=1}^{4} w_d \cdot s_d,\quad s_d \in [0,100]$$

四维 = 国籍（常驻国与目标地文化距离）/语言能力（目标地语言掌握度）/教育经历（跨国教育经历丰富度）/文化背景（文化圈跨度），权重待定版。UI mock 的 factors 三因子（气候/生活成本/文化适应）是前端演示维度，与需求四维不同物（mock 结构披露，不参与结论）。库内可落地的代理口径（候选）：**口径 A（地理/流动/教育三维代理）**——s_geo = f(country_name 与目标国距离)、s_flow = g(跨国流动事件数)、s_edu = h(跨国教育经历)；**口径 B（capability 面扩展）**——在四维模型（毅力/创新/学科匹配/政治倾向）外新增适应性维（需模型迭代）。两口径都未立项，按 B10 不写伪分，`scholar_environment_adaptability_score` 留 null。

**降档/升档触发器**：①甲方裁定适应性口径=口径 A（三维代理合成，权重公示）→ 转换可算升**完全转换支持**（语言/文化两维降维披露）；②引入语言能力数据源（ORCID 语言字段/多语论文署名比）→ 四维闭合升完全转换支持；③维持现状（口径未立项+两维零承载）→ 部分支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在需求文档 | 主需求《科技信息展示系统和科技专题服务系统.md》（SRS 人才引进推荐评估同文转述） |
| 所属四级功能 | 1.1.1.1.4.3.4 人才引进推荐评估（4 个 L5） |
| 所属 L5 | 学者适配度分析（1.1.1.1.4.3.4.2，3 叶） |
| 本件叶 | **学者适应性评估（1.1.1.1.4.3.4.2.1）——需求明列** |
| 同 L5 相邻叶 | 学者贡献度分析（.1，1.1.1.1.4.3.4.1——注意跨 L4 编号，贡献度族件承接）/ 文化融入度分析（.3） |
| UI 容器 | `talentRecommendSpec.js:22` 能力映射 L6 项 → `DifficultyTab` mock 消费 |

本件与文化融入度分析（.3）是同 L5 的近邻——两者都观测文化维度，本件是综合评分、.3 是单维深入；若文化融入度件立项，文化背景维的数据缺口结论可直接复用本件 §3.3 探针（三源无文化评分面）。

## 二、计算过程

### 2.1 方法选择（文献依据）

若口径闭合，方法选**代理指标加权合成（OECD 流动口径的落地版）**：地理距离/流动经历/教育跨度三维各建 0-100 代理分，加权合成。选择理由：其一，跨国流动经历是适应性文献的标准代理（R2），久新 mobility_event 面直接可映射（298,384 行事件、8,748 跨国）；其二，ACSS 框架（R3）的社会文化适应面在库内无量表数据，但学术适应面（教育/科研经历）有 experience 面落点——代理合成是数据可及性下唯一诚实的方法；其三，UI mock 三因子（气候/生活成本）中的气候/生活成本维依赖目标地选择，属用人单位侧参数而非学者侧数据——这提示适应性评分本质是「学者×目标地」二元评分，单一学者侧数据面不足以闭合，需用人单位侧配置（目标地语言/文化参数）配对。语言维按论文语言弱代理不派生（§2.6）。

### 2.2 装载与地理代理读数

经 `_gkxdb.py` 连 gkx、直连 dev 与久新（三源串行只读）。主画像 `ads_talent_profile` 100,000 行，`country_name` 非空 38,467（38.47%，产物派生键 `jiuxin_country_field_coverage_pct`）——schema 文档明示该字段是**机构所在地代理**非已核验居住地，代理语义在 note 写死。Top8 常驻国：中国 21,611/美国 5,654/英国 1,860/澳大利亚 1,068/香港 1,065/德国 713/加拿大 641/日本 468——地理分布有区分度（中美双主力），可支撑「与目标地文化距离」的代理计算。覆盖率分子分母同表同 WHERE（100,000 全量非采样，B3）。

### 2.3 流动维：mobility_event 面与跨国事件

`ads_talent_mobility_event` 298,384 行，事件类型三种：EDUCATION_TO_WORK 7,991/RESEARCH_FIELD_CHANGE 281,117/WORK_TO_WORK 9,276——字段级探针 `is_cross_country`/`cross_country` 语义的跨国事件 8,748 在案（产物 `jiuxin_mobility_cross_country_events`）。跨国流动经历是 OECD 口径（R2）适应性代理的核心观测：有跨国工作/学习经历的学者，到新环境再适应的风险显著更低。8,748 相对 100,000 人才池的占比约 8.7%，代理读数有量级支撑。

### 2.4 教育经历维：experience 面双在

`ads_talent_experience` 140,887 行覆盖 49,279 人才（人均 2.9 段经历），其中教育段（`experience_type='EDUCATION'`）56,302 行；经历表 `country` 字段非空 60,637 行（43.1%）——**但跨国经历人才数为 0**（`jiuxin_multi_country_experience_talents=0`，0.0%，分母=经历表 49,279 人才池）：同一人才的多段经历 country 字段实质未回填为多国值（多为单国多机构），跨国教育经历读数在经历表面不可得，只能靠 mobility_event 的跨国事件面补。这一「字段在、多国值未回填」的发现是本件关键负结论：教育经历维的**结构**双在（140,887 行/49,279 人），但跨国教育子维的数据语义弱。

### 2.5 三源排除与评分面未立项

**gkx**：280 表 adapt/assimil/mobility/language 词族 0 命中；`dwd_scholar` 27 列逐一核对（national/citizen/language/birth/country 词族 0 命中）——国籍与语言维在 gkx 学者面**结构级缺失**（`gkx_scholar_nationality_language_cols=[]`）；工作经历面 `dwd_scholar_work_experience` 22 列（org/department/position 结构在，无国家列）。**dev**：gkxlumenx_* 全 schema adapt/assimil/difficulty/talent 词族 0 命中（`dev_adapt_like_tables=[]`）。**久新**：203 表 adapt/assimil/language/culture 词族 0 命中（`jiuxin_adapt_like_tables=[]`）；capability 模型唯一在册公式四维=科研毅力/创新/学科匹配/政治倾向——**无「环境适应性」维**。评分结果面三源未立项。

### 2.6 稳健性与口径敏感性

三维代理口径的敏感性定性：地理维用 country_name（机构所在地代理）会系统性低估流动性强的学者（常驻国≠工作史）；流动维用跨国事件数（8,748/100,000≈8.7%）对无流动记录的学者给低分，但「无记录」可能意味「未迁移」也可能意味「事件未采集」——区分不开，代理分需带置信披露；教育维的跨国教育子维已证实不可得（§2.4），只能降维到「教育段数」这种弱代理。语言维若用论文语言代理：en 3,828,053/4,000,000=95.7% 的论文是英文——对中文用人单位场景，「英文论文占比高」不等于「中文工作语言能力」，代理语义反向，本件不派生（B10）。文化维零承载，不代理。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TALENTIR_004.py`（三源串行只读；gkx 经 `_gkxdb.py`；dev/久新直连；零 `demo_*`）；运行 `python3 code/M_SCIUI_TALENTIR_004.py`。
- 产物：`code/M_SCIUI_TALENTIR_004_out.json`。正文数字与产物键逐一对应：`jiuxin_talent_profile_rows=100000` + `jiuxin_country_name_nonnull=38467` + 派生键 `jiuxin_country_field_coverage_pct=38.47`（§2.2）、`jiuxin_top8_countries`（§2.2）、`jiuxin_mobility_event_rows=298384` + `jiuxin_mobility_cross_country_events=8748` + `jiuxin_mobility_event_types`（§2.3）、`jiuxin_talent_experience_rows=140887` + `jiuxin_experience_distinct_talents=49279` + `jiuxin_experience_education_rows=56302` + `jiuxin_experience_country_nonnull=60637` + 派生键 `jiuxin_multi_country_experience_pct=0.0`（§2.4）、`jiuxin_paper_language_top8`（§2.6 语言弱代理证据）、`gkx_scholar_nationality_language_cols=[]` + `jiuxin_adapt_like_tables=[]`（§2.5/§3.3）、`scholar_environment_adaptability_score=null`（B10 留空）。
- 结果解读：三维有读数（地理 38.47% 覆盖/流动 8,748 跨国事件/教育 140,887 行）+ 两维零承载（语言弱代理不派生/文化无面）+ 评分面未立项——「口径未立项+事件无源」双缺确认，derived 留 null 即负结论登记。
- 对照需求功能要求的评审：「综合国籍、语言能力、教育经历、文化背景等多维信息」——**部分满足**：教育经历维结构+数据双在；国籍维只能常驻国代理（38.47% 覆盖）；语言/文化两维零承载；「对工作环境适应性进行量化分析」——评分算式三源未立项，量化分析待口径裁定。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 主画像行数 | `jiuxin_talent_profile_rows` | 100,000 |
| 覆盖 | 常驻国非空 | `jiuxin_country_name_nonnull` | 38,467（38.47%） |
| 分布 | Top8 常驻国 | `jiuxin_top8_countries` | 中国 21,611 / 美国 5,654 / … |
| 流动 | 事件总数 | `jiuxin_mobility_event_rows` | 298,384 |
| 流动 | 跨国事件 | `jiuxin_mobility_cross_country_events` | 8,748 |
| 教育 | 经历表行数 | `jiuxin_talent_experience_rows` | 140,887 |
| 教育 | 去重人才 | `jiuxin_experience_distinct_talents` | 49,279 |
| 教育 | 跨国经历人才 | `jiuxin_multi_country_experience_talents` | **0**（0.0%） |
| 排除 | gkx 国籍/语言列 | `gkx_scholar_nationality_language_cols` | []（27 列 0 命中） |
| 排除 | 久新适应表 | `jiuxin_adapt_like_tables` | []（203 表 0 命中） |
| 排除 | capability 四维 | `jiuxin_capability_model_formula` | 无适应性维 |
| 评分 | 适应性分 | `scholar_environment_adaptability_score` | null（B10） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---面|---|---|---|---|---|
| D1 | 地理（国籍代理） | jiuxin | `ads_talent_profile.country_name` | 38,467（38.47%） | 代理直查 | 有（代理，覆盖 38.47%） |
| D2 | 流动经历 | jiuxin | `ads_talent_mobility_event` | 298,384（跨国 8,748） | 直查 | **有** |
| D3 | 教育经历 | jiuxin | `ads_talent_experience` | 140,887（教育段 56,302） | 直查 | **有（跨国子维不可得）** |
| D4 | 语言能力 | 三源 | — | — | **不存在** | **缺（论文语言弱代理不派生）** |
| D5 | 文化背景 | 三源 | — | — | **不存在** | **缺（主降档因之一）** |
| D6 | UI 演示值 | UI | data.js difficultyEstimate | — | mock | 边界证据（不作源） |

`support_judgment="部分支持"`、产物与文首一致。

### 3.2 D1-D3 代理读数的覆盖与量级（久新）

地理代理覆盖率 38.47% 对 100,000 全池是「可用但需披露」的水平：Top8 国覆盖非空行的 94.4%（36,080/38,467），分布集中可支撑距离计算；流动维 8,748 跨国事件对 100,000 池约 8.7% 的人才有跨国记录；教育维 49,279 人（49.3%）有经历记录。三维合计的「全维可评」子池 = country_name 有值 ∩ 有经历记录的人才，需二次探针才可量化——本件未展开（评分口径未立项，聚合无意义），升档触发器①触发后再算。

### 3.3 D4/D5 语言/文化维的 absence_probe 全记录

否定性证据三件套：**查了什么**——gkx 280 表 adapt/assimil/mobility/language 词族 + `dwd_scholar` 27 列国籍/语言词族；dev 全 schema adapt/assimil/difficulty/talent 词族；久新 203 表 adapt/assimil/language/culture 词族 + capability 模型维度清单核对；需求原文算式段。**条件**——表级与列级存在性 + 模型维成员资格。**命中**——0（四源全部）。四缺失情形归属：**表不存在**（语言能力面/文化评分面三源均无）——修复动作是接外部数据源（ORCID 语言字段/多语论文署名比；文化距离维表），不是补数据。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 地理代理覆盖 | 38,467/100,000 = 38.47%（全量非采样） |
| 跨国事件量级 | 8,748（mobility_event 298,384 之内） |
| 经历表覆盖 | 140,887 行/49,279 人（教育段 56,302） |
| 跨国经历人才 | 0（经历表 country 多国值未回填） |
| gkx 国籍/语言列 | 27 列 0 命中（结构级缺失） |
| capability 四维 | 无适应性维（模型公式原文在案） |
| 脚本形态 | 三源串行只读；零 demo_* |

## 四、数据缺失情况

### 4.1 语言与文化两维零承载（结构级，主因）

需求四维中语言能力与文化背景在三源均无承载：gkx 学者面无 nationality/language 列（27 列词族 0 命中）；久新 203 表无语言/文化评分面；dev 无人才评估面。论文语言面（`ads_paper_profile.language`）虽在，但 en 占 95.7%——对中文用人单位场景代理语义反向（英文论文多≠中文能力强），本件不派生（B10）。四缺失情形归属「表不存在」，修复只能靠外部数据源：语言维可接 ORCID 语言字段或多语论文署名比，文化维可接文化距离维表（Hofstede 类）。

### 4.2 评分口径未立项（方法级，次因）

三源无适应性评分结果面：capability 模型四维（毅力/创新/学科匹配/政治倾向）无适应性维，说明久新侧的评分工程（有完整模型-分项-总分链路）尚未把适应性纳入模型。这与 CHINESE_RATIO 件的政治倾向维缺口同型：需求点名的评分轴，库内评分工程未立项。修复动作是模型迭代立项（在 capability 面加适应性维）或甲方裁定代理口径（口径 A）——裁定前本件保守交付三维代理读数，不合成伪适应性分。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 甲方裁定三维代理口径（地理/流动/教育） | 口径裁定 | 本件即期可升档 | 触发器①（§1.6） |
| 语言能力数据源接入（ORCID/多语署名比） | 外部数据源 | 本件 + 文化融入度件 | 补语言维 |
| 文化距离维表接入（Hofstede 类） | 外部数据源 | 本件 + 文化融入度件 | 补文化维 |
| 经历表 country 多国值回填 | 数据回填 | 本件跨国教育子维 | 修复「字段在值未回填」 |
| capability 面加适应性维 | 模型迭代 | 本件 + 族内评分件 | 评分工程立项 |

档位后果：三维口径裁定 → **完全转换支持**；语言源接入 → 四维闭合仍属完全转换支持（文化维继续披露）；现状 → 部分支持。推荐顺序：先裁口径（零成本即期），语言/文化源接入列中期，capability 模型迭代列远期。

## 参考文献

1. 科技部等八部门印发《关于开展科技人才评价改革试点的工作方案》的通知（国科发才〔2022〕255 号）[EB/OL]. 中华人民共和国科学技术部. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2022/202211/t20221109_183356.html （R1，2026-11-01 WebSearch 核验可达——分类评价框架，引才适配评估的岗位类型差异化依据）
2. OECD. Handbook on Measuring Human Capital Flows and Migration (OECD Handbook on Measuring International Migration through Censuses) [EB/OL]. OECD. https://www.oecd.org/en/publications/handbook-on-measuring-international-migration-through-censuses_19de3ab8-en.html （R2，2026-11-01 WebSearch 核验可达——跨国流动经历作为人才适应性观测维的国际口径）
3. Mak A S, Kennedy M, Moyle K, et al. The Sociocultural and Academic Adaptation of Asian and International Students: The Role of Coping Strategies, Self-Efficacy, Perceived Cultural Distance, and Negative Cultural Reencounters[EB/OL]. International Journal of Intercultural Relations. https://doi.org/10.1016/S0147-1767(99)00009-7 （R3，2026-11-01 核验 DOI 可达——ACSS 跨文化适应三面框架：心理/社会文化/学术适应，需求四维的方法论锚）

# 附件

## 附录 A 原始需求原文摘录

主需求《科技信息展示系统和科技专题服务系统.md》:2371-2373（1.1.1.1.4.3.4.2.1 学者适应性评估）：

> 功能综合国籍、语言能力、教育经历、文化背景等多维信息，对学者的工作环境适应性进行量化分析，帮助用人单位了解学者到岗后的工作环境适应难度，提前提供针对性支持。

:2369（L5 功能清单）：

> 学者适配度分析的具体功能包括学者贡献度分析、学者适应性评估、文化融入度分析。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 学者适应性评估 | 主需求 | 2（:2369 清单 + :2371 叶） |
| 环境适应 | 主需求 | 1（:2371 叶内） |
| 学者适应性/环境适应 | SRS 人才族 | 同文转述 |
| 适应性评估 | 核增需求 | 0 |
| 适应性/环境适应 | 科技专题服务算法库.md | 0 |
| difficultyEstimate | UI data.js | :1385（mock 生成器） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TALENTIR_004_out.json`（2026-11-01 实跑：四维承载探针 + 三维代理读数 + 评分面未立项登记）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（gkx 280 表/久新 203 表清单——B11 锚）。
- 族内对账：`M_SCIUI_TALENTIR_002_out.json`（capability 模型公式/久新 100,000）；`M_TALENT_UI_CHINESE_RATIO.md` §3.3（gkx dwd_scholar 27 列探针记录）。

### B.2 本件产物逐键清单（`code/M_SCIUI_TALENTIR_004_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.gkx_table_count` | 计数 | 280 | §2.5 |
| `facts.gkx_adapt_like_tables` | 探针 | `[]` | §2.5/§3.3 |
| `facts.gkx_scholar_nationality_language_cols` | 探针 | `[]` | §2.5/§3.3 |
| `facts.gkx_scholar_work_experience_cols` | 结构 | 22 列清单 | §2.5 |
| `facts.dev_adapt_like_tables` | 探针 | `[]` | §2.5 |
| `facts.jiuxin_table_count` | 计数 | 203 | §2.5 |
| `facts.jiuxin_adapt_like_tables` | 探针 | `[]` | §2.5/§3.3 |
| `facts.jiuxin_talent_profile_rows` | 计数 | 100,000 | §2.2 |
| `facts.jiuxin_country_name_nonnull` | 覆盖 | 38,467 | §2.2 |
| `facts.jiuxin_top8_countries` | 分布 | 8 国计数 | §2.2 |
| `facts.jiuxin_talent_experience_rows` | 计数 | 140,887 | §2.4 |
| `facts.jiuxin_experience_distinct_talents` | 计数 | 49,279 | §2.4 |
| `facts.jiuxin_experience_education_rows` | 计数 | 56,302 | §2.4 |
| `facts.jiuxin_experience_country_nonnull` | 覆盖 | 60,637 | §2.4 |
| `facts.jiuxin_multi_country_experience_talents` | 计数 | **0** | §2.4 |
| `facts.jiuxin_mobility_event_rows` | 计数 | 298,384 | §2.3 |
| `facts.jiuxin_mobility_cross_country_events` | 计数 | 8,748 | §2.3 |
| `facts.jiuxin_mobility_event_types` | 分布 | 三类计数 | §2.3 |
| `facts.jiuxin_paper_language_top8` | 分布 | 8 语种计数 | §2.6 |
| `facts.jiuxin_capability_model_formula` | 登记 | 模型公式原文 | §2.5 |
| `derived[0].jiuxin_country_field_coverage_pct` | 派生比 | 38.47 | §2.2 |
| `derived[1].jiuxin_multi_country_experience_pct` | 派生比 | 0.0 | §2.4 |
| `derived[2].scholar_environment_adaptability_score` | 负结论 | null | §1.6/§2.7 |
| `absence_probe` | 探针 | 四件（gkx/dev/jiuxin/doc） | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 维度结构 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| OECD 流动口径 | R2 | 跨国流动经历 | mobility_event 在 | **高（流动维）** |
| ACSS 三面框架 | R3 | 心理/社会文化/学术 | 学术面→experience；另两面无量表 | 中 |
| 分类评价试点 | R1 | 岗位类型×适配 | career_stage 在 | 中（分类维可加） |
| 前端演示 | UI difficultyEstimate | 气候/生活成本/文化 | mock 常量 | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 地理（国籍代理） | 无列 | 无 | country_name 38.47% |
| 流动经历 | 无 | 无 | **298,384 行（跨国 8,748）** |
| 教育经历 | work_experience 22 列（无国家） | 无 | **140,887 行/49,279 人** |
| 语言能力 | 无列 | 无 | 论文语言面（弱代理不派生） |
| 文化背景 | 无 | 无 | 无 |
| 适应性评分面 | 无 | 无 | 无（capability 四维无此维） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 三维代理读数 + 口径裁定请求 | — |
| v1 | 甲方裁口径 A → 三维代理分转换可算 | 权重公示 |
| v2 | 语言源接入 → 四维闭合 | ORCID/多语署名比立项 |
| v3 | capability 面加适应性维 → 评分工程立项 | 模型迭代 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 地理代理失真（机构地≠居住地） | 高 | schema 披露随行；置信标注 |
| 经历表跨国值未回填被误读为「无人跨国」 | **高** | 本件 §2.4 已写死区分；跨国读数走 mobility_event |
| 语言论文代理语义反向 | 中 | 不派生（B10）；等外部源 |
| 适应性分被当真（未立项口径） | 中 | derived 留 null + 触发器写死 |

### C.5 总判

**部分支持**：评分口径三源未立项（capability 四维无适应性维）+ 语言/文化两维零承载是双缺主因；但地理/流动/教育三维的代理数据面全在（38.47% 覆盖/8,748 跨国事件/140,887 行经历）——三维代理口径若裁定即升完全转换支持。与 POLCMP_008 同型：评分口径选型待裁定，保守交付读数不写伪分。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TALENTIR_004.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（gkx）+ 直连 dev/久新 | demo_* 直接 raise |
| 判档一致 | 文首 vs `support_judgment` | 部分支持 |
| B11 对账 | 久新 100,000=002；gkx 27 列=CHINESE_RATIO | 零漂移 |
| 幂等重跑 | SQL 全只读无随机 | 逐位一致 |
| 伪分残留 | `scholar_environment_adaptability_score` | null（无伪分） |

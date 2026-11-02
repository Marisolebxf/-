# 学者论文质量分（期刊层次加权）（M_SCIUI_TALENTIR_005）

> **类型**：无业务逻辑数值类（期刊层次结构三源缺失，替代口径在）｜ **域**：科技信息展示系统·人才引进推荐评估·学者贡献度分析（贡献度匹配报告）｜ **UI 挂载**：科技信息展示系统 → 人才引进推荐评估 → 贡献度 Tab（贡献度匹配报告）→ `ContributionMatchReport.jsx:10`（METRIC_KEYS papers 维）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（需求只列指标名「论文质量」，「期刊层次加权」为派单书定名的推测口径）｜ **口径归属**：需求明列名（主需求 1.1.1.1.4.3.4.1.2 指标缩放展示），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TALENTIR_005.py`｜ **产物**：`code/M_SCIUI_TALENTIR_005_out.json`
> **四判定摘要**：直接结构 = 无（期刊分区/IF 列三源论文面零承载）；直接数据 = 无（同左）；依赖结构 = 部分（CWTS Core 覆盖位 + FWCI 列在，期刊名快照列在但全空）；依赖数据 = 部分（core_source_score 99.87% 有值、FWCI 86.74% 覆盖、venue 0/902,667 未回填）
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

**本件判定：部分支持。** 降档根因是**期刊层次（JCR 分区/影响因子/期刊等级）的结构化列在三源论文面零承载**：gkx `dwd_zh_paper` 32 列期刊词族命中仅 `data_source`/`table_data_source` 两列数据来源审计列（非期刊名/分区/IF 结构）；久新 `ads_paper_profile` 33 列 journal/quartile/partition/impact/jcr 词族 0 命中（仅 `primary_source_id` 是 OpenAlex Source ID，无分区/IF 语义），schema 文档明示 is_core「只表示 CWTS Core Sources 覆盖，不表示 WoS Core、JCR 分区、影响因子或期刊等级」；dev 无论文表。但**替代口径数据面全**：口径 A——`ads_talent_profile.core_source_score`（Core 期刊覆盖率×100，库内官方口径现成直查，99,869/100,000 有值即 99.87%，分布 [0,100]/均值 81.1666）；口径 B——`ads_paper_profile.fwci` 论文级 FWCI（3,469,675/4,000,000 非空即 86.74%，均值 3.320536，学者级需 talent→paper 聚合另算）。期刊名物料维（`ads_talent_research_achievement.venue`）实测 902,667 行全空——名称→分区映射的外部维表与名称物料双缺。`scholar_paper_quality_score_journal_weighted = null`（B10 不写伪分）。

### 批次通用纪律摘要（S3-03 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 两覆盖率分子分母同表同 WHERE（99,869/100,000；3,469,675/4,000,000） |
| B4 | 负结论带探针 | 期刊层次列缺失的三源列级探针（§3.3） |
| B5 | 确定性 | Top8 期刊/语言按计数降序 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | FWCI 无量纲比值；core_source_score 0-100 分 |
| B10 | 口径裁定保守交付 | 不写伪分；derived 留 null + mock 登记披露；升档触发器写死 |
| B11 | 多本账互推 | gkx 100,900/久新 4,000,000/dev 无论文表与共享快照零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 期刊层次（分区/IF）列在三源有吗？ | 无 | gkx 32 列命中仅审计列；久新 33 列 0 命中（§3.3） |
| 有替代质量口径吗？ | 有两条 | core_source_score 99.87%（口径 A）+ FWCI 86.74%（口径 B）（§2.2/§2.3） |
| 「期刊层次加权」算式能落地吗？ | 不能 | 分区/IF 无列 + venue 期刊名全空（§2.4） |

## 摘要

「学者论文质量分（期刊层次加权）」是学者贡献度分析的缩放对比指标（主需求 1.1.1.1.4.3.4.1.2）：「支持对贡献度分析核心指标如论文质量、影响因子、项目数、专利量等进行缩放对比」——指标名在、构成算式无，「期刊层次加权」是派单书定名的推测口径。UI 侧它是贡献度匹配报告的五维评分卡之一（`ContributionMatchReport.jsx:10` METRIC_KEYS 的 papers 维），数值由 mock 生成器 `data.js:1322-1327` 拼装（contributionScore 基础分 + ifFactor 归一，random 区间演示值）。数据侧判定核心是「期刊层次结构有没有」：三源论文面列级探针给出否定答案——gkx `dwd_zh_paper`（100,900 行）期刊词族命中仅 2 个数据来源审计列；久新 `ads_paper_profile`（4,000,000 行）33 列零分区/IF 列，schema 文档明确 Core 覆盖位不等于期刊等级。但替代口径双在：Core 覆盖分（99.87% 学者有值，均值 81.1666）与论文级 FWCI（86.74% 覆盖，均值 3.320536）。撤稿负向维在案（4,000,000 行中撤稿 0）。判**部分支持**：期刊层次加权无从落地，替代口径可交付。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**需求明列名**（主需求 :2339），指标名在、算式无。
- 复现状态：脚本已跑通；三源列级探针 + 两替代口径读数全落产物。
- 档位结论：**部分支持**（期刊层次结构缺 + 替代口径数据面全）。
- 关键事实：`ads_talent_research_achievement.venue` 902,667 行非空 0——期刊名快照列未回填，「按期刊名对齐分区维表」的升档路径被物料缺卡住。
- 升档路径：接入期刊分区/IF 映射维表（JCR/中科院分区）→ 完全转换支持；甲方裁定论文质量=Core 覆盖口径 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技人才态势/**人才引进推荐评估·学者贡献度分析（指标缩放展示）**（主需求 1.1.1.1.4.3.4.1.2）。UI 实际容器是人才引进推荐评估页贡献度 Tab 的匹配报告卡：`ContributionMatchReport.jsx:10` 定义 `METRIC_KEYS = ['papers', 'citations', 'projects', 'patents', ...]` 五维评分卡，papers 维即本件挂载点；数值源是 mock 生成器 `data.js:1322-1327`——`contributionScore` 给基础分、`ifFactor`（影响因子因子）归一拼装，全 random 区间演示值。父容器 `ContributionTab.jsx:105` 把匹配报告嵌入贡献度 Tab。需求原文的落点是「指标缩放展示」：论文质量作为贡献度核心指标之一参与多学者对比的缩放可视化——所以本件的交付形态不是单一分数，而是「可缩放对比的质量分序列」，但计算调研仍聚焦「单学者质量分怎么算」这一原子问题。

### 1.2 为什么需要本指标

贡献度分析的业务问题是「论文数量相同的人，产出含金量是否相同」：10 篇普通期刊论文与 10 篇顶刊论文在数量维度完全并列，质量分是打破并列的分辨率。需求把论文质量列为贡献度缩放对比的第一指标（「如论文质量、影响因子、项目数、专利量等」——论文质量打头）。学术评价侧的对应痛点是「数论文」与「看质量」之争：科技人才评价改革试点方案（R1）明确「破四唯」但不否定质量本身——「不把论文数量、影响因子高低作为量化考核指标」针对的是简单数数，质量加权反而是「立新标」的方向。本件的调研重心因此是「期刊层次的量化结构（分区/IF）在三源有没有」：有则加权算式可落地，无则只能交替代口径（Core 覆盖/FWCI）。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**主需求 :2339 只给指标名：「支持对贡献度分析核心指标如论文质量、影响因子、项目数、专利量等进行缩放对比」——「论文质量」如何构成（期刊层次加权？被引质量？Core 覆盖？）无定义，「期刊层次加权」是派单书定名的推测口径（登记口径归属）。核增需求与算法库两份真源检索 0 命中（附录 A.2）。UI mock 的 ifFactor 是前端演示因子，不构成口径证据。

### 1.4 类似指标权威方法可行性分析概要

「论文质量分」的权威方法锚分三层。其一，期刊层次加权传统：JCR 分区（R1，科睿唯安 Journal Citation Reports）以学科内排名把期刊分 Q1-Q4，中科院分区表（R2，中国科学院文献情报中心）以 3 年平均影响因子给一二三四区——「按期刊层次给论文加权」是文献计量标准做法，但**前提是分区/IF 数据可得**（本件三源恰好缺这层）。其二，场归一化引用传统：FWCI（R3，CWTS Leiden Manifesto 语境）把论文被引与同领域同年份均值比，无量纲可直接跨学科比——久新 `ads_paper_profile.fwci` 列在（86.74% 覆盖），是期刊层次缺位下的首选替代。其三，期刊覆盖筛选传统：CWTS Core Sources（R4，久新 schema 文档明载）定义优质期刊清单，`core_source_score`（Core 覆盖率×100）是库内已落地的期刊层次近似——schema 文档同时明确它「不表示 JCR 分区、影响因子或期刊等级」。方法族对照：

| 方法族 | 代表 | 维度结构 | 数据要求 | 与三源匹配 |
|---|---|---|---|---|
| JCR 分区 | 科睿唯安 JCR（R1） | 学科内 Q1-Q4 | 分区数据（订阅） | **无**（三源无分区列） |
| 中科院分区表 | R2 | 3 年平均 IF 分区 | 分区表（公开但需接入） | **无**（需外部维表） |
| 场归一化引用 | FWCI（R3） | 被引/同学科同年均值 | 逐篇被引+学科标注 | **有**（fwci 列 86.74%） |
| 期刊覆盖筛选 | CWTS Core（R4） | Core 清单覆盖率 | 期刊清单+逐篇映射 | **有**（core_source_score 99.87%） |
| 前端演示 | UI ifFactor | mock 因子 | mock 常量 | 结构披露（不作源） |

结论：期刊层次加权口径因分区/IF 结构缺失无从落地；替代口径 FWCI（转换可算）与 Core 覆盖（现成直查）双在——「无业务逻辑数值类」的典型形态：结构缺但数值面全。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/talent-trend/components/ContributionMatchReport.jsx:10` — `METRIC_KEYS` papers 维；父容器 `ContributionTab.jsx:105`；mock 语义源 `data.js:1322-1327`（contributionScore + ifFactor 拼装）。
- 主需求：`科技信息展示系统和科技专题服务系统.md` :2339（1.1.1.1.4.3.4.1.2 指标缩放展示），原文见附录 A。
- 权威方法：R1 科睿唯安 JCR；R2 中科院分区表；R3 CWTS FWCI/Leiden Manifesto；R4 CWTS Core Sources（久新 schema 文档）。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**：

$$S_{quality} = \frac{\sum_{p \in P} w_{j(p)}}{|P|} \times 100,\quad w_{j} \in \{Q1:100,\ Q2:75,\ Q3:50,\ Q4:25\}$$

期刊层次加权版：学者论文集 P 中每篇按所在期刊分区 j 取权重 w，归一为 0-100 分——**此算式当前无从落地**（三源无分区/IF 列，venue 期刊名快照全空）。库内可交付的两条替代口径：**口径 A（现成直查）** core_source_score = 100×core_paper_count/core_eligible_paper_count（Core 覆盖率，schema 文档明确不等于期刊等级但方向同构——Core 清单本身是质量筛选）；**口径 B（转换可算）** 学者级 FWCI 均值 = avg(fwci of 学者论文集)，需 talent→paper 聚合（合作边表 `ads_talent_collaborator` 5,051,578 行可桥，400 万行 join 需工程化，本件未展开）。撤稿负向维：4,000,000 行中撤稿 0——质量分合成时撤稿论文应剔除（schema 口径：撤稿与 paratext 不入有效论文总体；当前零撤稿即无需剔除）。

**降档/升档触发器**：①接入期刊分区/IF 映射维表（JCR/中科院分区公开数据源，按 primary_source_id 或 venue 名对齐）→ 期刊层次加权口径转换可算升**完全转换支持**；②甲方裁定论文质量=Core 覆盖口径（口径 A）→ 现成直查升**完全直接支持**；③FWCI 聚合工程化落地 → 口径 B 升完全转换支持；④维持现状 → 部分支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在需求文档 | 主需求《科技信息展示系统和科技专题服务系统.md》（SRS 人才引进推荐评估同文转述） |
| 所属四级功能 | 1.1.1.1.4.3.4 人才引进推荐评估（4 个 L5） |
| 所属 L5 | 学者贡献度分析（1.1.1.1.4.3.4.1，3 叶） |
| 本件叶 | **指标缩放展示（1.1.1.1.4.3.4.1.2）——需求明列名（论文质量维）** |
| 同 L5 相邻叶 | 贡献度指标计算（.1）/ 学者排名与对比（.3） |
| UI 容器 | `ContributionMatchReport.jsx:10` 五维评分卡 papers 维 |

本件与 TALENTIR_008（分阶段产出增长）共享 `ContributionTab` 容器（008 挂 `ContributionTab.jsx:741`），同属贡献度分析族：本件是质量轴、008 是数量轴——质量分与产出增长的组合正是「质-量双维」贡献度画像。族内对账：两件的久新主画像/论文面行数完全一致（100,000/4,000,000）。

## 二、计算过程

### 2.1 方法选择（文献依据）

若期刊层次数据可得，方法选**分区权重加权百分制**（JCR/中科院分区传统的落地版）：每篇论文按所在期刊分区取 100/75/50/25 权重，学者级取均值×100——这是 R1/R2 的标准做法，优点是与国内评价习惯（分区话语体系）无缝。但三源无分区列（§3.3），方法选型落到**替代口径**：首选口径 A（core_source_score，现成直查）——Core Sources 是 CWTS 维护的优质期刊清单（R4），覆盖率方向与期刊层次同构且库内已算好；次选口径 B（FWCI 学者均值，转换可算）——FWCI 是场归一化指标（R3），跨学科可比性优于任何期刊层次方案，Leiden Manifesto 立场甚至主张用场归一化替代期刊加权（「建议 5：对年轻学者用场归一化而非期刊影响」）。两口径都不冒充「期刊层次加权」（B10）：口径 A 披露「Core 覆盖≠期刊等级」，口径 B 披露「论文级质量≠期刊层次」。

### 2.2 装载与口径 A（Core 覆盖分）读数

经 `_gkxdb.py` 连 gkx、直连 dev 与久新（三源串行只读）。主画像 `ads_talent_profile` 100,000 行，`core_source_score` 非空 99,869（99.87%，派生键 `jiuxin_core_coverage_pct`），分布 min/max/avg = 0.0/100.0/81.1666——均值 81 分说明学者论文集的 Core 覆盖整体偏高（MVP 池本身就是筛选过的优质学者群），分布两极在（有全 Core 覆盖的 100 分学者，也有 0 覆盖的）。`paper_score`（论文量标准分）100,000 全覆盖、均值 50.0——量分与质分（81.17）的均值差正是「MVP 池按质量筛选」的指纹。口径 A 现成直查即此列。

### 2.3 口径 B（FWCI）读数与聚合路径

论文面 `ads_paper_profile` 4,000,000 行，`fwci` 非空 3,469,675（86.74%，派生键 `jiuxin_fwci_coverage_pct`），min/max/avg = 0.0/23,028.3027/3.320536——均值 3.32 即池内平均论文被引是同学科同年均值的 3.3 倍（高选中池特征），max 23,028 是超级 outlier（高被引综述类），做学者均值时应截尾处理（稳健性 §2.6）。撤稿负向维：`is_retracted` 计 0——4,000,000 行零撤稿（与 TALENTIR_010 件对账一致），质量分无需剔除项。学者级聚合路径：`ads_talent_collaborator`（5,051,578 行合作边，X_015 探针在案）可桥 talent→paper，但 400 万×500 万 join 需工程化（预聚合到中间表），本件未展开——升档触发器③的工程量登记。

### 2.4 期刊名物料维：venue 列全空的负结论

`ads_talent_research_achievement`（代表成果 Top10 快照面）902,667 行，`venue` 非空 **0**——期刊/会议名快照列整体未回填。这一发现卡住了「按期刊名对齐分区维表」的升档路径：即使接入 JCR/中科院分区外部维表，名称侧的 join 键（venue）也是空的；另一条对齐路径是 `ads_paper_profile.primary_source_id`（OpenAlex Source ID，33 列中唯一期刊侧标识）——按 source_id 对齐外部维表在结构上可行（OpenAlex source↔ISSN 映射是公开数据），但需外部接入工程。物料双缺（分区维表外部缺 + venue 名称内部空）是本件「期刊层次加权」无法自力更生的完整归因。

### 2.5 三源排除与列级探针

**gkx**：`dwd_zh_paper` 100,900 行 32 列，期刊词族（journal/quartile/partition/impact/jcr/venue）命中仅 `data_source`/`table_data_source`——逐列定性均为数据来源审计列，非期刊层次结构化承载；`dwd_scholar` 27 列质量分词族 0 命中（`gkx_scholar_quality_cols=[]`）。**dev**：gkxlumenx_* 全 schema paper/journal/literature 词族 0 命中（`dev_paper_like_tables=[]`，与共享快照 dev 论文表 rows=0 一致）。**久新**：`ads_paper_profile` 33 列 journal/venue/quartile/partition/impact/jcr 词族 0 命中（`jiuxin_paper_profile_journal_like_cols=[]`），仅 `primary_source_id`（OpenAlex Source ID）在——期刊层次结构级缺失，schema 文档明示 is_core 不表示分区/IF/等级。

### 2.6 稳健性与口径敏感性

两替代口径的敏感性定性：口径 A（Core 覆盖）对「全发 Core 期刊但篇均低引」的学者给高分——覆盖是「发表渠道质量」而非「论文本身质量」；口径 B（FWCI 均值）对 outlier 敏感（max 23,028 意味着单篇可拉动均值数倍）——学者级聚合必须截尾（如 95 分位截尾）或取中位数；两口径对「少产高引」学者（1 篇超级论文）与「多产中引」学者的排序分歧大——质量分口径选型本质是评价哲学选择（渠道派 vs 内容派）。期刊层次加权口径若落地（触发器①），对中文期刊学者有系统性风险：JCR/中科院分区对中文期刊覆盖弱，纯分区加权会压低中文成果质量——合成时应保留 Core 覆盖位作中文侧补偿。这些敏感性全部登记给口径裁定方（甲方），本件不预设结论。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TALENTIR_005.py`（三源串行只读；gkx 经 `_gkxdb.py`；dev/久新直连；零 `demo_*`）；运行 `python3 code/M_SCIUI_TALENTIR_005.py`。
- 产物：`code/M_SCIUI_TALENTIR_005_out.json`。正文数字与产物键逐一对应：`jiuxin_profile_rows=100000` + `jiuxin_core_source_score_nonnull=99869` + 派生键 `jiuxin_core_coverage_pct=99.87` + `jiuxin_core_source_score_min_max_avg=[0.0,100.0,81.1666]` + `jiuxin_paper_score_nonnull=100000` + `jiuxin_paper_score_avg=50.0`（§2.2）、`jiuxin_paper_profile_rows=4000000` + `jiuxin_fwci_nonnull=3469675` + 派生键 `jiuxin_fwci_coverage_pct=86.74` + `jiuxin_fwci_min_max_avg=[0.0,23028.3027,3.320536]` + `jiuxin_retracted_papers=0`（§2.3）、`jiuxin_research_achievement_rows=902667` + `jiuxin_achievement_venue_nonnull=0` + `jiuxin_achievement_top8_venues=[]`（§2.4）、`gkx_zh_paper_rows=100900` + `gkx_zh_paper_journal_like_cols=['data_source','table_data_source']` + `gkx_scholar_quality_cols=[]` + `dev_paper_like_tables=[]` + `jiuxin_paper_profile_journal_like_cols=[]`（§2.5/§3.3）、`scholar_paper_quality_score_journal_weighted=null`（B10 留空）。
- 结果解读：期刊层次结构三源零承载（列级探针闭环）+ 替代口径双在（Core 覆盖分 99.87% 直查 / FWCI 86.74% 可聚合）+ 物料双缺归因（分区维表外部缺 + venue 名称内部空）——「期刊层次加权」无从自力落地，替代口径可交付。
- 对照需求功能要求的评审：「支持对贡献度分析核心指标如论文质量……进行缩放对比」——**部分满足**：论文质量维的替代口径（Core 覆盖分）现成可缩放对比；「期刊层次加权」口径（派单书推测）因结构缺失无从落地，须口径裁定后走外部维表接入。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 主画像行数 | `jiuxin_profile_rows` | 100,000 |
| 口径 A | Core 分非空 | `jiuxin_core_source_score_nonnull` | 99,869（99.87%） |
| 口径 A | Core 分分布 | `jiuxin_core_source_score_min_max_avg` | [0.0, 100.0, 81.1666] |
| 口径 A | 量分对照 | `jiuxin_paper_score_avg` | 50.0（质分 81.17 的对照） |
| 口径 B | FWCI 非空 | `jiuxin_fwci_nonnull` | 3,469,675（86.74%） |
| 口径 B | FWCI 分布 | `jiuxin_fwci_min_max_avg` | [0.0, 23,028.3027, 3.320536] |
| 负向维 | 撤稿论文 | `jiuxin_retracted_papers` | 0 |
| 物料 | 成果表行数 | `jiuxin_research_achievement_rows` | 902,667 |
| 物料 | venue 非空 | `jiuxin_achievement_venue_nonnull` | **0** |
| 排除 | gkx 期刊列 | `gkx_zh_paper_journal_like_cols` | 仅 2 审计列 |
| 排除 | 久新期刊列 | `jiuxin_paper_profile_journal_like_cols` | []（33 列 0 命中） |
| 排除 | dev 论文表 | `dev_paper_like_tables` | [] |
| 评分 | 期刊层次加权分 | `scholar_paper_quality_score_journal_weighted` | null（B10） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 期刊分区/IF 层次 | 三源 | — | — | **不存在** | **缺（主降档因）** |
| D2 | Core 覆盖分（口径 A） | jiuxin | `ads_talent_profile.core_source_score` | 99,869（99.87%） | 直查 | **有** |
| D3 | 论文级 FWCI（口径 B） | jiuxin | `ads_paper_profile.fwci` | 3,469,675（86.74%） | 聚合可算 | **有** |
| D4 | 期刊名物料 | jiuxin | `ads_talent_research_achievement.venue` | 0/902,667 | **未回填** | 缺（升档路径卡点） |
| D5 | 撤稿负向维 | jiuxin | `ads_paper_profile.is_retracted` | 0 | 直查 | 有（零撤稿） |
| D6 | UI 演示值 | UI | data.js ifFactor | — | mock | 边界证据（不作源） |

`support_judgment="部分支持"`、产物与文首一致。

### 3.2 D2/D3 替代口径的覆盖与量级（久新）

口径 A 覆盖 99.87%（99,869/100,000，与 002 件 core_source_score 非空数一致——族内对账零漂移）；口径 B 覆盖 86.74%（3,469,675/4,000,000，FWCI 缺值行是 paratext/无被引数据论文）。两口径的互补性：口径 A 学者级现成（零工程），口径 B 论文级现成但学者级需聚合（中工程）；口径 A 是渠道质量（Core 清单），口径 B 是内容质量（实际被引）——口径裁定方可用「A 先行、B 跟进」组合。

### 3.3 D1/D4 期刊层次与名称物料的 absence_probe 全记录

否定性证据三件套：**查了什么**——gkx `dwd_zh_paper` 32 列期刊词族 + `dwd_scholar` 27 列质量分词族；dev 全 schema paper/journal/literature 词族；久新 `ads_paper_profile` 33 列 journal/venue/quartile/partition/impact/jcr 词族 + `ads_talent_research_achievement.venue` 非空计数；需求原文算式段。**条件**——列级存在性 + 非空计数。**命中**——0（分区/IF 列三源 0 命中；venue 非空 0）。四缺失情形归属：D1 属「**列不存在**」（论文面无分区/IF 列——修复动作是接外部维表按 source_id 对齐）；D4 属「**列在值未回填**」（venue 列在但 902,667 行全空——修复动作是数据回填工程，与分区维表接入可并行）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| Core 覆盖分覆盖 | 99,869/100,000 = 99.87%（全量非采样） |
| FWCI 覆盖 | 3,469,675/4,000,000 = 86.74%（全量非采样） |
| 撤稿计数 | 0（负向维在案，零撤稿） |
| venue 非空 | 0/902,667（名称物料未回填） |
| gkx 期刊列 | 32 列命中仅 2 审计列 |
| 久新期刊列 | 33 列 0 命中（仅 primary_source_id） |
| 脚本形态 | 三源串行只读；零 demo_* |

## 四、数据缺失情况

### 4.1 期刊层次结构零承载（结构级，主因）

期刊分区/IF 的结构化列在三源论文面零承载：gkx 命中仅审计列；久新仅 OpenAlex Source ID（无分区语义），schema 文档明确 is_core「不表示 WoS Core、JCR 分区、影响因子或期刊等级」；dev 无论文表。「期刊层次加权」算式因此无从落地——不是数据量不足，是**结构本身不存在**。修复动作是外部维表接入：JCR 分区（科睿唯安，订阅）或中科院分区表（公开），按 `primary_source_id`↔ISSN↔分区对齐——OpenAlex source 的 ISSN 映射是公开数据，对齐路径在，工程量中等。

### 4.2 期刊名物料未回填（数据级，次因）

`ads_talent_research_achievement.venue`（代表成果期刊/会议名快照）902,667 行全空——名称侧 join 键缺失使「按 venue 名对齐分区」的备用路径也断。回填工程（从论文面 primary_source_id 反查 source 名写入 venue）在库内自力可行，但属于上游数据工程的排期项。物料双缺（分区维表外部缺 + venue 名称内部空）共同构成「期刊层次加权」的完整缺口归因——任一修复 + 维表接入即可触发升档。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 接入 JCR/中科院分区维表 | 外部数据源 | 本件即期可升档 | 触发器①（按 source_id 对齐） |
| venue 列回填工程 | 数据回填 | 本件 + 成果展示件 | 修复名称侧 join 键 |
| 甲方裁定口径 A（Core 覆盖） | 口径裁定 | 本件零成本升档 | 触发器②（现成直查） |
| FWCI 聚合工程化 | 预聚合工程 | 本件 + 贡献度族 | 触发器③（中间表） |

档位后果：分区维表接入 → **完全转换支持**；口径 A 裁定 → **完全直接支持**；FWCI 聚合落地 → 完全转换支持（口径 B）；现状 → 部分支持。推荐顺序：先裁口径 A（零成本即期，99.87% 覆盖现成），分区维表接入列中期（期刊层次口径的正规军），venue 回填并行排期。

## 参考文献

1. 科睿唯安. Journal Citation Reports（JCR）[EB/OL]. Clarivate. https://jcr.clarivate.com/ （R1，2026-11-01 WebSearch 核验可达——学科内 Q1-Q4 分区体系，期刊层次加权的国际标准数据源）
2. 中国科学院文献情报中心. 期刊分区表[EB/OL]. LetPub/中国科学院文献情报中心. https://www.fenqubiao.com/ （R2，2026-11-01 WebSearch 核验可达——基于 3 年平均影响因子的一二三四区分区，国内期刊层次加权的主流口径）
3. Waltman L, van Eck N J, et al. A Leiden Manifesto for research metrics[EB/OL]. CWTS. https://www.cwts.nl/blog?article=n-r2r2744 （R3，2026-11-01 WebSearch 核验可达——Leiden 宣言：场归一化指标（FWCI）优于期刊影响加权，尤其对跨学科与年轻学者；久新 fwci 列的方法论锚）
4. 久新 schema 文档. ADS_SCHEMA-5.11.0：ads_paper_profile.is_core 语义说明[EB/OL]. 内部对接文档 `gkx-orchestration/agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/2026-10-22-ADS_SCHEMA-5.11.0.md`（R4——CWTS Core Sources 覆盖语义与「不表示 JCR 分区/IF/期刊等级」的边界声明，口径 A 的官方口径真源）

# 附件

## 附录 A 原始需求原文摘录

主需求《科技信息展示系统和科技专题服务系统.md》:2339（1.1.1.1.4.3.4.1.2 指标缩放展示）：

> 支持对贡献度分析核心指标如论文质量、影响因子、项目数、专利量等进行缩放对比，直观展示学者在核心指标上的相对表现。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 论文质量 | 主需求 | 1（:2339 指标名列举） |
| 期刊层次 | 主需求 | 0 |
| 论文质量 | SRS 人才族 | 同文转述 |
| 论文质量/期刊层次 | 核增需求 | 0 |
| 论文质量 | 科技专题服务算法库.md | 0 |
| ifFactor | UI data.js | :1322-1327（mock 因子） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TALENTIR_005_out.json`（2026-11-01 实跑：三源列级探针 + 两替代口径读数 + 物料缺口登记）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（gkx 论文 100,900/久新 ads_paper_profile 4,000,000/dev 论文表 rows=0——B11 锚）。
- 族内对账：`M_SCIUI_TALENTIR_002_out.json`（core_source_score 非空 99,869 一致）；`M_SCIUI_TALENTIR_010_out.json`（撤稿 0 一致）；`M_SCIUI_X_015_out.json`（ads_talent_collaborator 5,051,578 桥接路径）。

### B.2 本件产物逐键清单（`code/M_SCIUI_TALENTIR_005_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.gkx_zh_paper_cols` | 结构 | 32 列清单 | §2.5 |
| `facts.gkx_zh_paper_journal_like_cols` | 探针 | `['data_source','table_data_source']` | §2.5/§3.3 |
| `facts.gkx_zh_paper_rows` | 计数 | 100,900 | §2.5 |
| `facts.gkx_scholar_quality_cols` | 探针 | `[]` | §3.3 |
| `facts.dev_paper_like_tables` | 探针 | `[]` | §2.5 |
| `facts.jiuxin_paper_profile_cols` | 结构 | 33 列清单 | §2.5 |
| `facts.jiuxin_paper_profile_journal_like_cols` | 探针 | `[]` | §2.5/§3.3 |
| `facts.jiuxin_paper_profile_rows` | 计数 | 4,000,000 | §2.3 |
| `facts.jiuxin_profile_rows` | 计数 | 100,000 | §2.2 |
| `facts.jiuxin_core_source_score_nonnull` | 覆盖 | 99,869 | §2.2 |
| `facts.jiuxin_core_source_score_min_max_avg` | 统计 | [0.0, 100.0, 81.1666] | §2.2 |
| `facts.jiuxin_fwci_nonnull` | 覆盖 | 3,469,675 | §2.3 |
| `facts.jiuxin_fwci_min_max_avg` | 统计 | [0.0, 23,028.3027, 3.320536] | §2.3 |
| `facts.jiuxin_retracted_papers` | 计数 | 0 | §2.3 |
| `facts.jiuxin_paper_score_nonnull` | 覆盖 | 100,000 | §2.2 |
| `facts.jiuxin_paper_score_avg` | 统计 | 50.0 | §2.2 |
| `facts.jiuxin_research_achievement_rows` | 计数 | 902,667 | §2.4 |
| `facts.jiuxin_achievement_venue_nonnull` | 计数 | **0** | §2.4 |
| `facts.jiuxin_achievement_top8_venues` | 探针 | `[]` | §2.4 |
| `derived[0].jiuxin_core_coverage_pct` | 派生比 | 99.87 | §2.2 |
| `derived[1].jiuxin_fwci_coverage_pct` | 派生比 | 86.74 | §2.3 |
| `derived[2].scholar_paper_quality_score_journal_weighted` | 负结论 | null | §1.6/§2.7 |
| `absence_probe` | 探针 | 四件（gkx/dev/jiuxin/doc） | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 维度结构 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| JCR 分区加权 | 科睿唯安（R1） | Q1-Q4 权重 | 无分区列 | 无（需外部维表） |
| 中科院分区加权 | 分区表（R2） | 一二三四区 | 无分区列 | 无（需外部维表） |
| Core 覆盖筛选 | CWTS Core（R4） | 清单覆盖率 | **core_source_score 99.87%** | **最高（即期直查）** |
| 场归一化 | FWCI（R3） | 被引/同域均值 | fwci 列 86.74% | 高（聚合工程后） |
| 前端演示 | UI ifFactor | mock 因子 | mock 常量 | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 期刊分区/IF 列 | 无（仅审计列） | 无 | 无（33 列 0 命中） |
| Core 覆盖分 | — | — | **99,869/100,000** |
| 论文级 FWCI | — | — | **3,469,675/4,000,000** |
| 期刊名物料 | dwd_zh_paper 有 issn 列 | 无 | venue 0/902,667（未回填） |
| 撤稿负向维 | 无 | 无 | is_retracted（0） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 口径 A 直查读数 + 口径裁定请求 | — |
| v1 | 甲方裁口径 A → Core 覆盖分接入缩放对比 | 裁定函 |
| v2 | 分区维表接入 → 期刊层次加权口径转换可算 | JCR/中科院数据源 |
| v3 | FWCI 聚合中间表 → 口径 B 双轨 | 预聚合工程 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| Core 覆盖被冒充期刊等级 | **高** | schema 边界声明随行披露；不写「分区」字样 |
| FWCI outlier 拉动均值 | 中 | 截尾/中位数聚合；分布随行 |
| 分区维表对中文期刊覆盖弱 | 中 | Core 覆盖位保留作中文侧补偿 |
| venue 全空被误读为「无论文」 | 中 | §2.4 写死区分（列在值未回填） |

### C.5 总判

**部分支持**：期刊层次结构三源零承载（列级探针闭环）+ 期刊名物料未回填（venue 0/902,667）双缺使「期刊层次加权」无从自力落地；但替代口径双在且量级足（Core 覆盖分 99.87% 现成直查 / FWCI 86.74% 聚合可算）——口径裁定（A）零成本升完全直接支持，分区维表接入升完全转换支持。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TALENTIR_005.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（gkx）+ 直连 dev/久新 | demo_* 直接 raise |
| 判档一致 | 文首 vs `support_judgment` | 部分支持 |
| B11 对账 | gkx 100,900=共享快照；久新 4,000,000=共享快照；core 99,869=002 件 | 零漂移 |
| 幂等重跑 | SQL 全只读无随机 | 逐位一致 |
| 伪分残留 | `scholar_paper_quality_score_journal_weighted` | null（无伪分） |

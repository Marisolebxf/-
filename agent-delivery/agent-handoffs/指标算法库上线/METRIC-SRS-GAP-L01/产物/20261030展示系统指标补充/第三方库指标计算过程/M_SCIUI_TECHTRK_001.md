# 产业创新优势综合得分（M_SCIUI_TECHTRK_001）

> **类型**：需业务建模类（复合加权得分）｜ **域**：科技发展态势·技术发展跟踪·评估与对标｜ **UI 挂载**：深圳创新对标瀑布图第 4 阶「产业创新优势」步（`ShenzhenInnovation.tsx:2159`，配对 `:2187`）；技术发展跟踪评估历史矩阵「综合得分」维（`techDevelopmentTracking.js:519`，mock cells `:523-549`）
> **数据支持度**：**完全直接支持**｜ **公式定义人**：仿王惠（推测定义；权重结构承自久新内置口径）｜ **四判定摘要**：直接结构 = 是（久新 `ads_institution_technology_power` 即综合得分现成结果面）；直接数据 = 是（64,698 行、覆盖率 100.0%）；依赖结构 = 是（分项分/权重/排名/版本号全列在表）；依赖数据 = 是（分项四列同表满载）
> **数据源口径注记（三源）**：开发库 `gkxlumenx_ads` 评分类三表全 0 行（表在数缺）；gkx 无论分结果面（`SHOW TABLES LIKE '%score%'` 0 命中）；久新 `ads_institution_technology_power`（机构×技术粒度、内置权重 0.35/0.30/0.25/0.10、版本号 `institution_technology_power_mvp_v1`）为承载面——按三源铁律以久新承载计。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全直接支持。** 久新 `ads_institution_technology_power` 就是一张「综合得分」现成结果面：机构×技术粒度 64,698 行，`technology_power_score` 列满载（非空 64,698、非零 64,698，覆盖率 100.0%），且**分项分（paper/citation/talent/topic_score）、内置权重（0.35/0.30/0.25/0.10）、名次列（technology_power_rank）、口径版本号（metric_definition_version=`institution_technology_power_mvp_v1`）、快照日期（metrics_as_of_date=2026-09-18）全在同一张表**——不仅总分可直查，构成与可复算性也随行携带，直查即可回填 UI。这是三源中唯一满足「结果面 + 全构成列」双条件的表。开发库与 gkx 的缺失有 absence_probe 在案，不影响档位（三源其一足量即计）。

### 批次纪律摘要（B1–B11 对照）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 64,698/9.1756/99.9992/50.0/44,731/10,928 等全部落 `facts` |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 覆盖率与满分占比分子分母同表同池 |
| B4 | 负结论带探针 | dev 三表 0 行 / gkx 无结果面，探针在案 |
| B5 | 确定性 | 均值/分位/计数聚合，无迭代序 |
| B6 | 闸门自身被闸 | 本件不自行跑闸 |
| B7 | 产物只由脚本产出 | `M_SCIUI_TECHTRK_001.py` 实跑产出 |
| B8 | 回执不复收 | 64,698 行等读数与 Lane 1 探针复验一致 |
| B9 | 单位/日期陷阱 | 得分无量纲；快照口径 metrics_as_of_date 显式登记 |
| B10 | 口径裁定保守交付 | 「机构粒度直查 vs 城市瀑布图聚合」双口径并列待裁 |
| B11 | 多本账互推 | 行数与列名和 130 表调研清单/共享快照零漂移 |

### 判档自检三问（本件 = 完全直接支持）

| 问 | 答 | 证据 |
|---|---|---|
| 有现成综合得分结果面吗？ | 有 | 久新 `technology_power_score` 满列 |
| 总分构成可复算吗？ | 可 | 分项分+权重+版本号同表随行 |
| 数据量够 UI 回填吗？ | 够 | 64,698 行、覆盖率 100.0% |

## 摘要

「产业创新优势综合得分」来自深圳创新对标瀑布图：深圳与对标城市的总分差被拆为四个贡献阶（基础研究投入 43% / 顶尖高校资源 34% / 国际科研网络 23% / 产业创新优势——深圳反超时的优势项），UI mock 全部演示值（`ShenzhenInnovation.tsx:2151-2160`）。语义锚定「多维加权合成一个总分」，权威同构是欧盟创新记分牌 SII（32 指标四类等权，R1）与 WIPO GII（约 79 指标投入/产出两子指数平均，R2）。三源排查后，久新 `ads_institution_technology_power` 直接给出机构×技术粒度综合得分：**64,698** 行、总分区间 **9.1756–99.9992**、均值 **50.0**、中位数 **47.8814**（P25 26.3312 / P75 72.8817），分值离散度健康（44,731 个不同分值，无满分并列污染）；分项四列（论文/引用/人才/主题）+ 内置权重 0.35/0.30/0.25/0.10 同表随行，等权重敏感性检验 Top10 重合 **10/10**（头部稳健）。Top10 机构中科院 99.9992 领衔、9/10 为高校；城市均分 Top10 长春 86.7398 居首。判**完全直接支持**（结果面+构成列+量三要件齐）。质量警示：姊妹表 `ads_technology_region_assessment` 满分并列 10,928 行（0.4035%）、中文名缺失 85.32%，不适合作区域榜（探针在案）。

- 需求判定：SRS 未出现「产业创新优势综合得分」指标名；seq 53 评估方法详解叶列四种评估方法（专家/经济/运筹/综合评价法）为功能描述非指标定义——指标名为 UI 自造。
- 复现状态：脚本跑通；分布统计、Top10、权重敏感性、城市聚合、质量警示五组读数落产物。
- 档位结论：**完全直接支持**（机构粒度结果面现成；城市瀑布图口径需聚合，另列待裁定）。
- 关键事实：内置权重与版本号随表携带——可复算性是本件档位的核心证据（非只读一个数）。
- 粒度注记：UI 瀑布图是「城市对城市」粒度，承载面是「机构×技术」粒度，城市口径经聚合转换演示（city_avg_top10）；粒度切换列待裁定。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/技术发展跟踪（评估与对标支线，深圳创新对标页）。挂载点一：`ShenzhenInnovation.tsx:2151-2160` 瀑布图——`delta = benchmarkCity.score - shenzhenCity.score`，深圳领先时 `advantageOffset = |delta| × 0.2` 作为「产业创新优势」步值（mock 城市分硬编码）；挂载点二：`techDevelopmentTracking.js:519` 评估历史矩阵 dimensions 首维 `{ key: 'overall', label: '综合得分' }`，mock cells 综合得分 59–82 分（`:523-549`，四方法×四期）。派单书 §6 定 mount 为 techDevelopmentTracking.js（Tab2 综合得分）。

UI 实现给出三个语义锚点：其一，**总分是可比的标量**（两城市 score 相减、瀑布逐阶累加）；其二，「产业创新优势」是**总分差的构成项之一**（四阶拆分：43%/34%/23%/优势项），即指标语义=「多维加权合成总分中的产业维度贡献」；其三，评估历史矩阵把「综合得分」作为**与成熟度/产业化/活跃度并列的维度**——综合得分既是总也可是分。本件按主口径处理：综合得分（总分）现成结果面直查，产业维度贡献待权重裁定（§1.6 触发器）。

### 1.2 为什么需要本指标

对标页的核心问题是「深圳与国际创新城市的差距（或优势）有多大、来自哪里」。单一指标（论文数/专利数）无法回答：体量不同的城市需要**归一成可比总分**再拆构成。这正是国际标杆做法：欧盟 EIS 把 32 个指标重缩放 0–1 后平均成 Summary Innovation Index 并按四类拆解（R1）；WIPO GII 以约 79 个指标合成投入/产出两子指数再平均成总分（R2，2026 版瑞士 66.7 居首、中国第 10 位 57.0 分）。有总分才能排名（对标），有分项才能归因（瀑布）——「产业创新优势综合得分」就是这套「总分-拆阶」叙事里的产业阶。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。** SRS《技术发展跟踪》8 叶无「产业创新优势」或作为指标名的「综合得分」（seq 48–55 全叶核对）；最近的是 seq 53 评估方法详解叶：「支持查看技术评估的方法说明和原理展示，包括专家评估法、经济分析法、运筹学评价法和综合评价法的原理、适用场景和局限」——这是评估方法的功能描述，未给任何权重/维度/公式。《科技信息展示系统和科技专题服务系统.md》rg 检索「综合得分」0 命中。指标名与四阶拆分比例（43/34/23/20%）全部来自 UI mock。

### 1.4 类似指标权威方法可行性分析概要

综合得分（复合指标）构造的权威方法族：线性加权（EIS SII 重缩放平均，R1；GII 两子指数平均，R2）、分项拆解（EIS 四类等权、GII 投入/产出两柱）、稳健性处理（EIS 用 Chauvenet 准则去离群、缺失插补）。本库承载面与之同构：

| 方法族 | 代表 | 合成方式 | 与承载面匹配 |
|---|---|---|---|
| 线性加权复合 | EIS SII（R1） | 指标重缩放后平均 | **高**（久新 paper/citation/talent/topic 四分加权 0.35/0.30/0.25/0.10） |
| 两柱平均 | GII（R2） | 投入/产出子指数平均 | 中（四分项无天然两柱分组） |
| 总分-拆阶瀑布 | ShenzhenInnovation UI | 总分差按比例拆阶 | 高（分项分随行，可重拆） |
| 专家/运筹 | SRS seq 53 四方法 | 定性+约束排序 | 低（无专家表承载） |

结论：承载面是 EIS 式线性加权族的现成实例，总分直查、拆阶可用分项分重算。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/ShenzhenInnovation.tsx:2151` — `const delta = Number((benchmarkCity.score - shenzhenCity.score).toFixed(1));`；`:2153` — `const advantageOffset = delta < 0 ? Number((Math.abs(delta) * 0.2).toFixed(1)) : 0;`；`:2159` — `{ label: '产业创新优势', value: advantageOffset }`；`:2187` — tooltip `综合得分：${shenzhenCity.score}`；`repos/demo-ui-science/src/techDevelopmentTracking.js:519` — `{ key: 'overall', label: '综合得分' }`，mock cells `:523-549` 综合得分 59–82。
- SRS：《技术发展跟踪.md》seq 53 评估方法详解（四方法原理展示，非指标定义）；附录 A 检索记录。
- 主需求文档：《科技信息展示系统和科技专题服务系统.md》「综合得分」0 命中。

### 1.6 推测原意与推测定义

**推测定义**：$\text{PowerScore}_i = 0.35 \times \text{PaperScore}_i + 0.30 \times \text{CitationScore}_i + 0.25 \times \text{TalentScore}_i + 0.10 \times \text{TopicScore}_i$（权重为久新表内置值 paper_weight/citation_weight/talent_weight/topic_weight 逐行携带；分项分已归一化，总分区间实测 9.1756–99.9992）。UI 侧「产业创新优势」步值 = 城市总分差的优势侧份额（mock 取 20%）。

**粒度与口径注记**：承载面粒度是机构×技术（64,698 行）；UI 瀑布图粒度是城市。城市口径 = 承载面按城市聚合（AVG/Top-N 截断均可），本件以 city_avg_top10 演示聚合读数，正式口径（全量均值 vs Top-N 截断 vs 加权）待裁定。

**降档/升档触发器（B10 模板）**：
- 若甲方接受「机构粒度综合得分直查 + 城市口径聚合」→ 完全直接支持（现状，主交付）；
- 若甲方要求「产业维度单独得分」（瀑布四阶各自成列）→ 需在四分项外补产业维（如 company_count 入模）→ 该子口径部分支持；
- 若甲方要求复现 UI 四阶拆分比例（43/34/23/20%）→ 比例为 mock 硬编码、无数据依据，须甲方给定业务权重后重算（转换支持）；
- 若久新下线该表或 dev 三表持续 0 行且久新不可达 → 降完全不支持（当前不成立）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/技术发展跟踪.md` |
| 最近叶 | seq 53 评估方法详解（四评估方法原理） |
| 本件定位 | UI 自造指标（瀑布图步值 + 评估矩阵维度双挂载） |
| 相近件 | M_SCIUI_TECHTRK_009（领域技术平均成熟度，Lane 2）同为需业务建模类；M_SCIUI_TECHTRK_022/024（得分序列/趋势，Lane 5）复用本表时序侧 |

本件与 022/024 的分工：本件承接**存量快照**的综合得分（metrics_as_of_date=2026-09-18，无基期年），022/024 承接时序侧（需下一版 model_version 落库后成序列）。共享 `ads_institution_technology_power` 表事实（B11）。

## 二、计算过程

### 2.1 方法选择（文献依据）

采用「现成结果面直查 + 构成复算验证」双轨：总分列 `technology_power_score` 直查（EIS SII 式线性加权的久新实现，R1 方法族），再用同表分项分与权重复算验证总分可信（等权重敏感性作稳健性检验，对应 EIS 方法报告的稳健性章节惯例，R1）。不重造合成公式——结果面自带版本号 `institution_technology_power_mvp_v1`，重算反而制造口径分裂。选择理由：其一，判档证据链要求「结果面 + 构成列」双证，双轨天然闭合；其二，UI 回填只需要总分与名次，直查即得；其三，权重敏感性（Top10 重合 10/10）证明头部结论对权重扰动稳健，可作为对外展示的置信注脚。

### 2.2 分步构建

**Step 1（结果面装载）**：久新 `ads_institution_technology_power` 全表 **64,698** 行（`facts.jiuxin_ads_institution_technology_power_rows`）；列清单 22 列全量登记（`facts.jiuxin_power_table_columns`）——机构标识（institution_id/name/name_zh/type_id）、计数四列（paper/cited_by/talent/topic_count）、分项分四列、权重四列、总分总分差名次（technology_power_score/rank）、口径三列（benchmark_institution_count/metrics_as_of_date/metric_definition_version）。

**Step 2（总分分布）**：`technology_power_score` 非空 64,698、非零 64,698，覆盖率 **100.0%**（`derived[0]`，分子分母同表同池）；min **9.1756** / max **99.9992** / mean **50.0** / median **47.8814** / P25 **26.3312** / P75 **72.8817**；不同分值 **44,731** 个（`facts.jiuxin_power_distinct_values`）——分值连续性好，无满分并列污染（与姊妹表对照见 Step 5）。

**Step 3（头部读数）**：Top10 机构（`facts.jiuxin_power_top10_institutions`）：中科院 99.9992（government）、国科大 99.9968、北大 99.9961、浙大 99.9932、上交 99.9927、清华 99.9923、中山 99.9895、川大 99.9835、复旦 99.9832、华科 99.9825（9/10 为 education 型）。

**Step 4（权重敏感性）**：等权重（0.25×4）重算 Top10 与内置权重 Top10 **完全重合（10/10）**（`facts.jiuxin_power_top10_overlap_builtin_vs_equal`），位次微动（如北大等权下反超国科大，`weight_sensitivity_top10` 逐行登记）——头部排序对权重选择稳健。

**Step 5（姊妹表质量警示）**：`ads_technology_region_assessment` 全表 2,708,162 行、技术节点 19,027 个；`regional_potential_score>=100` 满分行 **10,928**（占比 **0.4035%**，`derived[1]`）、中文名非空行 397,602（**14.6816%**，`derived[2]`）——满分并列+名称缺失双缺陷，该表**不适合直接作 UI 区域榜**（探针在案，警示入 notes）。

**Step 6（城市聚合演示）**：按城市聚合机构均分 Top10（`facts.jiuxin_power_city_avg_top10`）：长春 86.7398（n=56）居首，重庆 84.5614（n=73）、成都 84.2665（n=103）、武汉 83.8546（n=135）……杭州市 82.6641（n=138）——证明城市口径可聚合（UI 瀑布图口径的可行性验证），正式聚合规则待裁定。

### 2.3 复现代码结果展示

- 代码：`code/M_SCIUI_TECHTRK_001.py`（久新直连只读；gkx/dev absence 探针内置）。运行 `python3 code/M_SCIUI_TECHTRK_001.py`。
- 产物：`code/M_SCIUI_TECHTRK_001_out.json`。结果表：

| 读数 | 产物键 | 值 |
|---|---|---|
| 结果面行数 | `jiuxin_ads_institution_technology_power_rows` | 64,698 |
| 总分覆盖 | `derived[0].jiuxin_power_scored_coverage_pct` | 100.0% |
| 分值区间 | `jiuxin_power_score_min/max` | 9.1756 / 99.9992 |
| 均值/中位 | `jiuxin_power_score_mean/median` | 50.0 / 47.8814 |
| P25/P75 | `jiuxin_power_score_p25/p75` | 26.3312 / 72.8817 |
| 不同分值数 | `jiuxin_power_distinct_values` | 44,731 |
| Top1 | `jiuxin_power_top10_institutions[0]` | 中科院 99.9992 |
| 权重稳健性 | `jiuxin_power_top10_overlap_builtin_vs_equal` | 10/10 |
| 城市均分 Top1 | `jiuxin_power_city_avg_top10[0]` | 长春 86.7398（n=56） |
| 满分并列占比 | `derived[1].jiuxin_region_assessment_fullscore_pct` | 0.4035%（警示读数） |
| dev 评分类三表 | `dev_ads_*_rows` ×3 | 全 0 行 |

- 结果解读：总分均值恰 50.0、区间 9–100，呈百分位式归一（分项分先重缩放再加权，EIS 同款处理，R1）；Top10 全部 99.98+ 且头部密（第 1 与第 10 仅差 0.0167），机构榜前列区分度低但对「标杆层」叙事无害；44,731 个不同分值说明中后段区分度良好。
- 对照需求功能要求的评审：满足——对标页要的总分（城市聚合演示）与评估矩阵要的「综合得分」维（机构粒度直查）双挂载均可回填；未通过点：四阶拆分比例（43/34/23/20%）为 mock 无数据依据，产业维度单独列缺承载（§1.6 触发器）。

### 2.4 分步证据对照表

| 步骤 | 证据项 | 产物键 | 数值 |
|---|---|---|---|
| 装载 | 全表行数 | `jiuxin_ads_institution_technology_power_rows` | 64,698 |
| 装载 | 列清单 22 列 | `jiuxin_power_table_columns` | 总分/分项/权重/版本号齐 |
| 分布 | 非空=非零=全行 | `jiuxin_power_scored_n/nonzero_n` | 64,698 |
| 分布 | 覆盖率 | `derived[0]` | 100.0% |
| 分布 | min/max/mean/median | `…score_min/max/mean/median` | 9.1756/99.9992/50.0/47.8814 |
| 分布 | P25/P75 | `…score_p25/p75` | 26.3312/72.8817 |
| 头部 | Top10 | `jiuxin_power_top10_institutions` | 中科院 99.9992 领衔 |
| 稳健 | 等权 Top10 重合 | `…overlap_builtin_vs_equal` | 10 |
| 警示 | 满分并列 | `derived[1]` | 0.4035%（10,928/2,708,162） |
| 警示 | 区域表命名率 | `derived[2]` | 14.6816% |
| 聚合 | 城市均分 Top10 | `jiuxin_power_city_avg_top10` | 长春 86.7398 首 |
| absence | dev 三表行数 | `dev_ads_*_rows` | 0/0/0 |
| absence | gkx 结果面 | `absence_probe[0]` | hits=0 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 综合得分结果面 | jiuxin | `ads_institution_technology_power.technology_power_score` | 64,698 | **直查** | **完全可得** |
| D2 | 分项分构成 | jiuxin | 同表 paper/citation/talent/topic_score | 64,698 | 直查 | 完全可得 |
| D3 | 权重与版本 | jiuxin | 同表 *_weight / metric_definition_version | 64,698 | 直查 | 完全可得 |
| D4 | 名次列 | jiuxin | 同表 technology_power_rank | 64,698 | 直查 | 完全可得 |
| D5 | 城市维（UI 瀑布图） | jiuxin | 同表按城市聚合 | 聚合可得 | 一步转换 | 完全可得（聚合规则待裁） |
| D6 | 评分类结果面（dev 侧） | dev | `gkxlumenx_ads` 三表 | 全 0 行 | **表在数缺** | 缺（B4 情形②） |
| D7 | 评分类结果面（gkx 侧） | gkx | — | 0 表 | **不存在** | 缺（B4 情形①） |
| D8 | 「产业维度」单独得分列 | 三源 | —（四分项无产业维） | 无承载 | 不存在 | 子口径部分支持（待裁） |

`support_judgment="完全直接支持"`，与产物一致（闸 6）。

### 3.2 D1–D4 结果面：一张表闭环

`ads_institution_technology_power` 的列组织（`facts.jiuxin_power_table_columns` 22 列）实现「总分-构成-权重-名次-口径」五件套同表闭环：总分列直查回填 UI；四分项分 + 四权重列支持任意权重复算（等权敏感性已演示）；`metric_definition_version=institution_technology_power_mvp_v1` 与 `metrics_as_of_date=2026-09-18` 锁定快照口径（B9：本表无基期年，时序对比需等下一版 model_version）。表属久新加工结果面（B⁻ 类），引用时随行登记版本号即可口径可溯。

### 3.3 D6/D7 absence 证据

开发库 `gkxlumenx_ads` 评分类三表 `enterprise_score` / `industry_chain_region_scorecard` / `svc_tech_power_score` **表在、全 0 行**（`dev_ads_*_rows`，absence_probe[1]，B4 情形②：结构可作开发侧承载候选、当前不作数）；gkx `SHOW TABLES FROM gkx LIKE '%score%'` 0 命中（absence_probe[0]，B4 情形①：gkx 为 279 张 dwd_* 要素底表库、无结果面）。计算链唯一落久新——三源铁律下其一足量即计。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 64,698 行 | Lane 1 探针 `probe2` 先证一致 |
| 列名与 130 表调研清单 | 零漂移（B11） |
| 覆盖率分子分母同池 | 64,698/64,698（B3） |
| 满分占比分子分母同池 | 10,928/2,708,162（B3） |
| 脚本形态 | 只读查询，零 demo_* |

## 四、数据缺失情况

### 4.1 「产业维度」单独得分列缺失（构成级，主待裁定项）

UI 瀑布图把总分差拆四阶（基础研究投入/顶尖高校资源/国际科研网络/产业创新优势），承载面四分项是论文/引用/人才/主题——**没有产业维分项**（表内有 company_count 计数列但未入模得分）。若甲方要求四阶各自成列，需扩模（company_count 入分项或另立产业维），当前该子口径部分支持。处置：总分口径主交付，产业子维列待裁定（§1.6 触发器第二条）。

### 4.2 UI 四阶拆分比例无数据依据（口径级）

43%/34%/23%/20% 拆分比例为 ShenzhenInnovation mock 硬编码（`:2156-2159`），三源无承载。复现需甲方给定业务权重。这不是数据缺口而是口径缺口——总分与分项都齐，拆法待定。

### 4.3 dev 侧结果面空壳（数据级，B4 情形②）

三表 0 行（同 002 件事实）：结构骨架在、数据未同步。若未来同步，`svc_tech_power_score`（名称上最贴近技术力得分）是 dev 侧承载候选——当前 0 行不判支持。

### 4.4 时序侧暂缺（快照级）

本表为存量快照（metrics_as_of_date=2026-09-18），`base_years_used=[]`——单快照无同比/环比。时序叙事（评估历史矩阵四期对比的 UI 形态）需等下一版 model_version 落库，届时归 Lane 5 的 022/024 承接，与本件分工无冲突。

### 4.5 缺口与影响面小结

| 缺失项 | 类型 | 对档位的影响 |
|---|---|---|
| 产业维分项列 | 构成缺失 | 总分口径不受影响；产业子维待裁 |
| 四阶拆分比例 | 口径缺失 | 甲方定权重后可重拆 |
| dev 三表 0 行 | 数据未同步 | 不影响（久新足量） |
| gkx 无结果面 | 结构缺失 | 不影响（久新足量） |
| 单快照无时序 | 时间窗 | 时序侧归 022/024 |

## 参考文献

1. European Innovation Scoreboard 2026 – Methodology Report[EB/OL]. European Commission. https://research-and-innovation.ec.europa.eu/document/download/11ae69cb-a3f7-4340-9577-3f941232407a_en?filename=ec_rtd_eis-2026-methodology-report.pdf （R1，2026-11-01 WebSearch 核验可达；32 指标四类等权、重缩放 0–1 平均成 SII、Chauvenet 准则去离群——线性加权复合得分方法基准）
2. Global Innovation Index 2026: Powering entrepreneurs at the frontier of science[EB/OL]. WIPO. https://www.wipo.int/edocs/pubdocs/en/wipo-pub-2000-2026-en-global-innovation-index-2026.pdf （R2，2026-11-01 WebSearch 核验可达；139 经济体约 79 指标、投入/产出两子指数平均；瑞士 66.7 居首、中国第 10 位 57.0 分——总分-分项叙事基准）
3. 2025年中国创新指数比上年增长6.4%[EB/OL]. 国家统计局. https://www.stats.gov.cn/sj/zxfb/202610/t20261023_1965677.html （R3，2026-11-01 WebSearch 核验可达；国内综合指数分层合成先例）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》未出现「产业创新优势综合得分」。最近叶 seq 53 评估方法详解：

> 支持查看技术评估的方法说明和原理展示，包括专家评估法、经济分析法、运筹学评价法和综合评价法的原理、适用场景和局限性说明，帮助用户理解不同评估结果的产生依据。

《科技信息展示系统和科技专题服务系统.md》rg 检索「综合得分」0 命中。指标名与四阶拆分（基础研究投入 43% / 顶尖高校资源 34% / 国际科研网络 23% / 产业创新优势 20%）为 ShenzhenInnovation.tsx mock 自造。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 产业创新优势 / 综合得分 | 技术发展跟踪.md（8 叶） | 0（指标名） |
| 评估方法 | 技术发展跟踪.md seq 53 | 四方法原理描述（非定义） |
| 综合得分 | 科技信息展示系统和科技专题服务系统.md | 0 |
| 产业创新优势 | repos/demo-ui-science/src | ShenzhenInnovation.tsx:2159（瀑布步值） |
| 综合得分 | repos/demo-ui-science/src | techDevelopmentTracking.js:519（矩阵维度）等 |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_001_out.json`（2026-11-01 实跑；期间修正 mock cells 区间描述为「综合得分 59–82 分」后重跑，数值零漂移）。
- Lane 1 探针：`code/_lane1_probe_s3_01_out.json`、`code/_lane1_probe2_s3_01_out.json`（行数/列名先证；曾修正 institution_name/institution_type_id 列名后复验）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（dev 库清单/130 表调研清单背景）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_TECHTRK_001 | 文首 |
| `ui_evidence` | 证据 | 4 条组件行号 | §1.1/§1.5 |
| `requirement_trace.named_in_srs` | 事实 | false | §1.3/附录 A |
| `jiuxin_power_table_columns` | 结构 | 22 列 | §2.2/§3.2 |
| `jiuxin_ads_institution_technology_power_rows` | 计数 | 64,698 | §2.2 |
| `jiuxin_power_scored_n/nonzero_n` | 计数 | 64,698/64,698 | §2.2 |
| `jiuxin_power_score_min/max/mean/median/p25/p75` | 分布 | 9.1756/99.9992/50.0/47.8814/26.3312/72.8817 | §2.2 |
| `jiuxin_power_distinct_values` | 计数 | 44,731 | §2.2 |
| `jiuxin_power_top10_institutions` | 榜单 | 中科院 99.9992 … | §2.2 |
| `jiuxin_power_part_cols` | 结构 | 四分项列 | §2.2 |
| `jiuxin_power_weight_sensitivity_top10` | 榜单 | 双权重对照 | §2.2 |
| `jiuxin_power_top10_overlap_builtin_vs_equal` | 计数 | 10 | §2.2 |
| `jiuxin_power_city_avg_top10` | 榜单 | 长春 86.7398 … | §2.2 |
| `jiuxin_region_assessment_*` ×4 | 计数 | 2,708,162/10,928/397,602/19,027 | §2.2 |
| `derived[0]/[1]/[2]` | 派生比 | 100.0/0.4035/14.6816 | §2.2 |
| `support_judgment` | 判档 | 完全直接支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表文献/机构 | 合成方式 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 线性加权复合 | EIS SII（R1） | 重缩放 0–1 后加权平均 | 四分项×内置权重（现成） | **最高（承载面即实例）** |
| 两柱平均 | GII（R2） | 投入/产出平均 | 四分项无两柱分组 | 中 |
| 总分-拆阶 | UI 瀑布图 | 差值按比例拆 | 分项可重拆（比例待裁） | 高 |
| 专家/运筹 | SRS seq 53 | 定性+约束 | 无专家表 | 低 |
| 分层合成 | 中国创新指数（R3） | 领域→总指数 | 领域维=技术节点维 | 中 |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| jiuxin 结果面 | 64,698 行 | 覆盖 100.0%、44,731 分值 | 单快照无时序 |
| 分项+权重+版本 | 同表 22 列 | 版本号可溯 | 产业维分项缺 |
| 姊妹表 region_assessment | 2,708,162 行 | 满分并列 0.4035%、命名率 14.6816% | **不宜作区域榜** |
| dev 三表 | 0 行 | 空壳 | 数据未同步 |
| gkx 结果面 | 无表 | — | 结构缺失 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 机构粒度总分榜 + Top10 回填（内置权重 v1） | 无 |
| v2 | 城市口径聚合榜（瀑布图回填） | 聚合规则裁定（均值/Top-N/加权） |
| v3 | 产业维分项扩模（company_count 入模） | 甲方权重裁定 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 姊妹表满分并列被误用作区域榜 | **高** | 质量警示入 notes+正文 §2.2 Step5 |
| 机构榜 Top10 区分度低（差 0.0167）被过度解读 | 中 | tooltip 附分值+随行名次 |
| 四阶拆分比例被当真实口径 | 中 | §4.2 明示 mock 无依据 |
| 快照口径被当年化（误作 2026 年度值） | 中 | metrics_as_of_date 随行展示 |

### C.5 总判

**完全直接支持**：结果面（总分满列）+ 构成列（分项/权重/版本号）+ 数据量（64,698 行、覆盖 100.0%）三要件齐备；产业子维与城市聚合规则两口径事项并列待裁，不悬空。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_001.py` | 退出码 0，落 `_out.json` |
| 覆盖率复算 | 64,698/64,698 | = 100.0% |
| 满分占比复算 | 10,928/2,708,162 | = 0.4035% |
| 命名率复算 | 397,602/2,708,162 | = 14.6816% |
| 权重稳健性 | overlap_builtin_vs_equal | = 10 |
| 判档一致 | MD 文首 vs `support_judgment` | 完全直接支持 |
| mock 残留检查 | `rg "产业创新优势" repos/demo-ui-science/src` | 正式版替换后回填真数 |

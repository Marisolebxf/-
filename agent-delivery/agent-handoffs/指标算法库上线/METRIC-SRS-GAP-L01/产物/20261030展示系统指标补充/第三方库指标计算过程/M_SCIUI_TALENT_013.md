# 基线与风险解释（M_SCIUI_TALENT_013）

> **类型**：无业务逻辑数值类（读数组装卡）｜ **域**：科技信息展示系统·人才引进推荐评估·学者引进难度预测｜ **UI 挂载**：科技信息展示系统 → 人才引进评估页（talent-preview）→ 评估页评估 Tab → `EvaluationPage.jsx:637`（DataCard「基线与风险解释」）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（UI 拆件，需求未给「基线与风险解释」算式；本件不合成解释分，B10）｜ **口径归属**：UI 拆件（三份需求真源 0 命中），功能族最近义 = 主需求 1.1.1.1.4.3.4.2 学者引进难度预测，`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TALENT_013.py`｜ **产物**：`code/M_SCIUI_TALENT_013_out.json`
> **四判定摘要**：直接结构 = 无（「样本参考基线」型结果面与学者级风险解释结果面均无现成承载）；直接数据 = 无（同左）；依赖结构 = 部分（久新 cohort 分层基准 + capability 按 Field 分组结构在、gkx/dev 零承载）；依赖数据 = 部分（capability 99,996 行主领域 100.0% 可分组、迁移事件面 298,384 行在，但风险解释侧零承载）
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

**本件判定：部分支持。** 这张卡是双半卡：左半「案例基线」（同领域候选人均值雷达对照）的数据侧结构+数据双在——久新 `ads_talent_capability_assessment` 99,996 行主领域（primary_field_id）100.0% 可分组（派生键 `jiuxin_primary_field_coverage_pct`），按 Field 分组中位数可现转（Top5 领域组：工程学 17,769 人/中位数 29.4736、医学 15,606/30.2007、计算机科学 8,623/29.0106 等），且库内已有官方 cohort 基线机制在案（`ads_talent_potential_result` 100,000 行 cohort=primary_field:career_stage 分组 + capability 模型「少于 200 人组不发布」的基准发布纪律）；右半「风险解释」（数据完整度/主要不确定性/建议复核三行）的学者级风险解释结果面三源零承载——久新 210 张实测表 risk/barrier/compliance/difficulty/friction 词族 0 命中、gkx 280 表风险词族 7 表全为企业风险（失信/税务/执行）、dev `gkxlumenx_*` 0 命中，代理维仅在事件面（迁移事件跨国占比 2.93%）与负向维（撤稿 0）。半卡可算、半卡零承载 → 部分支持。

### 批次通用纪律摘要（S3-03 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实；久新表数写「实测 210 张（探测日）」 |
| B3 | 同基相除 | 两派生比分子分母均同表同 WHERE（99,996/99,996；8,748/298,384） |
| B4 | 负结论带探针 | 风险解释结果面缺失的三源+需求四向 absence_probe（§3.3） |
| B5 | 确定性 | 领域组按人数降序+id 升序双键排序；分布按枚举值排序 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | 评分无量纲；mobility 事件面不含 2026 正式事件（PARTIAL_YEAR 口径随行） |
| B10 | 口径裁定保守交付 | 不写伪解释分（derived 留 null）；UI 写死文案登记为演示值；升档触发器写死 |
| B11 | 多本账互推 | 久新 capability 99,996/profile 100,000/collaborator 5,051,578 与族内件（002/005/010/015）零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 「同领域基线」能算吗？ | 能（现转） | 按 Field 分组中位数 Top5 组在案，主领域覆盖 100.0%（§2.2/§2.3） |
| 库内有官方基线机制吗？ | 有（cohort 型） | potential_result cohort=primary_field:career_stage + 模型「少于 200 人组不发布」（§2.4） |
| 「风险解释」有结果面吗？ | 无（三源 0 命中） | absence_probe 四向全记录；代理维仅在事件面/负向维（§3.3） |

## 摘要

「基线与风险解释」是人才引进评估页评估 Tab 的第三张解释卡（`EvaluationPage.jsx:637`）：正文说明「案例基线来自同领域候选人均值，雷达图虚线为基线」，下方三行固定读数（数据完整度=中高、主要不确定性=合作窗口与资源包、建议复核=正式接触前补充尽调）全部为组件内写死演示文案；卡片名在三份需求真源 0 命中（UI 拆件），功能族最近义是主需求 :2367-2371 学者引进难度预测（引进阻力量化评分/策略建议与预警提示）与 :2453 尽调报告风险点分析。数据侧双半判定：基线半卡结构+数据双在——久新 `ads_talent_capability_assessment` 99,996 行主领域 100.0% 可分组，按 Field 分组中位数（工程学 29.4736/医学 30.2007/计算机科学 29.0106/生化遗传 30.1913/农生 30.2162）即「同领域候选人均值」的现转口径，且库内已有 cohort 分层基准官方机制（potential_result cohort 组 + 模型发布纪律）在案；风险解释半卡三源零承载（久新 210 张实测表 0 命中、gkx 7 表全企业风险、dev 0 命中），可用代理维只有迁移事件面（跨国事件占比 2.93%）与撤稿负向维（0）。判**部分支持**。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**UI 拆件**（卡片名三真源 0 命中）；功能族在（学者引进难度预测），卡片级算式无。
- 复现状态：脚本已跑通；Field 基线 Top5、cohort 样例、全池中位数、迁移事件三组读数全落产物。
- 档位结论：**部分支持**（基线侧可现转 + 风险解释侧零承载）。
- 关键事实：UI 三行解释读数（数据完整度=中高等）为前端演示值，不作数据证据；库内对应物只有事件置信度分布（0.7/0.9 两档）。
- 升档路径：甲方裁定「风险解释」= 代理维组合口径（迁移事件+撤稿）→ 可升完全转换支持；或接外部人才风险数据源。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技人才态势/**人才引进推荐评估·学者引进难度预测**（主需求 1.1.1.1.4.3.4.2 功能族；卡片名为 UI 拆件）。UI 实际容器是人才引进评估页（`talent-preview`）评估 Tab（`EvaluationPage.jsx`）第三行的第三张 DataCard：标题「基线与风险解释」，正文一段说明（案例基线=同领域候选人均值、雷达虚线为基线实线为当前对象、人工调权只影响演示分），下方 `evaluation-confidence-list` 三行固定读数——数据完整度「中高」、主要不确定性「合作窗口与资源包」、建议复核「正式接触前补充尽调」。这三行是**组件内写死常量**（非 state、非 props、无 mock 生成器参与），说明前端作者把它定位为「解释性占位文案」，等待正式版由算法回填。同页相邻卡：因子权重与人工调整（左）、引进障碍与风险合规评估（下排，TALENT_015 承接）。

### 1.2 为什么需要本指标

推荐评分给出「多少分」，基线解释回答「这个分在同类里算什么水平、凭什么信」。人才引进决策链条里，评分卡之后的自然追问有三：其一，「对照谁」——单独一个 87 分没有意义，必须有同领域候选人均值作参照系（雷达虚线）；其二，「有多准」——数据覆盖哪些维、缺哪些维（数据完整度）；其三，「哪里要人工补」——算法看不到的合作窗口、资源包等不确定性要显式提示给决策者（建议复核）。这三问正是官方评价改革强调的「评价结果使用」环节的可解释性要求（R1：科学使用评价结果）。本件的调研重心因此是「基线的库内承载」与「解释读数的库内对应物」：前者决定雷达虚线能不能真算，后者决定三行解释能不能从演示文案升级为数据读数。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「基线与风险解释」卡片名在三份需求真源 0 命中（UI 拆件）；功能族最近义段（主需求 :2367-2371 学者引进难度预测、:2453 尽调报告风险点分析）给的是功能行为（「建立量化模型，给出综合难度评分，并指出主要阻力来源」），没有「基线怎么取、解释读数怎么算」的任何算式。UI 三行解释读数为组件内写死演示文案，登记不作数据证据。

### 1.4 类似指标权威方法可行性分析概要

「基线对照」与「风险解释」的权威方法锚各一层。基线侧：科技人才评价改革试点方案（R1，国科发才〔2022〕255 号）确立「谁使用谁评价、以用定评、评用相适」与分类评价（按重大攻关/基础研究/应用开发/社会公益四类构建指标）——基线必须**同类可比**（分类评价思想），这正是库内 cohort=primary_field:career_stage 分组基线的方法论同构；久新 capability 模型的「少于 200 人组不发布」正是小样本组不发布基线的统计纪律。风险解释侧：现行有效的《科研失信行为调查处理规则》（R2，国科发监〔2022〕221 号，2022-08-25 印发，废止 2019 年 323 号试行规则）定义了抄袭剽窃/伪造篡改/买卖代写等失信行为清单——学术诚信解释维的官方判定轴；OECD 跨境劳动力流动壁垒研究（R3）系统列举工作许可/居留许可/边境检查/税收社保/技能认定/语言六类流动壁垒——国际流动解释维的国际权威口径。方法族对照：

| 方法族 | 代表 | 判定/基线轴 | 数据要求 | 与三源匹配 |
|---|---|---|---|---|
| 分类评价基线 | 试点方案（R1）+ 库内 cohort 机制 | 同类（领域×阶段）组统计量 | 领域标注+组容量 | **有**（primary_field 100.0% + cohort 组在案） |
| 科研诚信负面清单 | 失信规则（R2） | 撤稿/剽窃/伪造等行为 | 学术诚信事件面 | **部分**（撤稿位在、实测 0；其他行为面无） |
| 流动壁垒清单 | OECD（R3） | 签证/居留/认定/语言 | 出访与跨国事件 | **部分**（跨国迁移事件 8,748 在；签证/认定维无） |
| 前端演示 | UI 三行写死文案 | — | — | 结构披露（不作源） |

结论：基线侧官方机制库内同构在案（可现转）；风险解释侧两条权威轴（诚信行为/流动壁垒）库内分别只有撤稿位与跨国事件位两个可用代理，解释卡所需的「多行解释性读数」无从闭合。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/talent-preview/pageRenderer/EvaluationPage.jsx:637`（DataCard title 基线与风险解释）；`:639-651`（案例基线说明段 + 数据完整度/主要不确定性/建议复核三行写死读数）；`:643-651`（evaluation-confidence-list 三行）。
- 数值语义源：`repos/demo-ui-science/src/pages/talent-preview/data.js:290-314`（`recommendFactors.referenceChart` 样本参考基线 mock：方向匹配 84/平台带动 80/合作可达 78/团队承接 75/窗口稳定性 81；`referenceLabel`「当前样本参考基线」——演示值，不作数据证据）。
- 主需求：`科技信息展示系统和科技专题服务系统.md`:2367-2371（学者引进难度预测功能族）、:2453（定制化尽调报告生成含风险点分析），原文见附录 A。
- 权威方法：R1 国科发才〔2022〕255 号（科技部官网/中国政府网）；R2 国科发监〔2022〕221 号（科技部官网）；R3 OECD 流动壁垒研究。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**——本卡是读数组装卡而非单值指标，拆两个半卡：

- **基线半卡（可现转）**：同领域基线 = MEDIAN(overall_score | primary_field = f)，即目标学者所在 OpenAlex Field 的 capability 总分组中位数；雷达五维各自照抄（每维在该 Field 组内的中位数）。库内官方口径（cohort 型）为 primary_field:career_stage 双键分组 + 少于 200 人组不发布，本件交付单键（Field）中位数作演示口径，双键口径为正式版建议。
- **风险解释半卡（零承载）**：三行解释读数无库内结果面，`scholar_risk_explanation_score = null`（B10 不写伪分）。可用代理维组合的候选口径（须甲方裁定才可对外）：数据完整度 ← 事件置信度分布（0.7 档 281,117 条/0.9 档 17,267 条）；学术诚信 ← 撤稿位（实测 0）；流动风险 ← 跨国迁移事件占比 2.93%。

**降档/升档触发器**：①甲方裁定「风险解释」= 代理维组合口径（置信度+撤稿+跨国事件）并接受「事件面代理非评分面」披露 → 可升**完全转换支持**；②接外部人才风险数据源（诚信事件库/签证政策库）→ 解释半卡闭合可升完全转换支持；③若甲方要求独立「风险解释评分面」→ 三源无承载，维持部分支持不升档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在需求文档 | 主需求《科技信息展示系统和科技专题服务系统.md》（SRS 人才引进推荐评估同文转述） |
| 所属四级功能 | 1.1.1.1.4.3.4 人才引进推荐评估 |
| 功能族 | 学者引进难度预测（1.1.1.1.4.3.4.2，8 叶）——本卡横跨其「引进阻力量化评分（.7）」「策略建议与预警提示（.8）」的解释层 |
| 本件 | **基线与风险解释——UI 拆件（三真源 0 命中）** |
| 相邻承接件 | TALENT_015（引进障碍与风险合规评估，同页下排卡）；TALENTIR_010（风险与合规性评估，尽调侧 .6 叶）；TALENTIR_002（多维综合评价与评分，评分主体） |
| UI 容器 | `EvaluationPage.jsx:637` 第三行第三张 DataCard |

本卡与 TALENT_015 是同一评估页的「风险双卡」：本卡是横向解释层（基线对照+读数说明），015 是纵向分维卡（障碍三维+合规三维）；需求侧本卡无独立叶（拆件），015 至少挂着三个明列障碍子叶。族内对账：本件与 015 共享迁移事件面读数（298,384/8,748 两键零漂移），与 002 共享 capability 面读数（99,996/100,000 零漂移）。

## 二、计算过程

### 2.1 方法选择（文献依据）

基线半卡选**同类分组中位数**（分类评价思想的落地版）：按 R1「按照创新活动类型构建评价体系」的分类逻辑，基线组必须是目标学者的同类组——库内即 primary_field（领域）分组；统计量取中位数而非均值，理由是小容量组（如 6,239 人的农生组到 17,769 人的工程组）分布左偏时中位数稳健（本件同步算均值对照，各组均值均略高于中位数，偏态在案）；发布纪律援引库内 capability 模型「少于 200 人组不发布」的小样本组纪律。风险解释半卡无方法可选——评分面零承载（§3.3），任何「解释分合成公式」都是伪公式（F4），本件只登记代理维读数 + `scholar_risk_explanation_score=null`（B10）。诚信代理维的判定轴援引 R2 失信行为清单（撤稿是清单行为「买卖、代写、代投论文」等的结果面之一），流动代理维援引 R3 六类壁垒清单（跨国迁移事件是流动史的行为面证据）。

### 2.2 装载与基线承载面定位

经 `_gkxdb.py` 连 gkx、直连 dev 与久新（三源串行只读）。久新实测 210 张表（探测日，`facts.jiuxin_table_count`）。基线承载面定位：`ads_talent_profile`（100,000 行）**无 primary_field_id 列**——主领域标注不在主画像，而在 `ads_talent_capability_assessment`（99,996 行，`primary_field_id` 非空 99,996 = 全表，派生键 `jiuxin_primary_field_coverage_pct=100.0`，分子分母同表同全量）。这一发现决定了基线 SQL 的承载表选择：同领域分组必须在 capability 面做，画像面只出人数分母。

### 2.3 同领域基线（按 Field 分组）现转读数

按 primary_field 分组统计 capability 总分（人数降序取 Top5 组）：

| Field（openalex_field_id） | 领域名 | 组人数 | 均值 | 中位数 |
|---|---|---|---|---|
| 22 | 工程学 | 17,769 | 29.6236 | 29.4736 |
| 27 | 医学 | 15,606 | 30.2505 | 30.2007 |
| 17 | 计算机科学 | 8,623 | 28.9913 | 29.0106 |
| 13 | 生物化学、遗传学与分子生物学 | 8,330 | 30.1053 | 30.1913 |
| 11 | 农业与生物科学 | 6,239 | 30.1668 | 30.2162 |

五组均值与中位数差异均在 0.2 分以内（分布近对称），Top5 组合计 56,567 人覆盖 capability 面 56.6%——「同领域候选人均值」的雷达虚线在库内可现转。全池参考值：`overall_score` 全池中位数 30.3114（`jiuxin_capability_overall_median`），五组中位数（29.0-30.2）与全池高度接近，说明该评分的领域间分布同质性强，基线卡的区分度主要来自组内个体差而非领域间差。

```sql
SELECT c.primary_field_id, f.name_zh, COUNT(*), ROUND(AVG(c.overall_score),4),
       ROUND(MEDIAN(c.overall_score),4)
FROM ads_talent_capability_assessment c
LEFT JOIN ads_discipline_field f ON f.openalex_field_id = c.primary_field_id
WHERE c.primary_field_id IS NOT NULL
GROUP BY c.primary_field_id, f.name_zh
ORDER BY COUNT(*) DESC, c.primary_field_id ASC LIMIT 5;
-- → 工程学 17769/29.6236/29.4736；医学 15606/30.2505/30.2007；…（B5 双键排序）
```

### 2.4 库内官方基线机制：cohort 分层基准

久新已有 cohort 型分层基准的正式机制（schema 文档在案）：`ads_talent_potential_result`（100,000 行）按 cohort_id = `primary_field:career_stage` 双键分组发布潜力排名——cohort 样例 6 组（`jiuxin_potential_result_cohort_sample`）：fld_02df…:10_14 组声明 1,517 人/实测去重 1,601 人一致、fld_0abe…:10_14 组 2,092/2,206 一致等，cohort_talent_count 与实测 COUNT(DISTINCT talent_id) 逐组对账吻合；`potential_rank` 是组内排名位（cohort 词族列 = cohort_id/cohort_talent_count/potential_rank 三件套）。career_stage 分布：None 2 / 0_4（早期）10,353 / 5_9（中期）21,961 / 10_14（资深）67,684。这套机制 + capability 模型行（1 行，`talent_problem_match_shenzhen_v1`，观察窗 2000-2025，权重 0.25/0.25/0.40/0.10，「少于 200 人组不发布」发布纪律）共同构成「基线」的库内官方口径——UI 雷达虚线若要正式版，双键 cohort 基线比单键 Field 基线更贴官方机制。

### 2.5 风险解释半卡：代理维读数

三行解释读数无评分面，可用代理维三组读数落产物：

- **事件置信度面**（「数据完整度」的库内对应物）：`ads_talent_mobility_event` 共 298,384 条事件，assignment_confidence 取值仅两档——0.7 档 281,117 条、0.9 档 17,267 条（`jiuxin_mobility_confidence_dist`）：RESEARCH_FIELD_CHANGE 类事件全部 0.7 档，EDUCATION_TO_WORK/WORK_TO_WORK 类多为 0.9 档。
- **学术诚信负向维**：`ads_paper_profile.is_retracted` 全池 4,000,000 行撤稿 0（`jiuxin_retracted_papers`，与 TALENTIR_005/010 件对账一致）——「未发现异常」的库内证据是「零撤稿」，但只能覆盖 R2 失信清单中「撤稿」这一结果面，剽窃/伪造/代写等行为面无承载。
- **流动壁垒事件面**：跨国事件（is_cross_country=1）8,748 条，占全部迁移事件 2.93%（派生键 `jiuxin_cross_country_event_share_pct`，分子分母同表全量）；事件类型分布 RESEARCH_FIELD_CHANGE 281,117 / WORK_TO_WORK 9,276 / EDUCATION_TO_WORK 7,991；涉及去重人才 78,826 人。

### 2.6 稳健性与口径敏感性

基线半卡的敏感性：单键（Field）vs 双键（Field:career_stage）口径的组容量差异大——双键组最小仅 40 人（fld_0abe…:0_4），单键 Top5 组 6,239-17,769 人；小容量组的中位数受个体波动影响大，这正是库内「少于 200 人组不发布」纪律的存在理由，演示口径（单键）组容量充足、正式口径（双键）须执行发布纪律。风险解释半卡的敏感性：代理维都是「事件面/负向维」而非「评分面」——零撤稿不等于零诚信风险（只能覆盖结果面）；跨国事件占比是池级读数非个体读数（个体级需按 talent_id 下钻）；置信度分布是赋值方自评非独立审计。这些敏感性决定了代理维只能作「解释性参考」登记，不得升格为评分（B10）。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TALENT_013.py`（三源串行只读；gkx 经 `_gkxdb.py`；dev/久新直连；零 `demo_*`）；运行 `python3 code/M_SCIUI_TALENT_013.py`。
- 产物：`code/M_SCIUI_TALENT_013_out.json`。正文数字与产物键逐一对应：`jiuxin_table_count=210`（§2.2，探测日实测）、`jiuxin_capability_assessment_rows=99996` + `jiuxin_capability_pf_nonnull=99996` + `jiuxin_capability_rows=99996` + 派生键 `jiuxin_primary_field_coverage_pct=100.0`（§2.2）、`jiuxin_baseline_by_field_top5` 五组四元读数（§2.3）、`jiuxin_capability_overall_median=30.3114`（§2.3）、`jiuxin_potential_result_rows=100000` + `jiuxin_potential_result_cohort_like_cols=[cohort_id, cohort_talent_count, potential_rank]` + `jiuxin_potential_result_cohort_sample` 六组 + `jiuxin_potential_career_stage_dist` 四档（§2.4）、`jiuxin_capability_model_rows=1` + `jiuxin_capability_model_row_sample`（模型行全列）（§2.4）、`jiuxin_mobility_event_rows=298384` + `jiuxin_mobility_event_type_dist` 三型 + `jiuxin_mobility_cross_country_events=8748` + 派生键 `jiuxin_cross_country_event_share_pct=2.93` + `jiuxin_mobility_distinct_talents=78826` + `jiuxin_mobility_confidence_dist` 两档（§2.5）、`jiuxin_retracted_papers=0` + `jiuxin_profile_rows=100000`（§2.5）、`jiuxin_risk_like_tables=[]` + `jiuxin_profile_risk_like_cols=[]` + `gkx_table_count=280` + `gkx_scholar_risk_like_tables=[]` + `gkx_risk_like_tables_all` 七表企业风险 + `dev_talent_risk_like_tables=[]`（§3.3）、`scholar_risk_explanation_score=null`（B10 留空）。
- 结果解读：三个可用读数（Field 基线 Top5 组=雷达虚线现转口径；cohort 机制=官方基线口径在案；代理维三组=解释读数的库内候选）+ 一个不可用结论（学者级风险解释结果面三源零承载，不写伪分）。
- 对照需求功能要求的评审：「给出学者引进的综合难度评分，并指出主要阻力来源」——**部分满足**：基线对照半卡可现转（同领域组中位数 + 官方 cohort 机制）；「指出主要阻力来源」的解释读数侧零承载，UI 三行（数据完整度=中高等）仍为演示文案，须代理维裁定或外部源接入后回填。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 久新实测表数 | `jiuxin_table_count` | 210（探测日） |
| 装载 | capability 面行数 | `jiuxin_capability_assessment_rows` | 99,996 |
| 分组 | 主领域非空 | `jiuxin_capability_pf_nonnull` | 99,996（100.0%） |
| 基线 | 工程学组 | `jiuxin_baseline_by_field_top5[0]` | 17,769 人 / 均值 29.6236 / 中位数 29.4736 |
| 基线 | 医学组 | `jiuxin_baseline_by_field_top5[1]` | 15,606 / 30.2505 / 30.2007 |
| 基线 | 全池中位数 | `jiuxin_capability_overall_median` | 30.3114 |
| 机制 | cohort 词族列 | `jiuxin_potential_result_cohort_like_cols` | cohort_id/cohort_talent_count/potential_rank |
| 机制 | cohort 组样例 | `jiuxin_potential_result_cohort_sample` | 声明数与实测去重逐组一致（6 组） |
| 机制 | career_stage 分布 | `jiuxin_potential_career_stage_dist` | 0_4:10,353 / 5_9:21,961 / 10_14:67,684 / None:2 |
| 代理 | 置信度分布 | `jiuxin_mobility_confidence_dist` | 0.7 档 281,117 / 0.9 档 17,267 |
| 代理 | 跨国事件占比 | `jiuxin_cross_country_event_share_pct` | 2.93%（8,748/298,384） |
| 代理 | 撤稿负向维 | `jiuxin_retracted_papers` | 0 |
| 排除 | 久新风险词族表 | `jiuxin_risk_like_tables` | [] |
| 排除 | gkx 学者风险表 | `gkx_scholar_risk_like_tables` | []（7 表全企业风险） |
| 排除 | dev 人才风险表 | `dev_talent_risk_like_tables` | [] |
| 评分 | 风险解释分 | `scholar_risk_explanation_score` | null（B10） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 同领域分组键 | jiuxin | `ads_talent_capability_assessment.primary_field_id` | 99,996（100.0%） | 直查 | **有（基线半卡）** |
| D2 | 官方 cohort 基线机制 | jiuxin | `ads_talent_potential_result` + capability_model | 100,000 / 1 | 直查 | **有（正式口径在案）** |
| D3 | 事件置信度（完整度代理） | jiuxin | `ads_talent_mobility_event.assignment_confidence` | 298,384 事件 | 直查 | 有（代理维） |
| D4 | 学术诚信负向维 | jiuxin | `ads_paper_profile.is_retracted` | 0/4,000,000 | 直查 | 有（零撤稿，仅结果面） |
| D5 | 流动壁垒事件维 | jiuxin | `ads_talent_mobility_event.is_cross_country` | 8,748 | 直查 | 有（代理维） |
| D6 | 学者级风险解释结果面 | 三源 | — | — | **不存在** | **缺（主降档因）** |
| D7 | UI 演示值 | UI | EvaluationPage 写死文案 + data.js referenceChart | — | mock | 边界证据（不作源） |

`support_judgment="部分支持"`、产物与文首一致。

### 3.2 D1/D2 基线侧的覆盖与机制（久新）

主领域标注 100.0% 全覆盖是基线半卡最强的数据面事实：capability 面 99,996 行无一行缺 primary_field_id，且 Field 维度经 `ads_discipline_field`（openalex_field_id→name_zh）字典可读（Top5 组中文名直接可展示）。cohort 机制的三件套（分组键/组容量列/组内排名列）齐全，六组样例的声明人数与实测去重人数逐组吻合（如 fld_02df…:10_14 组 1,517/1,601、fld_0abe…:10_14 组 2,092/2,206）——机制自洽可审计。唯一口径注意点：profile 面（100,000）与 capability 面（99,996）差 4 行（eligibility 过滤，与 002 件对账一致），基线分母用 capability 面口径。

### 3.3 D6 风险解释结果面的 absence_probe 全记录

否定性证据三件套：**查了什么**——久新 210 张实测表（探测日）risk/barrier/compliance/difficulty/friction 词族 + `ads_talent_profile` 104 列 risk/barrier/baseline/compliance/difficulty 词族；gkx 280 表 scholar×risk/difficulty/eval 交叉词族与全库风险词族；dev `gkxlumenx_*` 全 schema talent/scholar×risk/eval/difficulty/baseline 词族；三份需求真源「基线与风险解释/样本参考基线/基线算式」检索。**条件**——表级与列级存在性 + 需求文本命中。**命中**——0（gkx 风险词族 7 表全为企业失信/税务/执行，无学者级承载；久新学者侧 0 表 0 列；需求侧卡片名 0 命中）。四缺失情形归属：**表不存在**（学者级风险解释结果面）——修复动作是接外部数据源或按代理维裁定口径，不是补数据同步。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 主领域覆盖率 | 99,996/99,996 = 100.0%（全量非采样） |
| Field 基线 Top5 | 五组人数 17,769/15,606/8,623/8,330/6,239，均值中位数差 <0.2 分 |
| cohort 对账 | 六组声明数=实测去重数（1,517/1,601 型逐组吻合） |
| 跨国事件占比 | 8,748/298,384 = 2.93%（全量非采样） |
| 置信度两档 | 0.7 档 281,117 + 0.9 档 17,267 = 298,384 |
| 三源风险词族 | 久新 []/gkx 学者侧 []（企业 7 表）/dev [] |
| 脚本形态 | 三源串行只读；零 demo_* |

## 四、数据缺失情况

### 4.1 学者级风险解释结果面零承载（结构级，主因）

「风险解释」所需的学者级风险/障碍/合规评分面（学术诚信事件、合作合规审查、出访敏感性等解释卡读数）在三源均无承载：久新学者侧 0 表 0 列（profile 104 列逐一核对）；gkx 风险词族全落企业域（失信/税务/执行），企业风险表 ≠ 学者风险表；dev 无人才评估面。四缺失情形归属「表不存在」，修复只有两条路：其一，接外部人才风险数据源（科研诚信事件库、签证政策库、安全审查公开信息）；其二，按 §1.6 触发器①由甲方裁定代理维组合口径（置信度+撤稿+跨国事件）——零成本但语义降格为「事件面解释」。

### 4.2 基线口径待裁（方法级，次因）

基线半卡数据面全但口径未闭合：单键（Field）演示口径已现转（Top5 组读数在案），双键（Field:career_stage）官方口径机制在但须执行「少于 200 人组不发布」纪律——小容量组（最小 40 人）的裁撤会让部分学者的基线组缺失，UI 须设计降级展示（回退单键组或显示「基线组样本不足」）。这与 002 件的「三套口径并存待裁」同型：数据在、口径权在甲方。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 代理维口径裁定（触发器①） | 口径裁定 | 本件即期可交付 | 置信度+撤稿+跨国事件组合，披露「事件面代理」 |
| cohort 双键基线正式化 | 工程启用 | 本件 + TALENT 族基线件 | 机制在库，启用+发布纪律 |
| 人才诚信事件库接入 | 外部数据源 | 本件 + TALENTIR_010 | R2 清单行为面 |
| 签证/安全审查政策库接入 | 外部数据源 | 本件 + TALENT_015 | R3 壁垒清单维 |

档位后果：代理维裁定 → **完全转换支持**（半卡闭合）；外部源接入 → 完全转换支持（语义正规）；要求独立评分面 → 维持部分支持。推荐顺序：即期走触发器①，cohort 正式化并行，外部源列中期。

## 参考文献

1. 科技部等八部门印发《关于开展科技人才评价改革试点的工作方案》的通知（国科发才〔2022〕255 号）[EB/OL]. 中华人民共和国科学技术部. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2022/202211/t20221109_183356.html （R1，2026-11-01 WebSearch 核验可达——按创新活动类型构建分类评价体系、以用定评评用相适，「同类可比基线」与评价结果使用可解释性的政策框架）
2. 科技部等二十二部门关于印发《科研失信行为调查处理规则》的通知（国科发监〔2022〕221 号）[EB/OL]. 中华人民共和国科学技术部. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2022/202209/t20220907_182313.html （R2，2026-11-01 WebSearch 核验可达——现行有效的科研失信行为清单（抄袭剽窃/伪造篡改/买卖代写等八类），学术诚信解释维的官方判定轴；2022-08-25 印发并废止 2019 年 323 号试行规则）
3. OECD. Barriers to cross-border labour mobility for TCNs – learning from other EU cross-border regions[EB/OL]. OECD. https://www.oecd.org/en/publications/mobility-and-integrated-labour-markets-for-third-country-nationals-in-greater-copenhagen_ba2a4777-en/full-report/barriers-to-cross-border-labour-mobility-for-tcns-learning-from-other-eu-cross-border-regions_2a29448d.html （R3，2026-11-01 WebSearch 核验可达——工作/居留许可、边境检查、税收社保、技能认定、语言等跨境流动壁垒清单，国际流动解释维的国际权威口径）

# 附件

## 附录 A 原始需求原文摘录

「基线与风险解释」卡片名在三份需求真源（主需求/SRS/核增需求/算法库）检索 0 命中——本卡为 UI 拆件。功能族最近义原文两段：

主需求《科技信息展示系统和科技专题服务系统.md》:2367（学者引进难度预测，总述）：

> 学者引进难度预测综合运用数据挖掘、自然语言处理及机器学习等技术，通过对专家的国籍、语言能力、文化背景等多元信息进行深度分析，同时结合专家过往的教育经历、科研履历，以及其在国际学术合作网络中的活跃度和与引进单位历次合作情况等历史数据，智能评估学者的适应性和引进阻力。

:2397（1.1.1.1.4.3.4.2.7 引进阻力量化评分）：

> 基于多维数据与历史案例，建立量化模型，给出学者引进的综合难度评分，并指出主要阻力来源，为决策团队提供直观的风险预警。

:2453（1.1.1.1.4.3.4.4.3 定制化尽调报告生成）：

> 用户可根据需求定制尽调维度，系统自动生成可视化尽调报告，包括学术背景、行业贡献、以往合作、奖项荣誉及风险点分析，满足各类招聘、评审和机构管理的精细化要求。

UI 组件原文（`EvaluationPage.jsx:639-651`）：「案例基线来自同领域候选人均值，雷达图虚线为基线，实线为当前对象。人工调权只影响演示分，不覆盖原始推荐结论。」+ 三行写死读数（数据完整度=中高/主要不确定性=合作窗口与资源包/建议复核=正式接触前补充尽调）——演示文案，不作数据证据。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 基线与风险解释 | 三份需求真源 | 0（UI 拆件） |
| 样本参考基线 | 三份需求真源 | 0 |
| 基线 | 主需求人才族段 | 0（卡片级） |
| 引进阻力/风险预警 | 主需求 | :2367/:2397/:2401（功能族最近义） |
| 风险点分析 | 主需求 | :2453（尽调报告叶） |
| referenceChart | UI data.js | :290-314（mock 基线演示值） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TALENT_013_out.json`（2026-11-01 实跑：三源探针 + Field 基线 Top5 + cohort 机制样例 + 代理维读数）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（久新 talent 族表清单——B11 锚）。
- 族内对账：`M_SCIUI_TALENTIR_002_out.json`（capability 99,996/profile 100,000 一致）；`M_SCIUI_TALENT_015_out.json`（迁移事件 298,384/跨国 8,748 一致）；`M_SCIUI_TALENTIR_005_out.json` / `M_SCIUI_TALENTIR_010_out.json`（撤稿 0 一致）。

### B.2 本件产物逐键清单（`code/M_SCIUI_TALENT_013_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.jiuxin_table_count` | 计数 | 210（探测日实测） | §2.2/§3.3 |
| `facts.jiuxin_capability_assessment_rows` | 计数 | 99,996 | §2.2 |
| `facts.jiuxin_capability_pf_nonnull` | 覆盖 | 99,996 | §2.2/§3.2 |
| `facts.jiuxin_capability_rows` | 计数 | 99,996 | §2.2 |
| `facts.jiuxin_profile_rows` | 计数 | 100,000 | §3.2 |
| `facts.jiuxin_baseline_by_field_top5` | 分布 | 五组四元 | §2.3/§3.2 |
| `facts.jiuxin_capability_overall_median` | 统计 | 30.3114 | §2.3 |
| `facts.jiuxin_capability_model_rows` | 计数 | 1 | §2.4 |
| `facts.jiuxin_capability_model_row_sample` | 登记 | 模型行全列（含发布纪律） | §2.4 |
| `facts.jiuxin_potential_result_cohort_like_cols` | 结构 | cohort 三件套列 | §2.4 |
| `facts.jiuxin_potential_result_rows` | 计数 | 100,000 | §2.4 |
| `facts.jiuxin_potential_result_cohort_sample` | 样例 | 六组（声明/实测对账） | §2.4 |
| `facts.jiuxin_potential_career_stage_dist` | 分布 | 四档 | §2.4 |
| `facts.jiuxin_risk_like_tables` | 探针 | [] | §3.3 |
| `facts.jiuxin_profile_cols_count` | 结构 | 104 列 | §3.3 |
| `facts.jiuxin_profile_risk_like_cols` | 探针 | [] | §3.3 |
| `facts.jiuxin_mobility_event_rows` | 计数 | 298,384 | §2.5 |
| `facts.jiuxin_mobility_event_type_dist` | 分布 | 三型 | §2.5 |
| `facts.jiuxin_mobility_cross_country_events` | 计数 | 8,748 | §2.5 |
| `facts.jiuxin_mobility_distinct_talents` | 计数 | 78,826 | §2.5 |
| `facts.jiuxin_mobility_confidence_dist` | 分布 | 两档 | §2.5 |
| `facts.jiuxin_retracted_papers` | 计数 | 0 | §2.5 |
| `facts.gkx_table_count` | 计数 | 280 | §3.3 |
| `facts.gkx_scholar_risk_like_tables` | 探针 | [] | §3.3 |
| `facts.gkx_risk_like_tables_all` | 探针 | 7 表（全企业风险） | §3.3 |
| `facts.dev_talent_risk_like_tables` | 探针 | [] | §3.3 |
| `derived[0].jiuxin_primary_field_coverage_pct` | 派生比 | 100.0（99,996/99,996） | §2.2 |
| `derived[1].jiuxin_cross_country_event_share_pct` | 派生比 | 2.93（8,748/298,384） | §2.5 |
| `derived[2].scholar_risk_explanation_score` | 负结论 | null | §1.6/§2.7 |
| `absence_probe` | 探针 | 四件（jiuxin/gkx/dev/doc） | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

### B.3 共享与族内读数消费

本件消费共享快照 talent 族表清单与族内件对账锚：capability 99,996（=002 件）、profile 100,000（=002/005 件）、迁移事件 298,384 与跨国 8,748（=015 件）、撤稿 0（=005/010 件）、collaborator 底料（015 件引用同源）——批内五键零漂移（B11）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 轴/基线机制 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 分类评价基线 | 试点方案（R1）+ 库内 cohort | 同类组统计量+发布纪律 | primary_field 100.0% + cohort 三件套 | **最高（机制同构）** |
| 诚信负面清单 | 失信规则（R2） | 八类失信行为 | 仅撤稿位（实测 0） | 中（结果面代理） |
| 流动壁垒清单 | OECD（R3） | 六类跨境壁垒 | 仅跨国迁移事件位 | 中（行为面代理） |
| 前端演示 | UI 三行写死 | — | mock 文案 | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 同领域分组键 | 无 | 无 | **primary_field 100.0%** |
| cohort 基线机制 | 无 | 无 | **potential_result 100,000 + model 1 行** |
| 事件置信度 | 无 | 无 | 298,384 事件两档 |
| 诚信负向维 | 无 | 无 | 撤稿 0（结果面） |
| 学者风险解释评分面 | 无（企业 7 表） | 无 | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | Field 基线 Top5 读数 + 代理维登记 + 口径裁定请求 | — |
| v1 | 代理维口径裁定 → 三行解释读数回填（披露事件面代理） | 裁定函（触发器①） |
| v2 | cohort 双键基线正式化（含 200 人发布纪律与降级展示） | 工程启用 |
| v3 | 诚信/签证外部源接入 | 数据源立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| UI 写死三行被当真实读数 | **高** | 演示文案登记 + 正式版回填前 KPI 位标注「演示」 |
| 零撤稿被读成「零诚信风险」 | 中 | 披露「仅撤稿结果面，R2 行为面无覆盖」 |
| 跨国占比 2.93% 是池级非个体级 | 中 | 个体下钻路径注明；解释卡加池级标注 |
| 双键小容量组基线不稳 | 中 | 200 人发布纪律 + 单键回退 |

### C.5 总判

**部分支持**：基线半卡结构+数据双在（Field 100.0% 可分组 + cohort 官方机制在案）可现转；风险解释半卡三源零承载（探针闭环），代理维组合是唯一即期路径。升档触发器两条（代理维裁定/外部源接入）写死不悬空，按 B10 保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TALENT_013.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（gkx）+ 直连 dev/久新 | demo_* 直接 raise |
| 判档一致 | 文首 vs `support_judgment` | 部分支持 |
| B11 对账 | capability 99,996=002；事件 298,384/8,748=015；撤稿 0=005/010 | 零漂移 |
| 幂等重跑 | SQL 全只读无随机 | 逐位一致 |
| 伪分残留 | `scholar_risk_explanation_score` | null（无伪分） |
| mock 残留检查 | `rg "referenceChart" repos/demo-ui-science/src/pages/talent-preview` | 正式版替换后无引用 |

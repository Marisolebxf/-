# 评估数据收集量（M_SCIUI_TECHTRK_014）

> **类型**：COUNT（评估证据量，多源分域）｜ **域**：科技发展态势·技术发展跟踪·技术评估工作流·数据收集｜ **UI 挂载**：科技信息展示系统 → 技术发展跟踪 → 技术评估工作流（`techDevelopmentTracking.js:1100` 五环节流程第 2 环）
> **数据支持度**：**部分支持**｜ **公式定义人**：工程侧推测定义（UI 未给公式；非招标原文闭合口径）｜ **口径归属**：需求未明列叶（三份指定说明书未出现指标名），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TECHTRK_014.py`｜ **产物**：`code/M_SCIUI_TECHTRK_014_out.json`
> **四判定摘要**：直接结构 = 部分（久新 data_coverage/evidence/graph 三表结构齐；dev/gkx 无）；直接数据 = 部分（久新 2026-10-16 单轮 19430 节点全域证据量有数；资讯域 0）；依赖结构 = 部分（五源中资讯源三库均无入链结构）；依赖数据 = 部分（论文/专利/项目/图谱四源量足，资讯缺）
> **数据源口径注记**：三源评估——开发库（10.50.11.76 `gkxlumenx_*`，禁 `demo_*`）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin_warehouse（47.93.119.170:29030 `gkx_technology_analysis_dev` 只读）。本件主数据面在久新。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（三源）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 降档根因唯一且清晰：UI 工作流第 2 环声明接入「论文、专利、项目、资讯和知识图谱」五源（`techDevelopmentTracking.js:1100`），久新本轮评估的证据量结果面（`ads_technology_data_coverage` 十域 + `ads_technology_assessment_evidence` 三类证据 + 图谱两表）对论文/专利/项目/图谱四源均有足量读数，唯独「资讯」源三库皆缺——久新 203 表无任何 news/media/literature 类表、data_coverage 的 MARKET 与 POLICY 域证据量恒 0（NOT_AVAILABLE，注记「No registered immutable source」）；gkx 虽有 `dwd_news_base`（20,000 行，共享快照键）但未进入技术评估链路；开发库无论文表、亦无资讯表。五源缺一源且该源在三库均无评估侧承载，按档位定义只能落在部分支持。

### 批次纪律摘要（B1–B11 对照，skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | `jiuxin_ui5source_align_rate_pct` 分子分母同源同轮（jiuxin data_coverage/graph_edge） |
| B4 | 负结论带探针 | absence_probe 四条（dev/gkx/jiuxin×2，见 §3.4） |
| B5 | 确定性 | 聚合均 ORDER BY 键排序；无 set 迭代序依赖 |
| B6 | 闸门自身被闸 | 本件不跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | `M_SCIUI_TECHTRK_014.py` 实跑产出，无手改 |
| B8 | 回执不复收 | 硬证据（表行数/域分布）亲自实跑 |
| B9 | 单位/日期陷阱 | 单轮快照按 metrics_as_of_date=2026-10-16；双 model_version 去重读数 |
| B10 | 口径裁定保守交付 | 「全量收集量」vs「本轮评估证据量」双口径并列（§1.6） |
| B11 | 多本账互推 | 共享快照 `ads_paper_profile=4,000,000` 等行数零漂移引用 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 结果面存在吗？ | 存在（久新） | `ads_technology_data_coverage` 194,300 行（单版本 19,430 节点×10 域） |
| 五源全有量吗？ | 否（缺资讯） | MARKET/POLICY 域 SUM=0；203 表无 news 类（absence_probe） |
| 覆盖几源？ | 4/5（80%） | `derived.jiuxin_ui5source_align_rate_pct` = 80.0 |

## 摘要

「评估数据收集量」是技术评估工作流「数据收集」环节的量化读数：用户在五环节流程图上点击第 2 环时，需要看到本轮评估到底接入了多少证据。本件实测：久新库的技术洞察 ADS 层为 19,430 个技术节点维护了十域证据量台账（`ads_technology_data_coverage`），本轮（model_version=technology_insight_mvp_v2_eto_cluster_technology，2026-10-16）论文域合计 108,479 条、专利域 1,071,763 条、机构域 2,528,802 条、图谱边 587,252 条；证据明细表 `ads_technology_assessment_evidence` 收录 269,882 条可溯源证据（论文 102,766 / 专利 95,170 / 科研项目 71,946）。但 UI 声明的五源中「资讯」源三库皆空（MARKET/POLICY 域恒 0、全库无新闻表、gkx 新闻表未入链），五源对齐率 80%。判**部分支持**；修复路径是把 gkx 资讯底表接入评估链或由甲方裁定资讯源降级口径。

- 需求判定：需求未明列叶（三份指定说明书未出现指标名；seq 52「评估流程概览」仅列环节名）。
- 复现状态：脚本已跑通；域级证据量、状态分布、证据明细三类读数落产物。
- 档位结论：**部分支持**（资讯源三库无评估侧承载，主降档因）。
- 关键事实：本轮单版本 19,430 节点，全表行数须按双版本去重读。
- 升档路径：gkx `dwd_news_base` 接入久新评估链（MARKET/POLICY 域从 NOT_AVAILABLE 转 AVAILABLE）→ 可升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/技术发展跟踪/**技术评估工作流**/评估流程概览（SRS seq 52，excel_row 55）。UI 侧的承载是 `buildWorkflow()` 生成的五环节流程条（`techDevelopmentTracking.js:1097-1105`）：评估准备 → **数据收集** → 方法选择 → 分析计算 → 结果生成；每环节有 status（completed/active/waiting）与 method 注记。本件挂载第 2 环：

```text
{ key: 'collect', label: '数据收集', status: 'completed',
  method: '接入论文、专利、项目、资讯和知识图谱' }   // techDevelopmentTracking.js:1100
```

值得记录的实现细节：`buildWorkflow` 的 activeIndex 由所选话题的平均成熟度动态决定（`averageMaturity >= 74 ? 4 : >= 62 ? 3 : 2`），即流程条是「评估进度可视化」而非静态装饰——数据收集环节的 completed 状态隐含断言「五源已接入完毕」。这个断言正是本件要拿数据检验的对象：五源各接了多少，UI 没有给任何数值位，mock 里也不存在「收集量」读数。换言之，这个指标在 UI 侧是**纯状态位**，数值语义（多少条）是展示系统投标叙事里「数据中台接入能力」的自然延伸，需要工程侧自行定义读数口径。

### 1.2 为什么需要本指标

评估结论的可信度取决于证据底盘的厚度。工作流把「数据收集」放在「方法选择」「分析计算」之前，业务语义是：先亮证据量、再谈评分——用户看到「论文 10 万条、专利 100 万条」才会相信后面的成熟度档与潜力分不是拍脑袋。对管理侧，收集量还是数据治理的监控读数：哪个域掉到 0、哪个域长期 RESEARCH_PROJECT_PROXY（科研项目代理），一眼可见。本件把「收集量」操作化为三个可直查读数：域级证据量（data_coverage）、可溯源证据行数（assessment_evidence）、图谱规模（graph_node/edge），三者互为校验。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。** SRS《技术发展跟踪.md》seq 52 原文：「以流程图形式展示技术评估的完整工作流程，包括评估准备、数据收集、方法选择、分析计算、结果生成等关键环节」——只定义了环节名与交互，无任何「量」的定义；《科技信息展示系统和科技专题服务系统.md》421 行为同段复述。「收集量」按什么粒度（条数/源数/域数）、算不算重复证据、跨轮次怎么累计，一概未提。

### 1.4 类似指标权威方法可行性分析概要

证据底盘量化在 Foresight 体系有直接对应物：OECD 把 horizon scanning 的第一步定义为系统性搜集信号并评估来源广度与可靠性（R1/R2），信号源的覆盖广度本身就是扫描质量的度量维度。方法族对照：

| 方法族 | 量化对象 | 数据要求 | 与本库匹配 |
|---|---|---|---|
| 证据台账法（OECD 信号扫描） | 各源信号量+来源可靠性 | 分源计数表 | **有**（data_coverage 十域+coverage_status） |
| 数据资产盘点法（数仓元数据） | 表行数+更新批次 | 元数据 | 有（data_version/metrics_as_of_date 批次列） |
| UI 状态位法（本项目现状） | 环节 completed 布尔 | 无需数值 | 现状即此，无信息量 |

结论：久新的 data_coverage 结构就是「证据台账法」的实现，本件直接消费。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/techDevelopmentTracking.js:1100` — `{ key: 'collect', label: '数据收集', status: 'completed', method: '接入论文、专利、项目、资讯和知识图谱' }`；上下文 `buildWorkflow` 1097–1105。
- SRS：`…/科技发展态势/技术发展跟踪.md` seq 52（excel_row 55）「评估流程概览」，原文见附录 A。
- 主需求文档：《科技信息展示系统和科技专题服务系统.md》:421 同段复述。

### 1.6 推测原意与推测定义

**推测定义（双口径并列，B10）**：

- 口径 A（**本轮评估证据量**，建议口径）：`collect_amount(domain) = SUM(evidence_count)` over `ads_technology_data_coverage`，限定单 model_version（v2）单 metrics_as_of_date——即「这一轮评估用了多少证据」；
- 口径 B（全域数据资产量）：`profile_sum(domain)` over `ads_technology_profile` 的 paper_count/patent_count 等列——「库里总共有多少」，与评估轮次无关。

两口径数值不同（如论文：口径 A=108,479 条证据 vs 口径 B=108,479 总数恰好同值，但机构域 A=2,528,802 证据与 B=2,528,802 同——本件实测两表在这些域同源对齐；差异主要在 PROJECT 与 APPLICATION_CASE 两域恒等 181,735，系科研项目代理 1:1 复用）。**降档/升档触发器**：若甲方接受口径 A 并允许「资讯源暂缺」随行披露 → 维持部分支持但语义闭合可上线；若 gkx `dwd_news_base`/`dwd_policy_base` 接入久新评估链（MARKET/POLICY 转 AVAILABLE）→ 升完全转换支持；若甲方要求五源全量才能出数 → 维持部分支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/技术发展跟踪.md` |
| 所属四级功能 | 技术发展跟踪（8 叶，seq 48–55） |
| 所属面板 | 技术评估工作流（seq 52–55，excel_rows 55–58） |
| 本件叶 | **评估流程概览（seq 52）之「数据收集」环节——需求未明列收集量指标** |
| 相邻叶 | 评估方法详解（seq 53，M_SCIUI_TECHTRK_015 关联）/ 评估参数配置（seq 54）/ 评估结果追踪（seq 55，Lane 4 的 022 承接） |
| UI 容器 | `techDevelopmentTracking.js` workflow 条第 2 环 |

本件与 Lane 4 的 022（评估结果追踪）构成工作流面板的「入口读数/出口读数」对：014 量化进多少证据，022 量化历轮得分变化。两件共享「轮次」概念——而久新侧只有单轮快照，这个共同缺口是工作流面板整体升档的统一前置。

## 二、计算过程

### 2.1 装载与版本去重（口径地基）

直连久新 Doris（47.93.119.170:29030，gkx_technology_analysis_dev，test2 只读）。第一件事是版本审计：`ads_technology_data_coverage` 全表 194,300 行，但 `COUNT(DISTINCT technology_node_id)` 只有 19,430——表内并存两个 model_version（`technology_insight_mvp_v1` 与 `technology_insight_mvp_v2_eto_cluster_technology`），逐节点同内容双写（19,430×10 域×2 版本=194,300，自洽）。本件所有读数按单版本（v2）口径；快照批次恒为 `metrics_as_of_date=2026-10-16` 单值，即「本轮评估」有明确的时间锚。这一步避免的最大陷阱是把 194,300 当证据量基数——数字翻倍而语义错。

### 2.2 域级证据量：十域台账实测

`SELECT domain_code, COUNT(*), SUM(evidence_count), AVG(evidence_count) … GROUP BY domain_code`（产物键 `jiuxin_data_coverage_by_domain`）：PAPER 108,479 / PATENT 1,071,763 / INSTITUTION 2,528,802 / ENTERPRISE 99,821 / LOCATION 1,354,081 / PROJECT 181,735 / APPLICATION_CASE 181,735 / **MARKET 0 / POLICY 0 / TRANSLATION 0**。三个零域各有状态注记（产物键 `jiuxin_data_coverage_status_dist` 与单节点样本）：MARKET/POLICY 是 `NOT_AVAILABLE`（「No registered immutable source」——源头未注册），APPLICATION_CASE 常态是 `NO_MATCHED_EVIDENCE`（「Research projects are evidence cases, not confirmed market application」——科研项目被当作案例代理），另有 13,415 行 `RESEARCH_PROJECT_PROXY` 明示代理状态。台账的诚实度值得肯定：缺什么、为什么缺、用什么代理，都在 coverage_status/coverage_note 两列写明，这比一个只报喜的计数表对评估工作流更有用。

### 2.3 证据明细与图谱规模（交叉校验）

证据侧三读数互相咬合：`ads_technology_assessment_evidence` 269,882 条（PAPER 102,766 / PATENT 95,170 / RESEARCH_PROJECT 71,946，`evidence_quality` 全量 TRACEABLE_INTERNAL_FACT、`evidence_direction` 全量 SUPPORTING）；`ads_technology_potential_evidence` 同为 269,882 行（与 assessment_evidence 逐行同构，双表冗余存储）；图谱侧 `graph_node` 19,430（与节点总数同基）+ `graph_edge` 587,252。校验关系：evidence 明细的论文/专利/项目三类计数 ≤ data_coverage 对应域证据量（102,766≤108,479、95,170≤1,071,763、71,946≤181,735），方向正确——明细是被评估引用的子集。这三组数字构成「收集量」读数的立体剖面：域台账给总量、明细表给引用量、图谱给关联规模。

### 2.4 五源对齐：UI 语义的逐源比对

把 UI 声明的五源（论文/专利/项目/资讯/知识图谱）映射到台账域：论文→PAPER（108,479>0 ✓）、专利→PATENT（1,071,763>0 ✓）、项目→PROJECT（181,735>0 ✓）、资讯→MARKET+POLICY（0+0=0 ✗）、知识图谱→graph_edge（587,252>0 ✓）。对齐率 `jiuxin_ui5source_align_rate_pct` = 4/5 = **80.0%**（产物 derived 键，分子分母同源同轮）。注意这是「有量/无量」的二值对齐，不度量质的覆盖；资讯源不是量小而是结构性为零——三库（dev/gkx/jiuxin）的评估链路里都没有它的位置（§3.4 探针）。

### 2.5 开发库与 gkx 侧的源可用性（非评估链的存量）

共享快照（`_shared_probe_s3_01_out.json`）与第五轮探针确认：gkx 有论文底表 `dwd_zh_paper` 100,900 行、新闻 `dwd_news_base` 20,000 行、政策 `dwd_policy_base` 20,000 行——存量存在但未接入久新技术评估链（久新论文域证据来自 OpenAlex 系，与 gkx 中文论文池是两个数据面）；开发库 `gkxlumenx_dwd` 无论文表、无资讯表（SHOW TABLES LIKE '%paper%' 命中 0）。这条读数划清了「库里有资讯数据」与「评估工作流接入了资讯源」的界线：前者真（gkx），后者假（三源皆无）。

### 2.6 稳健性与口径敏感性

两个口径陷阱：其一，PROJECT 与 APPLICATION_CASE 两域恒等（181,735=181,735），因 case_type 单值 RESEARCH_PROJECT、项目被 1:1 复用为应用案例（`ads_technology_application_case` 181,735 行全为 RESEARCH_PROJECT）——「项目源」和「应用案例源」名义两域、实为一源，五源对齐若按域数算会虚增；其二，TRANSLATION 域恒 0 是翻译流水线未发布（「Unified reviewed translation has not been published」），与技术证据无关，不应计入收集量叙事。本件的五源对齐已按 UI 原文五源映射，未把 APPLICATION_CASE/TRANSLATION 混入。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TECHTRK_014.py`（直连久新只读，全 SQL 留档产物；运行 `python3 code/M_SCIUI_TECHTRK_014.py`）。
- 产物：`code/M_SCIUI_TECHTRK_014_out.json`。正文数字与产物键逐一对应：`jiuxin_ads_technology_profile_rows=19430`（§2.1）、`jiuxin_data_coverage_by_domain` 十域（§2.2）、`jiuxin_assessment_evidence_by_type` 三类（§2.3）、`jiuxin_graph_edge_rows=587252`（§2.3）、`derived.jiuxin_ui5source_align_rate_pct=80.0`（§2.4）。
- 结果解读：四源足量、一源结构性缺失；证据台账诚实标注缺失原因，可直接驱动 UI 环节 tooltip。
- 对照需求功能要求的评审：五环节流程条的「数据收集 completed」状态——部分满足（四源可出量、资讯源无读数，建议 completed 状态加来源覆盖注记）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 版本 | 单版本节点数 | `jiuxin_data_coverage_node_count` | 19,430 |
| 台账 | 论文域证据量 | `jiuxin_data_coverage_by_domain[PAPER].evidence_sum` | 108,479 |
| 台账 | 专利域证据量 | `…[PATENT].evidence_sum` | 1,071,763 |
| 台账 | 机构域证据量 | `…[INSTITUTION].evidence_sum` | 2,528,802 |
| 台账 | 资讯双域 | `…[MARKET]/[POLICY].evidence_sum` | 0 / 0 |
| 明细 | 证据行数 | `jiuxin_assessment_evidence_rows` | 269,882 |
| 明细 | 三类分布 | `jiuxin_assessment_evidence_by_type` | 102,766/95,170/71,946 |
| 图谱 | 边规模 | `jiuxin_graph_edge_rows` | 587,252 |
| 对齐 | 五源对齐率 | `derived.jiuxin_ui5source_align_rate_pct` | 80.0%（4/5） |
| absence | 资讯源三库探针 | §3.4 四件套 | 全部命中 0 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 域级证据台账 | jiuxin | `ads_technology_data_coverage` | 194,300（单版本 19,430×10 域） | 直查 | **有** |
| D2 | 可溯源证据明细 | jiuxin | `ads_technology_assessment_evidence` | 269,882 | 直查 | 有 |
| D3 | 知识图谱 | jiuxin | `graph_node`/`graph_edge` | 19,430 / 587,252 | 直查 | 有 |
| D4 | 资讯源（评估链内） | dev / gkx / jiuxin | —（MARKET/POLICY 域恒 0；203 表无 news 类） | 0 | **不存在** | **缺（主降档因）** |
| D5 | 资讯源（链外存量） | gkx | `dwd_news_base`/`dwd_policy_base` | 20,000 / 20,000 | 存量有、未入链 | 修复素材 |

`support_judgment="部分支持"` 与文首一致（闸 6 对齐）。

### 3.2 D1 十域台账：本轮评估的证据底盘

单版本口径下十域证据量见 §2.2；域×状态交叉揭示结构：AVAILABLE 102,347 行（五域常态足量）、NOT_AVAILABLE 58,290 行（MARKET/POLICY/TRANSLATION 三域恒缺）、NO_MATCHED_EVIDENCE 20,248 行（APPLICATION_CASE/ENTERPRISE/PROJECT 部分节点无匹配）、RESEARCH_PROJECT_PROXY 13,415 行（项目代理显式标注）。台账把「有/无/代理」三态写进数据，评估工作流若要展示收集量，建议同构透出三态而非单一总数。

### 3.3 D2+D3 明细与图谱：可溯源与可关联

269,882 条证据全量 TRACEABLE_INTERNAL_FACT+SUPPORTING——本轮评估只引用内部可溯源事实，方向全部支持（无 CONTRADICTING 反证位使用），这与 baseline 场景定位一致；图谱 19,430 节点与 profile 同基、587,252 边支撑「知识图谱接入」读数。两组数字与 D1 的包容关系校验通过（§2.3）。

### 3.4 D4 资讯源 absence_probe 全记录

否定性证据四件套：**查了什么**——① dev `gkxlumenx_dwd` 按 coverage/collect/assess/score/potential/hotspot/heat/maturity/tech 关键词 SHOW TABLES 扫描（`_probe_lane3_gkx_out.json`）；② gkx 280 表按 assess/evaluation/score/coverage 关键词扫描；③ 久新 203 表 SHOW TABLES 后本地过滤 news/media/literature/report；④ 久新 data_coverage MARKET/POLICY 域 SUM 实测。**条件**——评估链路内的资讯类结果面/证据域。**命中**——0/0/0/0（四路全空；gkx 的 `dwd_news_base` 20,000 行存在但在②之外，属链外存量，已单列 D5）。四缺失情形归属：**表不存在**（dev/gkx 评估侧）+**域未注册源**（jiuxin MARKET/POLICY 的 NOT_AVAILABLE 注记），修复动作是接入而非补数。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 版本去重 | 194,300 = 19,430×10×2 版本，自洽 |
| 十域 SUM | PAPER 108,479 / PATENT 1,071,763 / MARKET 0 等，与 profile 汇总列同值 |
| 证据明细包容 | 102,766≤108,479 等三类校验通过 |
| 图谱规模 | node 19,430 = profile 行数；edge 587,252 |
| 资讯三库 | dev 0 表 / gkx 链外 2 表 / jiuxin 0 域，探针留档 |
| 脚本形态 | 单进程顺序查询，只读，零 demo_* |

## 四、数据缺失情况

### 4.1 资讯源结构性缺失（主因）

UI 五源声明的「资讯」在评估链内三库皆无承载（§3.4 四路探针）。这不是量小，是结构为零：久新源头未注册（NOT_AVAILABLE 注记原文「No registered immutable source」）、dev/gkx 无评估侧表。四缺失情形归属：源级缺失。修复路径唯一且明确：把 gkx `dwd_news_base`（20,000 行）/`dwd_policy_base`（20,000 行）注册为久新评估链的 MARKET/POLICY 源（需对齐 technology_node_id 的主题映射，工程量在映射不在管道），或由甲方裁定资讯源降级出数。

### 4.2 历史轮次缺失（次因，与 015/022 共享）

data_coverage 等表为单轮快照（2026-10-16），无 2023–2025 轮次台账——「收集量逐轮增长」的工作流叙事无数据面。这属于快照表设计（每轮重建），修复需久新侧保留轮次分区，展示系统侧无法自愈。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| gkx 资讯底表注册入链 | 数据工程 | 本件（资讯源）→ 升档 | MARKET/POLICY 转 AVAILABLE，五源对齐 80%→100% |
| 三态透出（有/无/代理） | 产品决策 | 本件即期 | tooltip 同构 coverage_status，零新工程 |
| 轮次分区保留 | 上游改造 | 本件+015+022 | 历史收集量序列 |

三条路径的档位后果：资讯入链 → 完全转换支持（五源全有量+台账结构在）；三态透出 → 语义闭合维持部分支持；轮次分区 → 解锁 022 历史叙事。推荐组合：即期三态透出，中期资讯入链。

## 参考文献

1. Strategic intelligence tools for emerging technology governance[EB/OL]. OECD, 2025. https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/07/strategic-intelligence-tools-for-emerging-technology-governance_b7009977/02c05775-en.pdf （R1，2026-11-01 WebSearch 核验可达）
2. Building capacity in technology horizon scanning[EB/OL]. OECD, 2026. https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/04/building-capacity-in-technology-horizon-scanning_7a0a98c6/b4f0d383-en.pdf （R2，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》seq 52（excel_row 55）：

> 以流程图形式展示技术评估的完整工作流程，包括评估准备、数据收集、方法选择、分析计算、结果生成等关键环节。用户可点击各环节查看详细说明和操作指南，支持高亮显示当前评估进度，提供流程导航功能快速定位特定评估阶段。

《科技信息展示系统和科技专题服务系统.md》:421 为同段复述。三份指定说明书中「评估数据收集量」指标名未出现；「数据收集」仅作为环节名列出，无任何量的定义。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 评估数据收集量 | 三份指定 SRS + 主文档 | 0 |
| 数据收集 | 技术发展跟踪.md:78（seq 52 功能描述）；主文档:421 | 2（均为环节名，非指标定义） |
| 收集量 | 全部需求文档 | 0 |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_014_out.json`（2026-11-01 实跑：十域台账、证据三读数、图谱规模、五源对齐率）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（gkx `dwd_zh_paper`=100,900、`dwd_news_base`=20,000、`dwd_policy_base`=20,000；dev 论文表 0）。
- 本 Lane 新增探针快照：`_probe_lane3_jiuxin_out.json`（203 表清单+DESC+样本）、`_probe_lane3_jiuxin2_out.json`（12 候选表 DESC/COUNT）、`_probe_lane3_jiuxin3_out.json`（值分布）、`_probe_lane3_jiuxin4_out.json`（口径审计）、`_probe_lane3_gkx_out.json`（gkx/dev 关键词扫描）、`_probe_lane3_final_out.json`（图谱/协作/资讯扫描）、`_probe_lane3_jiuxin6_out.json`（协作表）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_TECHTRK_014 | 文首 |
| `ui_evidence` | 证据 | techDevelopmentTracking.js:1100 等 2 条 | §1.1/§1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.jiuxin_ads_technology_profile_rows` | 计数 | 19,430 | §2.1 |
| `facts.jiuxin_data_coverage_rows` | 计数 | 194,300 | §2.1/§3.2 |
| `facts.jiuxin_data_coverage_node_count` | 计数 | 19,430 | §2.1 |
| `facts.jiuxin_data_coverage_by_domain` | 分布 | 10 域含 evidence_sum | §2.2/§3.2 |
| `facts.jiuxin_data_coverage_status_dist` | 分布 | 4 状态 | §2.2/§3.2 |
| `facts.jiuxin_assessment_evidence_rows` | 计数 | 269,882 | §2.3/§3.3 |
| `facts.jiuxin_assessment_evidence_by_type` | 分布 | PAPER/PATENT/RESEARCH_PROJECT | §2.3 |
| `facts.jiuxin_graph_node_rows` / `…_edge_rows` | 计数 | 19,430 / 587,252 | §2.3/§3.3 |
| `facts.gkx_dwd_zh_paper_rows_shared_snapshot` 等 3 键 | 快照引用 | 100,900/20,000/20,000 | §2.5 |
| `derived[0]` | 派生比 | jiuxin_ui5source_align_rate_pct = 80.0 | §2.4 |
| `absence_probe` | 负证据 | 4 条（dev/gkx/jiuxin×2） | §3.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `base_years_*` | 年份 | used=[2026]，missing=[2025,2024] | §4.2 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表文献/机构 | 量化对象 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 证据台账法 | OECD 信号扫描体系（R1/R2） | 分源信号量+可靠性 | data_coverage 十域三态 | **最高（现状即实现）** |
| 数据资产盘点 | 数仓元数据惯例 | 表行数+批次 | data_version/metrics_as_of_date | 中（辅助） |
| 状态位法 | 本项目 UI 现状 | 布尔 | workflow.status | 低（无信息量） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| data_coverage | 194,300（单版本 19,430×10） | 三态诚实标注 | MARKET/POLICY 恒 0 |
| assessment_evidence | 269,882 | 全量可溯源 | 无反证位使用 |
| graph_node/edge | 19,430 / 587,252 | 与 profile 同基 | — |
| gkx 资讯存量 | 20,000×2 表 | 链外 | 未注册入链 |
| 轮次 | 单轮 2026-10-16 | — | 无历史分区 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 四源收集量 + 三态 tooltip | 无 |
| v2 | gkx 资讯底表注册入链（五源 100%） | 主题映射工程 |
| v3 | 轮次分区→收集量增长序列 | 久新上游改造 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 双版本行数误读（194,300≠证据量） | 中 | 产物 note 写死单版本口径 |
| PROJECT/APPLICATION_CASE 双域同源误计 | 中 | 五源映射按 UI 原文，不按域数 |
| 资讯域 0 被读成「暂未更新」 | 低 | NOT_AVAILABLE 注记透出 |

### C.5 总判

**部分支持**：四源足量（论文 108,479/专利 1,071,763/项目 181,735/图谱边 587,252）、一源结构性为零（资讯），单轮快照无历史序列；升档触发器（资讯入链）与保守交付口径（三态透出）已写死 §1.6。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_014.py` | 退出码 0，落 `_out.json` |
| 数据入口 | 久新 Doris 直连（只读） | 203 表只读访问 |
| 域台账 | `facts.jiuxin_data_coverage_by_domain` | 10 域，MARKET/POLICY=0 |
| 五源对齐 | `derived.jiuxin_ui5source_align_rate_pct` | 80.0 |
| 共享快照对账 | `_shared_probe_s3_01_out.json` | gkx 三表行数零漂移 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 均为部分支持 |
| 负证据探针 | `absence_probe` 4 条 | 全部留 SQL 与命中数 |
| demo 禁引 | 脚本 grep demo_ | 0 命中 |

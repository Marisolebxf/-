# 技术潜力评估得分（M_SCIUI_TECHTRK_016）

> **类型**：SCORE（加权综合评分，六维体系）｜ **域**：科技发展态势·技术发展跟踪·潜力评估（UI 侧挂科技发展规划页维度）｜ **UI 挂载**：`techDevelopmentPlan.js:307`（规划维度雷达「潜力评估」）+ `techDevelopmentPlan.js:483`（详情卡「潜力评估」行）
> **数据支持度**：**部分支持**｜ **公式定义人**：库侧既成（久新 DETERMINISTIC_PERCENTILE_MODEL 六维加权）+ 工程侧映射定义（UI 维度↔库维度）｜ **口径归属**：需求未明列叶（三份指定说明书未出现指标名），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TECHTRK_016.py`｜ **产物**：`code/M_SCIUI_TECHTRK_016_out.json`
> **四判定摘要**：直接结构 = 是（久新 potential_assessment/dimension/evidence 三表族结构完整：总分+六维分+权重+加和可复算）；直接数据 = 是（19,430 节点全量有分、权重覆盖 100%）；依赖结构 = 部分（单场景 BASELINE，无可配置场景轴）；依赖数据 = 部分（单轮快照无历史；UI 区域粒度无承载）
> **数据源口径注记**：三源评估——开发库（`gkxlumenx_*`，禁 `demo_*`）+ gkx（只读 280 表）+ 久新 jiuxin_warehouse（只读 203 表）。本件主数据面在久新。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（三源）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 本批 5 件中数据面最强的一件：久新 `ads_technology_potential_assessment` 族三表构成教科书式的潜力评分体系——总分 potential_score（0-100，min 10.96/max 88.35/avg 44.87）、六维加权（SCIENTIFIC_SCALE 0.2 / SCIENTIFIC_GROWTH 0.2 / PATENT_CONVERSION 0.2 / SCIENTIFIC_IMPACT 0.15 / INDUSTRY_PARTICIPATION 0.15 / PROJECT_EVIDENCE 0.1，合计 1.0）、每维 raw_value→dimension_score→weighted_score 全链路、加和一致性 19,430/19,430 节点可复算、百分位与权重覆盖（恒 1.0）齐备，且 269,882 条证据可溯源。dev/gkx 探针零命中，三源中唯一承载。降档不在「有没有分」而在两个结构缺口：其一，scenario 轴只有 BASELINE 单值——UI 的「潜力评估」维度挂在多区域规划记录（深圳/大湾区/北京等）与科技发展规划页，库侧没有按区域/场景裁剪的评估面；其二，单轮快照（2026-10-16），UI 时间轴 2020–2026 的历史潜力分无承载。分数本身完全直接支持，维度语义与展示粒度的适配是部分支持。

### 批次纪律摘要（B1–B11 对照，skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 三派生键分子分母同源同版本（jiuxin v2） |
| B4 | 负结论带探针 | absence_probe 四条（dev/gkx 结果面、场景轴、轮次轴） |
| B5 | 确定性 | 聚合 ORDER BY dimension_code；单节点样本取 MIN(node_id) 确定性锚 |
| B6 | 闸门自身被闸 | 本件不跑闸门，派单方统一跑 |
| B7 | 产物只由脚本产出 | 实跑产出，无手改 |
| B8 | 回执不复收 | 加和一致率/v1v2 同分亲自实跑 |
| B9 | 单位/日期陷阱 | 单轮 2026-10-16；双版本去重；raw_value 可空（None）但 dimension_score 全有 |
| B10 | 口径裁定保守交付 | 「BASELINE 场景分」vs「区域裁剪分」双口径（§1.6） |
| B11 | 多本账互推 | 38,860/233,160/269,882 与共享快照及 015 件零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 潜力分存在吗？ | 存在且全量 | 19,430 节点 100% 有分，权重覆盖恒 1.0 |
| 评分体系可复算吗？ | 可 | 加和一致 19,430/19,430（`jiuxin_weighted_sum_consistent_nodes`） |
| 场景/轮次轴齐全吗？ | 不齐 | scenario 单值 BASELINE；单轮快照（探针） |

## 摘要

「技术潜力评估得分」在 UI 出现在两处：规划维度雷达的「潜力评估」维（权重 24%，描述「竞争力、发展潜力和宏观态势预测」）与规划记录详情卡「潜力评估」行（mock 值 80–95 分）。库侧实测给出三件硬货：一、`ads_technology_potential_assessment` 为 19,430 个技术节点全部评出 potential_score（0–100），方法标注 DETERMINISTIC_PERCENTILE_MODEL（确定性百分位模型）、场景 BASELINE、状态 ASSESSED；二、评分结构完全透明——`ads_technology_potential_dimension` 六维各带权重（科研规模 0.2/科研增长 0.2/专利转化 0.2/科研影响 0.15/产业参与 0.15/项目证据 0.1），weighted_score 加和与总分逐节点一致（19,430/19,430），单节点样本全链路（raw→维分→加权）可复算；三、每个分数有 269,882 条证据背书（与 014/015 件同源）。缺口同样明确：dev/gkx 零命中（探针留证），场景轴单值（不能按 UI 的区域/规划记录裁剪），单轮快照（无历史序列）。判**部分支持**：分数与公式即取即用，展示粒度适配与历史序列是两个待裁定项。

- 需求判定：需求未明列叶（展示系统三份说明书未出现；科技专题服务系统板块有近义功能叶，跨板块另计）。
- 复现状态：脚本已跑通；分数统计、六维权重、加和审计、单节点样本落产物。
- 档位结论：**部分支持**（分数直接支持，场景轴/轮次轴双缺）。
- 关键事实：v1 与 v2 两版本逐节点同分（19,430/19,430）——版本轴是冗余不是迭代，读数按单版本。
- 升档路径：scenario 轴扩充（区域/主题场景入库）→ 完全直接支持可期。

## 一、需求定义概述

### 1.1 所属功能模块

本件 UI 挂载在科技发展规划页（非技术发展跟踪页），但指标属技术发展跟踪域的潜力评估概念在规划页的复用：`techDevelopmentPlan.js:307` 的 `buildPlanDimensions()` 把「潜力评估」列为五大规划维度之一（key=potential，label=潜力评估，description=「竞争力、发展潜力和宏观态势预测」，score 取 records 的 potential 均值，weight=24%）；`techDevelopmentPlan.js:483` 的详情卡「规划判断」节给每条规划记录一行「潜力评估」（value=record.potential）。数据源是 `planRecords` 常量（45–171 行）：七条记录各带 potential 字段（92/95/86/88/90/87/80，演示值），另 `buildMetrics()` 296 行出「潜力均值」指标卡（average(records,'potential')）。

结构上的关键观察：UI 的潜力分是**记录级**属性——每条规划记录（如「全球智能机器人热点捕捉」92 分、「大湾区合成生物重点领域布局」95 分）自带一个 0-100 分，维度雷达把它聚成均值。而库侧的潜力分是**技术节点级**属性（19,430 个 tcn_* 节点各一分）。两个粒度之间需要一道「技术节点→规划记录」的映射（规划记录本质是区域×领域×年度的切片），这道映射三库皆无——这正是本件降档的展示侧根因。

### 1.2 为什么需要本指标

潜力分回答的是「下一步往哪投」：热度告诉now、成熟度告诉ready、潜力告诉next。规划页把它列进五大维度并给 24% 权重（五维中第二高），且在详情卡单列一行，说明业务叙事里「这个方向值不值得布局」主要由潜力分背书。库侧六维体系的价值在于潜力分不是黑箱：专利转化 0.2 + 科研增长 0.2 的权重结构明示「既要已验证的转化能力、也要仍在涨的科研势头」——这个可解释性是它对 mock 常量的本质优势。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。** 展示系统三份指定说明书未出现「技术潜力评估得分」。需求文档体系里的近义功能叶在**科技专题服务系统**板块：《技术链分析.md》seq 17「潜力评估模型计算」（功能描述「本功能基于多维指标构建潜力评估模型，支持用户对技术的商业化前景进行量化评分与横向对比…融合专利、论文等产业化数据，建立可配置的潜力评估体系」）与《可视化管理.md》seq 291「科技潜力评估可视化」（潜力矩阵图/风险与收益对比图）——描述了「多维指标+可配置体系」的定性要求，同样无公式、无权重、无维度清单。主需求文档 4285/4289 行为同段。这些是跨板块的方法参考，不构成本件的直接需求定义。

### 1.4 类似指标权威方法可行性分析概要

潜力评估的权威方法族与 015 件共享谱系但侧重不同：OECD/JRC 复合指标手册（R1）的十步流程是本件库侧实现的直接印证——理论框架（六维选定）→标准化（raw→dimension_score）→加权聚合（权重列+weighted_score）→稳健性（percentile 列）；Oslo 手册（R2）对 min-max 标准化与差异权重的统计规范对应 dimension_score 的生成；NASA TRL（R3）提供「阶段」视角，是潜力分的好搭档（库侧 stage_code 恰好补位）。方法族对照：

| 方法族 | 代表 | 潜力侧形态 | 与本库匹配 |
|---|---|---|---|
| 确定性加权百分位 | OECD/JRC 十步法（R1） | 六维加权 0-100 | **库侧现状即此**（DETERMINISTIC_PERCENTILE_MODEL） |
| 可配置场景评估 | 需求原文（seq 17「可配置」） | scenario 轴 | **无**（BASELINE 单值） |
| 阶段+潜力双轨 | NASA TRL（R3） | 档位+分 | 有（stage 表互补） |

结论：方法学上库侧已达到权威手册的推荐形态，缺口在「可配置」这一需求侧要求。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/techDevelopmentPlan.js:307`（维度雷达）、`:483`（详情卡行）、`:296`（潜力均值卡）、`:45-171`（planRecords mock）。
- SRS：展示系统三份说明书未出现指标名（检索记录见附录 A）；跨板块参考《04-科技专题服务系统/科技专题战略分析/技术链分析.md》seq 17。
- 主需求文档：《科技信息展示系统和科技专题服务系统.md》:4285-4289（潜力评估模型计算，跨板块段）。

### 1.6 推测原意与推测定义

**推测定义（双口径并列，B10）**：

- 口径 A（**BASELINE 场景技术潜力分**，库侧现状）：`potential(node) = Σᵢ wᵢ·scoreᵢ`，六维权重 (0.2,0.2,0.2,0.15,0.15,0.1)，场景 BASELINE、轮次 2026-10-16——直接可查，UI 技术详情位可用；
- 口径 B（**区域/规划记录裁剪分**，UI 语义）：`potential(region_slice) = AVG(potential(node) FOR node IN slice)`——需「规划记录→技术节点集」映射，三库无此映射表。

**维度映射（推测，需甲方确认）**：UI 记录级 potential ↔ 库侧区域×领域切片的节点分均值（口径 B）；维度雷达「潜力评估」↔ 切片均值再聚合。**降档/升档触发器**：若甲方接受口径 A（技术粒度潜力分先上线，规划记录暂以代表技术节点填充）→ 维持部分支持但两处挂载可填数；若久新扩充 scenario 轴（按区域/主题建场景）→ 口径 B 半自动化；若同时保留轮次 → 历史潜力序列补齐，升完全直接/转换支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 展示系统 SRS | 三份指定说明书未出现指标名（本件为 UI 驱动叶） |
| 跨板块参考叶 | 《技术链分析.md》seq 17「潜力评估模型计算」；《可视化管理.md》seq 291「科技潜力评估可视化」（均科技专题服务系统板块） |
| UI 容器 | 科技发展规划页：维度雷达（307）/ 详情卡（483）/ 指标卡（296） |
| 批内关系 | 与 015 共享分数（同值审计 100%）；与 018 共享潜力语义（018 的「发展潜力」卡）；014 的证据表为其背书 |

批内坐标：016 是 Lane 3 的「分数枢纽」——上游吃 014 的证据台账，下游喂 015 的矩阵行与 018 的潜力卡。三件共用「单轮快照」缺口，升档工程同一。

## 二、计算过程

### 2.1 装载与三表族结构

直连久新 Doris（只读）。表族三件：`ads_technology_potential_assessment`（38,860 行=19,430 节点×2 版本；assessment_id/总分/排名/百分位/权重覆盖/方法/状态）、`ads_technology_potential_dimension`（233,160 行=19,430×6 维×2 版本；dimension_code/raw_value/dimension_score/dimension_weight/weighted_score/coverage_status）、`ads_technology_potential_evidence`（269,882 行，evidence_type/evidence_year/evidence_summary/方向/质量）。三表以 technology_node_id+model_version 关联，版本审计：v1 与 v2 逐节点同分（`jiuxin_v1_v2_same_score_nodes`=19,430/19,430），全表读数按单版本。

### 2.2 六维权重体系实测

v2 单版本维度分布（产物键 `jiuxin_potential_dimensions_v2`）：六维各 19,430 行，权重恒定——SCIENTIFIC_SCALE 0.2 / SCIENTIFIC_GROWTH 0.2 / PATENT_CONVERSION 0.2 / SCIENTIFIC_IMPACT 0.15 / INDUSTRY_PARTICIPATION 0.15 / PROJECT_EVIDENCE 0.1，合计 1.0（派生键 `jiuxin_dimension_weight_sum`）。权重结构读作：三根支柱各两成（科研规模、科研增长、专利转化），两翼各一分半（科研影响、产业参与），项目证据一成垫底——转化与增长并重的设计，与「潜力=未来变现能力」的语义自洽。

### 2.3 单节点全链路复算（评分透明性验证）

取确定性锚节点（MIN(technology_node_id)=tcn_0000a456…，产物键 `jiuxin_potential_dimension_sample_node`）复算全链路：INDUSTRY_PARTICIPATION raw=0→维分 0→加权 0×0.15=0；PATENT_CONVERSION raw=2→维分 21.704668→加权 4.340934；PROJECT_EVIDENCE raw=0→0；SCIENTIFIC_GROWTH raw=None（空）→维分 75.876267→加权 15.175253（raw 空但维分有值，说明维分生成在 raw 归一化层之上、不依赖单列 raw 完整性，coverage_status=AVAILABLE）；SCIENTIFIC_IMPACT raw=None→21.817901→3.272685；SCIENTIFIC_SCALE raw=3→24.643574→4.928715。六维加和=27.717587=该节点总分（抽样核对产物键 `jiuxin_weighted_sum_consistent_nodes` 的逐节点版）。全量审计：19,430/19,430 节点 |Σweighted_score − potential_score|<0.0001——评分体系逐节点可复算，这在三库评估面里是唯一做到「公式级透明」的。

### 2.4 与 015 件的同值审计（跨表冗余披露）

stage 表 development_potential_score 与本表 potential_score 逐节点同值（38,860/38,860，015 件已审计）。含义：两表是同一管线的双视图——stage 表带解释文本（瓶颈/风险/建议），本表带结构分解（六维+百分位+权重覆盖）。UI 引用建议：详情卡「潜力评估」行取本表分、瓶颈行取 stage 表文本，一套分数两个视角，不重复计数。

### 2.5 场景轴与轮次轴核查

两路探针：scenario_id DISTINCT 单值 BASELINE（38,860 行全同）；metrics_as_of_date 单值 2026-10-16。结合 1.1 的粒度分析：UI 需要的「规划记录→技术节点集」映射（口径 B）在库侧等价于 scenario 轴的区域化——当前无承载。dev 侧 `evaluation_template`（8 行，indicators_json/weights_json）倒是「可配置权重」的参数容器（对应 SRS seq 54 评估参数配置），但它是模板不是结果面，且挂在 topic_enterprise 库与久新无管道。

### 2.6 稳健性与口径敏感性

分数分布对展示的含义：avg 44.87、max 88.35、无满分节点——确定性百分位模型的分布天然压中心，UI 若沿用 mock 的 80+ 观感需要重设分档文案（如 ≥70 高潜力 / 45–70 中 / <45 观察池）。raw_value 可空（SCIENTIFIC_GROWTH/IMPACT 样本节点 raw=None）但维分恒有——引用维分时不必做缺值处理，引用 raw 时需注意。百分位列（potential_percentile）min/max 已入产物，可与排名列（potential_rank）互校。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TECHTRK_016.py`（直连久新只读；运行 `python3 code/M_SCIUI_TECHTRK_016.py`）。
- 产物：`code/M_SCIUI_TECHTRK_016_out.json`。正文数字与产物键逐一对应：`jiuxin_potential_assessment_rows_total=38860`（§2.1）、`jiuxin_potential_dimensions_v2` 六维权重（§2.2）、`jiuxin_potential_dimension_sample_node` 全链路（§2.3）、`jiuxin_weighted_sum_consistent_nodes=19430`（§2.3）、`jiuxin_v1_v2_same_score_nodes=19430`（§2.1）、`jiuxin_potential_score_stats_v2`（§2.6）、派生 `jiuxin_potential_avg_score_v2=44.871899` / `jiuxin_dimension_weight_sum=1.0` / `jiuxin_score_span_pct=77.394874`。
- 结果解读：分数、公式、权重、证据四位一体全量可查，是三库评估面中唯一公式级透明的体系。
- 对照需求功能要求的评审：「多维指标构建潜力评估模型+量化评分+横向对比」（跨板块 seq 17 语义）——多维✓（六维）、量化✓（0-100）、可配置✗（单场景）、横向对比✓（rank/percentile 列）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 结构 | 总分表行数 | `jiuxin_potential_assessment_rows_total` | 38,860 |
| 结构 | 单版本节点 | `jiuxin_potential_assessment_nodes_single_version` | 19,430 |
| 体系 | 六维权重 | `jiuxin_potential_dimensions_v2` | 0.2×3+0.15×2+0.1，合计 1.0 |
| 复算 | 加和一致节点 | `jiuxin_weighted_sum_consistent_nodes` | 19,430/19,430 |
| 复算 | 样本节点全链路 | `jiuxin_potential_dimension_sample_node` | 六维 raw→score→weighted |
| 版本 | v1v2 同分 | `jiuxin_v1_v2_same_score_nodes` | 19,430 |
| 冗余 | stage 同值 | `jiuxin_stage_vs_potential_same_rows` | 38,860 |
| 证据 | 证据行数 | `jiuxin_potential_evidence_rows` | 269,882 |
| 分布 | 分数统计 | `jiuxin_potential_score_stats_v2` | 10.96/88.35/44.87 |
| absence | 场景轴/轮次轴 | §3.4 四件套 | 单值/单值 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 潜力总分 | jiuxin | `potential_assessment.potential_score` | 19,430（单版本全量） | 直查 | **有** |
| D2 | 维度分解 | jiuxin | `potential_dimension` 六维 | 116,580（单版本） | 直查 | 有 |
| D3 | 证据背书 | jiuxin | `potential_evidence` | 269,882 | 直查 | 有 |
| D4 | 场景轴（区域/主题裁剪） | 三库 | —（scenario 单值 BASELINE） | — | **不存在** | **缺（主降档因）** |
| D5 | 轮次轴 | 三库 | —（单轮 2026-10-16） | — | 不存在 | 缺 |

`support_judgment="部分支持"` 与文首一致（闸 6 对齐）。

### 3.2 D1–D3 分数体系：三库唯一的公式级透明评分

§2.1–§2.4 已列全。强调一点工程价值：加和一致性意味着前端可以自建「维度贡献分解图」（总分拆六维、每维显权重），不需要任何后端配合——这是六维表结构透出的免费红利。

### 3.3 D4 场景轴：从技术粒度到展示粒度的断层

UI 挂载点是规划记录（区域×领域切片），库侧分数是技术节点粒度。断层两侧各有一个半解：库侧 scenario 轴（扩充场景即切片）；展示侧映射表（规划记录→节点集，可用 profile 的 domains_raw/fields_raw+region_assessment 的 location 间接拼，但无现成表）。B10 双口径（§1.6）已把两个半解摆平：先口径 A 上线、scenario 扩充后口径 B 接管。

### 3.4 D4/D5 场景轴与轮次轴 absence_probe 全记录

否定性证据四件套：**查了什么**——① dev `gkxlumenx_dwd` potential/score 关键词（0 命中，评估类仅政策侧）；② gkx 280 表 potential 关键词（0 命中）；③ jiuxin scenario_id DISTINCT（单值）；④ jiuxin metrics_as_of_date DISTINCT（单值）。**条件**——多场景/多轮次潜力评估面。**命中**——0/0/1 单值/1 单值。归属：**结果面结构缺失**（场景列在但无枚举值填充；轮次属快照设计），修复在上游管线非展示侧。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 三表行数 | 38,860 / 233,160 / 269,882，=19,430×(2/12/…) 自洽 |
| 权重合计 | 0.2×3+0.15×2+0.1=1.0 |
| 加和审计 | 19,430/19,430 一致 |
| v1v2 同分 | 19,430/19,430 |
| stage 同值 | 38,860/38,860 |
| 样本链路 | raw(None)→维分有值 特性确认 |
| 脚本形态 | 只读、零 demo_*、确定性锚 |

## 四、数据缺失情况

### 4.1 场景轴缺失（主因）

scenario 单值 BASELINE，无区域/主题/规划场景。「可配置的潜力评估体系」（跨板块需求原文）的可配置部分缺失。修复路径：久新侧按 location×domain 组合建 scenario 枚举（region_assessment 已有 7,816 个 location 与节点关联，素材在库），工程量在评估管线重跑非新数据采集。

### 4.2 轮次轴缺失（次因）

单轮快照。潜力分的时序价值（「潜力在涨还是在跌」）无法表达，UI 趋势序列的「潜力」线无历史。与 015/022 共享缺口，修复同源。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 先行（节点分+六维分解图） | 产品决策 | 本件即期 | 零上游依赖，维度贡献图免费红利 |
| scenario 轴区域化 | 上游管线 | 本件+018 | region_assessment 素材在库 |
| 轮次快照保留 | 上游改造 | 本件+015+022 | 时序潜力线 |

档位后果：口径 A → 部分支持语义闭合上线；scenario 扩充 → 口径 B 可算，逼近完全转换支持；轮次齐 → 完全直接/转换支持。推荐：即期口径 A，中期 scenario 区域化。

## 参考文献

1. Handbook on Constructing Composite Indicators: Methodology and User Guide[EB/OL]. OECD/JRC, 2008. https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf （R1，2026-11-01 WebSearch 核验可达）
2. Use of innovation data for statistical indicators and analysis: Oslo Manual 2018[EB/OL]. OECD. https://www.oecd.org/en/publications/oslo-manual-2018_9789264304604-en/full-report/component-18.html （R2，2026-11-01 WebSearch 核验可达）
3. Technology Readiness Levels[EB/OL]. NASA. https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/ （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

展示系统三份指定说明书（《科技全域态势》《技术发展跟踪》《全球创新监测》）**未出现「技术潜力评估得分」指标名**（检索记录见 A.2）。跨板块参考原文（科技专题服务系统板块，非本件所属）：

《04-科技专题服务系统/科技专题战略分析/技术链分析.md》seq 17「潜力评估模型计算」：

> 本功能基于多维指标构建潜力评估模型，支持用户对技术的商业化前景进行量化评分与横向对比。用户可识别高潜力技术，制定优先发展策略。通过该功能，用户能将技术价值转化为产业机会，提升投资与布局的精准性。融合专利、论文等产业化数据，建立可配置的潜力评估体系，实现技术价值的客观度量。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 技术潜力评估得分 | 三份指定 SRS + 主文档（展示系统部分） | 0 |
| 潜力评估 | 技术链分析.md:63（seq 17，跨板块）；可视化管理.md:103（seq 291，跨板块）；主文档:4285/7341 等 | 跨板块功能叶（无公式） |
| 潜力均值 / potential | UI 组件 techDevelopmentPlan.js:296/307/483 | 3（mock 挂载） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_016_out.json`（2026-11-01 实跑：三表族统计、六维权重、加和审计、样本链路）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（`ads_technology_stage_assessment`=38,860 零漂移）。
- Lane 3 探针快照：`_probe_lane3_jiuxin2_out.json`（三表 DESC/COUNT）、`_probe_lane3_jiuxin3_out.json`（scenario/method/统计/维度分布）、`_probe_lane3_jiuxin4_out.json`（维度加和审计/样本/weight_coverage）、`_probe_lane3_jiuxin6_out.json`（v1v2 同分）、`_probe_lane3_gkx_out.json`（dev/gkx 关键词）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_TECHTRK_016 | 文首 |
| `ui_evidence` | 证据 | techDevelopmentPlan.js:307/483/296 | §1.1/§1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false**（跨板块另注） | §1.3/附录 A |
| `facts.jiuxin_potential_assessment_rows_total` | 计数 | 38,860 | §2.1 |
| `facts.jiuxin_potential_score_stats_v2` | 统计 | 10.96/88.35/44.87 | §2.6 |
| `facts.jiuxin_potential_dimensions_v2` | 体系 | 六维+权重 | §2.2 |
| `facts.jiuxin_potential_dimension_sample_node` | 样本 | 全链路六行 | §2.3 |
| `facts.jiuxin_weighted_sum_consistent_nodes` | 审计 | 19,430 | §2.3 |
| `facts.jiuxin_v1_v2_same_score_nodes` | 审计 | 19,430 | §2.1 |
| `facts.jiuxin_stage_vs_potential_same_rows` | 审计 | 38,860 | §2.4 |
| `facts.jiuxin_potential_evidence_rows` | 计数 | 269,882 | §2.1/§3.2 |
| `facts.ui_mock_plan_records_potential` | mock 登记 | 92/95/86/88/90/87/80 | §1.1 |
| `derived[0..2]` | 派生 | 44.871899 / 1.0 / 77.394874 | §2.6/§2.2 |
| `absence_probe` | 负证据 | 4 条 | §3.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 确定性加权百分位 | OECD/JRC（R1） | 六维+权重+加和可复算 | **最高（现状即实现）** |
| 可配置场景评估 | 需求 seq 17（跨板块） | scenario 单值 | 目标态（升档路径） |
| 标准化规范 | Oslo（R2） | raw→维分归一化 | 高 |
| 阶段双轨 | NASA TRL（R3） | stage 表互补 | 高（组合展示） |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| 总分 | 19,430（单版本） | 全量+rank+percentile | 单场景 |
| 六维分解 | 116,580 | 加和可复算 | raw 可空（不影响维分） |
| 证据 | 269,882 | 全可溯源 | — |
| 场景轴 | 0 枚举 | — | 结构缺失 |
| 轮次 | 1 | — | 无历史 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1 | 节点潜力分+六维贡献分解图 | 无 |
| v2 | scenario 区域化（口径 B） | 评估管线重跑 |
| v3 | 轮次快照（时序潜力线） | 上游改造 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 分数分布压中心（avg 44.87）vs mock 80+ 观感 | 中 | 分档文案重设（≥70/45–70/<45） |
| 双表同分误读两体系 | 中 | §2.4 冗余披露随行 |
| raw=None 被当缺值 | 低 | 维分不受 raw 空影响（§2.3） |

### C.5 总判

**部分支持**：分数体系三库唯一公式级透明（总分+六维+权重+加和+证据五件套全量），降档仅因场景轴/轮次轴两结构缺口；升档路径（scenario 区域化→轮次保留）明确且素材在库。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_016.py` | 退出码 0，落 `_out.json` |
| 权重合计 | `derived.jiuxin_dimension_weight_sum` | 1.0 |
| 加和审计 | `facts.jiuxin_weighted_sum_consistent_nodes` | 19,430 |
| 场景/轮次探针 | `absence_probe` 4 条 | 单值留证 |
| 共享快照对账 | `_shared_probe_s3_01_out.json` | 38,860 零漂移 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 均为部分支持 |
| demo 禁引 | 脚本 grep demo_ | 0 命中 |

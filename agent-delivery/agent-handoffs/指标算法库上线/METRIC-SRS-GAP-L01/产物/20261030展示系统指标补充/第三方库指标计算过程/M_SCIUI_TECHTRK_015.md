# 本次评估得分（当轮）（M_SCIUI_TECHTRK_015）

> **类型**：SCORE（综合评分，方法×维度矩阵）｜ **域**：科技发展态势·技术发展跟踪·技术评估工作流·本次评估｜ **UI 挂载**：科技信息展示系统 → 技术发展跟踪 → 评估结果追踪（`techDevelopmentTracking.js:510` 历史矩阵「本次评估」列）
> **数据支持度**：**部分支持**｜ **公式定义人**：工程侧推测定义（UI 未给公式；非招标原文闭合口径）｜ **口径归属**：需求未明列叶（三份指定说明书未出现指标名），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TECHTRK_015.py`｜ **产物**：`code/M_SCIUI_TECHTRK_015_out.json`
> **四判定摘要**：直接结构 = 部分（久新 stage_assessment 有分有阶段有瓶颈描述；无方法轴/维度轴矩阵）；直接数据 = 部分（单方法单场景单轮次 19,430 节点全量有分）；依赖结构 = 部分（四方法枚举、四维度映射均无承载）；依赖数据 = 部分（历史轮次 2023–2025 无）
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

**本件判定：部分支持。** UI 的「本次评估得分」是四方法（专家评估法/经济分析法/运筹学评价法/综合评价法）×四维度（综合得分/技术成熟度/产业化能力/创新活跃度）矩阵的当轮列——16 个格子。久新侧的承载是 `ads_technology_stage_assessment`：单方法（RULE_BASED_EVIDENCE_BASED）、单场景（PUBLISHED_BASELINE）、单轮次（2026-10-16），每节点一个 0-100 的 development_potential_score（19,430 节点全量有分）加阶段档与瓶颈文本。16 格中只有 1 格有直接数据面；方法轴在三库无任何承载（dev 的 `evaluation_template` 是参数模板不是评估结果，gkx 零命中），历史三轮（2023–2025）无快照。维度映射还要过一道语义坎：UI 的「技术成熟度」在库侧是阶段档（INDUSTRIALIZATION/ENGINEERING 两值）不是 0-100 连续分。矩阵语义只兑现十二分之一，判部分支持。

### 批次纪律摘要（B1–B11 对照，skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 两派生键分子分母同源同版本（jiuxin v2） |
| B4 | 负结论带探针 | absence_probe 五条（方法轴/维度轴/历史轮次三路留证） |
| B5 | 确定性 | 聚合 ORDER BY 键排序 |
| B6 | 闸门自身被闸 | 本件不跑闸门，派单方统一跑 |
| B7 | 产物只由脚本产出 | 实跑产出，无手改 |
| B8 | 回执不复收 | 表行数/分布/同值审计亲自实跑 |
| B9 | 单位/日期陷阱 | 单轮 2026-10-16；双版本去重；stage 与 potential 同分冗余披露 |
| B10 | 口径裁定保守交付 | 「单方法基线分」vs「四方法矩阵分」双口径（§1.6） |
| B11 | 多本账互推 | 38,860/19,430 与 016 件同源对账零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 当轮分数存在吗？ | 存在（单方法） | development_potential_score 19,430 节点全量有分 |
| 四方法矩阵存在吗？ | 不存在 | assessment_method 单值 RULE_BASED_EVIDENCE_BASELINE（探针） |
| 历史轮次存在吗？ | 不存在 | metrics_as_of_date 单值 2026-10-16（探针） |

## 摘要

「本次评估得分（当轮）」是评估历史矩阵的最后一列：四种评估方法各自给出综合得分与三个维度分。实测结果一好两坏：好的一面，久新 `ads_technology_stage_assessment` 为 19,430 个技术节点全部给出了本轮（2026-10-16）评分——development_potential_score 区间 [10.96, 88.35]、均值 44.87，且每个分数都伴随阶段档（产业化 10,408 / 工程化 9,022）、固定置信度 0.9、当前状态描述（「论文=2; 专利=4; 企业=0; 项目=0」式证据计数）、瓶颈摘要与行动建议——这是三库里唯一的评估结果面，dev/gkx 探针零命中。坏的一面有二：方法轴缺失——表内 assessment_method 只有 RULE_BASED_EVIDENCE_BASELINE 一个值，UI 四方法（专家/经济/运筹/综合）无一存在，dev 的 evaluation_template 8 行是参数模板非结果；轮次轴缺失——单轮快照，UI 的 2023/2024/2025 三列历史无承载。判**部分支持**：当轮「综合得分」一格可直查，矩阵其余格待方法接入与轮次累积。

- 需求判定：需求未明列叶（seq 55「评估结果追踪」述功能未定义评分模型）。
- 复现状态：脚本已跑通；分数统计、阶段分布、同值审计落产物。
- 档位结论：**部分支持**（方法轴×轮次轴双缺，当轮单方法有分）。
- 关键事实：stage 表与 potential 表分数逐节点 100% 同值（38,860/38,860）——同一分数双表冗余，引用只计一条证据。
- 升档路径：评估方法管线扩充（多方法枚举入库）+ 轮次快照保留 → 矩阵逐格补齐。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/技术发展跟踪/**技术评估工作流**/评估结果追踪（SRS seq 55，excel_row 58）。UI 侧承载是 `technologyTrackingEvaluationHistoryMatrix`（`techDevelopmentTracking.js:506-549`）：一个 periods×methods 的评估历史矩阵，periods 四列（2023/2024/2025 评估 + **本次评估**），methods 四行（专家评估法「专家校准与风险修正」/经济分析法「经济可行性与投入产出判断」/运筹学评价法「多目标排序与资源约束判断」/综合评价法「综合多维方法结果」），每格给 stage（阶段判断）+ risk（风险提示）+ dimensions 四维分（overall 综合得分 / maturity 技术成熟度 / potential 产业化能力 / activity 创新活跃度）。本件挂载「本次评估」列：

```text
{ key: 'current', label: '本次评估' }   // techDevelopmentTracking.js:510
```

mock 的当轮列读数（演示值，不参与支持度结论）：expert overall=82 / economic 78 / operations 75 / comprehensive 80；维度分如 expert 行 maturity=78、potential=77、activity=86。矩阵还带一张参数优化建议表（`technologyEvaluationParameterOptimizationSuggestions`，556–583 行），把权重（recommendedWeights）与阈值（recommendedThresholds）当成可调对象——这说明前端作者把「评分模型」理解为**多方法、带权重、可回溯调参**的体系，而不是单一分数。这个 UI 语义比库侧现状丰富得多，是本件判档的主要参照系。

### 1.2 为什么需要本指标

「本次评估得分」是整个工作流的输出锚点：方法选择（第 3 环）选了什么方法，最终都要落到当轮得分上才能被决策消费。多方法并排的意义是防单方法偏差——UI 的 risk 注记反复出现「需同步展示子方法差异」「单一方法风险需显性提示」，业务语义是：综合评价法的 80 分要能拆回专家 82/经济 78/运筹 75 的差异，用户才知道结论稳健不稳健。这也是为什么本件的调研重心是「方法轴」而非「分数」：分数库里有，方法结构库里没有。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。** SRS seq 55 原文只说「支持查看技术评估的历史记录和结果变化趋势…提供结果对比功能，支持不同时期、不同方法评估结果的并排展示」——「不同方法」作为功能词出现，但四方法是什么、分数怎么算、维度怎么加权，一个字没有。主需求文档 421 行段亦无。《科技专题服务算法库.md》技术链深度分析模型章节有方法学叙述（统一的数据采集、标准化处理、指标体系设计与算法优化），但属科技专题服务系统板块，非本件说明书。

### 1.4 类似指标权威方法可行性分析概要

UI 四方法就是经典评价方法族。权威系谱：NASA TRL 把成熟度做成 9 级标尺、每级有退出判据与客观证据要求（R1）——对应 UI「技术成熟度」维度与久新 stage_code 阶段档；OECD/JRC 复合指标手册给出十步建指流程（理论框架→选指标→标准化→加权聚合→敏感性→透明呈现），明确警告权重主观性风险（R2）——对应综合评价法与久新六维加权体系；Oslo 手册对创新指数的标准化（min-max/标准差）与聚合（等权/差异权重）给出统计规范（R3）。方法族对照：

| 方法族 | 代表 | 分数形态 | 与本库匹配 |
|---|---|---|---|
| 阶段标尺法（专家） | NASA TRL（R1） | 离散档位+证据 | **有**（stage_code 两档+证据计数） |
| 确定性加权模型 | OECD/JRC 十步法（R2） | 0-100 连续 | **有**（potential_score 六维加权） |
| 多方法并排 | UI 四方法矩阵 | 方法×维度 | **无**（方法轴单值） |

结论：库侧是「一条方法管线跑到底」，权威体系的多方法交叉验证结构缺位。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/techDevelopmentTracking.js:510`（本次评估列）；`506-549`（矩阵全量）；`556-583`（参数优化建议，权重/阈值体系佐证）。
- SRS：`…/技术发展跟踪.md` seq 55（excel_row 58），原文见附录 A。
- 主需求文档：无「本次评估得分」定义段。

### 1.6 推测原意与推测定义

**推测定义（双口径并列，B10）**：

- 口径 A（**单方法基线分**，库侧现状）：`score_current(node) = development_potential_score`，方法=RULE_BASED_EVIDENCE_BASELINE、场景=PUBLISHED_BASELINE、轮次=2026-10-16——「本次评估」退化为「本轮基线评估」，四方法并排只剩一行；
- 口径 B（**四方法矩阵分**，UI 语义）：`score_current(method, dim)` 四方法×四维度 16 格，专家/经济/运筹方法需另行建管线（文献方法见 §1.4），综合评价法可用口径 A 的六维加权分充当。

**维度映射（推测，需甲方确认）**：UI overall ↔ potential_score；UI potential（产业化能力）↔ PATENT_CONVERSION+INDUSTRY_PARTICIPATION 两维加权和；UI activity（创新活跃度）↔ SCIENTIFIC_GROWTH；UI maturity（技术成熟度）↔ stage_code 阶段档（非连续分，需档位折算或改口径）。**降档/升档触发器**：若甲方接受口径 A（单方法基线分+阶段档+瓶颈文本）→ 维持部分支持但当轮列可上线；若久新扩充方法管线（assessment_method 多值）→ 方法轴补齐；若保留轮次快照 → 历史三列补齐，二者齐备升完全转换支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/技术发展跟踪.md` |
| 所属四级功能 | 技术发展跟踪（8 叶，seq 48–55） |
| 所属面板 | 技术评估工作流（seq 52–55） |
| 本件叶 | **评估结果追踪（seq 55）之「本次评估」列——需求未明列指标名** |
| 相邻叶 | 评估流程概览（seq 52，014 承接）/ 评估方法详解（seq 53）/ 评估参数配置（seq 54） |
| UI 容器 | 历史矩阵「本次评估」列 + 参数优化建议表 |

批内关系：本件与 016（技术潜力评估得分）共享同一张底表——stage 表的 development_potential_score 与 potential 表的 potential_score 逐节点同值（§2.4 审计），两件是同一分数的两个 UI 视图（015 看方法×轮次矩阵、016 看维度×权重体系）；与 022（历史得分序列，Lane 4）互补，022 消费 periods 轴的 2023–2025 列，本件消费 current 列。三件共享「轮次缺失」缺口。

## 二、计算过程

### 2.1 装载与版本审计

直连久新 Doris（只读）。`ads_technology_stage_assessment` 全表 38,860 行 = 19,430 节点 × 2 model_version（v1 与 v2 逐节点同分，与 016 件共用审计），单版本口径 19,430。轮次恒单值：`metrics_as_of_date` 全表只有 2026-10-16（产物键 `jiuxin_stage_assessment_metrics_as_of_date`），即「本次评估」在库侧有且只有这一轮。方法枚举恒单值：assessment_method= RULE_BASED_EVIDENCE_BASELINE（38,860 行全同），scenario_type= PUBLISHED_BASELINE（全同）——UI 四方法在数据面的兑现度是 1/4 行。

### 2.2 当轮分数实测

v2 单版本分数统计（产物键 `jiuxin_development_potential_score_stats_v2`）：n=19,430（全量有分，无空）、min=10.95939、max=88.354264、avg=44.871899。分数不是均匀撒的：阶段档交叉显示 INDUSTRIALIZATION（产业化）10,408 节点（53.57%，产物派生键 `jiuxin_nodes_Industrialization_share_pct`）与 ENGINEERING（工程化）9,022 节点——注意这个二档分布与 stage 字典表（`ads_technology_transfer_stage` 8 档：BASIC_RESEARCH 基础研究 → INDUSTRIALIZATION 产业化，产物键 `jiuxin_transfer_stage_dict`）的 8 档体系相比只落在最高两档，说明本轮评估的节点池（ETO 研究簇技术）整体偏成熟端，或阶段判定规则只激活了上两档。无论哪种解释，UI 若直接消费，档位分辨率会显得粗。

### 2.3 分数的伴随证据（本表最独特的资产）

每个分数不是裸数：`current_status_description` 给证据计数（「论文=3; 专利=192; 企业=1; 项目=2」）、`key_bottleneck_summary` 给瓶颈（「当前内部证据未显示单一主导瓶颈」或「尚未观察到关联企业证据」）、`risk_summary` 统一提示（「需结合市场、政策、标准和真实应用数据复核」）、`action_recommendation` 给行动（「优先补齐缺失证据并进行专家审核」）。stage_confidence 恒 0.9（单值，非逐节点校准）。这组伴随字段让「本次评估得分」可以带着可解释性上线——这是它在三库中独一份的价值：dev/gkx 连分数都没有，更遑论解释链。

### 2.4 冗余审计：stage 表与 potential 表同分

JOIN 审计（产物键 `jiuxin_stage_vs_potential_same_score_rows`）：38,860 行逐节点 development_potential_score = potential_score，同值率 100%。结论：两张表是同一评分管线的双落点（stage 表带解释文本、potential 表带百分位与权重覆盖），不是两个独立方法。对 UI 的含义：「本次评估得分」若同时引两表会重复计数；对 016 件的含义：其六维加权体系就是本件分数的分解（016 已验证 weighted_score 加和=总分，19,430/19,430 节点一致）。

### 2.5 方法轴与轮次轴的结构性核查

三路探针闭环：① 方法轴——`SELECT DISTINCT assessment_method` 单值（jiuxin）；dev 侧 `gkxlumenx_topic_enterprise.evaluation_template` 8 行，列结构是 template_id/indicators_json/weights_json/is_default——是「评估参数配置」的模板库（对应 SRS seq 54），查无得分结果行；gkx 280 表 score/assess/evaluation 关键词零命中。② 轮次轴——metrics_as_of_date 单值；dev/gkx 无任何历轮评估表。③ 维度轴——potential_dimension 仅 BASELINE 场景 6 维（SCIENTIFIC_*3 + PATENT_CONVERSION + INDUSTRY_PARTICIPATION + PROJECT_EVIDENCE），无 UI 四维度直接对应列，映射靠语义推测（§1.6）。

### 2.6 稳健性与口径敏感性

分数对节点池的敏感性：均值 44.87 显著低于 mock 演示值（75–82），若直接上线会造成「评估普遍不及格」的观感——实际这是基线方法（证据计数驱动的确定性百分位模型）的分布特性，不是技术真的弱。口径 A 上线时必须带方法标签（RULE_BASED_EVIDENCE_BASELINE）与场景标签（PUBLISHED_BASELINE），并把 0.9 置信度改为真实的区间估计（当前是常数，无信息量）。UI 的 trend 列（+12.4% 等）在单轮快照下无历史可比，应隐藏或标「首轮无环比」。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TECHTRK_015.py`（直连久新只读；运行 `python3 code/M_SCIUI_TECHTRK_015.py`）。
- 产物：`code/M_SCIUI_TECHTRK_015_out.json`。正文数字与产物键逐一对应：`jiuxin_stage_assessment_rows_total=38860`（§2.1）、`jiuxin_stage_assessment_stage_code_dist`（§2.2）、`jiuxin_development_potential_score_stats_v2`（§2.2）、`jiuxin_transfer_stage_dict` 8 档（§2.2）、`jiuxin_stage_vs_potential_same_score_rows=38860`（§2.4）、派生 `jiuxin_nodes_Industrialization_share_pct=53.57` / `jiuxin_avg_score_v2=44.871899`（§2.2）。
- 结果解读：当轮单方法分数全量可查且带解释链；方法/轮次/维度三轴缺二剩半。
- 对照需求功能要求的评审：「不同时期、不同方法评估结果的并排展示」——时期轴 1/4（仅本次）、方法轴 1/4（仅基线法）、并排结构可由前端搭好等数据。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 版本 | 总行/单版本节点 | `…_rows_total` / `…_nodes_single_version` | 38,860 / 19,430 |
| 轮次 | 快照日期 | `jiuxin_stage_assessment_metrics_as_of_date` | 2026-10-16（单值） |
| 方法 | 方法枚举 | `jiuxin_stage_assessment_assessment_method` | RULE_BASED_EVIDENCE_BASELINE（单值） |
| 分数 | 统计三读数 | `jiuxin_development_potential_score_stats_v2` | min 10.96 / max 88.35 / avg 44.87 |
| 阶段 | 两档分布 | `jiuxin_stage_assessment_stage_code_dist` | 10,408 / 9,022 |
| 字典 | 8 档体系 | `jiuxin_transfer_stage_dict` | BASIC_RESEARCH→INDUSTRIALIZATION |
| 冗余 | 与 potential 同分 | `jiuxin_stage_vs_potential_same_score_rows` | 38,860（100%） |
| 派生 | 产业化占比 | `derived.jiuxin_nodes_Industrialization_share_pct` | 53.57% |
| absence | 方法轴/轮次轴/维度轴 | §3.4 五件套 | 命中 0/0/0 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 当轮分数 | jiuxin | `stage_assessment.development_potential_score` | 19,430（单版本全量有分） | 直查 | **有** |
| D2 | 解释链（阶段/瓶颈/建议） | jiuxin | 同表 5 文本列 | 38,860 | 直查 | 有 |
| D3 | 方法轴（四方法） | dev/gkx/jiuxin | —（dev evaluation_template 8 行为参数模板；jiuxin 方法单值） | — | **不存在** | **缺（主降档因）** |
| D4 | 轮次轴（2023–2025） | 三库 | —（单轮快照） | — | 不存在 | 缺 |
| D5 | 维度映射 | jiuxin | potential_dimension 6 维 | 116,580（单版本） | 语义推测 | 半（需甲方确认映射） |

`support_judgment="部分支持"` 与文首一致（闸 6 对齐）。

### 3.2 D1+D2 当轮分数与解释链

§2.2/§2.3 已列全。补充一个使用建议：stage_confidence 恒 0.9 与 risk_summary 全表同文，两列当前无区分度，上线时建议折叠为全局注记而非逐格展示。

### 3.3 D5 维度映射的可行性

UI 四维度中 overall 可直取（=development_potential_score）；potential/activity 可由 016 件的维度分组合（加权体系已验证可复算）；maturity 是阶段档非连续分——要么改 UI 语义为「阶段」（更诚实），要么定义档位折算（如 INDUSTRIALIZATION=85、ENGINEERING=70，需甲方定标）。映射表已写入产物 notes。

### 3.4 D3/D4 方法轴与轮次轴 absence_probe 全记录

否定性证据五件套：**查了什么**——① dev `gkxlumenx_dwd` score/assess/eval 关键词（仅政策侧 4 表，非技术评估）；② dev `topic_enterprise.evaluation_template`（DESC+COUNT=8，indicators_json/weights_json 结构，无结果行）；③ gkx 280 表同关键词（0 命中）；④ jiuxin assessment_method DISTINCT（单值）；⑤ jiuxin metrics_as_of_date DISTINCT（单值）。**条件**——多方法结果面/历史轮次表。**命中**——技术评估方法轴 0、历史轮次 0。归属：**结果面不存在**（非数据稀疏），修复需上游管线扩充，展示侧无法自建（专家评估法需专家评分数据，三库皆无）。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 双版本去重 | 38,860=19,430×2，v1/v2 同分 |
| 分数统计 | n=19,430 全量，avg 44.871899 |
| 阶段二档 | 10,408+9,022=19,430 自洽 |
| 同值审计 | stage=potential 38,860/38,860 |
| 方法/轮次 | DISTINCT 单值×2，探针留档 |
| mock 登记 | 82/78/75/80 标演示值 |
| 脚本形态 | 只读、零 demo_*、单进程 |

## 四、数据缺失情况

### 4.1 方法轴缺失（主因）

UI 四方法中专家评估法、经济分析法、运筹学评价法三者在三库无任何数据承载（§3.4）。这三种方法各有硬依赖：专家法需专家评分记录（人 sourced，库内无）、经济法需成本/收益/回收周期字段（久新 commercial_value_simulation 表在 203 表清单中存在但本件未探明其行数，属后续跟进项）、运筹法需资源约束参数。综合评价法可由现有六维加权体系充当（016 件）。修复是「补管线」不是「补数据」：每接入一种方法，矩阵多一行。

### 4.2 轮次轴缺失（次因）

单轮快照无 2023–2025 轮。参数优化建议表（UI 556–583 行）声称基于「近三期」历史记录调权重——这个叙事当前无数据支撑，首轮上线建议隐藏该表或改为静态模板。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 先行（基线分+解释链） | 产品决策 | 本件即期可交付 | 方法/场景标签随行 |
| 综合评价法行补齐 | 转换工程 | 本件+016 | 六维加权分即综合法结果，零新上游 |
| 专家评分记录表立项 | 上游扩充 | 本件（方法轴） | 最重但最贴需求原文 |
| 轮次快照保留 | 上游改造 | 本件+022 | 历史三列 |

档位后果：口径 A → 部分支持语义闭合；综合法行 → 方法轴 2/4；专家法+轮次齐 → 完全转换支持。推荐：即期口径 A + 综合法行，中期专家法立项。

## 参考文献

1. Technology Readiness Levels[EB/OL]. NASA. https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/ （R1，2026-11-01 WebSearch 核验可达）
2. Handbook on Constructing Composite Indicators: Methodology and User Guide[EB/OL]. OECD/JRC, 2008. https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf （R2，2026-11-01 WebSearch 核验可达）
3. Use of innovation data for statistical indicators and analysis: Oslo Manual 2018[EB/OL]. OECD. https://www.oecd.org/en/publications/oslo-manual-2018_9789264304604-en/full-report/component-18.html （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》seq 55（excel_row 58）：

> 支持查看技术评估的历史记录和结果变化趋势，用户可按时间、技术类型、评估方法等维度筛选查看评估结果。系统提供结果对比功能，支持不同时期、不同方法评估结果的并排展示，提供结果差异分析和变化原因说明，帮助用户理解技术发展的动态过程。

「本次评估得分（当轮）」指标名在三份指定说明书与主文档均未出现；「评估方法」作为筛选维度词出现，无方法定义。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 本次评估得分 | 三份指定 SRS + 主文档 | 0 |
| 本次评估 | 技术发展跟踪 UI 组件（techDevelopmentTracking.js:510） | 1（mock 矩阵列名） |
| 评估得分 / 评分模型 | 全部需求文档 | 0（「评分」仅出现于其他板块潜力评估语境） |
| 评估方法 | 技术发展跟踪.md seq 53「评估方法详解」（专家/经济/运筹/综合四方法名列举） | 1（方法名有列举、无算法定义） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_015_out.json`（2026-11-01 实跑：分数统计、阶段分布、字典、同值审计）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（`ads_technology_stage_assessment`=38,860 零漂移）。
- Lane 3 探针快照：`_probe_lane3_jiuxin_out.json`（DESC/样本）、`_probe_lane3_jiuxin3_out.json`（分布/统计）、`_probe_lane3_jiuxin4_out.json`（同值审计/完整样本）、`_probe_lane3_gkx_out.json`（dev/gkx 关键词）、`_probe_lane3_final_out.json`（evaluation_template DESC/COUNT、metrics_as_of_date 分布）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_TECHTRK_015 | 文首 |
| `ui_evidence` | 证据 | techDevelopmentTracking.js:510 等 2 条 | §1.1/§1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.jiuxin_stage_assessment_rows_total` | 计数 | 38,860 | §2.1 |
| `facts.jiuxin_stage_assessment_nodes_single_version` | 计数 | 19,430 | §2.1 |
| `facts.jiuxin_stage_assessment_metrics_as_of_date` | 日期 | 2026-10-16 | §2.1/§4.2 |
| `facts.jiuxin_stage_assessment_stage_code_dist` | 分布 | 10,408/9,022 | §2.2 |
| `facts.jiuxin_development_potential_score_stats_v2` | 统计 | min/max/avg | §2.2 |
| `facts.jiuxin_transfer_stage_dict` | 字典 | 8 档 | §2.2 |
| `facts.jiuxin_stage_vs_potential_same_score_rows` | 审计 | 38,860 | §2.4 |
| `facts.ui_mock_current_overall_scores` | mock 登记 | 82/78/75/80 | §1.1 |
| `derived[0]` | 派生比 | 工业化占比 53.57 | §2.2 |
| `derived[1]` | 均值 | 44.871899 | §2.2 |
| `absence_probe` | 负证据 | 5 条 | §3.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 分数形态 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 阶段标尺 | NASA TRL（R1） | 档位+证据 | stage_code+证据计数 | 高（档位粗） |
| 确定性加权 | OECD/JRC（R2） | 0-100 | potential_score 六维 | **高** |
| 标准化聚合 | Oslo（R3） | 指数 | 维度分可再聚合 | 中 |
| 多方法并排 | UI 矩阵 | 方法×维度 | **无** | 目标态 |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| 当轮分数 | 19,430 | 全量+解释链 | 单方法 |
| 维度分 | 116,580 | 加权可复算 | 映射需确认 |
| 方法轴 | 0 | — | 三方法无管线 |
| 轮次轴 | 1 轮 | — | 无历史 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1 | 基线分+阶段档+瓶颈文本（口径 A） | 无 |
| v2 | +综合评价法行（六维加权分） | 映射确认 |
| v3 | +专家/经济/运筹行 + 历史轮次 | 上游管线与评分数据立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 均值 44.87 vs mock 75+ 的观感落差 | 中 | 方法标签+分布说明随行 |
| 双表同分误读为两方法 | 中 | §2.4 审计结论写进使用说明 |
| stage_confidence 恒 0.9 误导 | 低 | 折叠为全局注记 |

### C.5 总判

**部分支持**：当轮分数+解释链三库独一份可直接上线；方法轴 1/4、轮次轴 1/4、维度映射半格——矩阵语义兑现 1/12，升档路径按「综合法行→专家法立项→轮次保留」三步走（§1.6 触发器）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_015.py` | 退出码 0，落 `_out.json` |
| 分数统计 | `facts.jiuxin_development_potential_score_stats_v2` | n=19,430, avg=44.871899 |
| 同值审计 | `facts.jiuxin_stage_vs_potential_same_score_rows` | 38,860 |
| 方法/轮次探针 | `absence_probe` 5 条 | 单值/单值留证 |
| 共享快照对账 | `_shared_probe_s3_01_out.json` | 38,860 零漂移 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 均为部分支持 |
| demo 禁引 | 脚本 grep demo_ | 0 命中 |

# 维度得分 TOP5（M_SCIUI_TECHTRK_019）

> **类型**：SCORE（维度分排序卡，区域竞争力画像子件）｜ **域**：科技发展态势·技术发展跟踪·重点区域画像｜ **UI 挂载**：科技信息展示系统 → 技术发展跟踪（页面族）→ 科技发展规划页重点区域画像卡 `TechDevelopmentPlan.tsx:3031`「维度得分（TOP5）」
> **数据支持度**：**部分支持**｜ **公式定义人**：工程侧推测定义（UI 无公式；非招标原文闭合口径）｜ **口径归属**：需求未明列叶（三份指定说明书未出现「维度得分（TOP5）」指标名），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TECHTRK_019.py`｜ **产物**：`code/M_SCIUI_TECHTRK_019_out.json`
> **四判定摘要**：直接结构 = 否（无区域粒度维度结果面）；直接数据 = 部分（久新两套分维体系现成，但分别是技术节点粒度与机构粒度）；依赖结构 = 部分（区域聚合链路可用但需口径裁定）；依赖数据 = 部分（深圳子盘 6,233 节点全量有分，区域五维名映射无承载）
> **数据源口径注记**：三源评估——开发库（`gkxlumenx_*`，禁 `demo_*`）+ gkx（只读 280 表，经 `code/_gkxdb.py`）+ 久新 jiuxin_warehouse（只读 203 表，Doris）。本件主数据面在久新。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（三源）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** UI 的「维度得分（TOP5）」是重点区域画像卡里的一张五维横条图（创新资源 92 / 科研产出 88 / 产业竞争力 85 / 人才支撑 78 / 开放协同 72，mock 演示值）——语义是「**某个区域**在五个**区域维度**上的得分排序取前五」。三源实测：gkx 280 表 dimension/score 关键词**零命中**（absence_probe 1）；开发库 `gkxlumenx_ads` 命中 3 张评分类表（enterprise_score / industry_chain_region_scorecard / svc_tech_power_score）但均为企业/产业链侧，无区域维度画像面；久新有两套现成分维体系——`ads_technology_potential_dimension` 六维（技术节点粒度，深圳子盘 6,233 节点全量有分）与 `ads_institution_technology_power` 四权重维（机构粒度，64,698 机构）——**两套都不是区域粒度**，且维度名与 UI 五维（创新资源/科研产出/产业竞争力/人才支撑/开放协同）零重合。区域维度需经「节点→区域子盘聚合」（口径 A，可行但语义需裁定）或「机构→城市映射」（库内无此映射列）转换，且五维名映射无任何库内承载须甲方裁定。结构有近似、数据有规模、语义槽错位，判部分支持。

### 批次纪律摘要（B1–B11 对照，skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | TOP5 均值分子分母同源同子盘（jiuxin 深圳子盘 v2） |
| B4 | 负结论带探针 | absence_probe 两路（gkx 0 命中 / dev 3 命中但语义错位）留证 |
| B5 | 确定性 | 维度排序按 avg_score DESC 固定序，聚合按键排序 |
| B6 | 闸门自身被闸 | 本件不跑闸门，派单方统一跑 |
| B7 | 产物只由脚本产出 | 实跑产出，无手改 |
| B8 | 回执不复收 | 表行数/维度分布/Top5 亲自实跑 |
| B9 | 单位/日期陷阱 | 双 model_version 去重（v2 口径）；快照制无年份轴 |
| B10 | 口径裁定保守交付 | 口径 A（节点子盘聚合）/口径 B（机构维度榜）双口径并列 + 升降档触发器（§1.6） |
| B11 | 多本账互推 | 深圳子盘 6,233 与 020/021/022 件同源对账零漂移；region_assessment 12,466=6,233×2 版本自洽 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 区域维度结果面存在吗？ | 不存在 | 三源无「区域×五维」结果面（gkx 0 命中 / dev 企业侧 / jiuxin 节点与机构粒度） |
| 近似分维体系可用吗？ | 可用（两套） | potential_dimension 六维深圳 6,233 节点；institution_power 四维 64,698 机构 |
| 五维名映射可裁定吗？ | 库内不可 | UI 五维名与库侧六维/四维零重合，需甲方语义裁定 |

## 摘要

「维度得分（TOP5）」是重点区域画像卡的五维条形组件：给一个区域（mock 语境为南山区/深圳湾），按五个维度打分排序展示前五。三源探测的结论是「结构近似、粒度错位」：久新 `ads_technology_potential_dimension` 提供六维 0-100 分体系（SCIENTIFIC_SCALE/GROWTH/IMPACT/PATENT_CONVERSION/INDUSTRY_PARTICIPATION/PROJECT_EVIDENCE），深圳子盘 6,233 个技术节点全量有分，TOP5 维均分为 65.5638（derived.jiuxin_shenzhen_dim_top5_avg），最高维 PROJECT_EVIDENCE 80.9386；`ads_institution_technology_power` 提供四权重维机构榜（64,698 机构，Top5 为中国科学院 99.9992 等）。但两套体系分别是技术节点粒度与机构粒度，UI 要的是区域粒度五维；UI 五维名（创新资源/科研产出/产业竞争力/人才支撑/开放协同）与库侧维度名零重合。开发库 `gkxlumenx_ads` 三张评分表为企业/产业链侧（enterprise_score 等），gkx 280 表零命中。判**部分支持**：口径 A（深圳子盘六维聚合 TOP5）可即刻出数，语义等价性须甲方裁定；口径 B（机构维度榜）是另一条现成路径但换掉了「区域」主语。

- 需求判定：需求未明列叶（三份说明书 0 命中；srs/05 与 03 的「维度得分」属其他系统板块）。
- 复现状态：脚本已跑通；深圳六维分布、全域对照、机构维度榜、Top5 机构四读数组落产物。
- 档位结论：**部分支持**（区域粒度结构缺失 + 维度名映射缺失双因）。
- 关键事实：深圳子盘 PROJECT_EVIDENCE 80.9386 / INDUSTRY_PARTICIPATION 76.0995 显著高于全域均值（43.9984/40.5735）——区域证据筛选偏置，读数必须随行披露。
- 升档路径：甲方裁定口径 A 维度映射 → 语义闭合；久新补机构→城市映射列 → 口径 B 区域化。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/技术发展跟踪/页面族尾段/**科技发展规划页·重点区域画像**（UI 组件 `TechDevelopmentPlan.tsx`）。画像卡由四块拼成：竞争力指标条（`keyAreaCompetitivenessMetrics`，:862-868，综合指数 78.5/创新能力 88/产业基础 85/开放协同 62/发展潜力 82）、**维度得分 TOP5**（:870-876 常量 + :3030-3038 渲染）、对标区域排名表（:879-884，南山区 78.5 第一）。本件挂载点：

```text
<section className="tzp-dimension-score-panel">
  <h4>维度得分（TOP5）</h4>            // TechDevelopmentPlan.tsx:3031
  {keyAreaDimensionScores.map(item => (  // :870-876 五维常量
    <div className="tzp-dimension-score-row">
      <span>{item.label}</span>
      <Progress percent={item.percent} showInfo={false} size="small" />
      <em>{item.percent}%</em>
```

mock 值（演示值，不参与支持度结论）：创新资源 92 / 科研产出 88 / 产业竞争力 85 / 人才支撑 78 / 开放协同 72（产物键 `ui_mock_dimension_scores_top5`）。组件行为是纯静态渲染：五条 Progress 横条按 percent 长度可视化，排序已在常量里写死（降序）。注意「TOP5」在 UI 语境是「五个维度各一条」，不是「某维度下前五名实体」——这是本件与排行榜类指标（如 017 热点榜）的本质区别，也决定了库侧对齐时应该找「区域×维度分」而不是「维度下 Top5 实体」。

### 1.2 为什么需要本指标

重点区域画像卡的业务问题是「这块区域搞技术发展的本钱是什么、短板在哪」：五维条把多维竞争力压成一眼可读的排序，决策者看长短条即可定位补强方向（方案区 mock 的「提升创新策源能力/强化产业转化效率」三方案正是对维度短板的回应，:855-860）。它是画像卡的诊断件：对标排名表（同卡片）回答「和别人比排第几」，维度得分回答「自己内部哪强哪弱」——前者是外标、后者是内诊，两者合起来才构成区域画像。数据侧的难点在于维度体系是纯 UI 侧虚构（五维名与任何权威体系的字面都不同），必须先解决「维度从哪来」的映射问题，才能谈「分数怎么算」。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「维度得分（TOP5）」在三份指定说明书（技术发展跟踪.md/科技全域态势.md/全球创新监测.md）与主需求文档均 0 命中。srs 全目录检索「维度得分」有两处命中但均非本件页面：`srs/05-深度挖掘算法`（机构技术力指数输出明细语境）与 `srs/03-新型高端智库系统/战略咨询智能支持`（技术体系分析语境）——属其他系统板块，本件页面（技术发展跟踪页面族）无该词。五维名「创新资源/科研产出/产业竞争力/人才支撑/开放协同」在全部需求文档 0 命中，属前端作者自拟。

### 1.4 类似指标权威方法可行性分析概要

区域维度画像在权威体系有三个直接先例。其一，WIPO 全球创新指数（GII）：两层级七支柱（制度/人力资本与研究/基础设施/市场成熟度/商业成熟度/知识与技术产出/创意产出）逐国打分排序（R1）——「多维打分+排序展示」的同构原型；其二，欧盟创新记分牌（EIS）：32 个指标聚合成 8 个创新维度，输出各区域相对欧盟均值的性能指数并分级（Strong/Moderate/Modest Innovator）（R2）；其三，OECD/JRC 复合指标手册：维度归一（min-max/z-score）→加权聚合→敏感性分析的十步流程，并明确要求维度权重主观性须披露（R3）。方法族对照：

| 方法族 | 代表 | 维度形态 | 与本库匹配 |
|---|---|---|---|
| 多支柱打分（GII） | WIPO GII（R1） | 国家×7 支柱 0-100 | **无区域粒度**（结构同构可借） |
| 区域创新记分牌（EIS） | EU EIS（R2） | 区域×8 维相对指数 | **无**（维度名亦不重合） |
| 复合指标构建（JRC） | OECD/JRC（R3） | 归一+加权方法论 | **有**（potential_dimension 六维即此产物） |

结论：库侧六维体系在方法学上就是 R3 流程的产物（百分位归一+固定权重），缺的不是「怎么算」而是「区域主语怎么进来、五维名怎么映射」。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3031`（h4「维度得分（TOP5）」）；`:870-876`（keyAreaDimensionScores 五维常量）；`:862-868`（同卡竞争力指标，佐证区域画像语境）。
- SRS：三份指定说明书 0 命中（附录 A 检索记录）；`kept_items` 的 mount 记录「techDevelopmentTracking.js（维度得分 TOP5）」经现场实查，实际渲染常量在 `TechDevelopmentPlan.tsx`（页面族共用的规划页），MD 按实查行号写。
- 主需求文档：无「维度得分」定义段。

### 1.6 推测原意与推测定义

**推测定义（双口径并列，B10）**：

- 口径 A（**区域子盘维度聚合**，库侧现状最短路径）：取久新 `ads_technology_potential_dimension` 的深圳子盘（6,233 节点），按六维各求 avg_score 降序取前五维展示——`TOP5(region) = sorted_dims(avg_score desc)[:5]`。读数已产出：PROJECT_EVIDENCE 80.9386 / INDUSTRY_PARTICIPATION 76.0995 / SCIENTIFIC_SCALE 70.3038 / PATENT_CONVERSION 50.4770 / SCIENTIFIC_GROWTH 50.0000（facts.jiuxin_shenzhen_dim_scores_desc）。维度名映射假设（须甲方裁定）：创新资源↔SCIENTIFIC_SCALE、科研产出↔SCIENTIFIC_IMPACT/SCIENTIFIC_GROWTH、产业竞争力↔PATENT_CONVERSION+INDUSTRY_PARTICIPATION、人才支撑↔（六维中无对应，需引 talent 维）、开放协同↔（六维中无对应）。
- 口径 B（**机构维度榜区域化**）：取 `ads_institution_technology_power` 四权重维（paper/citation/talent/topic，0.35/0.30/0.25/0.10），对城市内机构求维度均值构成「区域维度分」——需要机构→城市映射列，**库内实测无此列**（region_assessment 表有区域行但无机构维度下钻）。

**降档/升档触发器（B10 模板）**：若甲方裁定口径 A 维度映射（接受六维换名上屏）→ 维持部分支持但语义闭合可上线；若久新补机构→城市映射 → 口径 B 解锁，「区域主语」原味保留；若甲方要求五维名逐一对应 → 库内无 talent/开放协同维承载，维持部分支持不升档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | 技术发展跟踪.md（本件叶未明列；页面族归科技发展态势） |
| 所属页面 | 技术发展跟踪页面族 → 科技发展规划页重点区域画像 |
| 本件叶 | **维度得分（TOP5）——需求未明列，UI 自建组件** |
| 相邻组件 | 竞争力指标条（TECHTRK_001 族语境）/ 对标区域排名（TECHTRK_008 件承接）/ 方案区（无指标件） |
| UI 容器 | `tzp-dimension-score-panel` 五条 Progress |

批内关系：本件与 008（对标区域排名）同卡不同问（内诊 vs 外标）；与 020（技术发展指数）共享「深圳子盘聚合」口径底座；与 021/022 共享 hotspot/potential 双表；与 018（竞争力水平与潜力评估）共享「综合分+维度分」的拆分语义（018 是总分、本件是维度切面）。

## 二、计算过程

### 2.1 方法选择（文献依据）

维度分排序卡的权威方法是复合指标的**维度层呈现**：OECD/JRC 手册（R3）要求复合指标发布时必须同时给出维度层得分（不只总分），便于定位短板——本件 UI 五维条正是维度层呈现的形态。EIS（R2）的相对性能指数（区域分/欧盟均值×100）提供了「区域间可比」的归一范式；GII（R1）的支柱层排序则是「取前几维展示」的交互原型。本件计算按 R3 流程执行：子盘筛选 → 维度层均值 → 降序取五。库侧六维体系本身已按此流程产出（0-100 百分位分），本件只需在其上做区域子盘聚合，不重造归一化。

### 2.2 深圳子盘装载与版本审计

直连久新 Doris（只读）。`ads_technology_potential_dimension` 全表按 model_version 双版本（technology_insight_mvp_v1 / v2_eto_cluster_technology），本件统一取 **v2** 口径（与 015/016 件共用审计结论：v1/v2 逐节点同分）。深圳子盘筛选条件：region_assessment 表 region_name='深圳' 命中 12,466 行 = 6,233 节点 × 2 版本（facts.jiuxin_shenzhen_region_assessment），六维表 JOIN 后深圳子盘 6,233 节点全量有分（facts.jiuxin_shenzhen_dim_nodes），每维 6,233 行无缺失。区域证据面（facts.jiuxin_shenzhen_region_evidence_totals）：论文机构证据 3,455 / 专利机构证据 17 / 项目机构证据 46,330 / 机构计数和 34,617 / 企业计数和 4,179——注意深圳子盘是**经区域证据命中筛选**的节点集（证据挂靠深圳机构才入盘），这解释了 §2.3 的维度分布为何显著偏 PROJECT_EVIDENCE/INDUSTRY_PARTICIPATION（项目/产业证据是入盘主通道），选择偏置随读数披露。

### 2.3 六维分布实测（口径 A 主读数）

深圳子盘六维 avg_score 降序（facts.jiuxin_shenzhen_dim_scores_desc）：

| 排名 | dimension_code | avg_score | weight | 全域均值（对照） |
|---|---|---|---|---|
| 1 | PROJECT_EVIDENCE | 80.9386 | 0.10 | 43.9984 |
| 2 | INDUSTRY_PARTICIPATION | 76.0995 | 0.15 | 40.5735 |
| 3 | SCIENTIFIC_SCALE | 70.3038 | 0.20 | 45.5063 |
| 4 | PATENT_CONVERSION | 50.4770 | 0.20 | 46.1890 |
| 5 | SCIENTIFIC_GROWTH | 50.0000 | 0.20 | 48.2470 |
| 6 | SCIENTIFIC_IMPACT | 37.5699 | 0.15 | 42.6505 |

三个结构性读数：① TOP5 维均分 65.5638（derived.jiuxin_shenzhen_dim_top5_avg，分子 32,782 = 五维 avg×100 取整和 / 分母 500）；② 最高维 PROJECT_EVIDENCE 80.9386（derived.jiuxin_shenzhen_dim_top1_score）比全域同维均值 43.9984 高 36.94 分——这是子盘筛选机制的产物（项目证据是入盘主通道），不是「深圳项目真的碾压全国」的字面义；③ SCIENTIFIC_GROWTH 恰为 50.0000 且全库 institutional_power 各维均值也恰为 50.0（§2.5）——百分位制的基准锚点（中位=50），深圳子盘该维恰好落在全库中位。全域对照读数来自 facts.jiuxin_global_dim_scores（19,430 节点六维均值）。

### 2.4 「TOP5」语义的两种取法（UI 对齐辨析）

UI 是「取前五**维**」（五条横条），库侧口径 A 与之同构（六维降序取五，表 §2.3 前 5 行）。另一解读「某维度下 TOP5 **实体**」在库侧对应机构维度榜（§2.5）——`ads_institution_technology_power` Top5（facts.jiuxin_inst_power_top5）：中国科学院 99.9992（论文 177,917/人才 19,241）/ 中国科学院大学 99.9962（92,288/12,480）/ 北京大学 99.9961（66,635/9,127）/ 浙江大学 99.9932（61,455/8,624）/ 上海交通大学 99.9927（60,458/8,920）。两读数都落产物，MD 按 UI 语义（取维）为主读数、实体榜为口径 B 副产品，语义辨析写入 notes（B10）。

### 2.5 机构维度体系核查（口径 B 可行性）

`ads_institution_technology_power` 全表 64,698 机构（facts.jiuxin_inst_power_rows），四分维 paper_score/citation_score/talent_score/topic_score 加权 technology_power_score，权重四元组 0.35/0.30/0.25/0.10（facts.jiuxin_inst_power_weights）。全库维度均值（facts.jiuxin_inst_power_dim_avg）：五列全部恰为 50.0——印证该体系是 0-100 **百分位制**（全库中位锚定 50），维度分只有相对位次含义、无绝对水平含义。区域化（城市内机构求维均）在结构上可行，但 DESC 核查该表无 city/region 列，机构→城市映射须跨表（institution_profile 有城市字段，lane1 快照已证），映射可行性与维护成本须甲方裁定。另注意：percent 语义的维度均值对「区域」聚合后再平均，统计意义上是「区域内机构的平均百分位」，与 UI mock 的 92/88（绝对水平观感）有语义落差。

### 2.6 稳健性与口径敏感性

两条敏感性线：其一，子盘偏置——深圳子盘经区域证据筛选（§2.2），TOP2 维（PROJECT/INDUSTRY）高分部分来自入盘机制本身，若换「全域节点+深圳权重」口径，维序可能改变；产物 notes 已写死「选择偏置须随读数披露」。其二，维度名映射——口径 A 的六维名直译上屏（项目证据/产业参与度…）与 UI 五维名（创新资源/科研产出…）不可字面对应，任何映射方案都会留下「维度语义漂移」的口实，必须甲方书面裁定后上线（§1.6 触发器）。SCIENTIFIC_GROWTH=50.0000 与 inst_power 各维=50.0 的「整数巧合」也须写进使用说明：这是百分位基准值，不是巧合。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TECHTRK_019.py`（直连久新只读 + dev/gkx 探针；运行 `python3 code/M_SCIUI_TECHTRK_019.py`）。
- 产物：`code/M_SCIUI_TECHTRK_019_out.json`。正文数字与产物键逐一对应：`jiuxin_shenzhen_dim_scores_desc`（§2.3 六行）、`jiuxin_shenzhen_dim_nodes=6233`（§2.2）、`jiuxin_global_dim_scores`（§2.3 对照列）、`jiuxin_inst_power_top5`/`jiuxin_inst_power_dim_avg`/`jiuxin_inst_power_weights`（§2.4/§2.5）、`jiuxin_shenzhen_region_assessment`（12,466 行=6,233×2，§2.2）、`jiuxin_shenzhen_region_evidence_totals`（§2.2）、`ui_mock_dimension_scores_top5`（§1.1 演示值）、派生 `jiuxin_shenzhen_dim_top5_avg=65.5638` / `jiuxin_shenzhen_dim_top1_score=80.9386`（§2.3）。
- 结果解读：深圳子盘六维现成可聚合（口径 A 即刻出数），全域对照与机构榜两条参照线齐备；区域主语与五维名映射是仅剩的两个语义缺口。
- 对照需求功能要求的评审：五维条展示——结构可满足（聚合+排序+取五）；区域主语——子盘成立但维度名映射未闭合；TOP5 语义——取维与 UI 同构，取实体榜为备选。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 深圳子盘节点 | `jiuxin_shenzhen_dim_nodes` | 6,233 |
| 装载 | 区域评估行 | `jiuxin_shenzhen_region_assessment` | 12,466（=6,233×2 版本） |
| 维度 | 六维降序 | `jiuxin_shenzhen_dim_scores_desc` | 80.9386→37.5699 |
| 对照 | 全域六维均值 | `jiuxin_global_dim_scores` | 40.5735–48.2470 |
| 派生 | TOP5 维均分 | `derived.jiuxin_shenzhen_dim_top5_avg` | 65.5638 |
| 派生 | 最高维读数 | `derived.jiuxin_shenzhen_dim_top1_score` | 80.9386 |
| 机构 | 体系规模 | `jiuxin_inst_power_rows` | 64,698 |
| 机构 | 维度均值 | `jiuxin_inst_power_dim_avg` | 五列全 50.0（百分位锚） |
| 机构 | Top5 榜 | `jiuxin_inst_power_top5` | 中科院 99.9992 居首 |
| evidence | 子盘证据面 | `jiuxin_shenzhen_region_evidence_totals` | 项目证据 46,330 主导 |
| absence | gkx 维度面 | `absence_probe[0]` | 0 命中 |
| absence | dev 维度面 | `absence_probe[1]` | 3 表命中但为企业侧 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 维度分（技术粒度） | jiuxin | `ads_technology_potential_dimension` 六维 | 深圳子盘 6,233×6 全量 | 直查 | **有**（口径 A 底座） |
| D2 | 区域子盘定义 | jiuxin | `ads_technology_region_assessment`（region_name='深圳'） | 12,466（6,233 节点） | 直查 | 有 |
| D3 | 机构维度分 | jiuxin | `ads_institution_technology_power` 四维 | 64,698 机构 | 直查 | 有（口径 B 底座） |
| D4 | 区域粒度维度结果面 | gkx/dev/jiuxin | —（gkx 0 命中；dev 企业侧 3 表；jiuxin 无区域维表） | — | **不存在** | **缺（主降档因）** |
| D5 | 五维名映射 | — | UI 自拟名 | — | 无承载 | **缺（须甲方裁定）** |
| D6 | 机构→城市映射列 | jiuxin | inst_power 无 city 列（institution_profile 有，跨表） | — | 跨表可拼 | 半 |

`support_judgment="部分支持"` 与文首一致（闸 6 对齐）。

### 3.2 D1+D2 口径 A 底座

六维体系深圳子盘全量有分（§2.2/§2.3），聚合 SQL 已跑通、读数落产物——「维度分排序」的计算链路完全现成，这是本件不降「完全不支持」的原因。使用限制两条：子盘筛选偏置披露（§2.2）、维度名映射裁定（§1.6）。

### 3.3 D3 口径 B 底座

64,698 机构四维+权重+总分现成，Top5 榜可直接出（§2.4）。区域化需要机构→城市映射（D6），institution_profile 侧城市字段 lane1 快照已证存在（`_lane1_probe_s3_01_out.json` 的 ads_institution_profile 国家/城市分布 tag），跨表 JOIN 工程量小但维序语义（百分位均值的区域平均）须产品确认。

### 3.4 D4/D5 absence_probe 全记录

否定性证据两件套：**查了什么**——① gkx 280 表 `information_schema.tables` 扫 `%dimension%` OR `%score%`；② dev `gkxlumenx_dwd`+`gkxlumenx_ads` 同条件扫描。**条件**——区域粒度维度得分结果面。**命中**——gkx 0；dev 3（enterprise_score / industry_chain_region_scorecard / svc_tech_power_score，DESC 核查为企业评分/产业链区域记分卡/科技力评分，均无「区域×五维画像」语义）。归属：**结果面不存在**（非数据稀疏）。五维名（D5）属需求侧自拟语义槽，任何库都不可能有字面对应，修复动作是甲方映射裁定而非数据工程。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 双版本去重 | 12,466=6,233×2，取 v2 口径 |
| 六维行数自洽 | 6,233 节点 × 6 维全量非空 |
| 维序确定性 | avg_score DESC 固定序（B5） |
| 全域对照 | 六维全域均值 40.5735–48.2470 区间 |
| 百分位锚 | inst_power 五列均值全 50.0 |
| absence 留证 | gkx 0 命中 / dev 3 表语义错位，产物双记录 |
| mock 登记 | 92/88/85/78/72 标演示值 |
| 脚本形态 | 只读、零 demo_*、单进程 |

### 3.6 与同批件的底表共享

六维表与 015/016/020/022 共享（potential_dimension 族），深圳子盘 6,233 与 020（geo_yearly_metrics 深圳行）、021/022（hotspot 深圳序列）的子盘口径一致——本件 §2.3 的深圳读数可直接与 020 的深圳指数读数拼成「维度+总分」画像，批内互推零漂移（B11）。

## 四、数据缺失情况

### 4.1 区域粒度维度结果面缺失（主因）

三源均无「区域×维度分」现成结果面（§3.4）。这不是数据量问题（两套分维底座数据量充足），是**主语粒度**问题：技术节点粒度与机构粒度都有维度分，唯独区域粒度没有。两条修复路径（口径 A 子盘聚合 / 口径 B 机构城市化）都是转换工程，不需要新数据采集，这也是本件维持「部分支持」而非更悲观档位的依据。

### 4.2 维度名映射缺失（次因）

UI 五维名（创新资源/科研产出/产业竞争力/人才支撑/开放协同）是前端自拟，与库侧六维/四维零重合；「人才支撑」在六维中无对应维（须引 talent 轴），「开放协同」在两套体系中均无承载。映射方案（§1.6 口径 A 假设）只能覆盖 3/5 维字面语义，其余须甲方定标或改 UI 维度名。此缺口属需求侧语义槽，不可由数据侧单方闭合。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 先行（六维换名上屏） | 产品决策 | 本件即期可交付 | 偏置披露+映射裁定书随行 |
| inst_power 城市化 JOIN | 转换工程 | 本件+008（对标） | institution_profile 城市列跨表 |
| 久新建区域维度 ADS 层 | 上游扩充 | 本件+020+022 | 把子盘聚合固化为结果面 |
| UI 五维名改对齐库侧 | 前端改造 | 本件 | 零数据成本，语义零漂移 |

档位后果：口径 A 裁定 → 部分支持语义闭合；城市化 JOIN → 口径 B 解锁；区域维度 ADS 落地 → 可升完全转换支持。推荐组合：即期口径 A + 中期区域 ADS 立项。

## 参考文献

1. Global Innovation Index 2024[EB/OL]. WIPO. https://www.wipo.int/global_innovation_index/en （R1，2026-11-01 WebSearch 核验可达）
2. European Innovation Scoreboard[EB/OL]. European Commission. https://research-and-innovation.ec.europa.eu/statistics/performance-and-innovation-monitoring-innovation-scoreboards/european-innovation-scoreboard_en （R2，2026-11-01 WebSearch 核验可达）
3. Handbook on Constructing Composite Indicators: Methodology and User Guide[EB/OL]. OECD/JRC, 2008. https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

「维度得分（TOP5）」在三份指定说明书与主需求文档均未出现。检索记录：

| 检索词 | 文档 | 命中 |
|---|---|---|
| 维度得分 | 三份指定 SRS + 主文档 | 0 |
| 维度得分 | srs 全目录 | 2（05-深度挖掘算法/03-智库系统，均非本件页面） |
| 创新资源/科研产出/产业竞争力/人才支撑/开放协同 | 全部需求文档 | 0（UI 自拟维度名） |
| TOP5 | 技术发展跟踪.md | 0（SRS 层） |

UI 侧需求证据即挂载组件本身（§1.5），mock 五值为演示值。

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_019_out.json`（2026-11-01 实跑：深圳六维分布、全域对照、机构维度榜、Top5 机构）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（stage_assessment 38,860 等底表行数）；`code/_lane1_probe2_s3_01_out.json`（ads_institution_technology_power 体系、深圳/广东机构数 tag）。
- absence 记录：gkx dimension/score 扫描 0 命中；dev 3 表命中（企业侧语义错位），样本串落产物。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.jiuxin_shenzhen_dim_scores_desc` | 分布 | 六维降序含权重 | §2.3 主表 |
| `facts.jiuxin_shenzhen_dim_nodes` | 计数 | 6,233 | §2.2 |
| `facts.jiuxin_global_dim_scores` | 对照 | 六维全域均值 | §2.3 对照列 |
| `facts.jiuxin_inst_power_dim_avg` | 审计 | 五列 50.0 | §2.5 |
| `facts.jiuxin_inst_power_rows` | 计数 | 64,698 | §2.5 |
| `facts.jiuxin_inst_power_weights` | 权重 | 0.35/0.30/0.25/0.10 | §2.5 |
| `facts.jiuxin_inst_power_top5` | 榜单 | 中科院 99.9992 等 5 行 | §2.4 |
| `facts.jiuxin_shenzhen_region_assessment` | 计数 | 12,466 行/6,233 节点 | §2.2 |
| `facts.jiuxin_shenzhen_region_evidence_totals` | 证据 | 项目 46,330 等 | §2.2 |
| `facts.ui_mock_dimension_scores_top5` | mock | 92/88/85/78/72 | §1.1 |
| `derived.jiuxin_shenzhen_dim_top5_avg` | 派生 | 65.5638（32,782/500） | §2.3 |
| `derived.jiuxin_shenzhen_dim_top1_score` | 派生 | 80.9386 | §2.3 |
| `absence_probe` | 负证据 | 2 条 | §3.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

### B.3 共享快照消费

本件消费 `_lane1_probe2_s3_01_out.json` 的 institution_technology_power 体系结构 tag（四维名+权重）与深圳/广东机构计数语境；消费 `_shared_probe_s3_01_out.json` 的 stage_assessment=38,860 底表口径（v1/v2 双版本审计同 015 件）。引用数字与快照原值零漂移（W2-2）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 维度形态 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 多支柱排序 | WIPO GII（R1） | 国家×7 支柱 | 无（结构可借） | 高（形态同构） |
| 区域记分牌 | EU EIS（R2） | 区域×8 维 | 无 | 高（区域语义原型） |
| 复合指标维度层 | OECD/JRC（R3） | 归一+加权+维度披露 | **六维体系现成** | **最高（口径 A）** |
| 机构百分位维 | inst_power 四维 | 机构×4 维 | 现成 64,698 | 中（需城市化） |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| potential_dimension 六维 | 深圳子盘 6,233×6 | 全量有分 | 主语是节点非区域 |
| inst_power 四维 | 64,698 | 百分位锚 50 | 无城市列 |
| 区域维度 ADS | 0 | — | 结构缺失 |
| 五维名映射 | — | — | 需求侧语义槽 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1 | 口径 A 六维换名 TOP5（65.5638/80.9386 读数上屏） | 甲方映射裁定 |
| v2 | +口径 B 城市维度榜（inst_power 城市化） | 跨表 JOIN 工程 |
| v3 | 区域维度 ADS 结果面 | 久新上游建层 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 65.5638 被读作区域绝对水平 | 中 | 百分位语义+子盘偏置注记随行 |
| 维度名映射语义漂移 | 中 | 裁定书留痕，UI 名侧改优先 |
| inst_power 50.0 锚点误读为高分体系 | 低 | 使用说明写死百分位性质 |

### C.5 总判

**部分支持**：两套分维底座数据量充足（6,233 节点六维/64,698 机构四维），缺的是区域主语结构（D4）与需求侧维度名映射（D5）；口径 A 即刻可出数（65.5638/80.9386 已落产物），升档按「映射裁定→城市化→区域 ADS」三步走（§1.6 触发器）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_019.py` | 退出码 0，落 `_out.json` |
| 深圳六维 | `facts.jiuxin_shenzhen_dim_scores_desc` | 80.9386→37.5699 降序 |
| TOP5 派生 | `derived.jiuxin_shenzhen_dim_top5_avg` | 65.5638 |
| 机构榜 | `facts.jiuxin_inst_power_top5` | 中科院 99.9992 居首 |
| 共享快照对账 | `_shared_probe_s3_01_out.json` | 38,860 底表零漂移 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 均为部分支持 |
| demo 禁引 | 脚本 grep demo_ | 0 命中 |
| mock 残留 | `rg "keyAreaDimensionScores" repos/demo-ui-science/src` | 正式版替换后无引用 |

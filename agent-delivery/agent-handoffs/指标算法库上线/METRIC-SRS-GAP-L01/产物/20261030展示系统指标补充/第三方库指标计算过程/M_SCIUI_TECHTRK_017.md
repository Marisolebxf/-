# 技术热点热度值（M_SCIUI_TECHTRK_017）

> **类型**：SCORE（热度综合分，五分量合成）｜ **域**：科技发展态势·技术发展跟踪·竞争情报·热点热度｜ **UI 挂载**：`techDevelopmentPlan.js:327`（趋势序列「热点热度」线）+ `techDevelopmentPlan.js:473`（详情卡「热点热度」行）；语义源头 `techDevelopmentTracking.js:112` 起的话题热度字段
> **数据支持度**：**部分支持**｜ **公式定义人**：库侧既成（久新 hotspot_score 五分量合成）+ 工程侧读数定义（对齐 UI 榜单语义）｜ **口径归属**：需求未明列叶（三份指定说明书未出现指标名），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TECHTRK_017.py`｜ **产物**：`code/M_SCIUI_TECHTRK_017_out.json`
> **四判定摘要**：直接结构 = 是（久新 hotspot_snapshot/yearly/signal 三表族：总分+五分量+年度序列+信号词）；直接数据 = 部分（19,430 节点全量有分，但 82.22% 状态 INSUFFICIENT_EVIDENCE）；依赖结构 = 部分（五分量全为论文/专利衍射，无资讯热度分量）；依赖数据 = 部分（年度序列 2015–2026 全，但单版本无对照）
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

**本件判定：部分支持。** 久新 `ads_technology_hotspot_snapshot` 给出三库唯一的热度结果面：19,430 个技术节点每个都有 0–100 的 hotspot_score，由五分量合成（growth_score 增长 / author_diffusion_score 作者扩散 / institution_diffusion_score 机构扩散 / impact_score 影响 / patent_signal_score 专利信号），配 hotspot_rank 排名、五档 hotspot_status、年度序列 `hotspot_yearly`（2015–2026 十二年逐年分+同比+三年滚动）与热点信号词表 `hotspot_signal`（9,018 条）。降档有两因：其一，**证据强度断层**——82.22% 的节点（15,976/19,430）状态为 INSUFFICIENT_EVIDENCE，连 hotspot_rank=1 的节点也不例外，热度分可算但「热点」名义下多数节点证据不足以上榜；其二，**分量谱系偏科**——五分量全部由论文/专利衍射，UI 热点语义里的「资讯热度」零分量（与 014 件的资讯源缺失同根）。分数直接支持、榜单语义部分支持，综合判部分支持。

### 批次纪律摘要（B1–B11 对照，skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 两派生键分子分母同源同版本（jiuxin v2 单版本 19,430） |
| B4 | 负结论带探针 | absence_probe 四条（dev/gkx 结果面、资讯分量、权重文档） |
| B5 | 确定性 | 聚合 ORDER BY 键排序；Top 榜按 hotspot_rank 唯一序 |
| B6 | 闸门自身被闸 | 本件不跑闸门，派单方统一跑 |
| B7 | 产物只由脚本产出 | 实跑产出，无手改 |
| B8 | 回执不复收 | 状态分布/Top 榜/年度序列亲自实跑 |
| B9 | 单位/日期陷阱 | yearly 表 model_version 命名与 snapshot 不同（technology_hotspot_yearly_v1）；2026 年进行中数据需标注 |
| B10 | 口径裁定保守交付 | 「全量热度分」vs「证据充分榜（非 INSUFFICIENT 节点）」双口径（§1.6） |
| B11 | 多本账互推 | 38,860/233,160/9,018 与共享快照零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 热度分存在吗？ | 存在且全量 | hotspot_score 19,430 节点 100% 有分 |
| 榜单可信吗？ | 打折 | 82.22% INSUFFICIENT_EVIDENCE；rank1 亦然 |
| 资讯热度有吗？ | 无 | 五分量全论文/专利系；203 表无 news 类 |

## 摘要

「技术热点热度值」在 UI 是榜单与趋势线的主读数：话题热力榜按 heat 降序取 Top10、趋势序列画「热点热度」逐年线、详情卡给单记录 heat 分。库侧实测给出完整的的热度基础设施：`ads_technology_hotspot_snapshot` 单版本 19,430 节点全量评分（min 11.13 / max 79.09 / avg 42.98），Top5 为量子搜索算法与计算复杂性 79.09、JPEG 图像压缩标准与架构 77.25、医学教育中的移动技术整合 76.37 等（每分带五分量分解）；`ads_technology_hotspot_yearly` 233,160 行铺开 2015–2026 逐年热度（年度均值 2015 年 21.47 → 2022 峰值 38.48 → 2026 进行中 19.90），带同比变化与三年滚动分；`ads_technology_hotspot_signal` 9,018 条信号词（「强化学习」「Janus 颗粒」等，各带证据论文数与首见年份）。三个降档事实：82.22% 节点证据不足状态、五分量无资讯源、榜单 Top 名单偏传统主题（与 UI mock 的具身智能/量子纠错等前沿叙事错位）。判**部分支持**：分数与序列即取即用，榜单上线须带证据状态标签与口径裁剪。

- 需求判定：需求未明列叶（seq 48「话题热力图展示」述功能未定义热度算法）。
- 复现状态：脚本已跑通；分数统计、状态分布、Top5、年度序列、信号样本落产物。
- 档位结论：**部分支持**（证据强度断层+分量偏科双因）。
- 关键事实：rank=1 节点状态也是 INSUFFICIENT_EVIDENCE——榜单与状态必须同屏展示。
- 升档路径：证据阈值晋级规则（INSUFFICIENT 节点的上榜 suppression）+ 资讯分量接入 → 榜单语义闭合。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/技术发展跟踪/**技术评估结果**/话题热力图展示（SRS seq 48，excel_row 51）的热度读数，UI 侧具体挂载三处：① `techDevelopmentTracking.js:112` 起的 `coreHotTopics` 数组每项带 `heat` 字段（具身智能机器人 92、机器视觉与多模态感知 86 等 8 项核心话题），`buildMetrics()` 1015 行把它聚成「话题热度」指标卡（averageHeat），热力矩阵 `buildHeatMatrix()` 以 heat 为基线生成逐年注意力值；② `techDevelopmentPlan.js:327` 趋势序列第二条线 `name: '热点热度'`（values 由 average(records,'heat') 派生）；③ `techDevelopmentPlan.js:473` 详情卡 metricCards「热点热度」行（record.heat）。

值得记录的语义细节：tracking 页的 heat 是**话题级**（technology topic，如「量子计算纠错」），plan 页的 heat 是**记录级**（规划记录，如「全球智能机器人热点捕捉」96 分）——两处同名不同粒度，与 016 件同构的粒度断层。另外 `buildTrendSeries`（998–1010 行）的热度线由 seed（所选话题 heat 均值）线性外推 + 年份取模扰动生成，纯公式造线——前端作者没有假装有历史热度数据，这反而给库侧真实年度序列（hotspot_yearly 2015–2026）留出了干净的替换位。

### 1.2 为什么需要本指标

热度是跟踪系统的「入口读数」：用户第一眼看的是「什么在升温」，然后才下钻成熟度/潜力。热力图、榜单、趋势线三个消费位共用一个 heat 语义，说明它是技术发展跟踪板块的枢纽指标。库侧五分量设计的价值在于热度可拆解——一个节点的 79 分是增长驱动（growth_score 91.5）还是专利信号驱动（patent_signal_score 97.8），拆开看才知道「热」的性质：学术热、产业热还是扩散热。这比 mock 的裸常量多出一层可解释性。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。** SRS seq 48 原文：「基于技术领域关键词和主题，生成热度分布图，直观展示各技术话题的关注度和活跃程度」——定义了展示目标（关注度/活跃程度）未定义算法（怎么算热、分几个分量、时间窗多长）。主需求文档 421 行段同。《03-新型高端智库系统》技术体系分析.md:387 有一处公式级定义（「对每个关键词计算带时间衰减的热度值与增长率」）属另一系统板块，且是关键词粒度非技术节点粒度，仅作方法参考。

### 1.4 类似指标权威方法可行性分析概要

热度/突发检测的权威方法族：Kleinberg 突现检测（R1）把「话题在文档流中 sharply rising in frequency」形式化为无限状态自动机模型，是热度时间结构的经典——库侧 yearly 表的同比/滚动分是它的简化版；OECD 信号扫描体系（R2/R3）定义弱信号→议题的晋级评估流程，对应库侧五档 hotspot_status 的状态机设计。方法族对照：

| 方法族 | 代表 | 热度形态 | 与本库匹配 |
|---|---|---|---|
| 突现检测 | Kleinberg 2003（R1） | 时间轴 burst 区间 | 部分（yearly 同比/滚动有、burst 状态机无） |
| 多分量合成 | 久新既成 | 五分量 0-100 | **库侧现状**（论文/专利系） |
| 信号晋级评估 | OECD（R2/R3） | 弱信号→议题状态机 | 部分（五档 status 有、晋级证据规则未公开） |

结论：库侧是「多分量合成+状态标注」的工程实现，时间突现结构与资讯分量缺位。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/techDevelopmentPlan.js:327`（趋势线）、`:473`（详情卡）；`techDevelopmentTracking.js:112-231`（coreHotTopics heat 字段）、`:1015-1018`（buildMetrics 热度卡）、`:998-1010`（buildTrendSeries 造线公式）。
- SRS：`…/技术发展跟踪.md` seq 48（excel_row 51），原文见附录 A。
- 跨板块方法参考：《03-新型高端智库系统/战略咨询智能支持/技术体系分析.md》:387（时间衰减热度公式，关键词粒度）。

### 1.6 推测原意与推测定义

**推测定义（双口径并列，B10）**：

- 口径 A（**全量热度分**）：`heat(node) = hotspot_score`，19,430 节点全量出分——热力图/趋势线的底层数据位可直接填充；
- 口径 B（**证据充分榜**，建议榜单口径）：`ranking = nodes WHERE hotspot_status != 'INSUFFICIENT_EVIDENCE' ORDER BY hotspot_score DESC`——3,454 节点（17.78%）的子盘，榜单语义「热点」要求证据强度达标。

**降档/升档触发器**：若甲方接受口径 A+状态标签同屏 → 热力图/趋势线即期上线，榜单按口径 B 裁剪，维持部分支持语义闭合；若资讯分量接入（MARKET 域证据入链，与 014 件同工程）→ 分量谱系补全；若 INSUFFICIENT 节点的晋级规则（证据阈值）公开并可配置 → 状态机透明，两者齐备升完全转换支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/技术发展跟踪.md` |
| 所属四级功能 | 技术发展跟踪（8 叶，seq 48–55） |
| 所属面板 | 技术评估结果（seq 48–51） |
| 本件叶 | **话题热力图展示（seq 48）之热度读数——需求未明列「热度值」指标名** |
| 相邻叶 | 地理分布图（seq 49）/ 动态气泡图（seq 50，maturity/potential 轴与 016 件关联）/ 弦线图（seq 51） |
| UI 容器 | 热力矩阵、热度指标卡、趋势线、详情卡四消费位 |

批内关系：与 014 件共享资讯源缺失根因（五分量无资讯）；与 Lane 4 的 021（论文热度值）是近亲——021 是单源论文热度、本件是五分量综合热度，引用时注意区分；020（技术发展指数）若立项可消费本件年度序列做趋势段。

## 二、计算过程

### 2.1 装载与三表族结构

直连久新 Doris（只读）。表族三件：`ads_technology_hotspot_snapshot`（38,860 行=19,430 节点×2 版本；hotspot_score+五分量+rank+status）；`ads_technology_hotspot_yearly`（233,160 行=19,430×12 年，**model_version 命名为 technology_hotspot_yearly_v1**，与 snapshot 的 v1/v2 命名不同——产物键 `jiuxin_hotspot_yearly_model_version` 留证，避免误按 v2 过滤滤空）；`ads_technology_hotspot_signal`（9,018 行信号词，另有 filter_stage_20261031 / unfiltered_20261031 两个日期缀快照表，本件以主表为准）。snapshot 双版本逐节点同分（与 015/016 件同构审计），读数按单版本。

### 2.2 全量热度分与状态分布

v2 单版本（产物键 `jiuxin_hotspot_score_stats_v2`）：n=19,430 全量有分，min 11.12924 / max 79.090792 / avg 42.9827。五档状态分布（`jiuxin_hotspot_status_dist_v2`）：INSUFFICIENT_EVIDENCE 15,976（82.22%，派生键 `jiuxin_insufficient_evidence_share_pct`）、ESTABLISHED_GROWING 2,539（13.07%）、MATURE 766（3.94%）、WATCH 146（0.75%）、EARLY_EMERGING 3（0.02%）；证据充分子盘（非 INSUFFICIENT）3,454 节点占 17.78%（`jiuxin_hotspot_evidence_sufficient_share_pct`）。这个分布本身就是重要读数：库方诚实地把「分数可算」与「证据足以称热点」分开——82% 的节点有分但不够格叫热点。

### 2.3 Top 榜实测与分量分解

单版本 Top5（`jiuxin_hotspot_top5_v2`，JOIN profile 取中文名）：rank1 量子搜索算法与计算复杂性 79.090792、rank2 JPEG图像压缩标准与架构 77.245098、rank3 医学教育中的移动技术整合 76.369602、rank4 蒙特卡洛树搜索应用 76.108652（EARLY_EMERGING，Top5 唯一非 INSUFFICIENT）、rank5 地震波传播计算方法 74.775593。Top1 分量分解（`jiuxin_hotspot_top1_components`）：growth 91.538422 / author_diff 62.25745 / institution_diff 61.423645 / impact 61.670698 / patent_signal 97.817695——增长与专利信号双高驱动。两个榜单观察：其一，Top5 中 4 个状态 INSUFFICIENT_EVIDENCE，印证口径 B 必要性；其二，名单偏传统主题（JPEG/地震波传播），与 UI mock 的具身智能/量子纠错前沿叙事错位——这是 ETO 研究簇节点池（OpenAlex 系）与中文产业语境的语料差，榜单上线时预期管理要先行。

### 2.4 年度序列实测

`hotspot_yearly` 逐年分布（`jiuxin_hotspot_yearly_years`，12 条）：2026 均分 19.896688（进行中）、2025 30.850458、2024 34.486430、2023 35.907001、2022 38.478143（峰值）、2021 40.986620（实际最高）、2020 34.293855、2019 28.542624、2018 27.257966、2017 25.455052、2016 23.350815、2015 21.471375——逐年爬升至 2021 高点后回落。趋势状态分布（`jiuxin_hotspot_yearly_trend_status_dist`，单版本 194,300 行）：INSUFFICIENT_EVIDENCE 159,769 / DECLINING 12,264 / RISING 12,045 / STABLE 11,225 / BASELINE 33。年份覆盖与 UI 时间轴（2020–2026）完全重叠，趋势线的「热点热度」位可直接换真数据；2026 年低值须标「年度进行中，截至 2026-10-16」。

### 2.5 信号词表与资讯缺位

`hotspot_signal` 9,018 行覆盖 3,742 个节点（产物键 `jiuxin_hotspot_signal_distinct_nodes`），样本（`jiuxin_hotspot_signal_sample`）：「Janus 颗粒」（rank 1，证据论文 11 篇，首见 2013）、「强化学习」（rank 1，17 篇，2011）——信号词带首见年份与论文证据数，是「弱信号」叙事的直接素材。但 signal 的 evidence_paper_count 锚定论文系，全表无资讯类信号；结合五分量无资讯分量（§2.3）与 203 表无 news 类表（探针），「资讯热度」在三库的热度体系中零承载——这是与 014 件同根的结构缺口。

### 2.6 稳健性与口径敏感性

三个读数陷阱：其一，hotspot_score 的合成权重未入库（metric_definition_version 列有版本号但五分量→总分的配比公式无数据面承载，探针留证），复算只能验证分量存在性不能验证合成式——本件以分量读数交付、合成式标注「库方模型内部」；其二，author/institution_diffusion 两分量在 Top 榜多数节点取值高度集中（62.25745/61.423645 在 Top1-3 完全相同），疑似分量分数化后的饱和效应，分量间独立性存疑，展示分解图时须提示；其三，2026 年进行中数据与 2025 比较会得出「暴跌 36%」的假趋势，趋势线须带数据截止注记。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TECHTRK_017.py`（直连久新只读；运行 `python3 code/M_SCIUI_TECHTRK_017.py`）。
- 产物：`code/M_SCIUI_TECHTRK_017_out.json`。正文数字与产物键逐一对应：`jiuxin_hotspot_snapshot_rows_total=38860`（§2.1）、`jiuxin_hotspot_score_stats_v2`（§2.2）、`jiuxin_hotspot_status_dist_v2`（§2.2）、`jiuxin_hotspot_top5_v2`+`jiuxin_hotspot_top1_components`（§2.3）、`jiuxin_hotspot_yearly_years` 12 条+`jiuxin_hotspot_yearly_trend_status_dist`（§2.4）、`jiuxin_hotspot_signal_*` 三键（§2.5）、派生 `jiuxin_hotspot_evidence_sufficient_share_pct=17.78` / `jiuxin_insufficient_evidence_share_pct=82.22`。
- 结果解读：分数/序列/信号三件套全量可查；榜单须按口径 B 裁剪并带状态标签。
- 对照需求功能要求的评审：「展示关注度与活跃程度+悬停显示具体数值和趋势+点击深入查看详细评估数据」——关注度✓（score）、趋势✓（yearly 12 年）、点击详情半✓（详情参数需拼 016 维度分+015 阶段档）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 结构 | snapshot 总行/单版本 | `jiuxin_hotspot_snapshot_rows_total` / `…_nodes_single_version` | 38,860 / 19,430 |
| 分数 | 统计三读数 | `jiuxin_hotspot_score_stats_v2` | 11.13 / 79.09 / 42.98 |
| 状态 | 五档分布 | `jiuxin_hotspot_status_dist_v2` | 15,976/2,539/766/146/3 |
| 榜单 | Top5+中文名 | `jiuxin_hotspot_top5_v2` | 量子搜索 79.09 居首 |
| 分量 | Top1 五分量 | `jiuxin_hotspot_top1_components` | growth 91.54 / patent 97.82 |
| 序列 | 12 年均分 | `jiuxin_hotspot_yearly_years` | 2015 21.47→2021 40.99→2026 19.90 |
| 趋势 | 状态分布 | `jiuxin_hotspot_yearly_trend_status_dist` | RISING 12,045 等 |
| 信号 | 词表样本 | `jiuxin_hotspot_signal_sample` | 强化学习/Janus 颗粒等 |
| 派生 | 证据充分占比 | `derived.jiuxin_hotspot_evidence_sufficient_share_pct` | 17.78%（3,454/19,430） |
| absence | 资讯分量/合成权重 | §3.4 四件套 | 0/0 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 热度总分 | jiuxin | `hotspot_snapshot.hotspot_score` | 19,430（单版本全量） | 直查 | **有** |
| D2 | 五分量分解 | jiuxin | 同表 5 分量列 | 38,860 | 直查 | 有（分量间独立性存疑） |
| D3 | 年度序列 | jiuxin | `hotspot_yearly` | 233,160（12 年×19,430） | 直查 | 有 |
| D4 | 热点信号词 | jiuxin | `hotspot_signal` | 9,018 | 直查 | 有 |
| D5 | 资讯热度分量 | 三库 | —（203 表无 news；五分量无资讯位；gkx 新闻表链外） | 0 | **不存在** | **缺（主降档因）** |
| D6 | 合成权重口径 | jiuxin | —（metric_definition_version 仅版本号） | 0 | 不存在 | 缺（次因） |

`support_judgment="部分支持"` 与文首一致（闸 6 对齐）。

### 3.2 D1–D4 热度基础设施：三库唯一的完整体系

§2.1–§2.5 已列全。工程红利两点：yearly 表自带 yoy_change/rolling_3y_score 列，趋势线不用自算环比；signal 表带 first_observed_year，「N 年前首次出现的信号」这类叙事位可直接填充。

### 3.3 D5/D6 资讯分量与合成权重 absence_probe 全记录

否定性证据四件套：**查了什么**——① dev `gkxlumenx_dwd` hot/heat/score 关键词（0 命中）；② gkx 280 表 hotspot/heat 关键词（0 命中；`dwd_industry_analysis_topics` 1,052 行为产业分析文档主题表，12 列结构无热度值列，DESC 留证）；③ jiuxin 203 表 news/media/literature 本地过滤（0 命中）；④ jiuxin hotspot_score 合成权重（五分量与总分并存但配比公式无数据面承载）。**条件**——资讯类热度分量/合成权重口径。**命中**——0/0/0/0。归属：**结构缺失**（分量位与权重文档均未建），修复依赖上游（资讯入链与口径公开）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 双版本去重 | 38,860=19,430×2，两版同分 |
| yearly 版本名 | technology_hotspot_yearly_v1（与 snapshot 异名，产物留证） |
| 状态分布加和 | 15,976+2,539+766+146+3=19,430 自洽 |
| 年度覆盖 | 2015–2026 共 12 年×19,430=233,160 自洽 |
| Top 榜唯一序 | hotspot_rank 1–5 无重复节点（单版本口径） |
| 信号表 | 9,018 行/3,742 节点，样本含首见年份 |
| 脚本形态 | 只读、零 demo_*、单进程 |

## 四、数据缺失情况

### 4.1 资讯热度分量缺失（主因，与 014 件同根）

五分量全由论文/专利衍射，UI 热点语义的「产业资讯升温」无分量承载。gkx 有新闻底表（`dwd_news_base` 20,000 行，链外存量）但主题映射工程未建。修复路径与 014 件完全同一（资讯源注册入链），一次工程两件升档。

### 4.2 证据强度与口径透明度（次因）

82.22% 节点 INSUFFICIENT_EVIDENCE 且 Top1 亦然——「分数可算」与「可称热点」之间隔着证据阈值，而阈值的晋级规则未公开（合成权重同缺）。展示侧缓解：榜单按口径 B 裁剪+状态标签同屏；根本缓解：库方公开 status 晋级规则与分量合成式（属口径文档非数据工程）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 B 榜单+状态标签 | 产品决策 | 本件即期 | 3,454 节点证据充分子盘 |
| 资讯分量接入 | 数据工程 | 本件+014 | gkx 新闻表注册入链 |
| 晋级规则与合成式公开 | 口径文档 | 本件 | 消除复算黑箱 |
| 趋势线截止注记 | 前端 | 本件 | 2026 进行中数据防误读 |

档位后果：口径 B → 部分支持语义闭合；资讯分量+规则公开 → 升完全转换支持。推荐：即期口径 B+截止注记，中期资讯入链。

## 参考文献

1. Bursty and Hierarchical Structure in Streams[EB/OL]. Kleinberg J M. Data Mining and Knowledge Discovery, 2003. https://link.springer.com/article/10.1023/A:1024940629314 （R1，2026-11-01 WebSearch 核验可达）
2. Strategic intelligence tools for emerging technology governance[EB/OL]. OECD, 2025. https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/07/strategic-intelligence-tools-for-emerging-technology-governance_b7009977/02c05775-en.pdf （R2，2026-11-01 WebSearch 核验可达）
3. Building capacity in technology horizon scanning[EB/OL]. OECD, 2026. https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/04/building-capacity-in-technology-horizon-scanning_7a0a98c6/b4f0d383-en.pdf （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》seq 48（excel_row 51）：

> 基于技术领域关键词和主题，生成热度分布图，直观展示各技术话题的关注度和活跃程度。用户可通过时间轴调整查看不同时期的热度变化，支持鼠标悬停显示具体数值和趋势，点击热点区域可深入查看该话题的详细评估数据和相关技术参数。

「技术热点热度值」指标名在三份指定说明书与主文档均未出现。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 技术热点热度值 / 热度值 | 三份指定 SRS + 主文档（展示系统部分） | 0（「热度值」公式级定义仅见智库系统板块技术体系分析.md:387，跨板块） |
| 热度 | 技术发展跟踪.md seq 48 功能描述；科技全域态势.md:221（热力图展示，要素分布语境） | 2（均为功能描述） |
| 热点热度 | UI 组件 techDevelopmentPlan.js:327/473 | 2（mock 挂载） |
| 话题热力 | 技术发展跟踪.md seq 48 叶名 | 1 |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_017_out.json`（2026-11-01 实跑：分数统计、状态分布、Top 榜、年度序列、信号样本）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（`ads_technology_stage_assessment`=38,860 同基零漂移）。
- Lane 3 探针快照：`_probe_lane3_jiuxin2_out.json`（三表 DESC/COUNT）、`_probe_lane3_jiuxin3_out.json`（状态/年份/Top10/模型版本）、`_probe_lane3_jiuxin4_out.json`（版本×状态交叉、Top5 节点名、2026 覆盖度）、`_probe_lane3_final_out.json`（gkx 主题表 DESC/COUNT/样本）、`_probe_lane3_gkx_out.json`（关键词扫描）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_TECHTRK_017 | 文首 |
| `ui_evidence` | 证据 | techDevelopmentPlan.js:327/473 + tracking:112 | §1.1/§1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.jiuxin_hotspot_snapshot_rows_total` | 计数 | 38,860 | §2.1 |
| `facts.jiuxin_hotspot_score_stats_v2` | 统计 | 11.13/79.09/42.98 | §2.2 |
| `facts.jiuxin_hotspot_status_dist_v2` | 分布 | 五档 | §2.2 |
| `facts.jiuxin_hotspot_top5_v2` | 榜单 | 5 节点含中文名 | §2.3 |
| `facts.jiuxin_hotspot_top1_components` | 分量 | 五分量 | §2.3 |
| `facts.jiuxin_hotspot_yearly_model_version` | 版本 | technology_hotspot_yearly_v1 | §2.1 |
| `facts.jiuxin_hotspot_yearly_years` | 序列 | 12 年 | §2.4 |
| `facts.jiuxin_hotspot_yearly_trend_status_dist` | 分布 | 五态 | §2.4 |
| `facts.jiuxin_hotspot_signal_*` 三键 | 信号 | 9,018 行/3,742 节点/样本 | §2.5 |
| `facts.gkx_industry_analysis_topics_rows` | 对照 | 1,052（无热度列） | §3.3 |
| `facts.ui_mock_core_topics_heat` | mock 登记 | 92/86/81/74/78/84/89/77 | §1.1 |
| `derived[0..1]` | 派生比 | 17.78 / 82.22 | §2.2 |
| `absence_probe` | 负证据 | 4 条 | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 多分量合成+状态机 | 久新既成 | 五分量+五档 status | **最高（现状）** |
| 突现检测 | Kleinberg（R1） | yearly 同比/滚动（简化版） | 中（无 burst 状态机） |
| 弱信号晋级 | OECD（R2/R3） | signal 词表+status 档 | 中高（规则未公开） |
| 资讯热度 | — | **无** | 升档路径 |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| snapshot 总分+分量 | 38,860（单版本 19,430） | 全量 | 合成权重未公开 |
| yearly 序列 | 233,160 | 12 年完整 | 2026 进行中 |
| signal 词表 | 9,018 | 带首见年份 | 论文系单源 |
| 资讯分量 | 0 | — | 结构缺失 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1 | 热力图/趋势线真数据+口径 B 榜单+状态标签 | 无 |
| v2 | 资讯分量接入 | 与 014 件同工程 |
| v3 | 晋级规则/合成式公开+burst 结构 | 口径文档/模型迭代 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| Top 名单与中文产业语境错位 | 中 | 预期管理+领域筛选器先行 |
| 82% INSUFFICIENT 被忽略 | 中 | 状态标签强制同屏 |
| 2026 假暴跌误读 | 中 | 截止注记 |
| 分量饱和（62.26/61.42 集中值） | 低 | 分解图加独立性提示 |

### C.5 总判

**部分支持**：热度分/年度序列/信号词三件套三库唯一且全量；降档因资讯分量缺失（与 014 同根）与证据强度断层（82.22% INSUFFICIENT）；升档路径「资讯入链+规则公开」双轨明确。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_017.py` | 退出码 0，落 `_out.json` |
| 状态分布 | `facts.jiuxin_hotspot_status_dist_v2` | 五档加和=19,430 |
| 年度序列 | `facts.jiuxin_hotspot_yearly_years` | 12 条 2015–2026 |
| 证据充分占比 | `derived.jiuxin_hotspot_evidence_sufficient_share_pct` | 17.78 |
| 共享快照对账 | `_shared_probe_s3_01_out.json` | 同基零漂移 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 均为部分支持 |
| demo 禁引 | 脚本 grep demo_ | 0 命中 |

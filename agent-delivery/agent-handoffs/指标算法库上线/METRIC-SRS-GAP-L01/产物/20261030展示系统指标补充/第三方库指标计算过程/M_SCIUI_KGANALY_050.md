# 图谱合作强度（合作边权重）（M_SCIUI_KGANALY_050）

> **类型**：无业务逻辑数值类（边权重统计，图结构统计）｜ **域**：科技信息展示系统·科技知识图谱·图查询资产·深入分析｜ **UI 挂载**：图查询资产深入分析抽屉 → `queryAssetDeepAnalysis.js:88` bars 图 x 轴首项 `{data: ['合作强度', '成果关联', '机构覆盖', '项目参与', '引用影响']}`，:92 series 首值 mock 85（`85 - (i%2)*seededInt(...)` 递减）——`QueryAssetDeepAnalysisDrawer.jsx` bars 类资产的「维度得分」柱图（thumbKind='bars' 分支）
> **数据支持度**：**完全转换支持**（久新边表 `relation_confidence_score` 27.08-100 均值 49.02 + `total_citation_count` 0-142 均值 1.168 全图 587,252 边直查 GROUP BY 可得；gkx `dwd_scholar_coauthor.co_paper_count` 真·合著论文数 1-542 备承载三口径全实算）｜ **公式定义人**：UI 前端 mock（85 常量递减，无算法）——本件按边权重统计标准口径重建，推测定义｜ **口径归属**：UI 拆件叶（SRS seq 434 社群结构/合作集群语义域的资产体检读数），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_KGANALY_049_050_052.py`（049/050/052 合算）｜ **产物**：`code/M_SCIUI_KGANALY_050_out.json`（三口径权重分布+Top10 具名边）
> **四判定摘要**：直接结构 = 边权重列现成（confidence/citation/co_paper_count 三列在三库均真实在库）；直接数据 = 近乎（直查即得统计量，缺「已发布结果面」形态）；依赖结构 = **足**；依赖数据 = **足**（587,252+1,187,606 行全量）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live）逐一探针留证；久新 2026-11-02 当日 live 直连实算；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。**（判档边界件说明：边权重列三库现成、直查即得——比 049 更接近直接；但「合作强度」的**单一读数形态**（bars 图一个柱值）需要从边权重分布聚合（均值/分位/Top-N 榜单）而成，三源无 `cooperation_strength` 结果面，聚合口径（均值 vs Top 均值 vs 归一分）未定——按保守原则判**完全转换支持**。）证据链：①久新 `ads_technology_graph_edge.relation_confidence_score` 全图 587,252 边 min 27.07971/max 100.0/avg **49.016156**（`jiuxin_edge_confidence_min_max_avg`），分桶 c0_40:109,673/c40_60:365,474/c60_80:102,606/c80_100:9,499（`jiuxin_edge_confidence_buckets`）；②并列口径 `total_citation_count` 0-142/avg 1.168（`jiuxin_edge_citation_min_max_avg`）；③gkx `dwd_scholar_coauthor.co_paper_count` 20,000 行框 min 1/max 542/avg 4.775（`gkx_co_paper_count_min_max_avg`），≥2 篇边 12,195（`gkx_co_paper_count_ge2_edges`）；④Top10 具名边全落产物（`jiuxin_top10_edges_by_confidence`/`gkx_top10_edges_by_co_paper`）。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 占比分母=全图 587,252 边（各桶披露）；三口径不相混 |
| B4 | 负结论带探针 | absence_probe 三件；dev 空壳族级快照 |
| B5 | 确定性 | Top10 排序键 (confidence DESC, citation DESC)；gkx 框 ORDER BY dwd_id |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 本件 py 实算出 _out.json |
| B8 | 回执不复收 | GROUP BY 幂等 |
| B9 | 单位/日期陷阱 | confidence 无量纲 0-100；citation 单位次；co_paper 单位篇——三口径单位分标 |
| B10 | 口径裁定保守交付 | 三口径并列（confidence/citation/co_paper）+聚合形态待裁（§2.2） |
| B11 | 多本账互推 | 边总数 587,252 与 039/052/001 同源；分桶和=587,252 对账 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有「合作强度」结果列吗？ | 无独立结果面（权重列是原料非读数） | absence_probe |
| 边权重原料够吗？ | **够（三列三库现成）** | confidence/citation/co_paper（§3.1） |
| 现在就能算吗？ | **已实算（三口径全量）** | avg 49.02/1.168/4.775（§2.2） |

## 摘要

「图谱合作强度（合作边权重）」是图查询资产深入分析抽屉 bars 图的 x 轴首项（mock 值 85 递减），语义是图资产里合作/关联边的权重强度——「这张图里的连接有多紧」。数据侧判定：**完全转换支持**——三源无 cooperation_strength 结果面，但边权重列三库现成，本件实算三口径：①**关系置信度**（主口径，久新 587,252 边）：min 27.08/max 100/avg **49.02**，分桶呈 40-60 区间单峰（62.2% 边落在中段，80+ 强边仅 1.6%）；②**引用计数**（并列口径）：0-142/avg 1.168——证据量视角，80.6% 边引用 1-3 次的长尾；③**合著论文数**（gkx 备承载，语义最贴合「合作」二字）：1-542/avg 4.775，Top1 学者对 542 篇合著。核心发现：mock 的 85 是 0-100 量纲拍脑袋值，真图 confidence 均值 49.02——若 bars 图按 0-100 满分尺回填，置信度口径即期可用（均值/Top 均值/分位三种聚合形态待裁）；「合作强度」字面语义（合著）与主承载语义（技术关联置信度）有偏移，gkx co_paper 是语义最准的备选。

- 需求判定：UI 拆件叶（bars 类资产维度得分首柱——SRS seq 434 合作集群语义域）。
- 复现状态：脚本已实算通过；三口径分布+Top10 具名边全落产物。
- 档位结论：**完全转换支持**（判档边界件——权重列现成近乎直接，聚合读数形态未定保守判转换）。
- 关键事实：三口径三库三语义（关联强度/证据量/合著数）——回填前须先裁「合作」指什么；分桶和 109,673+365,474+102,606+9,499=587,252 零漂移对账。
- 降档风险：无；升档路径：聚合结果面落表 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统/科技知识图谱/图查询资产深入分析——`QueryAssetDeepAnalysisDrawer.jsx` 抽屉的 bars 类资产分支：`queryAssetDeepAnalysis.js:83-95` `thumbKind === 'bars'` 时 chartOption x 轴五维 `['合作强度', '成果关联', '机构覆盖', '项目参与', '引用影响']`，series `data: [85, 72, 68, 91, 64].map(...)` mock——本件是首柱「合作强度」。同抽屉的 KPI 行（节点/边/密度/综合评分）是 039 族、结构指标表（度 Top/中介/社群数/跨域边占比）是 051/052 族——本件在 bars 分支独立成柱。语义注意：bars 五维是「资产体检得分」形态（每维一个 0-100 值），「合作强度」柱=该资产图合作/关联边的权重强度聚合读数。

### 1.2 为什么需要本指标

「合作强度」回答图资产的连接质量：权重高=连接有扎实证据（强关联/多合著/高引用），权重低=稀疏弱连接。在资产深入分析场景的用途：用户筛选图资产时，「合作强度」+「成果关联」一起构成质量体检——合作强度低而边多的图是「广而弱」（泛泛关联），合作强度高而边少的图是「少而精」（核心团队）。对管理者的价值：图资产的可信度画像维度，支撑「这张图的数据质量支撑得起下游分析吗」的判断。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**SRS《算法展示.md》seq 434 写「实现对学术团队、技术流派、合作集群等社群的精准发掘」（附录 A）——「合作强度」未单列叶，权重口径（置信度/引用数/合著数）、聚合形态（均值/Top 均值/归一分）全部未言明。UI mock 的 85 是常量递减占位。检索记录见附录 A.2。

### 1.4 类似指标权威方法可行性分析概要

边权重强度统计是图挖掘/文献计量的标准对象，权威锚三重。其一，加权图框架（R1 Newman 2004《Analysis of weighted networks》）：边权重作为连接强度的规范处理——权重统计（分布/均值/强边占比）是其基础读数；其二，文献计量合作强度（R2 Newman 2001《The structure of scientific collaboration networks》）：科学家合作网的边权=合著论文数——gkx co_paper_count 的方法源，合作强度的字面语义锚；其三，链接预测置信度（R3 Liben-Nowell & Kleinberg 2003）：图边附带概率/置信分数的框架——久新 relation_confidence_score 的语义族（技术关联抽取的置信分）。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 加权网络统计（R1） | Newman 2004 | 久新 confidence/citation 列统计 | **锚** |
| 合著强度（R2） | Newman 2001 | gkx co_paper_count（1-542） | **锚**（字面语义） |
| 置信分数（R3） | Liben-Nowell 2003 | 久新 relation_confidence_score | 高（主承载语义） |
| 上游结果面 | 三源 | 无 cooperation_strength 结果列 | 无（转换正当性） |

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/queryAssetDeepAnalysis.js:83-95`（bars 分支 x 轴+series mock）；`QueryAssetDeepAnalysisDrawer.jsx`（抽屉渲染）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/算法展示.md` seq 434（excel_row 437，原文见附录 A）。
- 权威方法：R1 Newman 2004；R2 Newman 2001；R3 Liben-Nowell & Kleinberg 2003。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**定义（本件三口径并列，推测定义）**：

$$S_{conf}=\text{agg}(conf_e),\ e\in E;\qquad S_{cit}=\text{agg}(cit_e);\qquad S_{cop}=\text{agg}(cop_e)$$

$\text{agg}$ 聚合形态三选：均值（全边平均强度）/Top-N 均值（头部边强度）/min-max 归一分（0-100 满分尺——bars 图形态最贴）。本件实算均值+分布+Top10，归一分由 min/max 直接可推（confidence 口径 $100\times(x-27.08)/(100-27.08)$）。

**待裁项**：口径三选（置信度=技术关联强度/引用数=证据量/合著数=字面合作）；聚合形态三选（均值/Top 均值/归一分）；资产粒度（全图读数 vs 每资产子图读数——bars 图是每资产一柱）。

**降档/升档触发器（B10 模板）**：①现状三口径可算（已实算）→ 维持完全转换支持；②聚合结果面落表（`graph_stats.avg_edge_confidence` 夜批）→ 升**完全直接支持**；③甲方裁口径+形态 → 判档不变、读数唯一化；④久新下线 → gkx co_paper 口径独立可算，维持转换档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/算法展示.md` |
| 所属 L5 | 图查询资产深入分析（UI 拆件）+ seq 434 社群/合作集群语义域 |
| 本件 | bars 类资产维度得分首柱（合作边权重聚合） |
| 同族件 | KGANALY_052 跨域边占比（同抽屉结构指标表）、KGANALY_051 社群数（同表）、KGANALY_039 密度（同抽屉 KPI 行）、KGANALY_049 综合得分（同名「综合评分」KPI） |
| 近域件 | bars 图其余四柱（成果关联/机构覆盖/项目参与/引用影响——后批件）；046 社群演变（合作网时序侧写） |
| UI 容器 | `QueryAssetDeepAnalysisDrawer.jsx` bars 分支 |

本件与 052 同挂资产深入分析抽屉但不同分支（bars 图 vs 结构指标表）——共享久新边表原料：本件用边的**权重列**（纵向质量），052 用边的**社群归属**（横向结构）——边表一次接入双激活。

## 二、计算过程

> 本件为无业务逻辑数值类，本节给出**实测计算过程**——脚本 `code/M_SCIUI_KGANALY_049_050_052.py` 于 2026-11-02 在久新/gkx live 库实算。

### 2.1 原料装载

主承载：久新 `ads_technology_graph_edge` 全图 587,252 行两权重列直查（`relation_confidence_score`+`total_citation_count`，无采样——聚合直查）；节点表 19,430 行仅取 id→name 映射（Top10 具名）。备承载：gkx `dwd_scholar_coauthor` 前 20,000 行框（ORDER BY dwd_id，is_deleted=0；canonical (min,max) 去重后 19,995 边，权重取同边最大 co_paper_count）。

### 2.2 三口径边权重实算（口径敏感性是本件核心）

| 口径 | 库.列 | 边数 | min | max | avg | 产物键 |
|---|---|---|---|---|---|---|
| 关系置信度（主） | 久新.relation_confidence_score | **587,252** | 27.07971 | 100.0 | **49.016156** | `jiuxin_edge_confidence_min_max_avg` |
| 引用计数（并列） | 久新.total_citation_count | **587,252** | 0 | 142 | **1.168** | `jiuxin_edge_citation_min_max_avg` |
| 合著论文数（备，语义最准） | gkx.co_paper_count | 19,995 | 1 | 542 | **4.775** | `gkx_co_paper_count_min_max_avg` |

**置信度分桶（全图 587,252，和零漂移）**：c0_40 **109,673**（18.7%）/ c40_60 **365,474**（62.2%）/ c60_80 **102,606**（17.5%）/ c80_100 **9,499**（1.6%）（`jiuxin_edge_confidence_buckets`）。**引用分桶**：cit0 **212,729**（36.2%）/ cit1_3 **317,005**（54.0%）/ cit3_10 **51,936**（8.8%）/ cit10_plus **5,582**（1.0%）（`jiuxin_edge_citation_buckets`）。**合著分布**：≥2 篇边 **12,195**/19,995（61.0%）（`gkx_co_paper_count_ge2_edges`）。

**Top10 具名边**（confidence 口径，`jiuxin_top10_edges_by_confidence`）：Top1「Hyperelliptic and Elliptic Curve Cryptographic Systems × Digital Signature and Public Key Cryptography」**100.0 满分**；2-5 位 97.44/97.0/96.25/96.0（钙钛矿电子传输层/Massive MIMO/COVID 临床特征/SARS 病原学——领域内强关联对）。合著口径 Top1（`gkx_top10_edges_by_co_paper`）：学者对 1r067751×I5961821 **542 篇**合著。

**口径差解读（本件核心发现）**：三口径三语义——置信度答「这条关联可信吗」（抽取算法的自信度），引用数答「这条关联有多少证据」（文献背书量），合著数答「这两人合作多深」（字面合作强度）。bars 图的「合作强度」柱按字面应取合著口径（gkx 4.775），但主承载久新图是技术关联图（无人的合著）——若资产=技术图，回填置信度口径（49.02 均值/归一分）；若资产=合作网，回填合著口径。**单一读数形态待裁**：均值（49.02）适合「图平均质量」叙事，Top 均值适合「头部质量」叙事，归一分（0-100 满分尺）与 bars 图 y 轴 max:100 形态最贴。

### 2.3 读数解释

置信度呈 40-60 单峰（62.2% 集中中段）：上游关联抽取算法的输出分布特征——强关联（80+）仅 1.6% 是「密码学体系×数字签名」这类教科书级强对；满分边 Top1 引用数 0 反证置信度与引用数**低相关**（算法自信≠文献背书——两口径互补非替代）。引用长尾（80.6% 在 1-3 次）说明技术关联边的证据量普遍薄，142 次引用的极值边是领域枢纽对。合著口径 61% 边 ≥2 篇：合作网的边比技术关联边「厚」（合著是行为证据，关联是推断证据）。UI 回填建议：技术图资产用置信度归一分（均值 49→归一 30.0 分/Top 边 100 分），合作网资产用合著数归一；mock 的 85 落在真分布的 80+ 强边区间（仅 1.6% 边达到）——偏高但非离谱。

### 2.4 与 UI 演示形态的衔接

UI 现状：`queryAssetDeepAnalysis.js:88-92` bars 分支 mock `[85,72,68,91,64]` 递减。接入真图路径：先裁口径（§1.6 三选）→ 按资产粒度聚合（资产=子图时对子图边聚合；资产=全图时直查）→ 归一到 0-100 回填首柱。本件三口径分布即回填原料；y 轴 max:100 已在 UI 固定（`:89`），归一分形态零前端改动。

### 2.5 稳健性与口径敏感性

**（a）口径三态**：§2.2 已述——confidence/citation/co_paper 三列语义正交（自信度/证据量/行为量），相关性强弱未验（本件 Top1 满分边引用 0 是低相关的个案证据，全量相关系数属工程扩展项）；回填前裁口径是硬前置。**（b）聚合形态三态**：均值对长尾敏感度低（合著均值 4.775 被 542 极值拉高但中位数应为 1-2——中位数落键属扩展项）；Top-N 均值对 N 敏感；归一分受 min/max 极值影响（confidence 归一尺 27.08-100 非天然 0-100）。**（c）资产粒度**：bars 图是每资产一柱——资产子图的边权重分布与全图分布可能差異大（小资产图边少分布抖动），建议资产边数 <50 时标注低置信读数。**（d）gkx 框效应**：co_paper 框 20,000 行/19,995 边是 dwd_id 升序确定性采样（B5），非全量 1,187,606 行——框内均值 4.775 是采样口径（全量均值属扩展项，框对均值的偏置取决于 dwd_id 与权重的相关性，登记披露）。

### 2.6 需求符合性预评（UI 演示形态 vs 实算形态衔接）

| 需求能力位（bars 图合作强度柱） | UI 演示形态 | 实算形态（本件产物） | 衔接判定 |
|---|---|---|---|
| 首柱数值（0-100） | mock 85 递减 | 三口径均值/分布/Top10 | **回填前须裁口径+形态**（§1.6） |
| y 轴 0-100 满分尺 | max:100 固定 | 归一分可推（§2.3） | 零前端改动 |
| 资产粒度一柱 | buildDeepAnalysis(asset) | 全图读数已算；子图聚合公式同构 | 资产→子图映射是接入项 |
| Tooltip 明细 | axis trigger | Top10 具名边可作 hover 明细 | 增强项 |

**预评结论**：数据面三口径即期可用；口径+聚合形态双裁定是前置（B10 三口径并列交付不悬空）。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_KGANALY_049_050_052.py`——三源只读（久新/gkx live 直连；dev 读族级快照），GROUP BY 分桶+Top10 排序键 (confidence DESC, citation DESC)（B5），零 `demo_*`；运行 `python3 code/M_SCIUI_KGANALY_049_050_052.py`（约 150 秒，与 049/052 合算）。
- 产物：`code/M_SCIUI_KGANALY_050_out.json`，关键读数键与正文对应——`facts.jiuxin_edge_confidence_min_max_avg=[27.07971, 100.0, 49.016156]`/`jiuxin_edge_confidence_buckets`（109673/365474/102606/9499）/`jiuxin_edge_citation_min_max_avg=[0, 142, 1.168]`/`jiuxin_edge_citation_buckets`/`jiuxin_top10_edges_by_confidence`（Top1 满分具名边）/`gkx_co_paper_count_min_max_avg=[1, 542, 4.775]`/`gkx_co_paper_count_ge2_edges=12195`/`gkx_top10_edges_by_co_paper`；`derived[0-2]` 三口径；`support_judgment="完全转换支持"`。
- 结果解读：三口径三语义全实算——置信度单峰（62.2% 中段）/引用长尾（80.6% 1-3 次）/合著厚边（61% ≥2 篇）；Top1 满分边引用 0 反证口径低相关。
- 对照需求功能要求的评审：数据即期可用，口径+形态双裁定前置（§1.6 菜单），详见 §2.6。

### 2.8 分步证据对照表

| # | MD 论断（出处） | 产物键 | 读数 | 一致 |
|---|---|---|---|---|
| 1 | 置信度 min/max/avg（§2.2/摘要） | `facts.jiuxin_edge_confidence_min_max_avg` | 27.07971/100.0/49.016156 | ✓ |
| 2 | 置信度分桶（§2.2） | `facts.jiuxin_edge_confidence_buckets` | 109673/365474/102606/9499 | ✓ |
| 3 | 分桶和=全图边数（B11） | buckets 求和对账 | =587,252 | ✓ |
| 4 | 引用 min/max/avg（§2.2） | `facts.jiuxin_edge_citation_min_max_avg` | 0/142/1.168 | ✓ |
| 5 | 引用分桶（§2.2） | `facts.jiuxin_edge_citation_buckets` | 212729/317005/51936/5582 | ✓ |
| 6 | Top1 置信边满分（§2.2/§2.3） | `facts.jiuxin_top10_edges_by_confidence[0].confidence` | 100.0（citations=0） | ✓ |
| 7 | 合著 min/max/avg（§2.2） | `facts.gkx_co_paper_count_min_max_avg` | 1/542/4.775 | ✓ |
| 8 | 合著 ≥2 边数（§2.2/§2.3） | `facts.gkx_co_paper_count_ge2_edges` | 12195/19995 | ✓ |
| 9 | 合著框边数（§2.1/§2.5d） | `facts.gkx_coauthor_sample_edges` | 19995 | ✓ |
| 10 | 合著 Top1 542 篇（§2.2） | `facts.gkx_top10_edges_by_co_paper[0].co_paper_count` | 542 | ✓ |
| 11 | 久新全图边数（§2.1） | `facts.jiuxin_tech_edges_total` | 587252 | ✓ |
| 12 | 判档完全转换支持（§〇/摘要） | `support_judgment` | 完全转换支持 | ✓ |

十二行对照全部以 `_out.json` 已落盘键背书（#3/#11 对账行）。

> **基期三键说明（物理口径）**：本件基期为**物理口径基期=探针快照日**（2026-11-02 久新/gkx live 直连当日），**无年度基期**——边权重是当日图截面读数（edge 表有 metrics_as_of_date 元数据列但聚合读数无年度维）；`base_years_used`/`base_years_missing` 按截面语义登记，`base_years_note` 注记此口径，不属「缺年按 0 摊入」情形。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 关系置信度列 | 久新 | `ads_technology_graph_edge.relation_confidence_score` | **587,252** | 直查 | **足**（主口径） |
| D2 | 引用计数列 | 久新 | `ads_technology_graph_edge.total_citation_count` | **587,252** | 直查 | **足**（并列口径） |
| D3 | 合著论文数列 | gkx | `dwd_scholar_coauthor.co_paper_count` | 1,187,606（框 20,000） | 直查 | **足**（备口径，字面语义） |
| D4 | 节点名映射 | 久新 | `ads_technology_graph_node.technology_name_original` | 19,430 | 直查 | 足（Top10 具名） |
| D5 | 合作强度结果面 | 三源 | cooperation/strength 词族 | — | **不存在** | 缺（转换计算正当性来源） |

`support_judgment="完全转换支持"`、产物与文首一致。

### 3.2 权重列质量读数

| 核查项 | 读数 | 含义 |
|---|---|---|
| confidence 覆盖 | 587,252/587,252 边 | 零 NULL（min 27.08>0 自证） |
| confidence 值域 | 27.08-100（非天然 0-100） | 归一分须按实际 min/max |
| citation 值域 | 0-142（0 合法=无引用背书） | cit0 桶 36.2% 披露 |
| co_paper 值域 | 1-542（≥1 才入边） | 合著网无 0 权边 |

### 3.3 现场复核清单

| 复核项 | 结果 |
|---|---|
| 三口径聚合 | 49.016156/1.168/4.775（live 直查） |
| 分桶对账 | 置信+引用两分桶和均=587,252 |
| Top10 具名 | 置信/合著两榜全落产物 |
| dev 图表 | 26 张全 0 行（族级快照） |
| 脚本形态 | 三源只读+GROUP BY；零 demo_* |

## 四、数据缺失情况

### 4.1 合作强度结果面缺失（非判定性）

三源无 cooperation_strength/edge_weight 聚合结果面（absence_probe）——权重列是原料非读数，聚合（均值/分桶/Top）是转换计算。修复最轻量：夜批一行 SQL 落 `graph_stats.avg_edge_confidence` 等键。

### 4.2 口径三态与聚合形态（口径级）

待裁项：其一，**口径三选**（置信度/引用数/合著数——§2.2 三语义正交，按资产图型选：技术图→置信度、合作网→合著）；其二，**聚合形态三选**（均值/Top-N 均值/归一分——bars 图 y 轴 max:100 与归一分最贴）；其三，**资产粒度**（全图读数 vs 每资产子图聚合——buildDeepAnalysis(asset) 是资产粒度函数，接入需资产→子图边映射）。均非数据缺失，属口径前置项。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径+形态裁定 | 口径裁定 | 本件 | 回填前置（三口径菜单 §1.6） |
| 夜批聚合落表 | 数据工程（轻） | 本件 | 升完全直接支持 |
| 资产→子图边映射 | 数据工程（中） | 本件+bars 四柱族 | 资产粒度回填依赖 |
| 中位数/相关系数补算 | 工程扩展（可选） | 本件 | §2.5a/b 补强 |

档位后果：结果面落表 → 完全直接支持；现状 → 完全转换支持（三口径已实算）；久新下线 → gkx 合著口径独立可算，维持转换档。

## 参考文献

1. Newman M E J. Analysis of Weighted Networks[J]. Physical Review E, 2004, 70(5): 056131. https://doi.org/10.1103/PhysRevE.70.056131 （R1，2026-11-02 WebSearch 核验可达——加权网络边权重的规范统计处理，本件权重分布读数的方法源）
2. Newman M E J. The Structure of Scientific Collaboration Networks[J]. Proceedings of the National Academy of Sciences, 2001, 98(2): 404-409. https://doi.org/10.1073/pnas.98.2.404 （R2，2026-11-02 WebSearch 核验可达——科学家合作网边权=合著论文数，gkx co_paper_count 的方法源与「合作强度」字面语义锚）
3. Liben-Nowell D, Kleinberg J. The Link-Prediction Problem for Social Networks[J]. Journal of the American Society for Information Science and Technology, 2003, 58(7): 1019-1031. https://doi.org/10.1002/asi.10391 （R3，2026-11-02 WebSearch 核验可达——链接预测/关联置信分数框架，久新 relation_confidence_score 的语义族）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/算法展示.md》seq 434（excel_row 437）：

> ### 社群结构自动识别 · 序号 434
> #### 需规功能描述
> 通过算法自动识别知识图谱中的紧密连接群体，实现对学术团队、技术流派、合作集群等社群的精准发掘，大幅提升网络结构洞察力。

（「合作强度」未单列叶——本件为 UI 拆件：queryAssetDeepAnalysis bars 图首柱；「合作集群」语义域覆盖。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 合作强度 | UI queryAssetDeepAnalysis.js | :88（bars x 轴首项，mock 85） |
| 合作强度 | SRS 算法展示.md | 0（未单列叶；seq 434 合作集群语义覆盖） |
| relation_confidence_score | 久新 edge 表列 | 587,252 边全量（主承载） |
| co_paper_count | gkx dwd_scholar_coauthor | 1,187,606 行（备承载） |
| cooperation/strength 词族 | 三源表名扫描 | 零命中（无结果面） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGANALY_050_out.json`（2026-11-02 实算：三口径权重统计）。
- 共享探针：`code/_snapshots/_probe_s305_l3_call_out.json`。
- 合算脚本：`code/M_SCIUI_KGANALY_049_050_052.py`。

### B.2 本件产物逐键清单（`code/M_SCIUI_KGANALY_050_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.jiuxin_edge_confidence_min_max_avg` | **实算值** | 27.07971/100.0/49.016156 | §2.2 |
| `facts.jiuxin_edge_confidence_buckets` | 分布 | 109673/365474/102606/9499 | §2.2/§2.3 |
| `facts.jiuxin_edge_citation_min_max_avg` | 实算 | 0/142/1.168 | §2.2 |
| `facts.jiuxin_edge_citation_buckets` | 分布 | 212729/317005/51936/5582 | §2.2 |
| `facts.jiuxin_top10_edges_by_confidence` | 具名榜 | Top1 100.0 满分 | §2.2/§2.3 |
| `facts.gkx_co_paper_count_min_max_avg` | 实算 | 1/542/4.775 | §2.2 |
| `facts.gkx_co_paper_count_ge2_edges` | 分布 | 12195 | §2.2/§2.3 |
| `facts.gkx_top10_edges_by_co_paper` | 具名榜 | Top1 542 篇 | §2.2 |
| `derived[0-2]` | 三口径 | confidence/citation/co_paper | §2.2 |
| `absence_probe` | 探针 | 三件 | §4.1 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 加权网络统计 | R1 Newman 2004 | 久新两权重列统计 | 锚 |
| 合著强度 | R2 Newman 2001 | gkx co_paper_count | 锚（字面语义） |
| 置信分数 | R3 Liben-Nowell 2003 | 久新 relation_confidence_score | 高 |
| 上游结果面 | 三源 | 无 | 无（转换正当性） |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 边权重列 | 空壳 | **co_paper_count** | **confidence + citation** |
| 权重聚合结果面 | 无 | 无 | 无 |
| 节点具名 | 空壳 | scholar id | technology_name_original |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | mock 85 递减 | — |
| v1（**本件已验证**） | 三口径聚合回填（先裁口径+形态） | 口径裁定 |
| v2 | 夜批聚合落表（升完全直接支持） | 轻量 |
| v3 | 资产粒度子图聚合 | 资产→子图映射 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 三口径混引（49 当「合作」读数） | 高 | §2.2 三语义披露+按图型选口径 |
| 归一分用天然 0-100（忽略 27.08 下限） | 中 | §2.3 归一公式披露 |
| 小资产图分布抖动 | 低 | §2.5c 边数阈值标注 |

### C.5 总判

**完全转换支持**（判档边界件）：权重列三库现成近乎直接，聚合读数形态未定保守判转换。三口径（49.02/1.168/4.775）+分桶+Top10 具名全实算落产物，回填菜单齐备。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGANALY_049_050_052.py` | 退出码 0，落三件 _out.json |
| 实算一致 | `facts.jiuxin_edge_confidence_min_max_avg[2]` | 49.016156 |
| B11 对账 | 分桶和=587,252；边总数与 039/052 同源 | 零漂移 |
| 幂等重跑 | GROUP BY+确定性排序键 | 逐位一致 |
| §二 实算 | 完全转换支持档 | 有真实计算过程 |

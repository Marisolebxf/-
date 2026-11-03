# 论文热度值（M_SCIUI_TECHTRK_021）

> **类型**：HEAT（热度值，地理分布图着色轴 + KPI 复述）｜ **域**：科技发展态势·技术发展跟踪·热力图/地理分布图双视图｜ **UI 挂载**：科技信息展示系统 → 技术发展跟踪 → 地理分布图 `techDevelopmentTracking.js:339`（图例首型「论文热度」）
> **数据支持度**：**部分支持**｜ **公式定义人**：工程侧推测定义（UI 无独立公式；热度结构借 017 件语境）｜ **口径归属**：需求未明列叶（三份指定说明书 0 命中），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TECHTRK_021.py`｜ **产物**：`code/M_SCIUI_TECHTRK_021_out.json`
> **四判定摘要**：直接结构 = 部分（久新 hotspot_snapshot 有现成热度分但为技术节点粒度五分项合成，非论文粒度）；直接数据 = 部分（v2 全量 19,430 节点有分 + 论文年度序列现成）；依赖结构 = 部分（论文侧受关注度轴 cited_by_count/fwci 是原始指标非热度分）；依赖数据 = 部分（gkx download_num 全空、区域粒度着色值需聚合转换）
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

**本件判定：部分支持。** 「论文热度」在 UI 有两个呈现位：地理分布图图例首型（`technologyTrackingMapTechnologyTypes[0]`，:339，区域按论文热度着色）与话题热度 KPI（:1017-1024 `buildMetrics` 的 heat 槽）的论文侧重述。三源实测出的核心事实是**语义错位**：库侧唯一现成「热度分」是久新 `ads_technology_hotspot_snapshot.hotspot_score`——但它是**技术节点粒度**的五分项合成（0.40×growth + 0.15×author_diffusion + 0.15×institution_diffusion + 0.15×impact + 0.15×patent_signal，facts.jiuxin_hotspot_formula），论文份额与 FWCI 只是其中两轴（权重 0.55 的一部分），不是「论文」粒度的受关注度；v2 全量 19,430 节点有分（均值 42.9827，Top1 79.0908）。论文侧的受关注度承载是原始指标非热度分：`ads_paper_profile` 400 万行 cited_by_count（>0 占 66.4%，max 86,700）与 avg_fwci 3.3205；gkx `dwd_zh_paper.download_num` 实测**全空/0**（10.09 万行全表，非空 0 行——下载量热度轴无承载）。区域着色所需的「区域×论文热度」聚合面三源皆无现成，需在 geo_yearly_metrics 论文序列上转换。两个语义槽（论文粒度热度分/区域着色热度值）都无直接结果面，判部分支持。

### 批次纪律摘要（B1–B11 对照，skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | download_num 全空写实测非空 0 行，不写「未采集」 |
| B3 | 同基相除 | yoy 分子分母同源 geo_yearly_metrics 深圳行 |
| B4 | 负结论带探针 | 四路探针（gkx 下载列/heat 表、dev 论文表/heat 表）逐一留证 |
| B5 | 确定性 | Top5 按 hotspot_score DESC 固定序；年度序列升序 |
| B6 | 闸门自身被闸 | 本件不跑闸门，派单方统一跑 |
| B7 | 产物只由脚本产出 | 实跑产出，无手改 |
| B8 | 回执不复收 | hotspot 统计/Top5/论文画像/下载列四组亲自实跑 |
| B9 | 单位/日期陷阱 | 20 万采样=全表（100,900<20 万）note 写明；2026 PARTIAL_YEAR 剔比较 |
| B10 | 口径裁定保守交付 | 口径 A（节点热度 Top5）/口径 B（区域论文序列）双口径并列 |
| B11 | 多本账互推 | 深圳论文序列与 020 同值；yoy 41.5322% 两件共享；hotspot 底表与 015/022 对账 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 论文粒度热度分存在吗？ | 不存在 | hotspot_score 是节点粒度五分项；cited/fwci 是原始指标非热度分 |
| 区域着色热度值存在吗？ | 不存在（可转换） | geo_yearly_metrics 论文序列现成，聚合转换待裁定 |
| 近似热度分可用吗？ | 可用（借位） | hotspot v2 全量 19,430 有分，均值 42.9827 |

## 摘要

「论文热度」是地理分布图的图例首型——用户切到该型，地图区域按论文热度着色；它同时是「话题热度」KPI（017 件）的论文侧重述。三源探测给出一个清晰的分层结论：**「热度分」有、「论文粒度」无、「区域着色值」要转换**。久新 `ads_technology_hotspot_snapshot`（v2）为 19,430 个技术节点全量给出 hotspot_score（区间 [11.13, 79.09]、均值 42.9827），但公式明示它是五分项合成（growth 0.40 主导 + 作者扩散/机构扩散/影响/专利信号各 0.15），论文只是影响轴的一部分——Top5 节点（79.0908 量子搜索算法等，facts.jiuxin_hotspot_v2_top5）中 4 个的状态是 INSUFFICIENT_EVIDENCE（近期论文<3 篇），高分由 growth_score（88.88-98.53）驱动而非论文体量（recent_paper_count 仅 1-3 篇）——「热度≠论文多」的实证。论文侧受关注度的原始承载在 `ads_paper_profile`（400 万行，cited>0 占 66.4%，max 86,700，avg_fwci 3.3205）；gkx `dwd_zh_paper.download_num` 全空（非空 0 行）关闭了下载量轴。区域序列（口径 B）深圳论文 2015→2025 从 1,256 增至 24,904（约 19.8 倍），yoy +41.5322%（与 020 件同值）。判**部分支持**：节点热度与论文序列双承载可转换，论文粒度热度分与区域着色值两个语义槽无直接结果面。

- 需求判定：需求未明列叶（三份说明书 0 命中；srs/03 智库系统的「论文热度」属其他板块）。
- 复现状态：脚本已跑通；hotspot 统计/Top5、论文画像、下载列探针、深圳序列四组读数落产物。
- 档位结论：**部分支持**（语义槽错位：节点热度≠论文热度≠区域热度）。
- 关键事实：Top5 热点中 4 个 INSUFFICIENT_EVIDENCE、recent_paper_count≤3——高分由增长轴驱动，「论文热度」借位节点热度会被增长信号污染。
- 升档路径：论文粒度热度分建模（Altmetric 类加权）或区域聚合面固化 → 语义闭合。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/技术发展跟踪/**热力图与地理分布图双视图**（SRS 技术发展跟踪.md 页面主功能段）。本件挂载点：

```text
export const technologyTrackingMapTechnologyTypes = [   // techDevelopmentTracking.js:338-344
  { key: 'paper-heat', label: '论文热度', color: '#2563eb' },   // :339 图例首型
  { key: 'patent-active', label: '专利活跃', color: '#0f9f9a' },
  { key: 'project-application', label: '项目应用', color: '#f97316' },
  { key: 'investment-event', label: '投资事件', color: '#ef4444' },
  { key: 'research-institution', label: '研究机构', color: '#7c3aed' },
];
```

五型切换决定地图着色轴：论文热度型下，区域色深=论文热度值。第二呈现位是 KPI 区 `buildMetrics`（:1016-1026）：`{ key: 'heat', label: '话题热度', value: averageHeat, trend: '+12.4%' }`——话题热度对选中技术池取均值，其「论文侧重述」即本件语义（前端无独立「论文热度」计算函数，averageHeat 来自 topic.heat 字段的池均值）。mock 值均为演示值，不参与支持度结论。

### 1.2 为什么需要本指标

地理分布图的五型切换是「同一张地图、五种证据视角」的设计：论文热度回答「研究注意力在哪」，专利活跃回答「转化活动在哪」，投资事件回答「资本在哪」——五型叠加才能拼出技术发展的空间全貌。论文热度排首型的产品逻辑：论文是最连续、最厚重的证据流（相比投资/专利的稀疏性），作为默认着色轴最能避免「地图大片空白」。数据侧的对应难点是「热度」二字：论文的原始计量（篇数/引用/FWCI）是存量指标，「热度」要求时间衰减的受关注度（近期的、被讨论的），两者不是一回事——这正是 Altmetric 类补充计量学要解决的问题（§1.4），也是本件语义槽错位的根源。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「论文热度」在三份指定说明书 0 命中。srs 全目录检索命中 1 处：`srs/03-新型高端智库系统/战略咨询智能支持/技术体系分析.md:134`——词云+热度排行语境，属智库系统板块非本件页面。主需求文档 0 命中。「热度」在技术发展跟踪.md 出现于「话题热度」（017 件语境），未与「论文」连用。

### 1.4 类似指标权威方法可行性分析概要

论文受关注度的权威度量两族。其一，**Altmetric Attention Score**：对新闻、政策文档、博客、社交平台等多源提及加权求和（新闻 8 分/博客 5 分/推文 1 分等），输出单篇论文的受关注度分（R1）——「论文粒度热度分」的直接原型；其二，**引文侧热度**：FWCI（领域加权引用影响，R2 体系）与被引峰值滞后分析——利用引用的时序结构识别「正在升温」的论文。方法族对照：

| 方法族 | 代表 | 热度形态 | 与本库匹配 |
|---|---|---|---|
| 多源提及加权 | Altmetric（R1） | 单篇 0-N 分 | **无承载**（新闻/社交提及流库内无） |
| 领域加权引用 | FWCI 体系（R2） | 单篇比率 | **有**（ads_paper_profile.avg_fwci 3.3205） |
| 增长突发检测 | Kleinberg burst（R3） | 节点/主题级 | **有近似**（hotspot growth_score 轴） |

结论：FWCI 轴与 growth 轴库内现成，可组合出「论文侧重热度」的近似定义（口径 A 变体），但 Altmetric 式的社媒提及流无任何承载——论文粒度热度的「社会关注」维度不可建。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/techDevelopmentTracking.js:339`（图例首型 paper-heat）；`:338-344`（五型常量组）；`:1017-1024`（buildMetrics 的 heat 槽，averageHeat 池均值逻辑）。
- SRS：三份指定说明书 0 命中（附录 A 检索记录）；srs/03:134 命中属其他板块。
- 主需求文档：无「论文热度」定义段。

### 1.6 推测原意与推测定义

**推测定义（双口径并列，B10）**：

- 口径 A（**节点热度借位**，库侧现状最短路径）：取 `hotspot_snapshot`（v2）hotspot_score 直接充当「热度值」——读数：均值 42.9827、Top5 79.0908/77.2451/76.3696/76.1087/74.7756（facts.jiuxin_hotspot_v2_stats / jiuxin_hotspot_v2_top5）。语义偏差随行披露：该分 0.40 权重在增长轴（论文份额增速），非论文受关注度本体；Top5 中 4 个 INSUFFICIENT_EVIDENCE 证明高分可与小论文体量并存。
- 口径 B（**区域论文序列聚合**，着色轴语义）：对 geo_yearly_metrics 的区域×年度论文序列做时间衰减加权（如近三年窗），输出区域论文活跃度充当着色值——读数示例：深圳 2015→2025 从 1,256 增至 24,904，yoy +41.5322%（derived.jiuxin_shenzhen_paper_yoy_2025_vs_2024_pct）。

**降档/升档触发器（B10 模板）**：若甲方接受口径 A 借位（标注「技术节点热度（论文侧重）」）→ 部分支持语义闭合可上线；若接受口径 B 着色（论文活跃度而非热度）→ 地图型可上线但须改标签；若要求 Altmetric 式论文粒度热度 → 社媒提及流无承载，维持部分支持不升档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | 技术发展跟踪.md（本件叶未明列；页面功能段「热力图/地理分布图」语境） |
| 所属页面 | 技术发展跟踪（热力图+地图+气泡+雷达+弦线+工作流六视图） |
| 本件叶 | **地理分布图论文热度型——需求未明列** |
| 相邻型 | 专利活跃/项目应用/投资事件/研究机构四型（TECHTRK 族语境） |
| 姊妹件 | 017（技术热点热度值，Lane 3）——同 hotspot 底表不同粒度语义 |

批内关系：与 017 共享 hotspot_snapshot 底表（017 消费节点热度榜、本件消费论文侧重述与区域型）；与 020 共享深圳论文序列与 yoy 键（41.5322% 同值对账）；与 022 共享 hotspot_yearly 序列（本件的年度均分列在 022 件复用）。

## 二、计算过程

### 2.1 方法选择（文献依据）

论文热度的度量按 §1.4 三族评估后选双口径：口径 A 借用库侧现成 hotspot_score（其 growth 轴本质是 Kleinberg 式突发检测的工程化——近期份额 vs 基线份额的百分位，R3），口径 B 用区域年度序列的时间聚合（活跃度语义）。FWCI 轴（R2）作为论文侧质量读数登记（avg_fwci 3.3205）但不成热度——它是存量影响非受关注流量。Altmetric 式（R1）因社交流无承载直接排除，absence 留证（§3.4）。该选择把「热度」的操作定义收敛为「近期增长信号」（口径 A）或「近期产出活跃」（口径 B），两者都诚实于库内数据形态。

### 2.2 节点热度面装载与统计（口径 A 底座）

直连久新 Doris（只读）。`ads_technology_hotspot_snapshot` 按 model_version 取 v2（与 015/016/017 件共用双版本审计），19,430 节点全量有分（facts.jiuxin_hotspot_v2_stats）：n=19,430、nonnull=19,430（无缺失）、min=11.12924、max=79.090792、avg=42.9827。公式结构落产物（facts.jiuxin_hotspot_formula）：`0.40*growth + 0.15*author_diffusion + 0.15*institution_diffusion + 0.15*impact + 0.15*patent_signal`，paper_axis 注记「growth/impact 以论文份额与 FWCI 为轴（非单篇论文热度）」——本件判档的核心证据：公式里没有「论文」独立槽，论文信号被拆进 growth（份额增速）与 impact（FWCI 百分位）两轴后与其余三分项混合。

### 2.3 Top5 节点实测与「热度≠论文」实证

Top5（facts.jiuxin_hotspot_v2_top5，按 hotspot_score DESC）：① 量子搜索算法与计算复杂性 79.0908（INSUFFICIENT_EVIDENCE，growth 91.5384，recent_paper_count=1）；② JPEG 图像压缩标准 77.2451（同状态，growth 88.8775，recent 1）；③ 医学教育中的移动技术整合 76.3696（同，growth 88.8775，recent 1）；④ 蒙特卡洛树搜索算法应用 76.1087（EARLY_EMERGING，growth 98.528，recent 3）；⑤ 地震波传播计算方法 74.7756（INSUFFICIENT_EVIDENCE，growth 94.2148，recent 1）。关键实证：Top5 的 recent_paper_count 全部 ≤3、baseline_paper_count 全部 =0，但 growth_score 全部 >88——分数完全由「从 0 到 1 的份额跃迁」的百分位驱动，与「论文多/受关注多」无正相关。impact_score 五节点同值 61.6707（百分位同格），亦无区分度。若把该分直接当「论文热度」上屏，用户会把「增长型小节点」读成「论文热点」——语义污染的实证记录在案。

### 2.4 论文侧受关注度原始指标核查

`ads_paper_profile` 全表 4,000,000 行（facts.jiuxin_paper_profile_cited_stats）：cited_by_count 非空 4,000,000（全覆盖）、>0 共 2,655,946（66.4%）、max 86,700；avg_fwci 非空均值 3.3205（facts.jiuxin_paper_profile_avg_fwci_nonnull）。这两列是论文粒度受关注度的**原始材料**：可支撑「单篇高被引榜」「FWCI 分布」等统计，但都不是「热度分」——缺时间衰减、缺多源加权。由它们构建论文粒度热度分（如 cited 按 3 年窗衰减）属新建模型，本件登记为升档路径（§4.3）而非现成口径。

### 2.5 下载量轴的否定性探针（gkx）

gkx `dwd_zh_paper` 全表 100,900 行，对 download_num 列做非空与最大值探测（absence_probe[0]，采样 note：20 万采样协议下全表 100,900<20 万，等同全表）：非空 0 行、max=0——下载量轴在该库无承载（全空列）。rel_paper 列经 DESC 核查为关联论文 ID 列表非引用计数，不可充当热度轴。此路探针把「下载热度」的第三条可能路径正式关闭（B4 留证）。

### 2.6 区域序列与同比（口径 B 读数）

深圳论文年度序列（facts.jiuxin_shenzhen_paper_yearly，2015-2026）：1,256 / 1,552 / 2,069 / 2,789 / 4,022 / 5,671 / 7,395 / 10,005 / 12,243 / 17,596 / 24,904 / 2,666（2026 PARTIAL）。口径 B 的着色逻辑示例（近三年和）：2023-2025 合计 54,643 篇。yoy 派生：24,904−17,596=7,308，/17,596 = +41.5322%（derived 键，与 020 件同值——两件独立脚本各自实跑，B11 互推零漂移登记）。年度均分对照（facts.jiuxin_shenzhen_hotspot_yearly_avg）：深圳节点热度均分 2015 年 20.4871→2021 峰 57.5708→2025 回落 43.7929——论文量单调升而节点热度先升后回落，两轴背离再次印证「热度≠论文量」。

### 2.7 稳健性与口径敏感性

口径 A 的敏感性：hotspot_score 对增长轴的依赖（0.40 权重）使其在低基数节点（baseline=0）上系统性偏高——Top5 全部 baseline_paper_count=0 即此机制的产物；若上游把 growth 换成对数差或加最小基数门槛，Top5 会大换血。口径 B 的敏感性：着色聚合窗（3 年/5 年/衰减系数）直接决定区域相对位次；本件未定窗（登记示例窗），窗的裁定属甲方。两口径的读数都不得互相换算（节点粒度 vs 区域粒度），产物 notes 已写死隔离条款。

### 2.8 复现代码结果展示与分步对照

- 代码：`code/M_SCIUI_TECHTRK_021.py`（久新直连 + gkx 经 `_gkxdb.py` + dev 探针；运行 `python3 code/M_SCIUI_TECHTRK_021.py`）。
- 产物：`code/M_SCIUI_TECHTRK_021_out.json`。正文数字与产物键逐一对应：`jiuxin_hotspot_v2_stats`（§2.2）、`jiuxin_hotspot_v2_top5`（§2.3）、`jiuxin_hotspot_formula`（§2.2）、`jiuxin_paper_profile_cited_stats`/`jiuxin_paper_profile_avg_fwci_nonnull`（§2.4）、`gkx_paper_download_num_stats`（§2.5）、`jiuxin_shenzhen_paper_yearly`/`jiuxin_shenzhen_hotspot_yearly_avg`（§2.6）、derived yoy 41.5322%（§2.6）。
- 结果解读：节点热度面全量可查但语义借位有实证风险；论文原始指标厚实可建热度分；区域序列可撑地图型。
- 对照需求功能要求的评审：地图着色——口径 B 可满足（标签须改「论文活跃度」）；论文热度分——口径 A 借位可满足（披露增长轴污染）。

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 统计 | v2 热度分布 | `jiuxin_hotspot_v2_stats` | n=19,430，avg 42.9827 |
| 榜单 | Top5 节点 | `jiuxin_hotspot_v2_top5` | 79.0908→74.7756 |
| 公式 | 五分项结构 | `jiuxin_hotspot_formula` | growth 0.40 主导 |
| 论文 | 被引画像 | `jiuxin_paper_profile_cited_stats` | 400 万行，66.4%>0 |
| 论文 | FWCI 均值 | `jiuxin_paper_profile_avg_fwci_nonnull` | 3.3205 |
| 否定 | 下载量轴 | `gkx_paper_download_num_stats` | 非空 0 行 |
| 区域 | 深圳论文序列 | `jiuxin_shenzhen_paper_yearly` | 1,256→24,904 |
| 派生 | yoy 同比 | `derived.…yoy_pct` | +41.5322%（7,308/17,596） |
| absence | gkx heat 表 | `absence_probe[1]` | 0 命中 |
| absence | dev 论文/heat 表 | `absence_probe[2]/[3]` | 0 命中 / 2 表（产业链侧） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 节点热度分 | jiuxin | `hotspot_snapshot.hotspot_score`（v2） | 19,430 全量 | 直查 | **有**（借位口径 A） |
| D2 | 论文被引/FWCI | jiuxin | `ads_paper_profile.cited_by_count/avg_fwci` | 4,000,000 全覆盖 | 直查 | 有（原始指标） |
| D3 | 区域论文序列 | jiuxin | `ads_geo_yearly_metrics.paper_count` | 深圳 2015-2026 | 直查 | **有**（口径 B） |
| D4 | 论文下载量 | gkx | `dwd_zh_paper.download_num` | 非空 **0** 行 | **不存在** | **缺（轴关闭）** |
| D5 | 社媒/新闻提及流 | 三库 | —（Altmetric 式多源） | — | **不存在** | **缺（论文粒度热度不可建全）** |
| D6 | 区域×论文热度聚合面 | 三库 | — | — | 不存在（可转换） | 缺（待窗裁定） |

`support_judgment="部分支持"` 与文首一致（闸 6 对齐）。

### 3.2 D1 节点热度面

§2.2/§2.3 已列全。使用要点：借位上屏必须改标签（「技术节点热度」）并披露五分项结构；INSUFFICIENT_EVIDENCE 的高分节点（Top5 中 4 个）须带状态徽标，防止「热度榜=论文榜」的误读。

### 3.3 D2 论文原始指标

400 万行全覆盖的被引与 FWCI 是本件最厚的资产：任何论文粒度热度模型（衰减被引、被引加速度、FWCI×时效）都能在此上建。当前无现成模型层——`ads_paper_profile` 是画像表非热度表，构建属升档路径（§4.3）。

### 3.4 D4/D5/D6 absence_probe 全记录

否定性证据四件套：**查了什么**——① gkx `dwd_zh_paper.download_num` 非空/max（全表等同采样，note 写明）；② gkx 280 表扫 `%heat%` OR `%hot%`；③ dev `SHOW TABLES LIKE '%paper%'`；④ dev 两库扫 heat/hot。**条件**——论文粒度热度承载（下载列/热度表/论文表）。**命中**——① 非空 0 行；② 0 表；③ 0 表（`gkxlumenx_dwd` 无论文表，与共享快照一致）；④ 2 表（chain_hotspot / industry_chain_graph_snapshot，产业链侧语义错位）。社交流（D5）三库均无此表族，属数据源级缺失。归属：**轴/结果面不存在**。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| v2 去重 | 19,430 节点单版本口径 |
| Top5 确定性 | hotspot_score DESC 固定序 |
| 实证组 | Top5 recent≤3 / baseline=0 / growth>88 |
| 论文画像 | 400 万行全覆盖，66.4% cited>0 |
| 下载列 | 非空 0 行（全表，非采样截断） |
| 序列对账 | 深圳论文/yoy 与 020 件同值 |
| absence 留证 | 四路探针产物在案 |
| mock 登记 | 图例色值/KPI +12.4% 标演示值 |
| 脚本形态 | 只读、零 demo_*、gkx 经 _gkxdb.py |

### 3.6 与同批件的底表共享

hotspot_snapshot 与 015（stage 同管线）、017（热度榜主件）、022（yearly 序列）、023（状态机）五件共享——本件的公式结构与 Top5 实证是批内「热度语义」的公共证据，017/023 引用时应与本件 §2.2/§2.3 同值（B11）。

## 四、数据缺失情况

### 4.1 论文粒度热度分缺失（主因）

「热度分」的库侧唯一现成面在技术节点粒度（D1），论文粒度（单篇或论文主题粒度）无任何热度模型层。构建路径有二：衰减被引模型（D2 上建，工程量中）或增长突发检测（D2 年度字段上建）。社交流缺失（D5）使 Altmetric 式全维度热度不可建——这是数据源级天花板，非工程可解。

### 4.2 区域着色聚合面缺失（次因）

区域×论文热度的现成聚合面不存在，geo_yearly_metrics 论文序列可转换但聚合窗未裁定（§2.7）。且序列语义是「产出活跃度」，着色标签若保留「热度」二字须接受语义放宽（§1.6 触发器 B）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 借位上屏（改标签+状态徽标） | 产品决策 | 本件+017 | 即期可交付 |
| 口径 B 着色（近三年窗示例） | 产品决策 | 本件 | 标签改「论文活跃度」 |
| 衰减被引热度模型 | 转换工程 | 本件 | ads_paper_profile 上建 |
| 社交流接入 | 数据源立项 | 本件+017 | Altmetric 维度补全（长期） |

档位后果：口径 A/B 裁定 → 部分支持语义闭合；衰减模型落地 → 论文粒度热度可建（升完全转换支持的候选）；社交流接入 → 全维度热度。推荐：即期双口径裁定，中期衰减模型立项。

## 参考文献

1. How is the Altmetric Attention Score calculated?[EB/OL]. Altmetric. https://help.altmetric.com/support/solutions/articles/6000233311-how-is-the-altmetric-attention-score-calculated （R1，2026-11-01 WebSearch 核验可达）
2. Snowball metrics recipe book[EB/OL]. Elsevier / Snowball Metrics. https://elsevier.com/products/snowball-metrics （R2，FWCI 体系语境，2026-11-01 WebSearch 核验可达）
3. Kleinberg J. Bursty and Hierarchical Structure in Streams[EB/OL]. Cornell University. https://www.cs.cornell.edu/home/kleinber/bh.pdf （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

「论文热度」在三份指定说明书与主需求文档均未出现。检索记录：

| 检索词 | 文档 | 命中 |
|---|---|---|
| 论文热度 | 三份指定 SRS + 主文档 | 0 |
| 论文热度 | srs 全目录 | 1（03-智库系统:134，词云+热度排行语境，非本件页面） |
| 论文 + 热度（同段） | 技术发展跟踪.md | 0 |
| paper-heat | techDevelopmentTracking.js:339 | 1（UI 图例键） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_021_out.json`（2026-11-01 实跑：hotspot 统计/Top5/公式、论文画像、下载列探针、深圳序列）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（dwd_zh_paper=100,900 行、ads_paper_profile=4,000,000 行——本件实跑值与快照零漂移）。
- absence 记录：四路探针（gkx 下载列/heat 扫描、dev 论文/heat 扫描）产物在案。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.jiuxin_hotspot_v2_stats` | 统计 | n=19,430 / avg 42.9827 | §2.2 |
| `facts.jiuxin_hotspot_v2_top5` | 榜单 | 5 节点含状态/分项 | §2.3 |
| `facts.jiuxin_hotspot_formula` | 公式 | 五分项权重结构 | §2.2 |
| `facts.jiuxin_paper_profile_cited_stats` | 画像 | 400 万行 / 66.4%>0 | §2.4 |
| `facts.jiuxin_paper_profile_avg_fwci_nonnull` | 均值 | 3.3205 | §2.4 |
| `facts.gkx_paper_download_num_stats` | 否定 | 非空 0 行 | §2.5 |
| `facts.jiuxin_shenzhen_paper_yearly` | 序列 | 12 年 | §2.6 |
| `facts.jiuxin_shenzhen_hotspot_yearly_avg` | 序列 | 12 年均分 | §2.6 |
| `facts.ui_mock_map_type` | mock | 论文热度/#2563eb | §1.1 |
| `derived.jiuxin_shenzhen_paper_yoy_2025_vs_2024_pct` | 派生比 | 41.5322 | §2.6 |
| `absence_probe` | 负证据 | 4 条 | §3.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

### B.3 共享快照消费

本件消费 `_shared_probe_s3_01_out.json` 的 dwd_zh_paper=100,900 / ads_paper_profile=4,000,000 两键（底表规模与共享探针零漂移）；「gkxlumenx_dwd 无论文表」结论与快照一致（W2-1 资产复用，本件仅补 LIKE 探针留证）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 热度形态 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 多源提及加权 | Altmetric（R1） | 单篇分 | **无**（社交流缺） | 不可行 |
| 领域加权引用 | FWCI（R2） | 单篇比率 | **有**（3.3205 均值） | 中（存量非热度） |
| 突发检测 | Kleinberg（R3） | 节点级 | **有近似**（growth 轴） | 高（借位） |
| 区域活跃聚合 | 本口径 B | 区域级 | 序列现成 | 高（标签须改） |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| hotspot_snapshot | 19,430 | 全量+分项 | 节点粒度非论文 |
| paper_profile | 4,000,000 | 被引/FWCI 全覆盖 | 无热度模型层 |
| download_num | 0 非空 | — | 轴关闭 |
| 社交流 | 无表 | — | 数据源级缺失 |
| 区域聚合面 | 可转换 | 序列现成 | 窗未裁定 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1 | 口径 A 借位榜 + 口径 B 着色 | 双口径裁定 |
| v2 | 衰减被引论文热度模型 | 转换工程 |
| v3 | 社交流接入（Altmetric 维度） | 数据源立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 节点热度被误读为论文热度 | **高** | 改标签+五分项披露+状态徽标 |
| Top5 低基数高分污染 | 高 | baseline=0 徽标+门槛建议 |
| 口径 B 标签保留「热度」 | 中 | 改「论文活跃度」或窗裁定书 |

### C.5 总判

**部分支持**：节点热度面与论文原始指标双厚实，但「论文粒度热度分」「区域着色热度值」两个语义槽均无直接结果面；口径 A 借位有实证污染风险须标签隔离，社交流缺失是长期天花板。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_021.py` | 退出码 0，落 `_out.json` |
| 热度统计 | `facts.jiuxin_hotspot_v2_stats` | avg=42.9827 |
| Top5 | `facts.jiuxin_hotspot_v2_top5` | 79.0908 居首，4 个 INSUFFICIENT |
| 下载列探针 | `facts.gkx_paper_download_num_stats` | 非空 0 |
| yoy 对账 | derived 41.5322 | 与 020 件同值 |
| 共享快照对账 | 100,900 / 4,000,000 | 零漂移 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 均为部分支持 |
| demo 禁引 | 脚本 grep demo_ | 0 命中 |

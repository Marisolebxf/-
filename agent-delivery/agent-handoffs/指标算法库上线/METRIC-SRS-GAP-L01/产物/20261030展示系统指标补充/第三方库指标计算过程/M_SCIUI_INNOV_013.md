# 区域能力结构分析（M_SCIUI_INNOV_013）

> **类型**：COMPOSITE（五维构成雷达，双口径 A mock 十城 / 口径 B 全球城市 Top10）｜ **域**：科技发展态势·全球创新监测·载体对比视图第 2 项（雷达）｜ **UI 挂载**：全球创新监测页（`carrierRankingCompareModel.js:32` 对比视图『能力结构』+ `:604` 导出报告章节 + `:514` 雷达归一实现）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 推导叶（`cfg_metric` 无条目；指标名三份说明书 0 命中）
> **复现脚本**：`code/M_SCIUI_INNOV_013.py`｜ **产物**：`code/M_SCIUI_INNOV_013_out.json`
> **四判定摘要**：直接结构 = 否（三源无「能力结构」结果面）；直接数据 = 否；依赖结构 = 是（久新 ads_geo_yearly_metrics 171,736 行 CITY 级 2025 年 9,121 行五列全在：论文/项目/人才/机构/流入人才）；依赖数据 = 是（五维全量非空，min-max 归一即得雷达）
> **数据源口径**：本件支持度按「开发库 gkxlumenx_*（禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin（47.93.119.170:29030 只读）」三源评估（20261101 三源铁律）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** 三源无现成「能力结构」结果面（gkx capability/power/score/assessment/benchmark 五关键字 0 表；dev score/ability/capability/index 四关键字 0 表；久新 `ads_geo_yearly_index` schema 在但 0 行——预留件另立 014 件判读），但转换路径**结构+数据双达标**：久新 `ads_geo_yearly_metrics`（171,736 行）CITY 级 2025 年 9,121 行，**五维列一次取齐**——论文（paper_count）/项目（project_count）/人才（talent_count）/机构（institution_count）/流入人才（inbound_talent_count）——min-max 归一（×100 制）即得五维雷达。实测口径 A（mock 十城同构）：北京全维领跑（papers 100.0/projects 100.0/talents 100.0/institutions 96.05/inbound 100.0），上海次席（37.5/37.01/50.43/26.27/82.61），杭州第三（20.13/18.06/30.62/3.25/34.78）；伦敦机构维 100.0 反超其论文维 11.19（结构分化样本）。口径 B（全球城市 Top10）：北京外全部中国城市（上海/南京/广州/杭州/武汉/西安/成都/深圳/天津）——**全球城市论文 Top10 全由中国包揽**。语义降级披露：UI mock 五维是「创新投入/产出/环境/人才储备/政策支持」（投入/环境/政策三维 geo 池无对应列），本件改用数据可得的五计维是最近似结构。判**完全转换支持**。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 归一基准同组同维（A=mock 十城组内，B=Top10 组内） |
| B4 | 负结论带探针 | gkx 五关键字 0 表 + dev 四关键字 0 表 + 趋势类 2 表 0 行 |
| B5 | 确定性 | 榜单按 papers 降序；归一取组内极值（幂等重跑同值） |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑 |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | 2025 截面（2026 残年不用）；归一 0-100 制标注 |
| B10 | 口径裁定保守交付 | 双口径 + 语义降级披露 + mock 维 vs 数据维对照表 |
| B11 | 多本账互推 | geo 池 171,736 与 002/004/011 件同表同值；CITY 级 9,121 本件补测 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 五维原料齐吗？ | 齐（五列全在且非空） | `jiuxin_city_2025_rows=9121` + 五列 DESC |
| 现在能转换出雷达吗？ | 能（min-max 归一已实跑） | `jiuxin_mock_city_radar` / `jiuxin_global_city_top10_radar` |
| UI 五维语义有损吗？ | 有（投入/环境/政策三维降级为近似维） | §1.6 降级披露表——语义问题不阻断「结构+数据达标」判档 |

## 摘要

「区域能力结构分析」是全球创新监测页载体对比视图的**雷达图项**（`carrierRankingCompareModel.js:32`，成长态势/能力结构/关联协同/关键指标四视图第 2 项），导出报告自带同名章节（:604）。三源无现成结果面，但久新 `ads_geo_yearly_metrics` CITY 级 2025 年 9,121 行**五维计数列一次取齐**——这是全批唯一「结构+数据双达标」的五维城市面板。实测口径 A（mock 十城同构）：北京全维领跑 100/100/100/96.05/100，上海 37.5/37.01/50.43/26.27/82.61，杭州 20.13/18.06/30.62/3.25/34.78；结构分化样本——伦敦机构维 100.0（821 家）碾压其论文维 11.19（22,378 篇），纽约机构维 50.56、东京 61.3 同型——海外城市「多机构少产出」与中国城市「高产出于少数机构」形成镜像。口径 B（全球论文 Top10 城市）：**十城全为中国城市**（北京 160,529 / 上海 63,300 / 南京 46,790 / 广州 44,556 / 杭州 36,293 / 武汉 35,942 / 西安 32,525 / 成都 30,537 / 深圳 24,904 / 天津 23,352）。语义降级披露：UI mock 五维（投入/产出/环境/人才/政策）中投入/环境/政策三维在 geo 池无对应列（政策支持三源无城市级政策量化面），本件改用论文/项目/人才/机构/流入人才五计维——**结构骨架在、语义贴签需甲方裁定**。判**完全转换支持**：现在就能出图，维名贴签是配置问题非数据问题。

- 需求判定：**UI 推导叶**（指标名三份说明书 0 命中；最近锚为全球创新监测.md seq 85 城市对标分析『展示各城市在创新投入、创新产出、创新环境等方面的差异』——维度枚举级非公式定义）。
- 复现状态：脚本已跑通；双口径雷达 + 原始五维 + 三源负结论探针全部落产物。
- 档位结论：**完全转换支持**（五维结构+数据双达标，min-max 归一即得）。
- 关键事实：全球城市论文 Top10 全由中国包揽 + 中外城市「产出-机构」结构镜像，是本件两个可直接上屏的数据发现。
- 升档路径：上游填充 `ads_geo_yearly_index`（0 行预留表）→ 若出官方五维指数 → 升完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**全球创新监测**/载体排行对比视图（雷达）。挂载点实查：

- `src/pages/global-innovation/tabs/carrierRankingCompareModel.js:32`：`compareViewOptions { key: 'radar', label: '能力结构', title: '能力结构分析' }`——对比视图第 2 项。
- `carrierRankingCompareModel.js:604`：`buildCarrierCompareExportConfig contentItems { key: 'radar', label: '能力结构分析' }`——导出报告章节。
- `carrierRankingCompareModel.js:514`（雷达归一实现）：indicator = 用户勾选的 metrics（score/patents/papers/projects/rank 五选 N），每维按「值/组内最大值×100」相对归一（rank 反向 min/value×100）——**组内相对制**，非全局基准制。
- `src/pages/global-innovation/mockData.js:129`：城市雷达 mock 五维（创新投入/创新产出/创新环境/人才储备/政策支持，baseIndex 派生随机抖动——演示值，不参与支持度结论）。

UI 自身即归一雷达（值/组内最大×100），本件实测改全样本 min-max 归一并披露（与 004 件一致的保守透明中间态）。

### 1.2 为什么需要本指标

单维计数（论文数/专利数）回答「谁多」，能力结构雷达回答「强在哪」——把多源证据压成一城一形的五边形，是对比视图的**结构诊断器**：形状（哪维凸哪维凹）比面积（总量）更有信息量。本指标承担三职：①**结构对比**（对比视图选中 2-4 城的雷达叠加）；②**短板诊断**（弱维即政策建议的靶点——`weakDimension` 已在 UI 的 `buildCarrierIndexBreakdown` 实现）；③**要素分析入口**（城市创新能力分析页的『创新能力要素分析』视图（seq 86）与本件同族）。数据侧本件是「五维面板件」的代表：三源无结果面但久新一表五列齐——这类件的判档关键是「维数是否够 + 数据是否全量」，两者本件均达标。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「区域能力结构分析/能力结构」作为指标名三份说明书 0 命中。全球创新监测.md seq 85 最近锚：『系统提供对比视图，展示各城市在创新投入、创新产出、创新环境等方面的差异』——给了**维度枚举方向**（投入/产出/环境）但无维数、无归一式、无聚合式；seq 86『分析影响城市创新能力的关键要素，如人才、资金、政策』次之（要素枚举含人才/政策——与 mock 五维同名）。两处合起来能反推：需求方预期「城市×多维」的对比结构，但维度构成与归一制式完全留白。本件的五计维构造即填补该留白的保守方案。

### 1.4 类似指标权威方法可行性分析概要

区域能力结构的权威范式有三支。**欧盟 RIS 2025**（R1）：区域创新记分板——241 地区 23 指标 12 维度，**分位对齐归一**（Chauvenet 准则去极值 + 偏态变换 + 重缩放）后等权平均成 Regional Innovation Index——多维雷达的「维度→归一→聚合」完整管线标杆；**WIPO GII 2025**（R2）：78 指标 21 子支柱 7 支柱双分指数，指标 0-100 归一后加权平均，投入/产出双翼等权——「维度树+权重树」范式；**UI 自身范式**（R3，本件挂载实现）：值/组内最大×100 的组内相对归一——最简但受组内极值钳制。方法族对照：

| 方法族 | 归一 | 维度结构 | 三源承载 | 匹配度 |
|---|---|---|---|---|
| RIS 分位对齐（R1） | 全样本分位+去极值 | 12 维等权 | 五维计数列可承载 | **高（正式版范式）** |
| GII 加权维度树（R2） | 0-100 极值归一+权重 | 7 支柱加权 | 五维+权重可配 | 中高 |
| UI 组内相对制（R3） | 值/组内最大×100 | 用户勾选 N 维 | 即挂载实现 | 中高（即期可用） |
| min-max 全样本（本件实测） | 极值归一 | 五维等权 | 同上 | 中（钳制警示在案） |

结论：RIS 式分位归一是正式版推荐；本件实测用 min-max 是保守透明的中间态。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:32/:514/:604`（视图项+归一实现+导出章节）；`…/mockData.js:129`（mock 五维）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` seq 85（维度枚举锚）、seq 86（要素枚举锚）。
- 数据：`code/_snapshots/_probe_lane5_s3_01_out.json`（geo_yearly_metrics DESC+COUNT #5/#6/#44）；本件补测 CITY 级 2025 行数落 `code/_snapshots/_probe_lane7_innov013_out.json`。

### 1.6 推测原意与推测定义

**推测定义（双口径，均须披露口径假设）**：

- **口径 A（mock 十城五维·UI 同构）**：`radar(city, dim) = (v - min_g) / (max_g - min_g) × 100`，dim ∈ {papers, projects, talents, institutions, inbound_talents}，g = mock 十城组（深圳/北京/上海/杭州 + 纽约/伦敦/东京/新加坡/柏林 + 旧金山代硅谷）。实测北京全维领跑（100/100/100/96.05/100）、上海次席（37.5/37.01/50.43/26.27/82.61）。
- **口径 B（全球城市 Top10 五维）**：同式换组——全库 CITY 级按论文 Top10（全为中国城市）。实测北京 100/100/100/100/100 顶格，上海 29.12/30.82/39.54/29.53/81.82。
- **维名贴签（语义降级披露）**：UI mock 五维 vs 数据五维对照——

| UI mock 维 | geo 池对应列 | 状态 |
|---|---|---|
| 创新投入 | （无直接列；机构/流入人才可近似） | 降级 |
| 创新产出 | paper_count/project_count | **直接对应** |
| 创新环境 | （无对应列） | 降级 |
| 人才储备 | talent_count | **直接对应** |
| 政策支持 | （三源无城市级政策量化面） | 不可承载 |

**降档/升档触发器（B10 模板）**：本件已判完全转换支持（结构+数据达标），维名贴签是配置项；若甲方要求 mock 原五维语义（投入/环境/政策）→ 需扩政策/环境类原料（三源无）→ 降部分支持另立工程；若上游填充 `ads_geo_yearly_index` 官方五维 → 升完全直接支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` |
| 所属四级功能 | 全球创新监测（33 叶） |
| 本件挂载视图 | 载体对比视图雷达项（主）+ 导出报告章节 |
| 需求叶对应 | 无同名叶；最近 seq 85/seq 86 枚举级 |
| 批内相邻件 | M_SCIUI_INNOV_014（区域能力评分——同五维原料的加权聚合件，本件是结构件、014 是标量件）；M_SCIUI_INNOV_011（区域论文数——本件五维之第一维）；M_SCIUI_INNOV_004（活跃度——国家级同族复合件） |
| 跨模块参照 | 城市创新能力分析（seq 85/86 语境） |

本件与 014 是「结构/标量」姊妹：同一五维面板，本件消费形状（雷达五轴）、014 消费面积（加权标量）——两件合起来即「能力结构分析 + 能力评分」的完整对。与 004（国家级复合）构成「国家/城市」两级的方法论复用。

## 二、计算过程

### 2.1 装载与规模校验

久新 `ads_geo_yearly_metrics` 171,736 行（`facts.jiuxin_geo_yearly_metrics_rows`，共享探针快照原值断言通过）；CITY 级 2025 年 9,121 行（`jiuxin_city_2025_rows`，本件补测落 `code/_snapshots/_probe_lane7_innov013_out.json`——CONTINENT 6 / PROVINCE 1,807 / COUNTRY 222 / CITY 9,121 四级分布（CITY 全年总行 132,975 见 lane5 快照 #44，11,284 城见同 #44 locs 列））。五消费列全在（官方快照 #6 DESC）：paper_count / project_count / talent_count / institution_count / inbound_talent_count——五维面板一次取齐，无需跨表 JOIN。

### 2.2 gkx/dev 侧负结论（absence_probe）

gkx 280 表五关键字扫描（capability/power/score/assessment/benchmark）：**0 表**（`gkx_capability_like_tables=[]`）；gkx 指数类 4 表（dwd_dim_index_attribute 等）经甄别为宏观经济指标字典（规上工业 R&D 人员等），非区域能力结构承载，已排除。dev `gkxlumenx_dwd` score/ability/capability/index 四关键字 0 表；趋势对标类 2 表（enterprise_growth_trend / sz_city_benchmark）0 行（`dev_trend_benchmark_rows=[0,0]`）。

### 2.3 城市名匹配规约（ads_location 实测）

`ads_location` 命名规约实测：中国城市 name_zh 带「市」后缀（北京市/杭州市/上海市，深圳除外无后缀）、海外城市 name_zh 为 NULL 须按 name_en 精确匹配——本件 `fetch_city_rows` 用 `(zh_like, en_eq)` 二元组查询对（如 `("%北京%","Beijing")` / `("","New York")`），多命中取论文最大者。mock 十城全命中（硅谷无同名城，以 San Francisco 替代并披露）。

### 2.4 口径 A：mock 十城五维雷达（2025 截面）

原始五维（`jiuxin_mock_city_raw`）：北京 160,529/46,743/33,800/793/23、上海 63,300/18,807/17,272/299/19、伦敦 22,378/7,740/2,462/821/2、纽约 16,420/5,796/1,687/471/3……min-max 归一（`jiuxin_mock_city_radar`）：北京 100.0/100.0/100.0/96.05/100.0、上海 37.5/37.01/50.43/26.27/82.61、伦敦 11.19/12.05/6.02/**100.0**/8.7（机构维反超）——中外城市「产出-机构」结构镜像实证。

### 2.5 口径 B：全球城市 Top10 五维

全库 CITY 级 2025 按论文 Top10（`jiuxin_global_city_top10_raw`）：北京/上海/南京/广州/杭州/武汉/西安/成都/深圳/天津——**十城全为中国城市**。归一面板（`jiuxin_global_city_top10_radar`）：北京顶格 100×5，上海 29.12/30.82/39.54/29.53/81.82。

### 2.6 归一方法警示（min-max 钳制）

口径 A 伦敦机构维 100.0（821 家压顶）与口径 B 北京全维 100.0（五维全组内最大）——min-max 受极值钳制的实证；正式版建议 RIS 式分位归一（R1 范式：Chauvenet 准则去极值 + 分位对齐）。

### 2.7 复现代码结果展示

| 产物键 | 值（节选） |
|---|---|
| `jiuxin_city_2025_rows` | 9,121 |
| `jiuxin_mock_city_raw[0]` | Shenzhen 24904/9143/6462/113/10 |
| `jiuxin_mock_city_radar[0]` | Beijing 100.0/100.0/100.0/96.05/100.0 |
| `jiuxin_global_city_top10_raw[0..1]` | Beijing 160529/…；Shanghai 63300/… |
| `jiuxin_global_city_top10_radar[0]` | Beijing 100.0×5 |
| `derived.jiuxin_mock_city_radar_dimcount` | 5.0 |

### 2.8 分步证据对照表

| 步骤 | SQL/操作 | 产物键 | 结果 |
|---|---|---|---|
| S1 规模断言 | COUNT 全表 | `jiuxin_geo_yearly_metrics_rows` | 171,736 零漂移 |
| S2 CITY 行数 | COUNT CITY+2025 | `jiuxin_city_2025_rows` | 9,121 |
| S3 十城取数 | 二元组 LIKE/EQ 查询 | `jiuxin_mock_city_raw` | 11 城全命中 |
| S4 口径 A 归一 | min-max ×100 | `jiuxin_mock_city_radar` | 北京领跑 |
| S5 口径 B 取数 | Top10 by papers | `jiuxin_global_city_top10_raw` | 全中国十城 |
| S6 口径 B 归一 | 同式换组 | `jiuxin_global_city_top10_radar` | 北京顶格 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 源表 | 行数 | 库别 | 状态 |
|---|---|---|---|---|
| D1 城市五维面板 | ads_geo_yearly_metrics CITY 2025 | 9,121 | jiuxin | **全量（主承载）** |
| D2 地理维表 | ads_location | 224 国+11,284 城 | jiuxin | 全量（双名规约见 §2.3） |
| D3 gkx 能力类表 | — | 0 表 | gkx | 五关键字 0 命中 |
| D4 gkx 宏观指标字典 | dwd_dim_index_attribute 等 4 表 | 867/20,000 等 | gkx | 甄别排除（非能力结构语义） |
| D5 dev 评分类 | — | 0 表 | dev | 四关键字 0 命中 |

### 3.2 D1 主承载明细

五列全量非空（NULL 行在 PROVINCE 级早年存在，CITY 2025 行五列完整）；mock 十城与全球 Top10 双查询路径幂等（同 SQL 同值）。inbound_talent_count 是五维中量级最小的（0-23 区间）——归一后区分度反而最高（北京 100 vs 柏林 0）。

### 3.3 D3/D5 负结论面

gkx 五关键字（capability/power/score/assessment/benchmark）与 dev 四关键字（score/ability/capability/index）全 0——两库均无「能力结构」承载，判档依据落在久新转换路径。

### 3.4 D4 相邻承载甄别

gkx `dwd_dim_index_attribute`（867 行）/`dwd_macro_index_data`（20,000 行）是宏观经济指标字典与月度数据——语义为「规上工业 R&D 人员」等宏观面，非城市能力结构，登记排除理由防后批误用。

### 3.5 现场复核清单

- `SELECT COUNT(*) FROM ads_geo_yearly_metrics WHERE location_level='CITY' AND statistics_year=2025` → 9,121
- `SELECT paper_count FROM ads_geo_yearly_metrics m JOIN ads_location l ON … WHERE l.name_en='London' AND … AND statistics_year=2025` → 22,378
- 口径 A 北京行：`ORDER BY paper_count DESC LIMIT 1` → 160,529

## 四、数据缺失情况

### 4.1 UI mock 三维语义缺口（投入/环境/政策）

UI mock 五维中创新投入/创新环境/政策支持三维在 geo 池无对应列（政策支持三源无城市级政策量化面——gkx 政策表为国家级文本，非城市级量化）。**修复建议**：①维名贴签改「论文/项目/人才/机构/流入人才」（数据可得，即期）；②或扩政策/环境原料（上游工程，三源现无）。**影响面**：维名贴签不改则雷达语义与 mock 原意有损，须甲方裁定。

### 4.2 硅谷无同名城（地名映射缺口）

mock 十城的「硅谷」在 ads_location 无同名城（探针 0 命中）——本件以 San Francisco 替代。**修复建议**：建「硅谷→湾区城市群（San Francisco+San Jose+Oakland）」映射或改用湾区聚合。**影响面**：单城替代低估硅谷体量（San Francisco 论文 4,972 vs 北京 160,529）。

### 4.3 极值钳制（归一方法缺口）

min-max 归一受组内极值钳制（§2.6）。**修复建议**：正式版改 RIS 式分位归一。**影响面**：钳制不修则弱维区分度被压扁（口径 A 中国四城论文维被北京 100 压至 0-37.5 区间）。

## 参考文献

1. Regional Innovation Scoreboard 2025[EB/OL]. European Commission. https://research-and-innovation.ec.europa.eu/document/download/f6019e31-2927-4802-ae56-5f2fd92cb6c3_en （R1，区域多维创新记分板 241 地区 23 指标分位归一管线，2026-11-01 WebSearch 核验可达）
2. Global Innovation Index 2025 – Appendix I[EB/OL]. WIPO. https://www.wipo.int/web-publications/global-innovation-index-2025/en/appendix-i-conceptual-and-measurement-framework-of-the-global-innovation-index.html （R2，多维指标 0-100 归一+加权聚合范式，2026-11-01 WebSearch 核验可达）
3. SCImago Journal & Country Rank Help[EB/OL]. SCImago. https://www.scimagojr.com/help.php （R4，国别科学产出多维指标参照系，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

**「区域能力结构分析/能力结构」未作为指标名出现在三份说明书。** 检索记录（2026-11-01）：

| 检索词 | 范围 | 命中 |
|---|---|---|
| 能力结构 | 全球创新监测.md | 0 |
| 能力 | 全球创新监测.md | seq 73/84（评分/排名语境） |
| radar/能力结构 | UI 源码 | carrierRankingCompareModel.js:32/514/604（本件挂载） |

最近语义原文：
- seq 85：『用户可选择多个城市进行创新对标分析，系统提供对比视图，展示各城市在创新投入、创新产出、创新环境等方面的差异。』
- seq 86：『分析影响城市创新能力的关键要素，如人才、资金、政策，用户可查看各城市在不同要素上的表现。』

### A.2 检索记录逐行

（检索工具：ripgrep 于 SRS 目录与 repos/demo-ui-science/src；时间 2026-11-01；命中行号已实查 ±10 行上下文。）

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_013_out.json`（20261101 实跑：双口径雷达 + 原始五维 + 三源负结论在案）。
- 本 lane 共享探针：`code/_snapshots/_probe_lane5_s3_01_out.json`（geo DESC/COUNT #5/#6、location_level 分布 #44）。
- 本件补测：`code/_snapshots/_probe_lane7_innov013_out.json`（CITY 级 2025 四级分布）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INNOV_013_out.json`，20261101 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `jiuxin_geo_yearly_metrics_rows` | 计数 | 171,736 | §2.1 |
| `jiuxin_city_2025_rows` | 计数 | 9,121 | §2.1/§〇 |
| `jiuxin_mock_city_raw` | 面板 | 11 城五维原始值 | §2.4 |
| `jiuxin_mock_city_radar_dimnames` | 维表 | 五维名 | §1.6 |
| `jiuxin_mock_city_radar` | 面板 | 11 城五维归一值 | §2.4/§2.7 |
| `jiuxin_global_city_top10_raw` | 面板 | 10 城五维原始值 | §2.5 |
| `jiuxin_global_city_top10_radar` | 面板 | 10 城五维归一值 | §2.5 |
| `gkx_capability_like_tables` | 负结论 | [] | §2.2/§3.3 |
| `gkx_index_like_tables` | 甄别 | 4 宏观字典表 | §2.2/§3.4 |
| `dev_capability_like_tables` | 负结论 | [] | §2.2/§3.3 |
| `dev_trend_benchmark_rows` | 负结论 | [0,0] | §2.2 |
| `derived.jiuxin_mock_city_radar_dimcount` | 派生 | 5.0 | §2.7 |
| `absence_probe` | 探针 | 4 条（gkx×2/dev×2） | §2.2 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

### B.3 共享快照消费（B11 零漂移）

本件消费：官方 lane5 探针 #5（geo 171,736）作规模登记值；#6（DESC 五列）作列存在性证据；#44（location_level 分布：CITY 132,975 总行）作 CITY 面规模参照。本件补测 CITY+2025=9,121 落自有快照 `_probe_lane7_innov013_out.json`（四级分布完整）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 归一 | 三源承载 | 贴合度 |
|---|---|---|---|
| RIS 分位对齐（R1） | 分位+去极值 | 五维列可承载 | **高（正式版）** |
| GII 加权维度树（R2） | 0-100+权重 | 五维+权重可配 | 中高 |
| UI 组内相对制（R3） | 值/组内最大×100 | 即挂载实现 | 中高（即期） |
| min-max 全样本（实测） | 极值归一 | 同上 | 中（钳制警示） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| CITY 2025 五维 | 9,121 | 五列全量 | 无（计维口径） |
| ads_location 双名 | 11,284 城 | zh/en 双名 | 海外城 zh 为 NULL |
| gkx 能力类 | 0 表 | — | 结构缺失 |
| dev 评分类 | 0 表 | — | 结构缺失 |
| 政策/环境维 | 无 | — | 语义缺口（§4.1） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 五计维雷达（口径 A/B 直给）+ 维名贴签 | 甲方接受计维口径 |
| v2 | 分位归一替换 min-max | R1 范式移植 |
| v3 | 投入/环境/政策三维扩维 | 上游原料工程 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| mock 原五维语义有损 | **高** | 维名贴签甲方裁定 |
| 极值钳制压扁弱维 | 高 | 分位归一（v2） |
| 硅谷单城替代低估 | 中 | 湾区城市群映射 |
| inbound 维量级小被当总量读 | 低 | 维卡带量级标签 |

### C.5 总判

**完全转换支持**：五维结构+数据双达标（久新 CITY 级 9,121 行五列全量），min-max 归一即期出图；语义贴签（投入/环境/政策三维降级）是配置问题非数据问题，触发器写死 §1.6，按 B10 保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_013.py` | 退出码 0，落 `_out.json` |
| 数据入口 | jiuxin 直连只读；gkx 经 `_gkxdb.py` | demo_* 直接 raise |
| 口径 A 复算 | 北京论文 160,529/组内最大 160,529 | 100.0 |
| 口径 B 复算 | (63,300−23,352)/(160,529−23,352)×100 | 29.12（组内 min-max，与产物一致） |
| 判档一致 | MD 文首 vs 产物 `support_judgment` | 完全转换支持 |
| mock 残留检查 | `rg "baseIndex" repos/demo-ui-science/src/pages/global-innovation/mockData.js` | 正式版替换后无 mock |

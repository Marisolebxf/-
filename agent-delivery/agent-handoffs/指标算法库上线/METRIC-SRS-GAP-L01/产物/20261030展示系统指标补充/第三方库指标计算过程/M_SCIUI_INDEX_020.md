# 排名对比分析（M_SCIUI_INDEX_020）

> **类型**：简单统计类（多对象分维对比视图）｜ **域**：科技发展态势·科技指数·排行榜＞排名对比分析｜ **UI 挂载**：科技指数页 → 排行榜 Tab →「排名对比分析」按钮 → 对比抽屉（雷达+柱状+强弱项+方案管理）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：**需求明列叶**（SRS 科技指数.md seq 175 / excel_row 178）
> **复现脚本**：`code/M_SCIUI_INDEX_020.py`｜ **产物**：`code/M_SCIUI_INDEX_020_out.json`
> **四判定摘要**：直接结构 = 否（三源无现成「对比视图」结果面）；直接数据 = 否；依赖结构 = 是（久新 power 表=对象×四分项得分+总分同构面）；依赖数据 = 是（64,698 行全量，company 子池 13,939）
> **数据源口径**：三源评估——开发库 `gkxlumenx_*`（10.50.11.76:3306）+ 三方库 `gkx`（183.240.141.251:3318 只读）+ 久新库 `jiuxin_warehouse`（47.93.119.170:29030 只读）；本件主承载在久新。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** 对比分析的数据要件是「多对象×多分维同构得分面」——对比视图本质是把这张面按用户选的对象子集切片并排。三源盘点：现成「对比结果面」不存在（dev topic 库 `ent_compare_basket_item` 是用户收藏夹交互态非数据面；ads 库无对比表；gkx 无 score 表），但久新 `ads_institution_technology_power` 正是一张天然同构面：64,698 行（对象）×四分项得分（paper/citation/talent/topic）+总分+名次（版本 2026-09-18×mvp_v1，facts `jiuxin_power_rows`/`jiuxin_power_version`）——任意对象组过滤+分维并排即得雷达/柱状/强弱项/组均值全套对比读数。本件实测复现 UI 同构演示形态：企业 Top5 对比组（Google/BGI/中石化/腾讯/华为，facts `jiuxin_company_top5_compare_group`）、每人强弱项识别（`jiuxin_top5_strength_weakness`）、组均值 98.7077（derived `jiuxin_compare_group_avg_total`，493.5386/5）、组内极差 0.4742。结构+量+对比逻辑实测三证齐，判完全转换支持；分维语义偏移（学术四分族 vs UI 四维）按 B10 披露。

### 批次通用纪律摘要（S3-02 批 Lane 4，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 组均值/极差/分维差分子分母同表同池 |
| B4 | 负结论带探针 | 现成对比面 absence 三源留证（§3.3） |
| B5 | 确定性 | Top5 按 score DESC,name 双键；强弱项双键破平局 |
| B6 | 闸门自身被闸 | 本批不自跑闸门 |
| B7 | 产物只由脚本产出 | 改脚本→重跑 |
| B8 | 回执不复收 | 派单方硬复验 |
| B9 | 单位/日期陷阱 | 得分 float 精度保持；快照日期字符串化 |
| B10 | 口径裁定保守交付 | 学术四分族/UI四维双口径+触发器（§1.6） |
| B11 | 多本账互推 | 64,698/版本/company 13,939 与 INDEX_001/036 零漂移 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 多对象多分维同构面存在吗？ | 存在 | power 64,698×四分项+总分（facts） |
| 对象组过滤+并排跑通了吗？ | 跑通 | `jiuxin_company_top5_compare_group` 五行全分维 |
| 强弱项/组均值可算吗？ | 可算 | `jiuxin_top5_strength_weakness` + derived 组均值 |

## 摘要

「排名对比分析」是需求明列叶（SRS seq 175：「用户可选择多项科技成果进行对比分析，提供对比视图，展示各成果在不同指标上的表现差异和优劣势」），UI 落在排行榜 Tab 的对比抽屉（index.jsx:1229 Drawer，:1327 RankingComparePanel：四维雷达+分维柱状、已选对象 n/上限、平均分/最高分/leader、涨跌家数、单对象最强最弱维、推荐与已保存方案）。数据侧判定：三源无现成对比结果面（收藏夹≠数据面），但久新 power 表 64,698 行对象×四分项+总分是天然同构对比底座——过滤选组+分维并排即得全套对比读数。本件实测企业 Top5 组：Google 98.9091 / BGI 98.8549 / 中石化 98.7811 / 腾讯 98.5585 / 华为 98.4349，组均值 98.7077、极差 0.4742；强弱项全落产物（五家 strength 多为 citation/talent、weakness 集中 topic——学术尺下企业主题覆盖是共性短板）。判**完全转换支持**；UI 四维语义闭合待 INDEX_013 口径 B（对比逻辑与权重正交，闭合后同面复用）。

- 需求判定：**需求明列叶**（seq 175 / excel_row 178；主需求文档 1.1.1.1.4.1.8.3.5 同文）。
- 复现状态：脚本已跑通；对比组/强弱项/对照组/三个派生读数落产物。
- 档位结论：**完全转换支持**（要件面现役+对比逻辑实测）。
- 关键事实：dev `ent_compare_basket_item` 是交互收藏态——「对比」的用户侧容器在 dev 已有，缺的是数据侧分维面（久新补齐）。
- 升档路径：UI 四维（创新/影响/潜力/保障）分维闭合后对比视图语义全对齐（权重件前置）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/科技指数/排行榜/**排名对比分析**（1.1.1.1.4.1.8.3.5；SRS seq 175、excel_row 178——需求明列叶）。UI 挂载点 `index.jsx:1229`：`<Drawer title="排名对比分析">`（width 840，由榜单行「加入对比」按钮触发，上限 `MAX_RANKING_COMPARE_COUNT`）；面板主体 `RankingComparePanel`（index.jsx:1327 同文件内联组件）——上下文条（已选对象 n/上限、排行榜类型、筛选范围）；统计区（`averageScore` 平均分 / `highestScore` 最高分 / `leader` 领跑者 / riser、faller、stable 涨跌平家数 / `trendFocus` 趋势焦点）；图表区（`compareRadarOption` index.jsx:876 四维雷达 + `compareBarOption` index.jsx:951 分维分组柱状，四维=innovation/influence/potential/support）；单对象强弱项（`singleMaxKey`/`singleMinKey` 取 indicators 最大最小维）；推荐位与「已保存方案」（savedSchemes，本地交互态）。雷达与柱状读同一 `compareItems`（mock 由 `applyEvaluationModel` 派生 totalScore/四维分——「禁止手写」注释与 INDEX_001 同源）。

### 1.2 为什么需要本指标

单榜排序回答「谁高谁低」，对比视图回答「高在哪、低在哪」：把 2-N 个对象的分维得分并排成雷达/柱状，用户直接看到 A 的产出强 vs B 的人才强这类结构性差异——这是榜单的「解释层」。SRS 把它独立成叶（「帮助用户深入了解成果的特点和价值」），因为它服务的决策粒度不同：榜单用于筛选（找头部），对比用于评估（在候选间做取舍：引进哪家合作、对标哪个对象）。

### 1.3 需求文档是否给出定义方法

**需求文档给出了功能行为但没给对比口径。** seq 175 原文定义了交互（选择多项）、输出（对比视图）、内容（不同指标上的表现差异和优劣势）——但「对比哪些指标维」「差异怎么量化（差值？比值？雷达叠加？）」「优劣势判定规则」均无定义。UI 的四维雷达+最大最小维判定是前端作者的演示实现。检索记录见附录 A。

### 1.4 类似指标权威方法可行性分析概要

多维对比的通行形态有三族：雷达叠加（EIS 区域对比卡，R1——多对象多维归一分并排）；分维分组柱状（OECD MSTI 对比表，R2——同维跨对象直读差值）；优劣矩阵（强项/弱项象限，SWOT 式）。方法族对照：

| 方法族 | 代表 | 数据要求 | 与本库匹配 |
|---|---|---|---|
| 雷达叠加（UI 形态） | EIS（R1） | 对象×归一分维面 | **有（power 四分项现役）** |
| 分维柱状对比 | OECD MSTI（R2） | 同上 | **有（同面）** |
| 优劣矩阵 | SWOT 族 | 分维+阈值 | 部分（阈值需定义） |

完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-index/index.jsx:1229` — `<Drawer title="排名对比分析">`；`:1327` RankingComparePanel（averageScore `:1347-1349`、leader `:1352-1353`、singleMax/MinKey `:1369-1374`）；`:876` compareRadarOption；`:951` compareBarOption。
- 入口：`index.jsx:1183` 「排名对比分析」按钮（Badge 显示已选数）；榜单行 onAddToCompare。
- SRS：`…/科技发展态势/科技指数.md` seq 175（excel_row 178），原文见附录 A。

### 1.6 推测原意与推测定义

**推测定义**：给定对象组 $G$（$2\le|G|\le$ 上限）与分维集 $D$，输出每对象分维向量 $\{s_{o,d}\}$ 的并排视图 + 组级统计（均值/极值/leader）+ 对象级强弱项（$\arg\max_d s_{o,d}$ / $\arg\min_d s_{o,d}$）。

- **口径 A（建议口径：学术四分族对比）**：$D$=power 四分项（paper/citation/talent/topic），对象=机构（含企业/高校切片）——面现役、本件已实测全套读数；
- 口径 B（UI 语义：四维科技成果对比）：$D$=创新/影响/潜力/保障——需 INDEX_013 权重闭合后在同对象面上重算分维（对比逻辑全复用）。

**降档/升档触发器（B10 模板）**：口径 A 即期交付（分维标注「科技实力四指标」）；口径 B 随权重立项落地（无新增数据依赖，纯分维重算）；若要求「跨期对比」（同期 vs 上期对象组）→ 需多期快照（与 INDEX_019 同缺口，快照期次化前置）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md` |
| 所属四级功能 | 科技指数·排行榜（seq 171–177） |
| 本件叶 | **排名对比分析（seq 175，excel_row 178）——需求明列** |
| 排行榜族相邻叶 | 综合排名（171）/分类排名（172）/详情查看（173）/历史变化（174=INDEX_019）/筛选搜索（176）/结果导出（177） |
| 本批同 Lane | INDEX_019（抽屉邻位：详情 vs 对比）；INDEX_036（综合榜——对比对象的主来源）；INDEX_013（口径 B 前置） |

对比件在排行榜族的位置是「横向」维：历史变化（174）拉时间轴，本件（175）拉对象轴——两件共享同一承载面（power/年度面板），分别消费其横截面与时间截面。这也是两件判档结论相同（完全转换支持）而缺口不同的原因：本件的分维语义偏移在权重件，019 的综合名次历史同源。

## 二、计算过程

### 2.1 装载与对比底座确认

pymysql 直连久新只读库。对比底座 `ads_institution_technology_power`：64,698 行、版本 2026-09-18×institution_technology_power_mvp_v1（facts `jiuxin_power_rows`/`jiuxin_power_version`，与 INDEX_001/036 及共享探针 B1/B2 零漂移）。同构性核验：每行含四分项得分（paper_score/citation_score/talent_score/topic_score）+总分+名次+类型键（institution_type_id）——「对象×分维+总分」正是对比视图的数据形态；权重列随行（0.35/0.30/0.25/0.10，INDEX_013 已验合成自洽 abs_diff=0.0），分维到总分的可解释链路完整。

### 2.2 对象组构造（企业 Top5）

UI 演示语境取企业榜 Radio → 本件以 company 类型过滤+`ORDER BY technology_power_score DESC, institution_name` 双键（B5）取 Top5（facts `jiuxin_company_top5_compare_group` 全分维）：Google (US) 总分 98.909146（paper 98.5533/citation 99.5131/talent 98.9474/topic 98.2472）、BGI Group (CN) 98.8549、Sinopec (CN) 98.7811、Tencent (CN) 98.5585、Huawei (CN) 98.4349——五家四分维+总分+global_rank 十列全落产物，即雷达/柱状的直接数据源。

### 2.3 强弱项识别（单对象 max/min 维）

对组内每对象取四分维最大/最小维（双键破平局：`(score, dim_key)`，B5）：Google 强=学术影响 citation 99.5131 / 弱=主题覆盖 topic 98.2472；BGI 强=人才 talent / 弱=主题覆盖；中石化强=人才 / 弱=学术影响；腾讯强=学术影响 / 弱=主题覆盖；华为强=人才 / 弱=学术影响（facts `jiuxin_top5_strength_weakness` 五行全落）。结构性读数：五家弱项集中在 topic（主题覆盖）与 citation（学术影响）——学术尺下企业的共性短板是主题广度与引用深度，这与 INDEX_001 揭示的「企业让位于高校/院所」同构，是对比视图能提供的真实洞察。

### 2.4 组级统计（UI averageScore/最高分/极差）

组均值 98.7077（493.5386/5，derived `jiuxin_compare_group_avg_total`）；组内极差 0.4742（98.909146−98.434935，derived `jiuxin_compare_group_total_range`，分母=组内最低分——跨度键标注非比值）；分维差异度样例：citation 维组内极差占比 1.8561%（1.8471/99.5131，derived `jiuxin_compare_group_citation_spread_pct`）——头部五家总分接近但分维结构有别，雷达叠加正是呈现这种「总分相近、形状不同」的形态。

### 2.5 跨类型对照组（education Top3）

对比不限企业：education Top3 对照组（facts `jiuxin_education_top3_reference`）：国科大 99.998454（四维近满分形态）/北大/浙大——高校头部四分维全 99.99+ 的「满盘皆强」与企业组的「参差强」形成跨类型对比样例，验证对比逻辑对任意对象组的通用性（用户选跨类型组亦可用）。

### 2.6 稳健性与口径敏感性

对象组敏感：Top5 组读数依赖过滤键与排序键——换 education 组则强弱项形态完全不同（§2.5），对比结论只在组内有效，产物按组交付不建议跨组聚合。分维敏感：四分族（学术）与 UI 四维（创新语义）的名次与形状不可互推——雷达形状对比必须在同分维族内做（B10 已列）。同分同名列：双键排序（score, name）保证组构造确定性；强弱项 (score, dim_key) 同理。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INDEX_020.py`（久新直连）；运行 `python3 code/M_SCIUI_INDEX_020.py`。
- 产物：`code/M_SCIUI_INDEX_020_out.json`。正文数字对应键：`jiuxin_power_rows`/`jiuxin_power_version`（§2.1）、`jiuxin_company_top5_compare_group`（§2.2）、`jiuxin_top5_strength_weakness`（§2.3）、`jiuxin_education_top3_reference`（§2.5）、derived 三键（§2.4）。
- 结果解读：对象组/强弱项/组统计/对照组四组读数覆盖 UI 对比抽屉的全部数据位（雷达、柱状、平均/最高、leader 可由组数据派生、强弱项）。
- 对照需求功能要求的评审：对比视图回填——**有条件通过**：口径 A 即期可供（学术四分族+标注）；未通过点=分维语义与 UI 四维不同构（口径 B 待权重件）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 | 数值 |
|---|---|---|---|
| 底座 | 对比面规模 | `jiuxin_power_rows` | 64,698 |
| 底座 | 版本 | `jiuxin_power_version` | 2026-09-18×mvp_v1 |
| 组构造 | 企业 Top5 | `jiuxin_company_top5_compare_group` | Google 98.9091 首位 |
| 强弱项 | 五家 max/min 维 | `jiuxin_top5_strength_weakness` | 弱项集中 topic/citation |
| 组统计 | 组均值 | `jiuxin_compare_group_avg_total` | 98.7077（493.5386/5） |
| 组统计 | 组内极差 | `jiuxin_compare_group_total_range` | 0.4742 |
| 组统计 | 分维差异度 | `jiuxin_compare_group_citation_spread_pct` | 1.8561% |
| 对照 | education Top3 | `jiuxin_education_top3_reference` | 国科大 99.998454 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 对象×分维同构面 | jiuxin_warehouse | `ads_institution_technology_power`（四分项+总分） | 64,698 | 直查 | **有** |
| D2 | 对象类型切片键 | jiuxin_warehouse | `institution_type_id`（company 13,939 等） | 9 类 | 直查 | 有 |
| D3 | UI 四维分项 | 三源 | —（创新/影响/潜力/保障） | — | **不存在** | 缺（口径 B，权重件前置） |
| D4 | 对比交互容器 | dev | `ent_compare_basket_item`（topic 库） | — | 有 | 收藏态（前端已实现） |

`support_judgment="完全转换支持"`，与文首同档（闸 6）。

### 3.2 D1/D2 质量面

同构面三重可用性：分维完备（四分项+总分+名次随行）、权重可解释（INDEX_013 合成校验 abs_diff=0.0 背书）、版本单一（跨行可比）。类型切片九类全枚举（education 16,446/company 13,939/healthcare 10,877/facility 9,021/…，与 INDEX_036 facts 一致）——四榜 Radio 与跨类型对比的对象供给齐备。

### 3.3 D3 absence_probe 全记录

否定性证据三件套：**查了什么**——①久新 power 22 列核对（UI 四维语义分列）；②dev ads 68 表+topic 库 21 表扫描（对比结果面/收藏面区分）；③gkx `%rank%`/`%score%` 表扫描。**条件**——①现成四维科技成果对比面；②现成对比结果表。**命中**——①语义分列无（学术四分族替代）；②dev 仅收藏态交互表（非数据面，不构成承载）；③gkx 0 张。缺失情形归属：D3 为「分维语义未建设」（权重件管辖）；对比结果面为「无需存在」（对比是视图逻辑不是物化面——本件转换路径已证）。

## 四、数据缺失情况

### 4.1 UI 四维分项缺失（语义级，权重件前置）

UI 雷达/柱状读四维（创新/影响/潜力/保障），久新面是学术四分族——形状语义不同族。缺口归 INDEX_013 口径 B（体系赋权）管辖：权重闭合后在同对象面重算四维分，对比逻辑（§2.2-2.4 全部代码）零改动复用。本件不重复立项。

### 4.2 跨期对比缺失（时点级，与 019 同源）

「本期 vs 上期对象组对比」需多期快照（power 单期）。年度面板可支撑原始指标的跨期对比（INDEX_019 路径），综合分跨期需权重×多期双前置——列为远期，不阻塞即期交付。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 对比 API 直供 v1 | 数据工程 | 本件即期 | 对象组+分维+组统计+强弱项 |
| 四维分重算 | 建模工程 | 本件+013/036 | 权重闭合后同面复算 |
| 推荐位算法 | 产品决策 | 本件 | 推荐补齐对象（mock 有形态） |

## 参考文献

1. European Innovation Scoreboard 2024[EB/OL]. European Commission. https://research-and-innovation.ec.europa.eu/statistics/performance-indicators/european-innovation-scoreboard_en （2026-11-01 WebSearch 核验可达；多对象多维归一分雷达对比的国际范式）
2. OECD Main Science and Technology Indicators[EB/OL]. OECD. https://www.oecd.org/sti/msti.htm （2026-11-01 WebSearch 核验可达；分维跨对象直读差值的对照表范式）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/科技指数.md》seq 175（excel_row 178）——**需求明列叶**：

> ### 排名对比分析 · 序号 175
> - path: 智能服务集群/科技信息展示系统/科技发展态势/科技指数/排行榜/排名对比分析
>
> #### 需规功能描述
> 用户可选择多项科技成果进行对比分析，提供对比视图，展示各成果在不同指标上的表现差异和优劣势，帮助用户深入了解成果的特点和价值。

主需求文档 1.1.1.1.4.1.8.3.5 同文收录。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 排名对比分析 | 科技指数.md | **1（seq 175，需求明列）** |
| 排名对比分析 | 主需求文档 | 1（1.1.1.1.4.1.8.3.5） |
| 对比视图 | 科技指数.md | 1（seq 175 功能描述内） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INDEX_020_out.json`（2026-11-01 实跑）。
- 共享探针：`_probe_lane4_s302_out.json`（B1/B2 power 对账；E 组 dev 表扫描——ent_compare_basket* 收藏面确认；D3 gkx 扫描）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INDEX_020 | 文首 |
| `ui_evidence` | 证据 | 3 条组件行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **true**（seq 175/excel_row 178） | §1.1/附录 A |
| `facts.jiuxin_power_rows` | 计数 | 64,698 | §2.1 |
| `facts.jiuxin_power_version` | 版本 | 2026-09-18×mvp_v1 | §2.1 |
| `facts.jiuxin_company_top5_compare_group` | 对比组 | 5 行×全分维 | §2.2 |
| `facts.jiuxin_top5_strength_weakness` | 强弱项 | 5 行 | §2.3 |
| `facts.jiuxin_education_top3_reference` | 对照组 | 3 行 | §2.5 |
| `derived[0]` | 派生比 | 组均值 98.7077（493.5386/5） | §2.4 |
| `derived[1]` | 跨度 | 极差 0.4742 | §2.4 |
| `derived[2]` | 派生比 | citation 差异度 1.8561% | §2.4 |
| `absence_probe` | 探针 | 三源 3 条 | §3.3 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 数据形态 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 雷达叠加（UI 形态） | EIS（R1） | 对象×归一分维 | power 四分项现役 | **最高（口径 A）** |
| 分维柱状 | OECD MSTI（R2） | 同维跨对象 | 同面 | 高 |
| 优劣矩阵 | SWOT 族 | 分维+阈值 | 阈值需定义 | 中 |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| power 同构面 | 64,698 | 四分项+总分+名次 | 分维=学术族（语义偏移） |
| 类型切片 | 9 类 | OpenAlex 体系 | 国内口径映射（同 001） |
| UI 四维分 | — | — | 权重件前置 |
| 对比收藏容器 | dev topic 库 | 交互态 | 已实现（前端侧） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 对比 API（组/分维/统计/强弱项） | 无 |
| v2 | UI 四维分对比 | INDEX_013 权重闭合 |
| v3 | 跨期对比 | 多期快照 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 学术四分族雷达被当 UI 四维 | **高** | 图表标注「科技实力四指标」 |
| 跨组聚合误用 | 中 | 按组交付+组内结论限定 |
| 头部分维趋同致雷达形状扁平 | 低 | 极差/差异度读数联读 |

### C.5 总判

**完全转换支持**：同构面现役+对比逻辑实测；语义偏移以双口径披露，闭合路径与权重件联动不悬空。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INDEX_020.py` | 退出码 0，落 `_out.json` |
| power 对账 | `jiuxin_power_rows` vs INDEX_001/036 | 64,698 零漂移（B11） |
| 组构造复核 | company Top5 首位 | Google 98.909146 |
| 组均值复算 | Σtotal/5 | =derived.jiuxin_compare_group_avg_total |
| 判档一致 | MD 文首 vs `support_judgment` | 完全转换支持 |

# M_SCIUI_P10_014 单位贡献度（M_SS_UNIT_CONTRIB）—— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：软科学成果展示 New·多维统计·单位贡献度 Top8（`BottomTabs.jsx:568`）｜ **UI 挂载**：科技信息展示系统 → 创新载体孵化载体 New（软科学新页）→ 多维统计 tab「单位贡献度 Top8（点击柱条联动地图）」柱图
> **数据支持度**：**完全不支持**｜ **公式定义人**：mock 自设（`getContribution` 权重 20/0.4/0.15 无权威出处；SRS 468 未给权重）｜ **口径归属**：UI 挂载件（SRS 无同名指标；上位叶=软科学成果展示·序号 468「单位贡献度与空间分布统计」）
> **复现脚本**：`code/M_SCIUI_P10_014.py`（薄壳，指向共享探针 `code/_shared_s308_laneb_probe.py`）｜ **产物**：`code/M_SCIUI_P10_014_out.json`
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（三源无贡献度面）；直接数据=无；依赖结构=无（贡献度三要素 rating/progress/budget 随课题库零承载）；依赖数据=无（dev 课题表 0 行空壳；jiuxin 项目画像 1,838,841 行语义错位无评分/进度列）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全不支持。**（贡献度三要素随软科学课题库三源零承载；宿主无则贡献度无）。

### 批次通用纪律摘要（S3-08 批共用）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B4 | 负结论带探针 | absence_probe 三源逐一留证 |
| B5 | 列表 sorted() | 词族命中/基期 sorted |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳脚本重跑产出 |
| B9 | 单位/日期陷阱 | 经费单位万元（mock 55-120）披露 |
| B10 | ui_demo_fallback + 权重自设披露 | mock 权重 20/0.4/0.15 无权威出处 |
| 基期三键 | base_years_used/missing/note | 产物全键（全空登记） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有课题库（宿主）吗？ | 无 | dev fund_project/enterprise_fund_project 0 行空壳；gkx 无中文课题面 |
| 画像面可代理吗？ | 语义错位 | jiuxin ads_project_profile（1,838,841 行）OpenAlex 资助项目，无 rating/progress 列 |
| 权重口径有出处吗？ | 无 | mock 自设 20/0.4/0.15；SRS 468 未给——双缺（数据+口径） |

## 摘要

「单位贡献度 Top8」是软科学新页多维统计 tab 的左卡（`BottomTabs.jsx:568`）：承担单位贡献度合计柱图，点击柱条联动空间分布地图（`handleUnitClick`），邻卡为区域贡献度 Top8（M_SS_REGION_CONTRIB 同族）。口径为 mock 自设加权式 `getContribution(t) = round(rating×20 + progress×0.4 + min(30, budget×0.15))`（`BottomTabs.jsx:30-32`，注释自认「演示」）。数据侧判定：**完全不支持**——贡献度三要素（影响力评分/进度/经费）全部挂在软科学课题行上，而课题库三源零承载：dev `fund_project`（7 列）/`enterprise_fund_project`（9 列）均 0 行空壳；gkx 280 表无中文软科学课题面（`dwd_en_project` 20,000 行英文项目无评分/进度列）；jiuxin `ads_project_profile`（1,838,841 行）为 OpenAlex 资助项目画像，有 amount 金额面但无课题评分/进度语义——资金排名 ≠ 贡献度（权重结构缺失），语义错位不冒用。宿主无则贡献度无；且权重口径本身无权威出处（双缺：数据+口径）。

- 需求判定：**UI 挂载件**（SRS 无同名；上位叶=序号 468 单位贡献度与空间分布统计；另 1.2.x 成果优选「按贡献度排序」为消费侧上位）。
- 复现状态：薄壳已跑通；负结论落产物。
- 档位结论：**完全不支持**（课题库零承载连锁）。
- 关键事实：mock 权重三系数（20/0.4/0.15 封顶 30）纯演示自设——即使数据到位口径也需先立项。
- 升档路径：软科学课题库接入（承担单位+评分+进度+经费四列）+ 权重口径裁定 → 完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 软科学成果展示（New 页族）→ 多维统计与趋势分析 tab →「单位贡献度 Top8（点击柱条联动地图）」卡（`BottomTabs.jsx:568` SectionCard，MetricInfo 口径自述「承担单位贡献度合计（影响力×20+进度×0.4+经费权重）；点击联动空间分布」+MockBadge）。构建链：`getContribution`（`:30-32`）单课题加权 → `buildContributionSheets`（`:62-99`）unitMap 按承担单位聚合、contribution 降序 → `unitBarOption` 柱图 → `handleUnitClick` 地图联动。mock 课题源 `mockData.js:96` 起 SOFT_TOPICS（rating 4.2-4.9/progress 18-100/budget 55-120 万元）。

### 1.2 为什么需要本指标

单位贡献度回答「谁的课题产出贡献大」：管理者以此做资源精准分配与横向业绩对标（SRS 468 需规原文「有助于精准资源分配、横向比较和纲领性政策评估」）；空间联动版可看贡献的空间聚集。

### 1.3 需求文档是否给出定义方法

**三份说明书未给出该指标的计算方法。** M_SS_UNIT_CONTRIB 编号未在需求文档出现（UI MetricInfo 自设）；上位叶 468 只给功能行为（批量输出贡献度报表、多维图表联动地图），无贡献度公式（权重结构/归一化方法/TopN 口径均未定义）——mock 权重为演示自设。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①科研机构评价（中科院机构评价/学科评估：成果数量×质量加权，官方口径但颗粒为机构整体）；②成果计分制（科技奖励计分：国家级/省部级奖项固定分值，事件驱动）；③h 指数族（学术影响力，作者/机构粒度）。三族与本件「课题要素加权」口径均不同构：①缺课题要素行、②需奖励库、③需成果归属面——软科学课题库零承载下全部不可落地。完整版见附录 C。

### 1.5 引用来源

1. 中国科学院. 科研机构评价体系（机构评估口径）. https://www.cas.cn/
2. 教育部. 学科评估指标体系（第四轮/第五轮，成果质量加权）. https://www.cdgdc.edu.cn/dsl/
3. Hirsch J E. An index to quantify an individual's scientific research output. PNAS, 2005. https://www.pnas.org/content/102/46/16569

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：承担单位名下全部软科学课题的综合贡献得分排名（影响力+进度+经费三要素加权）。
- **操作化定义（未实现，沿用 mock 式但须披露自设）**：单位贡献度 = Σ_课题 round(rating×20 + progress×0.4 + min(30, budget×0.15))，按单位聚合降序 Top8。
- **降档触发器**：已处最低档。
- **升档触发器**：软科学课题库接入（承担单位+评分+进度+经费四列）→ 完全转换支持（权重口径随数据字典立项）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/软科学成果展示.md` |
| 所属四级功能 | 1.1.1.1.4.6 科技成果展示（域）|
| 所属页面 | 软科学成果展示 New（创新载体孵化载体 New 页族）|
| 本件叶 | 多维统计·单位贡献度 Top8（UI 挂载件；上位叶=序号 468）|
| 相近叶 | 区域贡献度 Top8（M_SS_REGION_CONTRIB 邻卡同族）/ 综合影响力（M_SS_IMPACT_SCORE，`:236` 同页）/P10_004 互动统计（同 BottomTabs 邻 tab）|
| UI 容器 | `BottomTabs.jsx:564-575` SectionCard |

## 二、计算过程

从缺。本指标需软科学课题行（承担单位+rating 评分+progress 进度+budget 经费四要素），三源探针（附录 B）证明零承载：dev 课题表 `gkxlumenx_ods.fund_project`（7 列）/`gkxlumenx_dwd.enterprise_fund_project`（9 列）均 0 行空壳；gkx 280 表贡献度词族（contrib/rating+progress 组合）0 命中（`dwd_en_project` 20,000 行英文资助项目无评分/进度列）；jiuxin 218 表（SHOW TABLES 实数）contrib 词族 0 命中，`ads_project_profile`（1,838,841 行、46 列）为 OpenAlex 资助画像——amount 金额面可算「单位获资助排名」但权重结构（影响力×进度×经费）缺失，资金排名 ≠ 贡献度，语义错位不冒用。宿主课题库零承载则三要素无从取数，禁伪公式；mock 权重 20/0.4/0.15 为演示自设（代码注释自认「演示」），ui_demo_fallback 披露。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 软科学课题库（宿主） | dev `fund_project`/`enterprise_fund_project` | **0 行空壳** |
| 课题评分（rating） | dev/gkx/jiuxin | **无列**（三源无课题评分语义） |
| 课题进度（progress%） | dev/gkx/jiuxin | **无列** |
| 课题经费（budget） | dev 空壳列 / jiuxin amount | dev 0 行；jiuxin 语义为资助金额非立项经费 |
| 承担单位维度 | 同课题库 | 随宿主零承载 |
| 资助金额面（代理候选） | jiuxin `ads_project_profile` | **语义错位**（无权重结构，不冒用） |

### 3.2 现场复核清单

UI 链实读：`BottomTabs.jsx:568` 卡标题+MetricInfo（口径自述含 MockBadge）、`:30-32` getContribution 权重式（注释「与列表页口径一致（演示）」）、`:62-99` buildContributionSheets 三聚合降序、`mockData.js:96` 起 SOFT_TOPICS 三要素演示值。三源实连复核（共享探针 + 逐表实查）：dev 课题表 COUNT=0；gkx 词族 0 命中；jiuxin 218 表 contrib 0 命中、ads_project_profile 46 列 DESCRIBE 实核无 rating/progress 列。

## 四、数据缺失情况

### 4.1 缺口清单

①软科学课题库无表（宿主主因）；②课题评分/进度两要素无列（即使库在也缺要素）；③权重口径无立项（mock 自设无权威出处）；④承担单位-地理映射（空间联动）随宿主缺失。

### 4.2 修复建议与影响面

短期：卡片维持 mock 并标注演示态。中期：软科学课题库接入（四列齐备）+ 权重口径随数据字典立项 → 完全转换支持（单位/区域两卡 + 空间联动一次升档）。远期：成果归属面接入 → 权威加权（机构评价口径）可对齐。同族联动：M_SS_REGION_CONTRIB（区域贡献度邻卡）与 M_SS_IMPACT_SCORE（综合影响力）同根同判。

### 4.3 影响面

多维统计 tab 的单位/区域两张贡献度卡维持 mock；SRS 468「批量输出贡献度报表」承诺整链无数据支撑；成果优选排序（按贡献度）消费点同判。

## 参考文献

1. 中国科学院. 科研机构评价体系. https://www.cas.cn/
2. 教育部学位与研究生教育发展中心. 学科评估指标体系. https://www.cdgdc.edu.cn/dsl/
3. Hirsch J E. An index to quantify an individual's scientific research output. PNAS, 2005, 102(46): 16569-16572. https://www.pnas.org/content/102/46/16569

# 附件

## 附录 A 原始需求原文摘录

- SRS《软科学成果展示.md》序号 468（excel_row 471，path=…/多维统计与趋势分析/单位贡献度与空间分布统计）：「平台批量输出各单位、机构及区域的课题贡献度报表，多维图表（如饼图、柱状图）联动地理分布地图，高亮展示资源聚集和业绩对标情况。有助于精准资源分配、横向比较和纲领性政策评估，实现成果整理的标准化和信息共享。」
- 检索记录：`rg M_SS_UNIT_CONTRIB|单位贡献度` 三份说明书 → 编号 0 命中；功能叶 468 命中（上位覆盖）。
- 实查定位链：清单挂点 BottomTabs.jsx:568 直核 → :30-32 getContribution 权重式 → mockData.js:96 SOFT_TOPICS。
- mock 参照：权重 20/0.4/0.15（封顶 30）；课题三要素 rating 4.2-4.9/progress 18-100/budget 55-120 万元。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_014_out.json`）

metric_id/batch=S3-08/ui_evidence（3 条组件行号）/requirement_trace（named_in_srs=false + SRS 锚 468）/facts（ui_mount/ui_formula/ui_build/ui_mock_note/dev_topic_tables/gkx_topic_note/jiuxin_project_note/contribution_like_columns=[]/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）/derived[0]（负结论 null）/absence_probe（三源三条）/support_judgment=完全不支持/notes（5 条）/base_years 三键（全空）/ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：机构评价（成果质量加权）→ 奖励计分制（事件分值）→ h 指数族（学术影响力）——三族与课题要素加权式均不同构。数据矩阵：课题宿主 0；三要素（评分/进度/经费）两缺一错位。分期方案：一期课题库四列接入（升完全转换）、二期权重立项、三期成果归属面（权威口径对齐）。风险登记：资助金额排名冒充贡献度（语义污染）、mock 权重冒充正式口径（双缺披露）、空间联动随宿主缺失。总判：完全不支持（宿主连锁；升档=库+口径双立项）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_014.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneb_probe.py` | 快照词族面零漂移 |
| 判档一致 | MD 文首「完全不支持」= out.json `support_judgment` | 一致 |
| 负证据 | absence_probe 三条（课题表 0 行/画像语义错位） | 逐一可复验 |
| mock 披露 | 权重式+三要素演示值仅 §1.1 语义描述 | 不参与支持度结论 |

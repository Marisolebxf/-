# M_SCIUI_THINK_014 竞赛排行榜 TOP10 —— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：科技服务全景·智库服务·竞赛排行榜 TOP10（TechCompetition.jsx:323+98-136，排行榜 tab 榜单表格）｜ **UI 挂载**：科技信息展示系统 → 科技服务全景 → 科技竞赛 → 排行榜 tab「竞赛排行榜 TOP10」表格（`TechCompetition.jsx:323`）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（指标名三源 0 命中；榜单排序键无定义）｜ **口径归属**：UI 挂载件（`_phase3_screen_v3.json` kept_items），SRS 无同名指标
> **复现脚本**：`code/M_SCIUI_THINK_014.py`（薄壳，读共享探针快照 `_snapshots/_shared_s309_think_beta_probe{1,2}_out.json` + mock 源断言）｜ **产物**：`code/M_SCIUI_THINK_014_out.json`
> **四判定摘要**：直接结构=无；直接数据=无；依赖结构=无（团队竞赛得分面三源 0 表，score 命中全为企业/产业链评分语义错位）；依赖数据=无（竞赛主档三源 0 表，competition 命中全为产业链竞争力/科研问题竞争排名语义错位，jiuxin 最近邻 46,835 行为城市×科研问题排名非团队榜）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全不支持。**（排序键与排序域双前提三源零承载）

### 批次通用纪律摘要（S3-09 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B4 | 负结论带探针 | absence_probe 三源逐一留证（§三/附录 B） |
| B5 | 列表 sorted() | 词族命中/score 序列/ctx_refs sorted |
| B7 | 数字-出处核对 | 10/98.5/89.9/46,835/22,445/16,725/7,370/295/9,367 均对产物键 |
| B10 | ui_demo_fallback 披露 | mock 10 条榜单（98.5→89.9）披露 |
| 基期三键 | base_years_used/missing/note | 产物全键（全空登记） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有团队竞赛得分面（排序键）吗？ | 无 | score 词族命中全为企业/产业链评分（enterprise_score 族） |
| 三源有竞赛主档（排序域）吗？ | 无 | competition 词族命中全语义错位（产业链竞争力/科研问题排名） |
| 最近邻可用作代理吗？ | 不可 | jiuxin 46,835 行排名表的 subject 是城市/机构非参赛团队 |

## 摘要

「竞赛排行榜 TOP10」是科技竞赛页排行榜 tab 左栏的榜单表格（`TechCompetition.jsx:323` Card，`rankingColumns`（`:98-136`）四列：排名（前三名奖杯徽标）/团队（队名+机构）/项目名称/得分；mock `competitionRankings` 10 条，QuantumForce 98.5 居首至 MedTechPro 89.9）。数据侧判定：**完全不支持**——排行是排序面，排序操作零成本，判档只看两前提：团队竞赛得分（排序键）三源 0 表（dev score 命中 `enterprise_score`/`svc_tech_power_score` 等企业评分族，S3-08 INCUB_043/047 已证评分模型域双缺）；竞赛主档（排序域）三源 0 表（jiuxin 最近邻 `ads_research_problem_competition_rank` 46,835 行实测为城市×科研问题竞争力排名：scope=CITY 22,445/PROVINCE 16,725/COUNTRY 7,370/DISTRICT 295，dimension 五维各 9,367——subject 是城市/机构非参赛团队，禁作代理）。与 THINK_003（评审得分）构成键-榜对、与 THINK_013（报名数）同宿主缺，独立留证。

- 需求判定：指标名三份说明书未出现；上位叶 SRS 序号 592（成绩榜单接口）/585（排行榜关联归档）覆盖。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技服务全景 → 科技竞赛 → WorkbenchTabs 排行榜 tab（TrophyOutlined，`TechCompetition.jsx:310-349`）→ 左栏「竞赛排行榜 TOP10」表格 + 右栏「竞赛类型分布」饼图（CONTEST_001 域）。表格四列由 `rankingColumns`（`:98-136`）定义：排名列带 `rank-1/2/3` 奖杯徽标样式（`:103-109`）、团队列 Avatar+队名+机构（`:112-125`）、项目名称、得分（`:132-135` 渲染强调样式）；`pagination={false}` 固定 10 行。mock `competitionRankings`（`mockData.js:271-283`）10 条：rank 1-10，score 98.5/97.2/96.8/95.5/94.3/93.7/92.5/91.8/90.6/89.9 递减，机构覆盖清华/北大/中科院/复旦/哈工大/浙大/上海交大/中科大/北航/中山大学。

### 1.2 为什么需要本指标

TOP10 榜单是竞赛页的**头部成果展示面**：把团队×项目×得分的头部十名推到眼前，回答「这届比赛谁最强」。它与 KPI 四卡（量级面）、竞赛卡（供给面）、类型分布（结构面）构成竞赛运营全貌；榜单的排序键（评审得分）即 THINK_003 的指标——003 是键，本件是键的排序呈现，两者构成键-榜对。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**（SRS 序号 592 要求「为成绩排行榜、参赛行为等提供独立数据接口」，接口有要求、榜单口径（排序键/取前 N/同分处理）无定义。）

### 1.4 类似指标权威方法可行性分析概要

权威侧无国标榜单口径；竞赛平台通用实践：评审得分 ORDER BY DESC LIMIT 10，同分并列（rank_ties）或按提交时间破平。Kaggle leaderboard 公开口径：团队×里程碑得分滚动榜（公榜/私榜分离防过拟合）。方法族：①评审得分排序（平台自建评审系统）；②平台 API 榜单直连（Kaggle/天池 leaderboard）；③综合积分制（多轮赛事累计，如 ACM-ICPC 区域赛积分）。榜单属平台自设运营面。

### 1.5 引用来源

1. Kaggle Competitions Leaderboard（团队榜单口径：公榜/私榜、同分处理）. https://www.kaggle.com/competitions
2. 阿里云天池大赛排行榜（团队×得分排序口径）. https://tianchi.aliyun.com/competition
3. 中国「互联网+」大学生创新创业大赛（全国总决赛获奖名单公示口径）. https://cy.ncss.cn

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：某场（或某届综合）科技竞赛按评审得分取前 10 的团队榜：排名/团队/机构/项目/得分五元组。
- **操作化定义（本件未实现）**：TOP10 = (团队, 机构, 项目, 得分) ORDER BY 得分 DESC LIMIT 10（同分并列，破平规则待定）。
- **降档触发器**：已处最低档。
- **升档触发器**：竞赛评审系统落库（团队×竞赛×评审得分，即 THINK_003 的排序键面）→ 完全转换支持（ORDER BY 即得）；赛事平台 API 直连（leaderboard 回传）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：科技竞赛·排行榜 tab·TOP10 榜单。
- 相近叶：竞赛项目评审得分（THINK_003，排序键，同判零承载构成键-榜对）；数据科学赛道报名数（THINK_013，同宿主缺）；竞赛类型分布（CONTEST_001，路γ，同 tab 右栏饼图）。
- 同宿主缺：竞赛主档 0 表导致整页竞赛族（003/004/005/013/014、CONTEST_001）全零承载。

## 二、计算过程

从缺。榜单需「团队得分面（排序键）+ 竞赛主档（排序域）」双前提，三源探针（附录 B）证明双面零承载：排序键侧——dev score 词族命中 `enterprise_score`/`svc_tech_power_score`/`industry_chain_region_scorecard` 等全为企业/产业链评分面（S3-08 INCUB_043/047 已证评分模型域评分面+模型双缺，本件独立复核一致），团队×竞赛×评审得分三源 0 表；排序域侧——competition 词族 dev 7 张全语义错位（产业链竞争力/企业排名/政策排名/竞争定位文案）、gkx 0 张、jiuxin 4 张（`ads_research_problem_competition_rank` 46,835 行 + talent 评分 demo 表 3 张）。jiuxin 最近邻结构实测排除：`competition_scope` 分布 CITY 22,445/PROVINCE 16,725/COUNTRY 7,370/DISTRICT 295、`ranking_dimension` 五维（FRONTIER_LEADERSHIP/RESEARCH_SUBJECT_TOTAL/INVESTMENT/OVERALL_COMPETITION/RESEARCH_HEAT）各 9,367——它按城市/机构对科研问题（problem_id 前缀 rp_）竞争力排名，subject 非参赛团队、metric 非竞赛得分，禁作代理。排序操作本身（ORDER BY score DESC LIMIT 10）零成本，缺的是排序键数据。禁伪公式。mock 10 条（QuantumForce 98.5→MedTechPro 89.9）为演示量级参照（ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 团队竞赛得分面（排序键） | dev/gkx/jiuxin | **无表**（score 命中全为企业/产业链评分） |
| 竞赛主档（排序域） | dev/gkx/jiuxin | **无表**（competition 命中全语义错位） |
| 科研问题竞争排名（最近邻） | jiuxin | 语义错位（46,835 行，subject=城市/机构） |
| 团队/机构维 | mock | 演示态（10 队静态） |

### 3.2 现场复核清单

UI 链实读：`TechCompetition.jsx:323` Card title；`:98-136` rankingColumns 四列；`:103-109` 前三名奖杯徽标；mock 源 `mockData.js:271-283`（10 条榜单，本件脚本对源文件断言：rank 序列 ≥10 条、QuantumForce/score 98.5 在册）。三源实连复核（本件脚本断言）：dev 542 表 competition 命中 7 张语义错位清单在册；gkx 280 表 `[]`（断言通过）；jiuxin 218 表命中 4 张且 `ads_research_problem_competition_rank` 在列（断言通过）；jiuxin 排名表 46,835 行 + `competition_scope`/`ranking_dimension` 列名断言通过（二期快照）；scope/dimension 实测分布（三期快照）与正文一致。

## 四、数据缺失情况

### 4.1 缺口清单

①团队竞赛得分面无表（三源，排序键缺失）；②竞赛主档无表（三源，排序域缺失）；③榜单口径未定（单场 vs 跨场综合、同分破平规则、届次时间窗）；④评审得分本身的产生机制（专家打分/系统自动评分）未建——与 THINK_003 同根。

### 4.2 修复建议与影响面

短期：竞赛评审系统落库（团队×竞赛×评审得分，覆盖 THINK_003 排序键）→ 本件完全转换支持（ORDER BY DESC LIMIT 10 即得）。中期：赛事平台 API 对接（Kaggle/天池 leaderboard 回传）→ 热门赛事直连。远期：多轮赛事综合积分制榜单（ACM 类积分口径）。同根修复：THINK_003（评审得分）与本题共用评分面，一次立项两件激活；整页竞赛族（004/005/013、CONTEST_001）随竞赛主档接入整族升档。推荐：评审系统+主档随竞赛模块后端一并立项。

### 4.3 影响面

排行榜 tab 榜单为 mock 演示态；整页竞赛域无后端接口调用；右栏类型分布饼图（CONTEST_001）同 mock。

## 参考文献

1. Kaggle Competitions Leaderboard（团队榜单口径）. https://www.kaggle.com/competitions
2. 阿里云天池大赛排行榜（团队×得分排序口径）. https://tianchi.aliyun.com/competition
3. 中国「互联网+」大学生创新创业大赛（总决赛获奖名单公示口径）. https://cy.ncss.cn

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 竞赛排行榜|排行榜 TOP10|TOP10` 三份说明书 + 主需求 → 指标名 0 命中。
- 清单挂载：`_phase3_screen_v3.json` kept_items mount=`pages/tech-service/TechCompetition.jsx:323`（实查确认 :323 Card + :98-136 列定义）。
- SRS 上位叶：科技竞赛.md 序号 592「成绩榜单接口：为成绩排行榜、参赛行为等提供独立数据接口，保证多终端展示、用户互动的高效流转与管理」；序号 585「将参赛者数据、参与记录、论坛发言、排行榜等内容关联归档」。
- mock 参照（`mockData.js:271-283`）：10 条榜单 rank 1-10，score 98.5→89.9。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_THINK_014_out.json`）

facts（ui_mount/ui_mock_note/ui_neighbors/ranking_prereq_note 双前提/competition_host_note 主档 0 表/jiuxin_rp_rank_note 46,835 行实测分布/score_semantic_note 评分语义错位/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）；derived[0]（competition_top10_negative 负结论 null 登记）；absence_probe（三件，双面零承载断言）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2021-2026 / note）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：评审得分排序（平台自建，ORDER BY DESC LIMIT 10）→ 平台 API 榜单直连（Kaggle/天池 leaderboard）→ 综合积分制（多轮累计）。数据矩阵：团队得分面三源 0 表；竞赛主档三源 0 表；jiuxin 最近邻 46,835 行为城市×科研问题排名（subject=城市/机构，禁代理）。分期方案：一期评审系统落库（完全转换支持，与 THINK_003 联动）、二期赛事 API 对接、三期综合积分制。风险登记：榜单口径（单场/综合/同分破平）未定、评审机制未建、jiuxin 排名表误用风险（语义错位须显著标注）。总判：完全不支持（双前提皆缺，升档=评审系统+主档立项，一次激活键-榜两件）。

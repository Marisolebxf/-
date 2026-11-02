# M_SCIUI_THINK_013 数据科学赛道报名数 —— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：科技服务全景·智库服务·确认报名＞数据科学（TechCompetition.jsx:163-168+174，报名弹窗×赛道饼图合成语义）｜ **UI 挂载**：科技信息展示系统 → 科技服务全景 → 科技竞赛 → 竞赛卡报名弹窗 + 排行榜 tab 赛道分布饼图（`TechCompetition.jsx:163-168`/`:174`）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（指标名三源 0 命中；赛道报名口径无定义）｜ **口径归属**：UI 挂载件（`_phase3_screen_v3.json` kept_items），SRS 无同名指标
> **复现脚本**：`code/M_SCIUI_THINK_013.py`（薄壳，读共享探针快照 `_snapshots/_shared_s309_think_beta_probe{1,2,4}_out.json`）｜ **产物**：`code/M_SCIUI_THINK_013_out.json`
> **四判定摘要**：直接结构=无；直接数据=无；依赖结构=无（竞赛主档三源 0 表，competition 词族命中全为产业链竞争力/科研问题竞争排名语义错位）；依赖数据=无（报名流水三源 0 表，enroll 词族命中全为临床试验入组/注册资本/课题条目污染）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全不支持。**（竞赛主档与报名流水双面三源零承载）

### 批次通用纪律摘要（S3-09 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B4 | 负结论带探针 | absence_probe 三源逐一留证（§三/附录 B） |
| B5 | 列表 sorted() | 词族命中/mock 值/ctx_refs sorted |
| B7 | 数字-出处核对 | 0/15/5600/3,358,401/46,835 均对产物键 |
| B10 | ui_demo_fallback 披露 | mock 6 竞赛 participants 与饼图 15 披露 |
| 基期三键 | base_years_used/missing/note | 产物全键（全空登记） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有竞赛主档吗？ | 无 | competition 词族命中全语义错位（产业链竞争力/企业评分/科研问题竞争排名） |
| 三源有报名流水吗？ | 无 | enroll 词族命中全污染（临床试验入组/注册资本/课题条目） |
| UI 报名动作有落库链路吗？ | 无 | handleRegister 仅前端 message.success，无接口调用 |

## 摘要

「数据科学赛道报名数」的挂载语义由两个 UI 元素合成：竞赛卡「立即报名」按钮触发的确认弹窗（`TechCompetition.jsx:163-168`，onOk 仅 `message.success('报名成功！请查看报名确认邮件。')` 纯前端提示）与排行榜 tab 赛道分布饼图的数据科学扇区（`:174`，mock 15 场）。指标回答「数据科学类赛事报了多少人/队」。数据侧判定：**完全不支持**——需要竞赛主档（含赛道字段）+ 报名事件流水双前提面：竞赛主档三源 0 表（competition 词族命中 `chain_competitiveness` 产业链竞争力、jiuxin `ads_research_problem_competition_rank` 46,835 行科研问题区域竞争排名，全语义错位）；报名流水三源 0 表（enroll 词族命中 gkx `enrollment_count` 临床试验入组、`registered_capital` 注册资本、jiuxin `ads_institution_topic_entry` 335.8 万行 OpenAlex 课题条目）。UI 报名动作本身无后端链路。与 THINK_014 同宿主缺，报名子面独立留证。

- 需求判定：指标名三份说明书未出现；上位叶 SRS 序号 588（竞赛发布与组织）/584（竞赛项目数据归集与分类）覆盖。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技服务全景 → 科技竞赛 → 竞赛卡瀑布流（三 tab：正在进行/即将开始/已结束）+ 排行榜 tab。竞赛卡（`TechCompetition.jsx:60-94`）带报名按钮（`:86-91`，completed 态禁用），点击触发 `handleRegister` 的 Modal.confirm（`:163-168`）；排行榜 tab 右栏「竞赛类型分布」饼图 `typeDistribution`（`:173-180`），首扇区数据科学 value=15。mock `competitions` 6 条（`mockData.js:265-270`），comp1「2026国际数据科学挑战赛」type=数据科学、participants=5600、teams=1200。

### 1.2 为什么需要本指标

赛道报名数是竞赛运营的**漏斗读数**：按赛道（数据科学/AI/创新创业/量子计算/生物医药）切分报名量，回答「哪类赛事最吸引参赛者」。管理者用它评估赛道热度与资源投放；与参赛人数（THINK_004）、奖金总额（THINK_005）构成竞赛运营三角。数据科学赛道是 SRS 序号 584「搭建数据科学竞赛社区」的核心赛道，故单列。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**（挂载点为清单实查定位，l3 名「确认报名＞数据科学」即弹窗动作×赛道扇区合成。）

### 1.4 类似指标权威方法可行性分析概要

权威侧无国标报名口径；赛事运营通用实践：报名事件表（用户 ID+竞赛 ID+赛道/队伍+时间戳）按赛道分组计数， Kaggle/天池等数据科学竞赛平台公开「参赛队伍数」（teams 口径）。方法族：①报名事件按赛道分组 COUNT（平台自建）；②赛事主档 participants/teams 快照列直读（爬取/对接）；③第三方赛事平台 API。报名属平台自设运营指标。

### 1.5 引用来源

1. Kaggle Competitions（数据科学竞赛参赛队伍数公开口径）. https://www.kaggle.com/competitions
2. 阿里云天池大赛（参赛队伍/人数统计口径）. https://tianchi.aliyun.com/competition
3. 中国「互联网+」大学生创新创业大赛（报名统计口径，教育部赛事) . https://cy.ncss.cn

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：数据科学类赛事的报名人数/队数（按竞赛主档 type=数据科学筛选，累计或按届）。
- **操作化定义（本件未实现）**：赛道报名数 = COUNT(报名事件 WHERE 竞赛.type='数据科学')（人次）或 COUNT(DISTINCT 队伍)（队次）。
- **降档触发器**：已处最低档。
- **升档触发器**：竞赛主档接入（SRS 序号 584）+ 报名事件表落库（序号 588）→ 完全转换支持；赛事平台 API 直连（报名数回传）→ 完全直接支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：科技竞赛·报名动作×数据科学赛道。
- 相近叶：参与人数（THINK_004，participants 快照口径同缺）；竞赛排行榜 TOP10（THINK_014，同宿主缺）；CONTEST_001 竞赛类型分布（路γ，同饼图）。
- 同宿主缺：竞赛主档 0 表导致整页竞赛族（THINK_003/004/005/013/014、CONTEST_001）全零承载，本件为报名子面独立留证。

## 二、计算过程

从缺。本指标需「竞赛主档（含赛道/类型字段）+ 报名事件流水（用户×竞赛×时间戳）」双前提面，三源探针（附录 B）证明双面零承载：竞赛主档侧——dev competition 词族命中 7 张全语义错位（`chain_competitiveness` 产业链竞争力评分、`enterprise_ranking`/`enterprise_score` 企业评分排名、`policy_support_rank` 政策排名、`cms_pano_competitive_position` 竞争定位文案）；jiuxin 命中 4 张（`ads_research_problem_competition_rank` 46,835 行科研问题区域竞争排名，competition_scope=CITY 22,445/PROVINCE 16,725/COUNTRY 7,370/DISTRICT 295；另 3 张人才评分 demo 表）——无一张科技赛事主档。报名流水侧——enroll 词族 dev 表名 0 命中；gkx 列名命中全污染（`dwd_clinical_trial.enrollment_count` 临床试验入组人数、`registered_capital*` 注册资本）；jiuxin 唯一表名命中 `ads_institution_topic_entry`（3,358,401 行）为 OpenAlex 课题条目快照（列含 openalex_topic_id/observed_paper_count），entry=条目非报名。UI 报名动作本身纯前端（onOk 仅 message.success，无接口无落库）。双面皆缺禁伪公式。mock 6 条竞赛与饼图 15 为演示量级参照（ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 竞赛主档（含赛道字段） | dev/gkx/jiuxin | **无表**（competition 词族全语义错位） |
| 报名事件流水 | dev/gkx/jiuxin | **无表**（enroll 词族全污染） |
| 赛道分布快照（typeDistribution 代理） | UI mock | 演示态（15 场静态值） |
| 科研问题竞争排名 | jiuxin | 语义错位（46,835 行，非科技赛事） |
| 课题条目面 | jiuxin | 语义错位（335.8 万行，entry=条目） |

### 3.2 现场复核清单

UI 链实读：`TechCompetition.jsx:163-168` Modal.confirm onOk=message.success；`:86-91` 报名按钮；`:174` 饼图扇区；mock 源 `mockData.js:265-270`（6 竞赛）+ `:271-283`（排行榜）。三源实连复核（本件脚本断言）：dev 542 表 enroll 表名 `[]`；gkx 280 表 `[]`；jiuxin 218 表 `['ads_institution_topic_entry']` 且 `openalex_topic_id` 列在册（断言通过）；gkx 三表 enroll 列污染断言逐一通过（enrollment_count/registered_capital*）；jiuxin 课题条目 3,358,401 行断言通过；competition 词族 dev 7 张/jiuxin 4 张语义错位清单在册。

## 四、数据缺失情况

### 4.1 缺口清单

①竞赛主档无表（三源，赛事名称/领域/主办方/影响力字段全缺）；②报名事件流水无表（三源）；③UI 报名动作无后端链路（连演示落库都没有）；④赛道口径未定（type 字段枚举：数据科学/AI/创新创业/量子计算/生物医药/机器人，与 SRS 序号 584「标准化分类」待对齐）；⑤人次 vs 队次口径未定。

### 4.2 修复建议与影响面

短期：竞赛主档接入（SRS 序号 584 赛事归集：全球科技赛事名称/领域/主办方/影响力）+ 报名接口落库（序号 588 全流程组织支持）→ 本件 + THINK_003/004/005/014 + CONTEST_001 整族升完全转换支持。中期：赛事平台 API 对接（Kaggle/天池类公开报名数）→ 热门赛事直连。远期：竞赛社区全链路（序号 585 参赛社区内容结构化整合：参赛者/参与记录/论坛/排行榜关联归档）。推荐：主档+报名接口随竞赛模块后端一并立项（一源解全族）。

### 4.3 影响面

科技竞赛页报名按钮为纯前端演示；整页竞赛域（KPI 四卡/竞赛卡/排行榜/类型分布/社区讨论）全 mock 无后端接口。

## 参考文献

1. Kaggle Competitions（数据科学竞赛参赛队伍数公开口径）. https://www.kaggle.com/competitions
2. 阿里云天池大赛（参赛队伍/人数统计口径）. https://tianchi.aliyun.com/competition
3. 中国「互联网+」大学生创新创业大赛（报名统计口径）. https://cy.ncss.cn

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 数据科学赛道|赛道报名|报名数` 三份说明书 + 主需求 → 指标名 0 命中。
- 清单挂载：`_phase3_screen_v3.json` kept_items mount=`pages/tech-service/TechCompetition.jsx:174`，l3=确认报名＞数据科学（实查确认 :163-168 弹窗 + :174 扇区合成语义）。
- SRS 上位叶：科技竞赛.md 序号 588「竞赛发布与组织：以专题形式发布竞赛信息，提供竞赛活动全流程的组织支持」；序号 584「对全球科技赛事名称、领域、主办方、影响力等信息进行标准化分类整理」。
- mock 参照（`mockData.js:265-270`）：comp1 数据科学赛 participants=5600 teams=1200；typeDistribution（`:174`）数据科学 15。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_THINK_013_out.json`）

facts（ui_mount/ui_track_context/ui_mock_note/dev_enroll_word_tables=[]/dev_enroll_note/gkx_enroll_word_tables=[]/gkx_enroll_semantic_note 三污染/jiuxin_enroll_tables=[ads_institution_topic_entry]/jiuxin_enroll_semantic_note/competition_host_note 主档 0 表/register_action_note 无后端/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）；derived[0]（datascience_track_registrations_negative 负结论 null 登记）；absence_probe（三件，双面零承载断言）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2021-2026 / note）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：报名事件按赛道分组 COUNT（平台自建）→ 赛事主档 participants/teams 快照（对接/爬取）→ 第三方赛事 API（Kaggle/天池公开口径）。数据矩阵：竞赛主档三源 0 表；报名流水三源 0 表；jiuxin 科研问题竞争排名（46,835 行）与课题条目（335.8 万行）语义双错位。分期方案：一期主档+报名接口（完全转换支持）、二期赛事平台 API、三期竞赛社区全链路（序号 585）。风险登记：赛道枚举口径待与 SRS 584 对齐、人次/队次双口径需裁定、UI 无后端链路需前后端同步立项。总判：完全不支持（双面皆缺，升档=竞赛模块后端整体立项）。

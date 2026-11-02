# M_SCIUI_P10_004 互动统计（M_SS_INTER_*）—— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：软科学成果展示 New·成果互动与传播中心·互动统计（`BottomTabs.jsx:866`）｜ **UI 挂载**：科技信息展示系统 → 创新载体孵化载体 New（软科学新页）→ 评论交流 tab「互动统计与传播分析」四格统计+六月趋势
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（M_SS_INTER_* 为 UI 自设编号族；互动行为四分法口径无权威定义）｜ **口径归属**：UI 挂载件（SRS 无同名指标；上位叶=软科学成果展示·序号 475「互动统计与传播分析」）
> **复现脚本**：`code/M_SCIUI_P10_004.py`（薄壳，指向共享探针 `code/_shared_s308_laneb_probe.py`）｜ **产物**：`code/M_SCIUI_P10_004_out.json`
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（三源无互动事件表）；直接数据=无；依赖结构=无（interact 词族命中全为股东/报表分享/期刊占比语义污染）；依赖数据=无（用户行为流水零承载，宿主课题库亦零承载）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全不支持。**（用户互动事件流水三源零承载，词族命中全为解析歧义污染）。

### 批次通用纪律摘要（S3-08 批共用）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B4 | 负结论带探针 | absence_probe 三源逐一留证 |
| B5 | 列表 sorted() | 污染清单/mock 序列 sorted 登记 |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳脚本重跑产出 |
| B9 | 单位/日期陷阱 | mock 趋势仅 2026-03~08 六月段 |
| B10 | ui_demo_fallback 披露 | mock 四格+六月序列全披露 |
| 基期三键 | base_years_used/missing/note | 产物全键（全空登记） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有互动事件流水吗？ | 无 | interact 词族表名+列名双扫：命中全为股东（shareholder）/BI 报表分享/期刊占比语义 |
| 宿主对象（软科学课题）存在吗？ | 无 | dev 课题表 0 行空壳；jiuxin project 为 OpenAlex 英文资助项目 |
| 有代理路径吗？ | 无 | dev app_social_details（旧页社交表）为成就页点赞收藏且 0 行；jiuxin 协作列为机构语义非用户行为 |

## 摘要

「互动统计与传播分析」是软科学新页评论交流 tab 的传播分析卡（`BottomTabs.jsx:866`）：四格统计绑定 M_SS_INTER_* 编号族（累计评论/累计点赞/累计分享/知识库条目），配评论/点赞双线六月趋势图。数据侧判定：**完全不支持**——互动统计的原料是「用户×成果×行为类型×时间戳」平台行为日志，三源逐一探查零承载：dev interact 词族命中为 `enterprise_shareholder`（股东，share 解析歧义）与 `jimu_report_share`（BI 报表分享配置）等污染；gkx 同族污染（股东/期刊占比）；jiuxin 218 表（SHOW TABLES 实数）0 张互动事件表（列命中 cooperation/collaborator 全为机构合作语义）。更深一层：软科学课题库本身三源零承载（宿主不存在），互动面更无从挂起。mock 侧评论/点赞计数为前端会话运行时态（useState 种子+用户操作），六月趋势为固定演示序列。

- 需求判定：**UI 挂载件**（SRS 无同名；上位叶=序号 475 互动统计与传播分析，另有 472/473/474 同域邻叶）。
- 复现状态：薄壳已跑通；负结论落产物 `derived[0]`。
- 档位结论：**完全不支持**（行为流水+宿主对象双零）。
- 关键事实：M_SS_INTER_* 四编号全部指向不存在的 `ads_soft_science_interact` mock 源表（MetricInfo 自述）。
- 升档路径：平台互动事件表入湖（cms/app 运营域）→ 课题互动面可挂。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 软科学成果展示（New 页族：`achievement-preview-new/soft-science-new/`）→ 评论交流与专家答疑 tab「互动统计与传播分析」卡（`BottomTabs.jsx:866` SectionCard）。卡内：①四格统计 `statItems`（`:753-758`）：累计评论（`comments.length`，M_SS_INTER_COMMENT）/累计点赞（`totalLikes` 求和，M_SS_INTER_LIKE）/累计分享（`INTERACTION_TREND.shares` 求和，M_SS_INTER_SHARE）/知识库条目（`kbEntries.length`，M_SS_INTER_KB），每格带 MetricInfo+MockBadge；②趋势折线（`:681-682`）评论/点赞双系列（`mockData.js:214-220` 六月：评论 12/19/15/24/31/18、点赞 45/62/58/80/96/54、分享 8/14/11/19/27/16）。

### 1.2 为什么需要本指标

互动统计是成果传播效果的行为学读数：评论/点赞/分享量反映课题成果的社会触达与参与深度（SRS 475 需规原文「衡量推广覆盖面、调整宣传策略」语义）；知识库归档量反映成果沉淀复用。

### 1.3 需求文档是否给出定义方法

**三份说明书未给出该指标的计算方法。** M_SS_INTER_* 编号族未在需求文档出现（UI MetricInfo 自设）；上位叶 475 只给功能行为（自动统计互动行为及传播效果、生成影响力报告），无行为四分法口径、无去重规则（同一用户多次点赞计几次）、无时间窗（累计 vs 月度）。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①Altmetric/ PlumX 替代计量学（在线关注计数：news/policy/blog/social 分渠道）——学术成果传播监测的事实标准，但监测对象是公开学术成果的社会传播，非平台内互动；②CNKI 知网节「被引/下载」统计（使用行为面）；③CNKI 学术互动/知网社区评论（平台内互动先例）。三族均需行为日志流水——本库三源零承载，权威方法不可落地。完整版见附录 C。

### 1.5 引用来源

1. Altmetric. How Altmetric tracks attention（替代计量口径）. https://www.altmetric.com/about-altmetric/what-we-do/
2. Plum Analytics. PlumX Metrics（使用/捕获/提及三族）. https://plumanalytics.com/learn/about-metrics/
3. 中国知网. 知网节统计指标（下载/被引口径）. https://www.cnki.net/

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：软科学课题成果页的用户互动行为四分法计数（评论/点赞/分享/归档），累计+月度双口径。
- **操作化定义（未实现）**：累计评论 = COUNT(评论事件)；月度点赞 = COUNT(点赞事件) GROUP BY 月；分享去重按（用户,成果）对；知识库条目 = 归档记录数。
- **降档触发器**：已处最低档。
- **升档触发器**：平台互动事件表入湖（用户 ID+成果 ID+行为类型+时间戳四列即可）→ 完全转换支持；软科学课题库同步接入（宿主对象）→ 挂载闭环。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/软科学成果展示.md` |
| 所属四级功能 | 1.1.1.1.4.6 科技成果展示（域）|
| 所属页面 | 软科学成果展示 New（创新载体孵化载体 New 页族）|
| 本件叶 | 成果互动与传播中心·互动统计四格（UI 挂载件；上位叶=序号 475）|
| 相近叶 | 序号 472 评论交流与专家答疑（同 tab 宿主）/473 关注收藏与动态推送/474 多渠道社交分享（分享格的上位）；P10_014 单位贡献度（同 BottomTabs 邻卡）|
| UI 容器 | `BottomTabs.jsx:858-877` SectionCard |

## 二、计算过程

从缺。本指标需「用户×成果×行为类型×时间戳」互动事件流水，三源探针（附录 B）证明零承载：dev 542 表 interact/comment/like/share/review 词族双扫命中全为语义污染——`enterprise_shareholder`/`dwd_forg_shareholder_info`/`dwd_org_shareholder_info`（股东，share 解析歧义）、`jimu_report_share`/`onl_drag_share`（BI 报表分享配置）；gkx 280 表同族污染（股东/`dwd_market` 市场/期刊 share 占比列）；jiuxin 218 表（SHOW TABLES 实数）表名 0 命中，列命中（cooperation/collaborator，60+ 表）全为机构合作语义。且宿主对象（软科学课题库）三源零承载（`fund_project`/`enterprise_fund_project` 0 行空壳、jiuxin `ads_project_profile` 为 OpenAlex 英文资助项目非深圳软科学课题）——流水无处可挂。禁伪公式；mock 四格与六月序列为演示参照（ui_demo_fallback 披露，其中评论/点赞为前端会话运行时态）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 互动事件流水（用户×成果×行为×时间） | dev/gkx/jiuxin | **无表**（词族命中全污染） |
| 宿主对象（软科学课题库） | dev/gkx/jiuxin | **零承载**（dev 空壳 0 行；jiuxin 为英文项目库） |
| 行为类型字典（四分法） | — | 无定义（UI 自设） |
| 旧页社交面（app_social_details） | dev `gkxlumenx_app` | 0 行空壳且语义为成就页点赞收藏 |

### 3.2 现场复核清单

UI 链实读：`BottomTabs.jsx:866` 卡标题+MetricInfo（源表自述 ads_soft_science_interact（Mock））、`:753-758` statItems 四编号、`:681-682` 趋势双系列、`mockData.js:214-220` INTERACTION_TREND。三源实连复核（共享探针 `_shared_s308_laneb_probe.py`）：词族命中清单见 absence_probe 三条；污染逐表定性见 facts 语义注记。

## 四、数据缺失情况

### 4.1 缺口清单

①互动事件流水无表（主因）；②宿主课题库零承载（挂载无处）；③行为四分法口径无定义（累计/月度、去重规则未定）；④知识库归档面（KB_STORAGE_KEY 为前端 localStorage 键，非库表）。

### 4.2 修复建议与影响面

短期：无库内路径；卡片维持 mock 并标注演示态。中期：软科学课题库接入（宿主）+ 平台互动事件表入湖（用户/成果/行为/时间四列）→ 完全转换支持。远期：替代计量扩展（外部分享回流监测）→ 传播效果面。同域联动：序号 472/473/474 邻叶同根因（同缺行为流水），一次接入四叶受益。

### 4.3 影响面

软科学新页评论交流 tab 的传播分析卡四格+趋势全 mock；「影响力数据报告」（SRS 475 承诺）整链无数据支撑。

## 参考文献

1. Altmetric. What we do / attention metrics. https://www.altmetric.com/about-altmetric/what-we-do/
2. Plum Analytics. PlumX Metrics. https://plumanalytics.com/learn/about-metrics/
3. 中国知网. 知网节统计指标. https://www.cnki.net/

# 附件

## 附录 A 原始需求原文摘录

- SRS《软科学成果展示.md》序号 475（excel_row 478，path=…/成果互动与传播中心/互动统计与传播分析）：「自动统计用户互动行为及成果传播效果，生成影响力数据报告，为管理部门和课题负责人衡量推广覆盖面、调整宣传策略和促进社会参与提供科学参考。」
- 检索记录：`rg M_SS_INTER|互动统计` 三份说明书 → 编号族 0 命中；功能叶 475 命中（上位覆盖）。
- 实查定位链：清单挂点 BottomTabs.jsx:866 直核（SectionCard+MetricInfo）→ :753-758 statItems → mockData.js:214-220。
- mock 参照：六月序列 评论 [12,19,15,24,31,18]/点赞 [45,62,58,80,96,54]/分享 [8,14,11,19,27,16]（2026-03~08）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_004_out.json`）

metric_id/batch=S3-08/ui_evidence（3 条组件行号）/requirement_trace（named_in_srs=false + SRS 锚 475）/facts（ui_mount/ui_stat_items/ui_trend_chart/ui_mock_note/dev_interact_word_tables/dev_interact_semantic_note/gkx_interact_word_tables/gkx_interact_semantic_note/jiuxin_interact_tables/jiuxin_interact_note/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）/derived[0]（负结论 null）/absence_probe（三源三条，污染清单逐一定性）/support_judgment=完全不支持/notes（5 条）/base_years 三键（全空）/ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：替代计量（Altmetric/PlumX，公开传播监测）→ CNKI 使用统计（下载/被引）→ 平台内互动计数（本件口径，四分法）。数据矩阵：行为流水三源 0；宿主课题库 0；行为字典无。分期方案：一期课题库接入（宿主）、二期互动事件表（四列即可）、三期外部传播回流。风险登记：share 解析歧义污染词族（股东/报表/占比三种错义）、前端运行时态冒充统计数据、localStorage 键误当库表。总判：完全不支持（双零：流水+宿主；升档路径两步）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_004.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneb_probe.py` | 快照词族面零漂移 |
| 判档一致 | MD 文首「完全不支持」= out.json `support_judgment` | 一致 |
| 负证据 | absence_probe 三条（污染逐表定性） | 逐一可复验 |
| mock 披露 | 四格+六月序列仅 §1.1 语义描述 | 不参与支持度结论 |

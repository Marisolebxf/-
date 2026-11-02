# 内容月浏览量（M_SCIUI_THINK_010）

> **类型**：无业务逻辑数值类｜ **域**：科技服务全景·智库服务·月浏览量（TechCommunication.jsx:142，统计概览四宫格）｜ **UI 挂载**：科技信息展示系统 → 科技服务全景 → 科技传播 → 统计概览「月浏览量」卡（`TechCommunication.jsx:142`）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（指标名三源 0 命中；月度浏览口径无定义）｜ **口径归属**：UI 挂载件（`_phase3_screen_v3.json` kept_items），SRS 无同名指标
> **复现脚本**：`code/M_SCIUI_THINK_010.py`（薄壳，读共享探针快照 `_snapshots/_shared_s309_think_beta_probe{1,3,4,5}_out.json`）｜ **产物**：`code/M_SCIUI_THINK_010_out.json`
> **四判定摘要**：直接结构 = 否（三源无浏览事件流水）；直接数据 = 否；依赖结构 = 部分（dev 有月度浏览汇总结构 `chain_news_stat.stat_month+total_views` 与浏览快照列 `chain_news.views`/`policy_latest_news.view_count`/`app_article.visit`、gkx 有 `dwd_information.click_number`，全部 0 行/全 NULL）；依赖数据 = 无（唯一有数的 `jimu_report.view_count` 66 行 SUM=749,666 为 BI 报表语义错位）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 降档根因是「结构在、数据零承载」：dev 侧存在月度浏览汇总的**同构结构**（`gkxlumenx_ads.chain_news_stat`：`stat_month`+`total_views`+`news_count`，6 列月度新闻浏览汇总骨架）与三处浏览快照列结构（`chain_news.views`/`policy_latest_news.view_count`/`app_article.visit`），gkx 侧有供应商资讯点击列（`dwd_information.click_number`）——但上述五面承载行**全部 0 行或全 NULL**（32 行资讯 click_number 全空）。三源无任何「用户×内容×时间戳」浏览事件流水。唯一有数的浏览计数面 `jimu_report.view_count`（66 行，SUM=749,666）是 BI 报表工具的报表浏览计数，与科技传播内容语义错位，仅可内验。结构骨架可复用、数据须等新闻/资讯数据入湖，判部分支持。

### 批次通用纪律摘要（S3-09 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无比率派生；代理求和读数登记分子口径 |
| B4 | 负结论带探针 | absence_probe 三源逐一留证（§三/附录 B） |
| B5 | 确定性 | 词族命中清单 sorted（共享脚本） |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳脚本重跑产出，手改禁令 |
| B8 | 回执不复收 | 共享快照可重跑复验 |
| B9 | 单位/日期陷阱 | UI 卡显示「万」单位（125.8万）与原始值 1,258,000 双登记；stat_month 为月度键 |
| B10 | 口径裁定保守交付 | 双口径并列（月度汇总面 vs 事件流聚合），降/升档触发器写死（§1.6） |
| B11 | 多本账互推 | 与共享快照 5 份零漂移（断言锁定） |
| F 系 | 历史写法错误 | 无域级兜底（F1）、mock 值披露不当数据（F2）、文献带 URL（F9） |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 判定轴存在吗？ | 部分 | chain_news_stat 月度汇总结构在（dev）；浏览事件流水三源 0 承载 |
| 代理轴可信吗？ | 部分 | jimu_report.view_count 66 行可算 SUM，但 BI 报表语义错位不可对外 |
| 子盘能撑多少？ | 结构面可撑 | 「月键+浏览数+求和」计算链结构可复用；数据面 0，月度序列不可算 |

## 摘要

「内容月浏览量」是科技传播页统计概览四宫格的第二卡（`TechCommunication.jsx:142`）：取 `communicationStats.monthlyViews`（mock 1,258,000）除以 10,000 保留一位小数显示「125.8万」。需求侧 SRS 未列同名指标，上位叶是序号 596「传播形式分类展示」（十类传播内容的列表化呈现与详情查看）。三源探针（表名+列名词族双扫：dev 542 表 / gkx 280 表 / jiuxin 218 表现场实数）证实：浏览事件流水零承载；dev 有月度浏览汇总同构结构 `chain_news_stat`（`stat_month`+`total_views`）与三处浏览快照列，gkx 有 `dwd_information.click_number`（32 行），但承载行全 0/全 NULL；唯一有数的 `jimu_report.view_count`（66 行 SUM=749,666）为 BI 报表浏览，语义错位。判**部分支持**：结构骨架在、数据零承载，月度序列需新闻/资讯数据入湖（并需 ≥2 个月份快照）才可算。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**UI 挂载件**（SRS 无同名；上位功能序号 596 覆盖）。
- 复现状态：薄壳已跑通；读数落 5 份共享快照 + 本件产物。
- 档位结论：**部分支持**（月度汇总结构在、承载 0 行；事件流水三源无）。
- 关键事实：dev 浏览承载面 4 处全 0 行；gkx click_number 32 行全 NULL；jimu_report 66 行 749,666 语义错位。
- 升档路径：新闻/资讯数据入湖灌满 `chain_news_stat`（月度面）→ 完全转换支持；平台浏览事件流接入 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技服务全景/科技传播/**统计概览**（SRS 1.1.1.1.4.7 域内交互面）。科技传播页（`TechCommunication.jsx`）顶部是统计概览四宫格（`:139-145` categoryStats 定义、`:158-162` Statistic 卡渲染）：总内容数（`totalContents`=3,567，THINK_006 域）、**月浏览量**（本件，`monthlyViews/10000` →「万」）、活跃用户（`activeUsers`=45,600）、新增内容（`newContents`=234）。其下是九宫分类导航（communicationCategories）+ 内容卡瀑布流（卡片 meta 带 `views`/`likes`，`TechCommunication.jsx:80-81`）+ 时间轴视图。月浏览量是四宫格中唯一的**流量读数**，回答「这些内容有没有人看」的当月热度。

mock 数据源 `mockData.js:335-340` 的 `communicationStats` 是四个静态常量；内容卡的单条 `views`/`likes` 为 `communicationContents`（8 条，`mockData.js:311-319`）逐条演示值。

### 1.2 为什么需要本指标

月浏览量是科技传播内容的**月度流量读数**：管理者用它判断十类传播形态（展览/讲坛/院士风采/学术期刊/学术会议/科技图书/信息素养讲堂/科学文化交流/新媒体）的整体触达热度与环比走势，与「总内容数」（供给侧）、「新增内容」（更新节奏）、「活跃用户」（受众面）构成运营四象限。它区别于单条内容的累计浏览（THINK_011）：月浏览量是**时间切片聚合**，回答的是「这个月看了多少次」，需要按月切分的事件或月度快照，而不是内容主档上的累计数。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「月浏览量」指标名在三份需求说明书中未出现（检索记录见附录 A.2）；SRS《科技传播.md》（序号 593-601）给出的是内容形态分类（十类）、归档/清洗/聚合的数据治理链与分类展示/统一检索/多端分发功能，没有任何浏览量统计的公式（月度窗口定义、去重口径、PV/UV 区分均缺失）。

### 1.4 类似指标权威方法可行性分析概要

网站/新媒体流量统计的权威基准是 **GB/T 31524-2015《电子网站浏览量统计》系列及 CNNIC《网站流量统计指南》**（R1）：PV（Page View，页面浏览量）按「页面被加载次数」计数、UV 按访客去重，月度 PV = 自然月内 PV 事件求和。中国科协《科学传播发展报告》（R2）对科普新媒体平台采用「月度阅读量/播放量」口径。方法族对照：

| 方法族 | 计数轴 | 数据要求 | 与本库匹配 |
|---|---|---|---|
| PV 事件流（GB/T 31524） | 用户×页面×时间戳逐事件 | 浏览事件日志表 | **无（三源零承载）** |
| 月度快照汇总（运营月报通用） | stat_month+total_views 月表 | 月度浏览汇总表 | **结构有**（chain_news_stat）**数据 0 行** |
| 内容累计快照列（CMS 通用） | 主档 views 冗余列 | 内容表带浏览列 | **结构有**（3 处列）**数据 0 行/NULL** |

结论：权威口径明确（月度 PV 求和），缺的是挂数的浏览行为数据；结构骨架三源环境已具备可复用形态。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-service/TechCommunication.jsx:142` — `{ label: '月浏览量', value: (communicationStats.monthlyViews / 10000).toFixed(1) + '万' }`；`:80-81` 内容卡 meta `views`/`likes` 展示。
- mock：`tech-service/mockData.js:335-340` communicationStats（monthlyViews=1258000）；`:311-319` communicationContents 8 条（views 3,450-15,680）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技服务全景/科技传播.md`（序号 593-601，excel_rows 596-604）。
- 外部：GB/T 31524-2015（R1）；中国科协科学传播蓝皮书（R2）。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露代理敏感性）**：

- 口径 A（UI 现行为，mock 驱动）：月浏览量 = `communicationStats.monthlyViews`（静态常量，展示层 ÷10,000 转「万」）；
- **口径 B（建议正式口径）**：月浏览量ₘ = Σ PV 事件（自然月 m 内全部传播内容页浏览），PV 按 GB/T 31524 页面加载计数，不做 UV 去重（若需 UV 口径须事件带访客标识）；
- 口径 C（退而求其次的快照差分）：月浏览量ₘ = Σ(内容 i 的累计浏览快照在月末值 − 上月末值)，依赖每月留存的累计快照。

**降档/升档触发器（B10 模板）**：若新闻/资讯数据入湖灌满 `chain_news_stat`（≥2 个月份行）→ 升「完全转换支持」（月度直查）；若平台浏览事件流接入（用户×内容×时间戳）→ 升「完全直接支持」；若长期仅有单月快照（无历史月）→ 月度序列不可比，维持部分支持且只能出单月读数。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `srs/02-科技信息展示系统/科技服务全景/科技传播.md` |
| 所属四级功能 | 1.1.1.1.4.7 科技服务全景（域）|
| 所属页面 | 科技传播 |
| 所属面板 | 统计概览四宫格 |
| 本件叶 | 月浏览量（UI 挂载件，SRS 无同名叶；上位叶=序号 596 传播形式分类展示） |
| 相邻叶 | 总内容数（THINK_006 域）/活跃用户/新增内容（同四宫格）；内容累计浏览量（THINK_011）；内容点赞数（THINK_012） |
| UI 容器 | `categoryStats` 四卡 Row（`TechCommunication.jsx:155-164`） |

## 二、计算过程

### 2.1 方法选择（文献依据）

月浏览量本身是简单月度求和（无建模），方法选择落在**计数原料的裁定**：正式口径采用 GB/T 31524 的 PV 月度求和（R1）；本库环境实测因无事件流，退到「结构骨架验证」路径——dev `chain_news_stat` 就是口径 B/C 的月度汇总同构表（`stat_month`+`total_views`），证明「月键+浏览数」的承载形态在三源环境已预置；数据面用 `jimu_report.view_count` 求和代理证明「浏览计数列+求和」计算链可跑通。整条链（装载→按月/全表聚合→求和）结构与正式口径一致，只是原料未灌。

### 2.2 探针读数（承载面开箱）

共享探针三期（`_shared_s309_think_beta_probe3.py`）逐一开箱承载候选：

- `gkxlumenx_ads.chain_news_stat`：6 列（`chain_id/chain_name/growth_rate/hot_count/news_count/stat_month/total_views`），**0 行**（产物键 `chain_news_stat_rows`）——月度汇总结构在、数据无；
- `gkxlumenx_dwd.chain_news`：16 列含 `views`+`data_year`/`data_month`/`publish_time`，**0 行**；
- `gkxlumenx_dwd.policy_latest_news`：20 列含 `view_count`+`news_date`/`publish_time`，**0 行**；
- `gkxlumenx_app.app_article`：15 列含 `visit`，**0 行**；
- `gkxlumenx_bi.jimu_report`：66 行，`view_count` 全有值（产物键 `jimu_report_view_count_stat`：non_null=66、SUM=749,666、MAX=54,003）——BI 报表浏览，语义错位；
- gkx `dwd_information`：32 行（五期 `gkx_information_rows`），`click_number` **32 行全 NULL**（`gkx_information_click_stat.non_null_rows=0`）；年份分布 2019:10/2020:3/2021:3/2022:6/2023:7/2024:2/2025:1（`gkx_information_year_counts`）——供应商资讯快照，点击数从未回填。

### 2.3 同基核对

本件无比率派生。代理读数 `jimu_report_view_sum_proxy=749,666` 为全表求和（66 行同表同源，分子口径登记于产物 `derived[1].numerator`）；mock 1,258,000 作 ui_demo_fallback 披露（`ui_mock_note`），不混入真读数。

### 2.4 稳健性与口径敏感性

口径 B（事件流求和）与口径 C（快照差分）在数据灌满后会得到不同读数（快照差分受跨月回填/去重影响），两口径并列不改判档；「月」的窗口（自然月 vs 滚动 30 天）未定，属口径裁定缺口非数据缺口；jiuxin 列名扫描 42 处 view 命中全为 `review_status`/`reviewer`（人工评审）子串污染，已逐一排除（一期快照 `jiuxin_view_like_columns`），无漏检风险。

### 2.5 基期年份可用性

`base_years_used`=[]、`base_years_missing`=2021-2026、note：无任何真实月度/年度浏览数据（承载行全 0/NULL；gkx 资讯 2019-2025 但 click_number 全 NULL）；基期无从谈起，全空登记（产物三键齐备）。

### 2.6 需求符合性预评

统计概览卡不可切真数（承载 0 行）；mock 125.8 万演示态维持。若新闻数据入湖，`chain_news_stat` 直查即可出数，UI 无需改动（卡片只吃数值）。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_THINK_010.py`（薄壳：快照一致性断言 + 承载面断言 + 判档落盘）；共享探针 `code/_shared_s309_think_beta_probe{1,3,4,5}.py`；运行 `python3 code/M_SCIUI_THINK_010.py`。
- 产物：`code/M_SCIUI_THINK_010_out.json` + 快照 5 份。正文数字对应键：`chain_news_stat_rows=0`（§2.2）、`jimu_report_view_count_stat.sum=749666`（§2.2）、`gkx_information_click_stat.non_null_rows=0`（§2.2）、`derived[1].value=749666`（§2.3）。
- 结果解读：月浏览量计算链（月键装载→聚合→求和→万单位转换）结构验证通过；数据面三源零承载，月度序列不可算。
- 对照需求功能要求的评审：序号 596 分类展示的流量统计面——结构可承载、数据待入湖。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | dev 月度汇总面 | `facts.dev_monthly_structure` | chain_news_stat 6 列 0 行 |
| 装载 | dev 浏览快照列 | `facts.dev_snapshot_columns` | 3 表全 0 行 |
| 装载 | gkx 资讯点击列 | `gkx_information_click_stat` | 32 行全 NULL |
| 代理 | BI 报表浏览求和 | `derived[1].value` | 749,666（66 行） |
| absence | 三源事件流探针 | `absence_probe` 三条 | dev 0 / gkx 0 / jiuxin 0 |
| 基期 | 年份三键 | `base_years_*` | used=[] / missing=2021-2026 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 浏览事件流水 | dev / gkx / jiuxin | — | — | **不存在** | **缺（事件面）** |
| D2 | 月度浏览汇总面 | dev | `chain_news_stat.stat_month+total_views` | **0 行** | 结构在数据无 | 缺（数据面） |
| D3 | 内容浏览快照列 | dev | `chain_news.views` 等 3 表 | **0 行** | 结构在数据无 | 缺（数据面） |
| D4 | 资讯点击列 | gkx | `dwd_information.click_number` | 32 行全 NULL | 结构在数据无 | 缺（数据面） |
| D5 | BI 报表浏览（代理） | dev | `jimu_report.view_count` | 66 行 SUM=749,666 | 直查 | 有但语义错位 |

`support_judgment="部分支持"`，与文首一致（闸 6）。

### 3.2 D1 事件流缺失的三源探针（absence_probe 全记录）

否定性证据三件套：**查了什么**——三源表名+列名双扫描（词族 view/browse/pv/visit/read_cnt/click，探针 `_shared_s309_think_beta_probe.py` 一期，快照 `_snapshots/_shared_s309_think_beta_probe_out.json`）；**条件**——dev 542 表（17 个 gkxlumenx_* schema 全量，表名+列名双查 information_schema）、gkx 280 表、jiuxin 218 表（现场 SHOW TABLES 实数）逐表 DESCRIBE；**结果**——dev 表名命中 1（`policy_support_overview`，overview 子串误中，0 行）；gkx 表名 0 命中；jiuxin 表名命中 1（`ads_research_problem_overview_snapshot`，同样子串误中）；列名正语义命中全部落在 0 行/NULL 表（见 §2.2）。四种缺失情形归属：**表不存在**（事件流水表）+**表存在但 0 行**（汇总面/快照列表）。

### 3.3 D5 代理面质量

`jimu_report` 66 行全部有 view_count（non_null=66），SUM=749,666、MAX=54,003——积木报表（BI 工具）配置主档的浏览计数，字段完整性极好；但它的「内容」是数据分析报表（api_url/js_str/css_str 等配置列），不是科技传播十类内容。作为「浏览计数列+求和」计算链验证面合格，作为月浏览量总体**错位**，不可对外。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 事件流探针 | dev 0 / gkx 0 / jiuxin 0（表名+列名双扫） |
| 月度汇总结构 | chain_news_stat 6 列（stat_month+total_views）0 行 |
| 浏览快照列 | 3 表（chain_news/policy_latest_news/app_article）全 0 行 |
| gkx 点击列 | dwd_information.click_number 32 行全 NULL |
| BI 代理读数 | 66 行 SUM=749,666（语义错位仅内验） |
| 脚本形态 | 薄壳 + 共享探针 5 快照，零 demo_* |

## 四、数据缺失情况

### 4.1 浏览行为数据缺失（数据级，主因）

三源无平台用户浏览行为日志（absence_probe 见 §3.2）；dev 预置的月度汇总面与浏览快照列全部 0 行——这是**表存在但数据未灌**情形：修复动作不是建表而是**灌数**（把新闻/资讯爬取或 CMS 埋点数据落入 `chain_news`/`chain_news_stat`/`policy_latest_news`），或直接接入平台 PV 埋点流。月度序列还需 ≥2 个月份快照才可成趋势。

### 4.2 宿主内容主档薄弱（随动缺口）

SRS 序号 596 定义了十类传播形态，三源侧 `cms_content_news` 仅 12 行通用新闻且**无浏览列**；`app_article` 0 行。浏览量的宿主对象（十类内容主档）本身待建全，此缺口与数据缺口同源（内容运营数据未入湖）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 新闻/资讯数据入湖 | 数据灌载 | 本件 + THINK_011 + THINK_006/009 | 灌满 chain_news/chain_news_stat/policy_latest_news 即激活 |
| 平台 PV 埋点接入 | 外部数据源 | 本件 + THINK_011/012 全互动族 | 用户×内容×时间戳事件流，整族升直接支持 |
| 十类内容主档建全 | 主数据 | 本件 + THINK_006 | 对齐 SRS 序号 596 分类法 |

三条路径档位后果：仅灌数 → 完全转换支持（月度面直查）；接入事件流 → 完全直接支持；维持现状 → 部分支持（仅结构可复用）。推荐：先推新闻/资讯入湖（一源解三件），远期接 PV 埋点。

## 参考文献

1. GB/T 31524-2015 电子网站浏览量统计系列标准（PV/UV 口径）[S]. 国家标准全文公开系统. https://openstd.samr.gov.cn （R1，2026-11-02 检索可达；月度 PV=自然月内页面加载事件求和）
2. 中国科学技术协会. 科学传播发展研究报告（科普新媒体平台月度阅读量口径）[R/OL]. https://www.cast.org.cn （R2，2026-11-02 检索可达）
3. CNNIC. 中国互联网络发展状况统计报告（网站流量统计方法附录）[R/OL]. https://www.cnnic.net.cn （2026-11-02 检索可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技服务全景/科技传播.md》序号 596（excel_row 599）：

> 传播形式分类展示：以专题形式对创新成果展览、科普展览、科学人讲坛、院士风采展示、学术期刊、学术会议、科技图书展览、信息素养大讲堂、科学文化交流、新媒体公众号等内容进行分类展示，支持内容的列表化呈现与详情查看。

序号 600（excel_row 603）：

> 内容数据接口服务：提供具体传播内容的详细数据接口，包括文本、图片、元数据，支撑前端对内容详情的完整呈现。

「月浏览量」指标名本身在三份说明书未出现（检索记录见 A.2）。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 月浏览量 | 科技信息展示系统和科技专题服务系统.md / srs/…/科技传播.md / 科技竞赛.md | 0（指标名未出现） |
| 浏览量 | srs/…/科技传播.md | 0（功能描述无流量统计句） |
| 传播形式分类展示 | SRS 序号 596 | 1（上位功能叶） |
| monthlyViews | repos/demo-ui-science tech-service | TechCommunication.jsx:142 + mockData.js:337 |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_THINK_010_out.json`（20261102 实跑）。
- 共享探针：`code/_snapshots/_shared_s309_think_beta_probe{1,3,4,5}_out.json`（一期词族三源双扫 / 三期承载面开箱 / 四期语义裁定 / 五期数值补采）。
- 判档负证据：absence_probe 三条（dev 0 事件流 / gkx 0 / jiuxin 0），三源逐一留证。

### B.2 本件产物逐键清单（`code/M_SCIUI_THINK_010_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_THINK_010 | 文首 |
| `ui_evidence` | 证据 | 3 条组件行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false**（上位功能覆盖） | §1.3/附录 A |
| `facts.dev_monthly_structure` | 结构 | chain_news_stat 月度汇总骨架 | §2.2 |
| `facts.dev_snapshot_columns` | 结构 | 3 表浏览快照列全 0 行 | §2.2/§3.1 |
| `facts.gkx_information_click` | 事实 | 32 行全 NULL | §2.2/§3.1 |
| `facts.dev_bi_view_proxy` | 代理 | 66 行 SUM=749,666 | §2.2/§3.3 |
| `derived[0]` | 负结论 | monthly_views_negative=null | §2.7 |
| `derived[1]` | 代理读数 | 749,666 | §2.3 |
| `absence_probe` | 负证据 | 三源三条 | §3.2 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `notes` | 披露 | 语义错位 + mock 不参与结论 | §3.3/§4.1 |
| `base_years_*` | 基期三键 | used=[] / missing=2021-2026 / note | §2.5 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表文献/机构 | 计数轴 | 数据要求 | 本库承载 | 贴合度 |
|---|---|---|---|---|---|
| PV 事件流月度求和 | GB/T 31524（R1） | 用户×页面×时间戳 | 浏览事件日志 | 无 | **最高（目标态）** |
| 月度快照汇总 | 运营月报通用 | stat_month+total_views | 月度汇总表 | 结构在 0 行 | 高（灌数即活） |
| 累计快照差分 | CMS 冗余列通用 | 主档 views 列按月留档 | 内容表浏览列 | 结构在 0 行 | 中（需月度留档机制） |
| BI 报表浏览代理 | jimu_report | 报表 view_count | — | 有（66 行） | 低（语义错位，仅内验） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| 浏览事件流 | 三源 0 表 | — | 结构缺失 |
| chain_news_stat | 0 行（6 列结构在） | — | 数据未灌（主因） |
| 浏览快照列 3 表 | 0 行 | — | 数据未灌 |
| dwd_information.click_number | 32 行全 NULL | 2019-2025 资讯在 | 点击数未回填 |
| jimu_report.view_count | 66 行 SUM=749,666 | 全有值 | 语义错位 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 结构复用说明 + mock 维持 | 无 |
| v2 | 新闻/资讯入湖 + 月度面灌数 + 真数上线 | 数据源立项 |
| v3 | PV 埋点事件流 + UV 口径扩展 | 埋点系统对接 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| BI 浏览数被误当内容浏览对外 | **高** | notes 禁用注记 + UI 不上代理版 |
| 月度窗口口径（自然月 vs 滚动 30 天）未定 | 中 | 需求确认后写进数据字典 |
| 单月快照无历史月不可成趋势 | 中 | 入湖时同步回灌历史月 |

### C.5 总判

**部分支持**：月度浏览汇总结构与浏览快照列结构三源环境已预置（chain_news_stat 等 5 面），承载行全 0/NULL；事件流水零承载（探针留证）；升档路径明确——新闻/资讯入湖即升完全转换支持，PV 埋点接入升完全直接支持；触发器写死 §1.6，按 B10 保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_THINK_010.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s309_think_beta_probe{1,3,4,5}.py` | 快照键与本件 facts 零漂移 |
| 数据入口 | 直连 dev 10.50.11.76 / gkx 183.240.141.251 / jiuxin 47.93.119.170 | demo_* 直接 raise |
| 判档一致 | MD 文首「部分支持」= out.json `support_judgment` | 一致 |
| 负证据探针 | `absence_probe` 三源三条 | dev 0 / gkx 0 / jiuxin 0 |
| mock 披露 | mock 1,258,000（125.8万）仅 §1.1 语义描述 | 不参与支持度结论 |

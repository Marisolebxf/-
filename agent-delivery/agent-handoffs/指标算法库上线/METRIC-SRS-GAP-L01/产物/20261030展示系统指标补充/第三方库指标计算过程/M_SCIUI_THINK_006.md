# M_SCIUI_THINK_006 平台内容总条数 —— 指标信息 MD

> **类型**：简单统计类（平台内容总条数 = 内容主档全量 COUNT）｜ **域**：科技服务全景·科技传播·总内容数（TechCommunication.jsx:141，清单 row_01=709 实查定位）｜ **UI 挂载**：科技创新服务全景平台 → 科技传播 → 统计概览四卡之一「总内容数」（`TechCommunication.jsx:141`，`Statistic` 卡渲染 `:154-161`，mock 3,567）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（指标名三源 0 命中；清单 row_01=709 语义注宽泛）｜ **口径归属**：UI 挂载件，SRS 无同名指标（科技传播页为全景平台 1.2 域 UI 挂载）
> **复现脚本**：`code/M_SCIUI_THINK_006.py`（薄壳，指向共享探针 `code/_shared_s309_alpha.py` + `_probe_s309_alpha_b.py`）｜ **产物**：`code/M_SCIUI_THINK_006_out.json`
> **四判定摘要**：直接结构=否（三源无「平台发布内容」结果面）；直接数据=否；依赖结构=部分（dev CMS 主档结构完整在：cms_content_news 16 列含 domain/kind/content/pub_date/status）；依赖数据=部分（CMS 三表合计 29 行近乎空壳；gkx 新闻族 1,994,085 行但总体错位）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 降档根因是「主档量不足 + 代理总体错位」双因叠加：①**口径正确的结构面量不足**——dev CMS 内容主档结构完整（`cms_content_news` 16 列：domain/title/org_ids/kind/content/risk/status/pub_date/source_url…），但三表合计仅 **29 行**（cms_content_news 12 + cms_content_sz 11 + cms_content_region_roster 6），`app_article` 与 `ods.news` 双 0 行空壳——结构在、量近乎空壳；②**量足的面总体错位**——gkx 内容词族五表合计 1,994,085 行（`dwd_org_important_news_info` 1,668,414 行为机构重要新闻、`dwd_zh_paper_reference_content` 196,619 行为论文引用内容、`dwd_industry_chain_news_info` 108,052 行为产业链新闻等），语义是企业/产业链新闻池而非「平台发布内容」；jiuxin 2 表（`ads_talent_media_report` 30 行 + sentiment 15 行）为人才媒体报道。UI 需要的「平台内容总数」无任何一源能同时满足口径与量。

### 批次通用纪律摘要（S3-09 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归册后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无除式（计数读数语义） |
| B4 | 负结论带探针 | absence_probe 四件（三源 + UI 勾稽核） |
| B5 | 确定性 | 逐表 COUNT 精确计数（非估算） |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 数字-出处核对 | 29/1,994,085/3,567/3,516 均对快照与 mockData 核验 |
| B8 | 回执不复收 | 探针可复跑复验 |
| B9 | 单位/日期陷阱 | 计数无单位；mock 差 51 勾稽断裂披露 |
| B10 | 口径裁定保守交付 | 双口径并列（CMS 主档口径 vs 新闻池代理口径），代理禁对外 |
| B11 | 多本账互推 | 与 THINK_009 共享快照零漂移 |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 判定轴存在吗？ | 部分 | dev CMS 主档结构在（16 列），量 29 行近乎空壳 |
| 代理轴可信吗？ | 部分 | gkx 199 万行为新闻池语义，总体≠平台内容 |
| 子盘能撑多少？ | 结构面可撑 | 主档灌数即 COUNT 即活（计算链零成本） |

## 摘要

「平台内容总条数」是科技传播页统计概览四卡之首（`TechCommunication.jsx:141`，label=总内容数，mock `totalContents=3,567`）：回答「平台上发布的展览/讲座/期刊/图书/视频等内容存量多大」。同卡组另有月浏览量（THINK_010）/活跃用户/新增内容。mock 九分类卡合计 3,516 与总数 3,567 **差 51 不勾稽**——演示值自证。数据侧判定：**部分支持**——dev CMS 内容主档结构完整（`cms_content_news` 16 列含 domain/kind/content/pub_date/status）但三表合计仅 29 行近乎空壳；gkx 内容词族五表 1,994,085 行全为企业/产业链新闻语义（`dwd_org_important_news_info` 1,668,414 行机构重要新闻等）；jiuxin 45 行人才媒体报道。口径正确面量不足、量足面总体错位——判部分支持。与 THINK_009（发布时间趋势）共享内容主档缺口。升档路径：dev CMS 主档灌数 → 完全直接支持（COUNT 即活）。

- 需求判定：**UI 挂载件**（三说明书无同名；清单 row_01=709）。
- 复现状态：薄壳已跑通（三源行数断言 + 勾稽核）。
- 档位结论：**部分支持**（结构面在量近乎空壳 + 代理面总体错位）。
- 关键事实：`cms_content_news` 12 行 vs mock 3,567——真实主档量级差 300 倍。
- 升档路径：dev CMS 主档灌数（平台发布内容接入）→ 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技创新服务全景平台/科技服务全景/科技传播（`TechCommunication.jsx`）。页面结构：页头「科技传播」→ 统计概览四卡（`:141-144` categoryStats：总内容数/月浏览量/活跃用户/新增内容，`Statistic` 渲染 `:154-161`）→ 分类导航九分类卡（`:163-185`，CategoryCard 含 icon/name/count）→ 筛选栏（搜索/视图模式/排序：最新发布/最多浏览/最多点赞，`:189-228`）+ 热门标签 → 主区卡片流（ContentCard：类型图标/标题/摘要/日期/浏览/点赞，`:56-89`）或时间轴视图（communicationTimeline）→ 详情抽屉（InsightDetailDrawer：内容类型/分类/发布时间/浏览量/点赞数）。

本件挂载位即四卡之首：`{ label: '总内容数', value: communicationStats.totalContents }`（`:141`）——mock 值 3,567。九分类导航卡每类给 count（156/234/89/45/178/567/123/234/1890），是「总条数按类分解」的界面表达。

### 1.2 为什么需要本指标

内容总数回答「这个平台沉淀了多少内容资产」：管理者看内容供给规模与结构（九类分布），用户判断平台信息丰富度。它与月浏览量（消费侧）、活跃用户（用户侧）、新增内容（供给速率）构成传播页的运营四角——总数是存量底盘。分类导航与总数卡共用内容主档——总数本质是主档 COUNT、分类是主档按 category 分组计数。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「平台内容总条数」指标名在三份需求说明书中未出现（检索记录见附录 A）；清单 row_01=709 的语义注为「文章/报告等内容受用户欢迎程度的统计——回答『这些内容有没有人看』」——注的是浏览受欢迎度而指标名是总条数，清单语义与挂载件有错位（总条数是供给存量非受欢迎度），本件按指标名口径（主档 COUNT）调研。

### 1.4 类似指标权威方法可行性分析概要

内容总量的权威口径族（完整版指向附录 C）：①政府网站与政务新媒体检查指标（R1）：信息发布总量（年度报送）；②中国科协科学传播统计（R2）：科普内容制作数（视频/图文分类计数）；③媒体行业 CMS 通例（R3）：内容主档全量 COUNT（含状态过滤：已发布/下线）。三族一致依赖「内容主档（类型+状态+发布时间）」——dev CMS 结构与此完全同构（16 列），缺失的只是数据量。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-service/TechCommunication.jsx:141` — 总内容数卡（清单挂载位）；`:154-161` — Statistic 渲染；`:163-185` — 九分类卡。
- mock：`repos/demo-ui-science/src/pages/tech-service/mockData.js:335-340` — communicationStats；`:299-308` — communicationCategories 九类 count。
- 清单：`code/_phase3_screen_v3.json` kept_items row_01=709（mount=TechCommunication.jsx:142 系月浏览卡位，实查总内容数卡 `:141`）。
- 同族件：THINK_009（内容发布时间趋势，共享快照）；THINK_010/011/012（浏览/点赞族，路 β 同页四卡）。

### 1.6 推测原意与推测定义

**推测定义（须披露代理敏感性）**：
- 口径 A（UI 现行为，mock 驱动）：$\text{TotalContents} = |\{c \in C_{\text{mock}}\}|$——mock 常量直读；
- **口径 B（建议正式口径）**：$\text{TotalContents} = |\{c \in C_{\text{cms}} : \text{status}(c) = \text{已发布}\}|$——dev CMS 内容主档按发布状态过滤后 COUNT，分类卡为主档按 category 分组计数。

**降档/升档触发器（B10 模板）**：dev CMS 主档灌数（平台发布内容接入，≥千行量级）→ **完全直接支持**（COUNT 即活）；接受 gkx 新闻池代理 → 仍部分支持且语义须标注「企业/产业链新闻池规模，非平台内容总数」；仅有结构无数据 → 维持部分支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在域 | 科技创新服务全景平台（主需求 1.2 域）·科技服务全景·科技传播 |
| 所属页面 | 科技传播（TechCommunication） |
| 所属面板 | 统计概览四卡之首 |
| 本件叶 | 平台内容总条数（UI 挂载件 THINK row_01=709） |
| 相邻叶 | THINK_010 月浏览量/THINK_011 累计浏览量/THINK_012 点赞数（同卡组+卡片流+抽屉）；THINK_009 发布时间趋势（时间轴视图） |
| UI 容器 | `Statistic` 卡 + 九分类 CategoryCard |

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径 B（CMS 主档口径，判定依据）**：平台内容总条数 = dev CMS 内容主档（cms_content_news + cms_content_sz + cms_content_region_roster，status=已发布过滤）COUNT——口径正确、结构在，量近乎空壳（三表合计 29 行）。
- **口径 C（新闻池代理口径，禁对外）**：gkx 内容词族五表合计 1,994,085 行——量足但语义为企业/产业链新闻池（dwd_org_important_news_info 机构重要新闻 1,668,414 行、zh_paper_reference_content 论文引用内容 196,619 行等），非「平台发布内容」。
- **裁定**：以口径 B 判档（结构部分可得、量不足）→ 部分支持；口径 C 登记为规模参照非判档依据。

### 2.2 探针读数实测

dev CMS 主档逐表 COUNT（`_probe_s309_alpha_b` 快照）：

| 表 | 行数 | 语义 |
|---|---|---|
| `gkxlumenx_cms.cms_content_news` | **12** | 内容新闻主档（16 列：domain/title/org_ids/kind/content/risk/status/pub_date/source_url…） |
| `gkxlumenx_cms.cms_content_sz` | **11** | 深圳内容补档 |
| `gkxlumenx_cms.cms_content_region_roster` | **6** | 区域名单内容 |
| `gkxlumenx_app.app_article`（+category/collect） | **0** | app 文章主档空壳 |
| `gkxlumenx_ods.news` | **0** | ods 通用新闻空壳 |
| `gkxlumenx_dwd.policy_latest_news` / `chain_news` | **0 / 0** | 政策/链新闻空壳 |

CMS 口径合计 = 12+11+6 = **29 行**（产物键 `dev_cms_content_sum`）。gkx 五表 1,994,085 行、jiuxin 2 表 45 行（`ads_talent_media_report` 30 + `ads_talent_media_sentiment_assessment` 15，30 列含 published_at/title/publisher）。

### 2.3 读数落盘与同基核对

主档三表同库同 schema（gkxlumenx_cms）逐表精确 COUNT 求和（B3 同基——非跨源混算）；mock 3,567 作 ui_demo_fallback 披露不混入真读数；口径 C 五表合计同为同库（gkx）同词族求和（产物 `derived[1]`，规模参照）。

### 2.4 稳健性与口径敏感性

主档近乎空壳（29 行）意味着 COUNT 读数对灌数进度极敏感——任何一批接入都会成倍改变总数（量级脆弱性，与 gkx 医疗器械 10,000 行稳定面不同）；口径 C 若混入 zh_paper_reference_content（论文引用）会引入「学术文献≠发布内容」的语义污染，已从判档依据剔除。status 过滤规则（已发布/下线/草稿）待主档灌数时随数据字典裁定。

### 2.5 基期年份可用性

总条数为存量截面读数（无时序维度）——`base_years_used=[]`、`missing=[2021-2026]`、note 注明不适用基期；若接入真实主档，以收录起始年为基期（与 SOFTSCI_003 分布件同款基期处理）。

### 2.6 需求符合性预评

统计卡可直切真数的前提是主档灌数：灌数后 COUNT 即活（计算链零成本）；九分类卡同步按 category 分组激活。当前 29 行状态下切真数会呈现「平台只有 29 条内容」的失真读数——不满足上线条件，维持 mock 或推灌数。

### 2.7 复现代码结果展示

复现入口 `code/M_SCIUI_THINK_006.py`，产物 `code/M_SCIUI_THINK_006_out.json`；关键读数：`dev_cms_content_sum=29`（§2.2）、`gkx_content_table_rows` 五表（§2.2）、`derived[0]` 负读数 null 登记（无可信总数）、`derived[1]=1994085` 规模参照。对照需求功能要求（内容规模统计）：**部分满足**（结构链路可用、量不足须披露）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | dev CMS 主档三表 | `dev_cms_content_sum` | 29（12+11+6） |
| 装载 | dev 空壳面 | `dev_app_article`/`dev_news_ods` | 0 / 0 |
| 代理 | gkx 内容词族五表 | `derived[1]` | 1,994,085 |
| 代理 | jiuxin 内容词族 | `jiuxin_content_word_rows` | 30+15 |
| 勾稽 | mock 九类合计 vs 总数 | `ui_categories` | 3,516 vs 3,567（差 51） |
| absence | 三源内容主档探针 | `absence_probe` | dev 结构在量空 / gkx 语义错位 / jiuxin 人才域 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 平台内容主档（发布内容×类型×状态） | dev | `gkxlumenx_cms.cms_content_news` 等 | 29 | 结构在量空 | **主降档因之一** |
| D2 | 内容状态/类型字典 | dev | cms status/kind 列 | （列在） | 结构在 | 待灌数配套 |
| D3 | 新闻池代理面 | gkx | 内容词族五表 | 1,994,085 | 量足语义错位 | **主降档因之二** |
| D4 | 人才媒体报道面 | jiuxin | `ads_talent_media_report` 等 | 45 | 人才域 | 语义排除 |

`support_judgment="部分支持"`，与文首一致（闸 6）。

### 3.2 内容主档面三源探针（absence_probe 全记录）

否定性证据四件套：**查了什么**——content/article/publish/media/news/cms 词族表名扫描 + 逐表 COUNT + UI 勾稽核；**条件**——dev 17 schema/542 表、gkx 280 表、jiuxin 218 表（`SHOW TABLES` 现场实数）；**结果**——dev 词族命中 51 表中主档族仅 3 表有数（29 行）、app/ods/dwd 新闻族 5 表 0 行、其余为图谱/全景/审计类非内容主档；gkx 命中 5 表全为企业/产业链新闻语义；jiuxin 命中 2 表为人才媒体报道。四缺失情形归属：**表存在但数据量不足**（dev CMS 主档）+ **语义错位**（gkx/jiuxin 代理面）。

### 3.3 D1 主档结构面质量

`cms_content_news` 16 列（id/domain/title/org_ids/kind/content/risk/status/pub_date/source_url/is_deleted/created_by/created_at/updated_by/updated_at）——domain/kind/status/pub_date 四维正好覆盖「类型×状态×发布时间」的权威口径要求（§1.4 R3 通例），结构设计与口径 B 完全同构；缺陷仅在量（12 行）。`cms_content_sz`（深圳补档，district/industry/park/cert 维度）与 `cms_content_region_roster`（区域名单）为同族补充面。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| CMS 主档三表 | 12+11+6=29 行（16 列结构在） |
| 空壳面复核 | app_article 0/ods.news 0/policy_latest_news 0/chain_news 0 |
| gkx 五表 | 1,994,085 行（语义逐一登记） |
| jiuxin 两表 | 30/15 行（人才媒体报道） |
| UI 勾稽核 | 九类 3,516 ≠ 总数 3,567（差 51） |
| 判档 | 部分支持（产物 = 文首） |

## 四、数据缺失情况

### 4.1 平台内容主档量不足（数据级，主因）

dev CMS 主档结构完整但 29 行近乎空壳——「平台发布内容接入」未实施或未灌数。四缺失情形归属：**表存在但数据量不足**。修复动作是**内容源接入与灌数**（平台自有内容 CMS 化 + 外采内容入档），结构零改动。

### 4.2 代理面语义错位（随动披露）

gkx 199 万行新闻池与 jiuxin 45 行媒体报道不可挪用：前者是企业/产业链新闻（org_important_news_info 机构重要新闻等）、后者是人才维报道——与「平台发布内容」不同总体。若强行代理须整卡换语义（新闻池规模），不在本件交付。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| CMS 主档灌数 | 数据接入 | 本件 + THINK_009/010/011/012 | 内容族五件一揽子（主档是共同地基） |
| status/kind 字典配套 | 数据字典 | 本件 | 已发布过滤+九类映射 |
| 浏览/点赞事件表立项 | 数据工程 | THINK_010/011/012 | 主档之外的消费侧流水（另件处理） |

档位后果：主档灌数 → 完全直接支持（COUNT 即活）；仅新闻池 → 维持部分支持（代理禁对外）；无动作 → 维持部分支持。推荐：内容族合并推主档灌数（一源解五件）。

## 参考文献

1. 国务院办公厅. 政府网站与政务新媒体检查指标（信息发布总量口径）[EB/OL]. https://www.gov.cn （R1，2026-11-02 检索可达）
2. 中国科学技术协会. 全国科普统计调查方案（科普内容制作数）[EB/OL]. https://www.cast.org.cn （R2，2026-11-02 检索可达）
3. 中国记协. 媒体内容资产管理系统建设指南（内容主档通例）[EB/OL]. https://www.zgjx.cn （R3，2026-11-02 检索可达）

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 平台内容总条数|总内容数|内容总数` 三份说明书 + 主需求 → 指标名 0 命中（「总内容数」仅 UI 卡 label 命中）。
- 清单登记：`_phase3_screen_v3.json` kept_items row_01=709，mount=`pages/tech-service/TechCommunication.jsx:142`（清单行号系月浏览卡位；实查总内容数卡 `:141`——登记修正）。
- UI 行为链：categoryStats 数组（`:139-144`）→ Statistic 卡 map（`:154-161`）→ 总内容数卡；九分类卡（`:163-185`）→ CategoryCard count 渲染。
- mock 参照（`mockData.js:335-340`）：totalContents 3,567；`:299-308`：九类 156/234/89/45/178/567/123/234/1890（合计 3,516）。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 平台内容总条数 / 总内容数 | 三份说明书 + 主需求 | 0（指标名） |
| 总内容数 | UI 组件（TechCommunication.jsx:141） | 1（统计卡 label） |
| 内容总数 | mockData（communicationStats.totalContents） | 1（mock 字段） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_THINK_006_out.json`（20261102 实跑）。
- 共享探针：`code/_shared_s309_alpha.py` → `_snapshots/_shared_s309_alpha_out.json`（三源内容词族 + 行数）。
- 深度探针：`code/_probe_s309_alpha_b.py` → `_snapshots/_probe_s309_alpha_b_out.json`（CMS 主档列结构 + 逐表行数）。

### B.2 本件产物逐键清单（`code/M_SCIUI_THINK_006_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` / `batch` | 标识 | M_SCIUI_THINK_006 / S3-09 | 文首 |
| `ui_evidence` | 证据 | 4 条（统计卡/渲染/mock/九分类） | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false**（row_01=709） | §1.3 |
| `facts.dev_cms_content_news` | 结构证据 | 16 列 12 行 | §2.2/§3.3 |
| `facts.dev_cms_content_sum` | 计数 | 29 | §2.2 |
| `facts.gkx_content_table_rows` | 代理证据 | 五表行数 | §2.2 |
| `derived[0]` | 负读数 | null（无可信总数） | §二 |
| `derived[1]` | 规模参照 | 1,994,085 | §2.2 |
| `absence_probe` | 负证据 | 四件 | §3.2 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `base_years_*` | 基期三键 | used=[] / missing=[2021-2026] / note | §2.5 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表机构 | 数据轴 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 政务新媒体信息发布总量 | 国办（R1） | 发布条数（年度） | CMS 结构同构、量空 | 最高（目标态） |
| 科普内容制作数 | 中国科协（R2） | 视频/图文分类计数 | kind 列可承载 | 高 |
| CMS 主档 COUNT 通例 | 行业（R3） | 主档×状态过滤 | status 列在 | 高 |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 缺口 |
|---|---|---|
| dev CMS 主档 | 29 行 | 量不足（主因） |
| status/kind 字典 | 列在 | 灌数配套 |
| gkx 新闻池 | 1,994,085 行 | 语义错位（禁代理对外） |
| jiuxin 媒体报道 | 45 行 | 人才域排除 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1 | CMS 主档灌数（完全直接支持，COUNT 即活） | 内容源接入 |
| v2 | 九类映射字典 + status 过滤上线 | 数据字典 |
| v3 | 浏览/点赞事件流水（THINK_010/011/012 解锁） | 事件表立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 29 行状态下切真数呈现失真读数 | **高** | 上线门槛（灌数后切） |
| 新闻池被误当平台内容总数 | 中 | 代理禁对外注记 |

### C.5 总判

**部分支持**：CMS 主档结构完整同构权威口径但量近乎空壳（29 行），gkx/jiuxin 量足面语义错位；主档灌数即升完全直接支持，触发器写死 §1.6，按 B10 保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_THINK_006.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s309_alpha.py` | 快照三源表数 542/280/218 |
| 深度探针 | `python3 code/_probe_s309_alpha_b.py` | CMS 三表 12/11/6 |
| 判档一致 | MD 文首「部分支持」= out.json `support_judgment` | 一致 |
| 断言 | CMS 合计 29 / gkx 合计 1,994,085 | 脚本内 assert 通过 |
| §二结构 | 2.1-2.8 编号小节 | 齐备 |
| mock 披露 | 3,567/3,516 差 51 仅 §1.1/§2.2 描述 | 不参与支持度结论 |

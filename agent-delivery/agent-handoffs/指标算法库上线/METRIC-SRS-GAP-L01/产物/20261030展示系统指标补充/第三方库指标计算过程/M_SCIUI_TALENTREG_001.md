# 代表性成果（卡片式统计）（M_SCIUI_TALENTREG_001）

> **类型**：无业务逻辑数值类（四卡计数 + 代表作列表）｜ **域**：科技信息展示系统·重点科技人才画像·基础画像（信息展示方式）｜ **UI 挂载**：科技信息展示系统 → 重点科技人才画像 → 基础画像（L3 详细层）→ `ProfileBasicPanel.jsx:301`（InfoCard「代表性成果（卡片式统计）」）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（UI 拆件，需求只给卡片式展示行为不给四卡构成算式；本件不合成影响力分，B10）｜ **口径归属**：卡片名 UI 拆件（三真源 0 命中），展示行为对应主需求 1.1.1.1.4.3.3.1.1(3) 卡片式展示，`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TALENTREG_001.py`｜ **产物**：`code/M_SCIUI_TALENTREG_001_out.json`
> **四判定摘要**：直接结构 = 无（「四卡式代表作统计」现成结果面无）；直接数据 = 无（同左）；依赖结构 = 部分（久新代表成果快照面 + 论文/专利/被引/H 计数列 + 项目关联面三腿结构在，著作腿结构零承载）；依赖数据 = 部分（profile 100,000 行计数列全铺、achievement 902,667 行覆盖 100,000 人，著作 0 承载、项目分级/经费 0 承载）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 四卡逐腿盘点（与 UI 论文/著作/专利/科研项目四 StatCard 一一对应）：**论文腿最强**——`ads_talent_profile.paper_count`/`citations_count`/`h_index` 三列 100,000 行 100.0% 全铺（合计论文 6,764,149 篇/被引 185,229,713 次/H 和 1,445,108），代表成果快照面 `ads_talent_research_achievement` 902,667 行覆盖 100,000 人（人均 9.03 条，与 schema「每人才 Top 10」口径互证），但实测 `achievement_type` 仅 paper 一种（project/award/patent 型各 0 行）、`venue` 列非空 0；**专利腿在**——`patent_grant_count`/`patent_family_count` 各 6,490 人非空（授权合计 85,069 项/族 68,314）；**项目腿半在**——计数列 `project_count` 100.0% 全铺且与 `ads_talent_project` 关联面 7,702,366 行同读数互证（is_lead 全 0），但「国家级/国际」分级与「经费万元」结构零承载（Grant 维度 schema 标注关联 DWD Grant、ADS 未发布）；**著作腿零承载**——久新 book/monograph 词族表级+列级双零、gkx `dwd_scholar` 无 book 列、OpenAlex 体系 book/book-chapter 属 work type 而久新 paper_profile 未做类型区分。三腿在+一腿缺 → 部分支持（口径 A：论文/专利/代表作卡可交付）。

### 批次通用纪律摘要（S3-03 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实；久新表数写「实测 210 张（探测日）」 |
| B3 | 同基相除 | 覆盖率分子分母同表同 WHERE；人均成果比分母=同表去重人才 |
| B4 | 负结论带探针 | 著作腿/项目分级经费面的三源+需求五向 absence_probe（§3.3） |
| B5 | 确定性 | 类型分布按计数降序+类型名升序；字段计数键名直书 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑；产物零手改 |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | 经费「万元」为 UI mock 单位（库内无经费列不产生单位运算）；快照无年度运算 |
| B10 | 口径裁定保守交付 | impactScore 等演示分不写伪值；著作/分级缺维不代理；升档触发器写死 |
| B11 | 多本账互推 | profile 100,000/achievement 902,667/venue 0/talent_project 7,702,366 与族内件（002/005/008/010）零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 四卡腿各有承载吗？ | 论文全/专利在/项目半/著作无 | 计数列非空 100,000/6,490/100,000/0（§2.2） |
| 代表成果卡（列表）有现成面吗？ | 有（久新独有） | 902,667 行、人均 9.03、schema Top10 确定性排序（§2.3） |
| 著作腿能代理吗？ | 不能 | 三源表级+列级双零；论文数冒充著作数是口径偷换（B10） |

## 摘要

「代表性成果（卡片式统计）」是重点科技人才画像·基础画像 L3 详细层的成果卡（`ProfileBasicPanel.jsx:301`）：论文/著作/专利/科研项目四 StatCard（各带被引/授权/经费 sub 行）+ 下方代表成果卡片列表（type 标签+title+venue·year·被引 meta 行）。需求侧卡片名为 UI 拆件（三真源 0 命中），组件行为对应主需求 :1905-1907 卡片式展示（「结构化卡片形式呈现，美观直观，便于快速浏览与对比」），「代表性成果」语义词在 :1463/:2271 出现。数据侧久新给了接近完整的承载：profile 计数列三腿现成（论文 100.0% 全铺、专利 6,490 人、项目计数与关联面互证），代表成果快照面 902,667 行按 schema「cited_by_count DESC, publication_year DESC NULLS LAST, work_id ASC 取 Top 10」确定性排序——正是三评改革「推行代表作评价制度」（R2）的库内落地件。两个硬缺口卡住完全档：著作腿三源零承载（book 词族表级+列级双零、OpenAlex 类型未区分）；项目卡的国家级/国际分级与经费万元结构未发布（Grant 维度仅在 DWD 侧）。另有物料缺：achievement.venue 902,667 行非空 0，代表成果卡渲染须回退 title+year+citations。判**部分支持**。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**UI 拆件**（卡片名 0 命中）；展示行为在（卡片式展示叶），四卡数值构成算式无。
- 复现状态：脚本已跑通；计数腿/快照面/类型分布/字段完整性/项目关联面读数全落产物。
- 档位结论：**部分支持**（三腿在 + 著作腿零承载 + 项目分级/经费未发布）。
- 关键事实：`achievement_type` 实测仅 paper（902,667 行），project/award/patent 型各 0 行——UI 代表作列表的专利/项目彩色标签在数据侧暂无同型物料。
- 升档路径：著作腿接图书/专著源（或裁撤该卡）+ Grant 分级/经费面发布 → 可升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技人才态势/**重点科技人才画像·基础画像·信息展示方式**（主需求 1.1.1.1.4.3.3.1.1(3) 卡片式展示；卡片名为 UI 拆件）。UI 实际容器是人才画像页基础画像面板（`ProfileBasicPanel.jsx`）L3「成果与影响力」区的第一张 InfoCard，仅当详情层级切到「详细」（`showL3`）才渲染：标题「代表性成果（卡片式统计）」，上半 `tl-tp-stat-grid` 四张 StatCard——论文（total 篇 + sub「被引 X 次 · 篇均 Y · 影响力 Z」）、著作（total 部 + 被引/影响力）、专利（total 项 + 授权/被引/影响力）、科研项目（total 项 + sub「国家级 X / 国际 Y · 经费约 Z 万元」）；下半 `representative.map` 渲染代表成果卡片列表——type 标签（patent 橙/project 绿/其余蓝）、title、`[venue, year, 被引].filter(Boolean).join(' · ')` meta 行。数值源是 mock 生成器 `data.js:828-866`：`papers.total/avgCitations/impactScore`、`books.total=random(1,12)`、`patents.granted=⌊total×randomFloat(0.5,0.9)⌋`、`projects={national: random(3,18), international: random(1,8), fundingWan: random(800,12000)}`——全 random 演示值。

### 1.2 为什么需要本指标

人才画像的「成果面」要回答三个递进问题：有多少（四卡计数）、好在哪（被引/授权/经费 sub 行）、拿什么作代表（代表作列表）。四卡形态是「快速浏览与对比」需求（:1907 原文）的直接落地——用户扫一眼卡片即可完成学者的量级定位；代表作列表则是「代表性成果」语义的深读入口（需求 :1463「对人才详细背景、代表性成果及社会影响进行多维展示」），它的方法论背景是代表作评价制度：三评改革（R2）明确「推行代表作评价制度」——不数总数、看最好的少数几篇。库内快照面的「每人才 Top 10 按被引降序」正是这一制度的工程化。本件的调研重心因此是「四条腿的承载分别在哪、缺在哪」：论文/专利腿直查、项目腿关联面、著作腿缺口定性——这是卡片式统计卡的典型判档结构。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**卡片名「代表性成果（卡片式统计）」三真源 0 命中（UI 拆件）；组件行为对应的卡片式展示叶（:1905-1907）只给展示行为（「采用卡片式页面设计，将人才信息以结构化卡片形式呈现」）；「代表性成果」语义词在 :1463/:2271/:6558/:7949 出现但均为展示语境（「多维展示」「深入浏览…代表性成果」「维护代表性成果」）——四卡的计数口径（论文含不含会议？专利授权还是申请？项目国家级怎么判？）与代表作的选取规则（Top 几、按什么排序）需求侧无一字。UI mock 的 random 数值是前端演示值，不构成口径证据。

### 1.4 类似指标权威方法可行性分析概要

「代表性成果统计卡」的权威方法锚分三层。其一，代表作评价制度：三评改革意见（R2，国办发〔2021〕32 号转入深化阶段，R1 为其科技人才评价延伸）「推行代表作评价制度」——代表作的选取规则（少数、高质量、可公开）与库内「每人才 Top 10 按被引降序」直接同构。其二，成果分类统计传统：科技统计年鉴体系（R3，国家统计局/科技部）把科技产出按论文/著作/专利/项目四类分列——正是 UI 四卡的类目学来源；其中国内科技论文统计（CSTPCD）与专利统计年报分别给出论文/专利的官方计数口径。其三，文献计量 indicators 传统（OECD Frascati 手册的产出测量章节，方法论背景）：产出统计的「stock vs flow」口径（累计量 vs 年增量）须显式声明——profile 计数列是累计量口径。方法族对照：

| 方法族 | 代表 | 类目/规则 | 数据要求 | 与三源匹配 |
|---|---|---|---|---|
| 代表作制度 | 三评改革（R2） | 少数高质量代表作 | 排序键+TopN 截断 | **有**（快照面 Top10 按被引降序现成） |
| 四类分列统计 | 科技统计年鉴（R3） | 论文/著作/专利/项目 | 四类计数列 | **部分**（论文/专利/项目在、著作无） |
| 产出测量口径 | OECD Frascati（背景） | stock/flow 声明 | 时间窗 | 有（快照=stock 口径） |
| 前端演示 | UI random 四卡 | — | mock 常量 | 结构披露（不作源） |

结论：代表作腿与论文/专利/项目三腿有官方口径同构承载，著作腿与项目细分（分级/经费）两条缺口的修复动作不同（外部源 vs 维度发布）。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/talent-trend/components/ProfileBasicPanel.jsx:301`（InfoCard title）；`:305-330`（四 StatCard）；`:333-346`（representative 列表渲染）。
- 数值语义源：`repos/demo-ui-science/src/pages/talent-trend/data.js:828-866`（papers/books/patents/projects mock 生成器全 random）。
- 主需求：`科技信息展示系统和科技专题服务系统.md`:1905-1907（卡片式展示）、:1463/:2271（代表性成果语境），原文见附录 A。
- 权威方法：R2 三评改革意见（国办发〔2021〕32 号）；R3 科技统计年鉴体系。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**——四卡 + 列表逐腿：

- **论文卡**：total = `paper_count`（累计量口径）；sub = 被引 `citations_count` / 篇均 = 被引/论文 / 影响力分不合成（mock 结构披露，B10）。
- **著作卡**：无承载——`books.total` 无库内对应列；不得以论文数冒充（口径偷换禁止）。若甲方裁撤该卡或接图书源，缺口关闭。
- **专利卡**：total = `patent_family_count`（族口径）或 `patent_grant_count`（授权口径，UI「授权」sub 行对应），授权率 = 授权/族（演示口径，库内两列在）。
- **项目卡**：total = `project_count`（100.0% 全铺）；「国家级/国际」与「经费万元」标注「数据待接」（Grant 维度未发布，`experience.project_ids` 实测全空）。
- **代表成果列表**：`ads_talent_research_achievement` 按人才直查（schema Top10 规则），type 标签现阶段全为 paper 型；meta 行因 venue 全空回退 `title + year + 被引`。

**降档/升档触发器**：①著作腿接图书/专著数据源（或 UI 裁撤著作卡）+ Grant 分级/经费面发布 → 四腿闭合可升**完全转换支持**；②甲方裁定「三腿先行、著作卡显 0/隐藏」→ 维持部分支持但交付语义闭合；③仅裁撤不作数 → 维持部分支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在需求文档 | 主需求《科技信息展示系统和科技专题服务系统.md》 |
| 所属四级功能 | 1.1.1.1.4.3.3 重点科技人才画像（4 个 L5） |
| 所属 L5 | 基础画像（1.1.1.1.4.3.3.1）→ 信息展示方式（.1）→ 卡片式展示（(3)） |
| 本件 | **代表性成果（卡片式统计）——卡片名 UI 拆件，挂卡片式展示行为叶** |
| 相邻承接件 | TALENTPF_006（学术影响力量化卡，同面板下一卡：影响力指数/H 指数/学科贡献度/领域热度）；TALENTIR_005（论文质量分，贡献度侧质量轴） |
| 语义词邻近 | :1463 全球人才态势（多维展示）、:2271 领域图谱节点聚焦、:6558/:7949 内容维护侧 |
| UI 容器 | `ProfileBasicPanel.jsx:301` L3 成果区第一卡 |

本卡与 TALENTPF_006 是同面板「成果与影响力」双卡：本件是**量**轴（四类计数+代表作）、006 是**热**轴（领域热度/影响力）；与本件共享 achievement 面的是 TALENTIR_005（venue 0 读数两件一致）与 TALENTIR_008（分阶段产出，共享 profile 计数列）。

## 二、计算过程

### 2.1 方法选择（文献依据）

四卡逐腿选法：**论文/专利腿**用直查计数（stock 口径，Frascati 产出测量的累计量口径，与科技统计年鉴的存量表同型）；**代表作腿**直接采库内快照面的官方规则——schema 文档明载选取规则为 `cited_by_count DESC, publication_year DESC NULLS LAST, work_id ASC` 取每人才 Top 10（确定性排序，B5 同构），这正是 R2「代表作评价制度」的工程落地：以被引为第一排序键（质量优先）、年份与 work_id 破平（确定性），本件不另造排序公式；**项目腿**用关联面计数（talent_project 7,702,366 行与 profile.project_count 互证）；**著作腿**无从选法（三源零承载），留缺不代理。影响力 sub 分（impactScore）不合成（评分口径未闭合，B10）。

### 2.2 装载与计数腿读数

经 `_gkxdb.py` 连 gkx、直连 dev 与久新（三源串行只读）。久新实测 210 张表（探测日）。`ads_talent_profile` 100,000 行计数腿逐列实测：`paper_count` 非空 100,000（100.0%，合计 6,764,149）、`citations_count` 非空 100,000（合计 185,229,713）、`h_index` 非空 100,000（合计 1,445,108）、`project_count` 非空 100,000（合计 7,702,366）；`patent_grant_count` 非空 6,490（合计 85,069）、`patent_family_count` 非空 6,490（合计 68,314）——专利腿是 6.5% 覆盖的稀疏面（MVP 池以论文型学者为主），UI 专利卡在该池多数个体显示 0 是真实读数而非缺数。著作腿列级排除：profile 104 列 book/monograph 词族 0 命中（`jiuxin_profile_book_like_cols=[]`）。

### 2.3 代表成果快照面：代表作制度的库内落地

`ads_talent_research_achievement` 902,667 行、覆盖去重人才 100,000 人（= profile 全池，派生键 `jiuxin_achievement_talent_coverage_pct=100.0`），人均 9.03 条（派生键 `jiuxin_achievement_per_talent_avg`，schema「每人才 Top 10」口径互证——人均略低于 10 因部分学者有效论文不足 10 篇）。类型分布：**paper 902,667 行是唯一类型**（project/award/patent 型各 0 行）——UI 代表作列表的专利橙标/项目绿标现阶段无同型物料。字段完整性：title 非空 902,666、year 非空 902,667、cited_by_count 非空 902,667，**venue 非空 0**（与 TALENTIR_005 件读数一致，B11）——meta 行 `[venue, year, 被引].filter(Boolean)` 的 filter 正好吸收 venue 空值，卡片渲染回退 `title + year + 被引` 两段式，UI 结构对物料缺天然兼容。

```sql
SELECT achievement_type, COUNT(*) FROM ads_talent_research_achievement
GROUP BY achievement_type ORDER BY COUNT(*) DESC, achievement_type ASC;
-- → paper 902667（唯一类型；project/award/patent 各 0）
SELECT COUNT(`venue`) FROM ads_talent_research_achievement;  -- → 0（物料未回填）
```

### 2.4 项目腿：关联面互证与细分缺口

项目腿双面互证：`ads_talent_project` 关联面 7,702,366 行、覆盖去重人才 93,675 人，与 profile.`project_count` 合计 7,702,366 **逐位一致**（两表同读数，B11 互证）；is_lead 分布全 0（7,702,366 行无一「牵头」标记——schema 该列在但未启用）。细分缺口：UI 项目卡 sub 行「国家级 X / 国际 Y · 经费约 Z 万元」所需的分级列与经费列在 talent_project 面零承载——absence_probe 在案（Grant 维度 schema 标注关联 DWD Grant、ADS 未发布分级/经费面）；另一路径 `ads_talent_experience.project_ids` 实测非空 0 行（`jiuxin_experience_with_projects=0`）——履历侧项目指针列整体未回填，项目腿只能走 talent_project 面。

### 2.5 三源排除与 gkx 侧定位

**gkx**：280 表 achievement/award/honor/representative 词族 0 命中（无代表成果表）；`dwd_scholar` 27 列中成果词族仅 `paper_nums`/`citation_nums`/`h_index`/`reference_nums` 四计数列（无 patent/book/project 列）——gkx 能出论文卡但出不了专利/项目/代表作三腿。**dev**：achievement/award 词族命中 `gkxlumenx_dwd.org_achievement_year` / `gkxlumenx_ods.achievement_year` 2 张——机构级年度成果计数面（org_ 前缀），非学者级且非代表作快照，不构成本件承载（「机构≠学者、年度计数≠代表快照」双不同物）。**久新**：四腿中三腿的唯一现成承载方（计数列+快照面+关联面），著作腿同样零承载（book 词族表级 0：`jiuxin_book_like_tables=[]`）。

### 2.6 稳健性与口径敏感性

四个敏感性登记：其一，专利腿稀疏（6,490/100,000=6.5%）——「专利 0」在多数个体是真实值，UI 若把 0 显示为「—」会混淆「无专利」与「无数据」两种语义；其二，快照面排序键单一（被引降序）——高被引综述会挤占代表作位（与 TALENTIR_005 的 FWCI outlier 问题同源），代表作制度若要求「多样性」须改多键，属口径裁定；其三，type 单型（全 paper）——UI 三色标签的绿/橙分支是超前设计，等 award/patent 型物料回填；其四，project_count 与关联面同读数但语义不同（一个是汇总计数、一个是明细行数，本池恰好相等是发布口径使然），引用时须写明来源面。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TALENTREG_001.py`（三源串行只读；gkx 经 `_gkxdb.py`；dev/久新直连；零 `demo_*`）；运行 `python3 code/M_SCIUI_TALENTREG_001.py`。
- 产物：`code/M_SCIUI_TALENTREG_001_out.json`。正文数字与产物键逐一对应：`jiuxin_table_count=210`（§2.2，探测日）、`jiuxin_profile_rows=100000` + `jiuxin_profile_paper_count_nonnull=100000` + `jiuxin_profile_paper_count_sum=6764149` + `jiuxin_profile_citations_count_sum=185229713` + `jiuxin_profile_h_index_sum=1445108` + `jiuxin_profile_patent_grant_count_nonnull=6490` + `jiuxin_profile_patent_grant_count_sum=85069` + `jiuxin_profile_patent_family_count_nonnull=6490` + `jiuxin_profile_patent_family_count_sum=68314` + `jiuxin_profile_project_count_sum=7702366`（§2.2）、`jiuxin_research_achievement_rows=902667` + `jiuxin_achievement_talents=100000` + `jiuxin_achievement_type_dist` + `jiuxin_achievement_paper_rows=902667` + `jiuxin_achievement_project_rows=0` + `jiuxin_achievement_award_rows=0` + `jiuxin_achievement_patent_rows=0` + `jiuxin_achievement_title_nonnull=902666` + `jiuxin_achievement_venue_nonnull=0` + `jiuxin_achievement_year_nonnull=902667` + `jiuxin_achievement_cited_by_count_nonnull=902667`（§2.3）、`jiuxin_talent_project_rows=7702366` + `jiuxin_talent_project_talents=93675` + `jiuxin_talent_project_is_lead_dist=[[0,7702366]]` + `jiuxin_experience_with_projects=0`（§2.4）、`jiuxin_book_like_tables=[]` + `jiuxin_profile_book_like_cols=[]` + `gkx_table_count=280` + `gkx_achievement_like_tables=[]` + `gkx_scholar_achievement_cols`（paper_nums/citation_nums/h_index/reference_nums）+ `dev_achievement_like_tables`（2 张机构级）（§2.5/§3.3）、派生键 `jiuxin_achievement_per_talent_avg=9.03` + `jiuxin_paper_count_coverage_pct=100.0` + `jiuxin_achievement_talent_coverage_pct=100.0`（§2.2/§2.3）。
- 结果解读：四个可用读数（论文腿三列全铺；代表作快照面 100% 覆盖+确定性规则；专利腿稀疏但真实；项目腿双面互证）+ 两个缺口（著作腿零承载；项目分级/经费未发布）+ 一个物料缺（venue 0，渲染回退在案）。
- 对照需求功能要求的评审：「将人才信息以结构化卡片形式呈现，便于快速浏览与对比」——**部分满足**：论文/专利/项目三卡与代表作列表可真实回填（mock 替换）；著作卡无库内对应、「国家级/国际/经费」sub 行数据待接；代表作列表 type 标签现阶段全为论文型。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 久新实测表数 | `jiuxin_table_count` | 210（探测日） |
| 论文腿 | 计数覆盖 | `jiuxin_profile_paper_count_nonnull` | 100,000（100.0%） |
| 论文腿 | 论文合计 | `jiuxin_profile_paper_count_sum` | 6,764,149 |
| 论文腿 | 被引合计 | `jiuxin_profile_citations_count_sum` | 185,229,713 |
| 论文腿 | H 指数合计 | `jiuxin_profile_h_index_sum` | 1,445,108 |
| 专利腿 | 授权覆盖/合计 | `jiuxin_profile_patent_grant_count_nonnull/_sum` | 6,490 / 85,069 |
| 专利腿 | 族覆盖/合计 | `jiuxin_profile_patent_family_count_nonnull/_sum` | 6,490 / 68,314 |
| 项目腿 | 计数合计 | `jiuxin_profile_project_count_sum` | 7,702,366 |
| 项目腿 | 关联面行数/人才 | `jiuxin_talent_project_rows` / `_talents` | 7,702,366 / 93,675 |
| 项目腿 | is_lead 分布 | `jiuxin_talent_project_is_lead_dist` | 全 0 |
| 项目腿 | 履历指针列 | `jiuxin_experience_with_projects` | 0（未回填） |
| 代表作 | 快照行数/覆盖 | `jiuxin_research_achievement_rows` / `_talents` | 902,667 / 100,000 |
| 代表作 | 人均条数 | `jiuxin_achievement_per_talent_avg` | 9.03（Top10 口径互证） |
| 代表作 | 类型分布 | `jiuxin_achievement_type_dist` | 仅 paper |
| 代表作 | 字段完整性 | `jiuxin_achievement_*_nonnull` | title 902,666 / venue **0** / year 902,667 / cited 902,667 |
| 著作腿 | 表级+列级 | `jiuxin_book_like_tables` / `jiuxin_profile_book_like_cols` | [] / []（双零） |
| 排除 | gkx 成果表/列 | `gkx_achievement_like_tables` / `gkx_scholar_achievement_cols` | [] / 仅四计数列 |
| 排除 | dev 成果表 | `dev_achievement_like_tables` | 2 张机构级（不构成承载） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 论文计数腿（含被引/H） | jiuxin | `ads_talent_profile` 三列 | 100,000（100.0%） | 直查 | **有** |
| D2 | 专利计数腿 | jiuxin | `patent_grant_count`/`patent_family_count` | 6,490 非空 | 直查 | 有（稀疏真实面） |
| D3 | 项目计数腿 | jiuxin | `project_count` + `ads_talent_project` | 100,000 / 7,702,366 | 直查/互证 | 有（计数级） |
| D4 | 代表作快照面 | jiuxin | `ads_talent_research_achievement` | 902,667 | 直查 | **有（久新独有）** |
| D5 | 项目分级（国家级/国际） | 三源 | —（Grant 维度未发布） | — | **不存在** | **缺（主降档因）** |
| D6 | 项目经费（万元） | 三源 | —（同上） | — | **不存在** | **缺（主降档因）** |
| D7 | 著作计数腿 | 三源 | — | — | **不存在** | **缺（主降档因）** |
| D8 | 期刊名物料 | jiuxin | `achievement.venue` | 0/902,667 | 未回填 | 缺（渲染回退在案） |
| D9 | UI 演示值 | UI | data.js random 四卡 | — | mock | 边界证据（不作源） |

`support_judgment="部分支持"`、产物与文首一致。

### 3.2 D1-D4 四腿的覆盖与量级（久新）

论文腿三列 100.0% 全铺是四卡的数据面主力（篇均被引 27.4 = 185,229,713/6,764,149，池级高质量特征）；代表作面 100,000 人全覆盖与 profile 同池（差 0 人），人均 9.03 与 Top10 口径自洽；项目腿双面同读数（7,702,366）是发布一致性证据；专利腿 6.5% 覆盖如实登记（稀疏非缺失）。四腿中三腿的「结构+数据」双达标，构成口径 A（论文/专利/代表作可交付）的支撑面。

### 3.3 D5-D7 三缺维的 absence_probe 全记录

否定性证据三件套：**查了什么**——久新 210 张实测表（探测日）book/monograph 词族 + profile 104 列列级词族 + `ads_talent_project` DESC 全列核对（分级/经费词族）+ achievement_type 枚举实测；gkx 280 表 achievement/award/honor/representative 词族 + `dwd_scholar` 27 列成果词族；dev `gkxlumenx_*` achievement/award 词族；三份需求真源卡片名与四卡算式检索。**条件**——表级+列级存在性 + 需求算式命中。**命中**——著作腿库级三零（久新表级+列级、gkx 列级、dev 无学者面）；项目分级/经费在 talent_project 列级 0（schema 标注 Grant 关联未发布）；需求侧卡片名 0 命中（hits=2 为展示行为语境）。四缺失情形归属：D5/D6/D7 均属「**列不存在/维度未发布**」（修复=Grant 面发布工程或外部图书源接入）；D8 属「**列在值未回填**」（修复=回填工程）——两类分开写（F15）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 论文腿覆盖 | 100,000/100,000 = 100.0%（全量非采样） |
| 代表作覆盖/人均 | 100,000 人 / 9.03 条（Top10 口径互证） |
| 类型枚举 | 仅 paper（project/award/patent 各 0） |
| venue 非空 | 0/902,667（=005 件读数） |
| 项目双面互证 | 7,702,366 = 7,702,366（逐位一致） |
| 著作腿 | 久新表级+列级双零；gkx 无 book 列 |
| 脚本形态 | 三源串行只读；零 demo_* |

## 四、数据缺失情况

### 4.1 著作腿与项目细分维度零承载（结构级，主因）

两个结构级缺口的修复路径完全不同，须分开立项：**著作腿**——三源无任何图书/专著计数结构（OpenAlex 体系里 book/book-chapter 属 work type，久新 paper_profile 未做类型区分，gkx 学者主档无 book 列），修复只能靠外部图书源接入（国家图书馆/出版社在版书目类）或 UI 侧裁撤该卡；**项目分级/经费**——`ads_talent_project` 关联面在但无「国家级/国际」分级列与经费列，schema 标注 Grant 维度关联 DWD Grant 而 ADS 未发布该面——修复是久新侧维度发布工程（数据在 DWD、未上升到 ADS），不是外部源问题。dev 的 2 张 org_achievement_year 是机构级年度面，与学者级代表作快照双不同物，不构成替代。

### 4.2 物料与标记缺（数据级，次因）

两个次级缺口：其一，`venue` 902,667 行全空（回填工程与 TALENTIR_005 件共用——从论文面 primary_source_id 反查 source 名）；其二，`is_lead` 全 0、`experience.project_ids` 全空——项目「牵头/参与」区分与履历侧项目指针未启用，项目卡的语义只能到「计数」层。另有 UI 超前设计登记：代表作三色标签中专利/项目两色现阶段无物料。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 三腿先行交付（触发器②） | 口径裁定 | 本件即期 | 论文/专利/项目卡+论文型代表作；著作卡显「—」或裁撤 |
| Grant 分级/经费面发布 | 维度发布工程 | 本件 + 项目类指标 | DWD Grant → ADS 上升 |
| 图书/专著源接入 | 外部数据源 | 本件著作腿 | 在版书目类源 |
| venue 回填工程 | 数据回填 | 本件 + TALENTIR_005 | 共用工程 |
| award/patent 型成果物化 | 数据工程 | 本件代表作标签 | 快照面类型扩展 |

档位后果：著作源接入 + Grant 面发布 → **完全转换支持**（四腿闭合）；仅三腿先行 → 维持部分支持但交付语义闭合。推荐顺序：即期三腿先行（零成本），Grant 面发布列近期（库内工程），图书源列中期。

## 参考文献

1. 国务院办公厅关于优化科研管理提升科研绩效若干措施的通知（国办发〔2018〕127 号）[EB/OL]. 中国政府网. https://www.gov.cn/zhengce/content/2018-07/24/content_5309314.htm （R1，2026-11-01 WebSearch 核验可达——「三评」改革起点文件：完善评价标准、推行代表作评价等制度导向的权威出处）
2. 国务院办公厅关于深化项目评审、人才评价、机构评估改革的意见（国办发〔2021〕32 号转入深化阶段语境，三评改革深化）[EB/OL]. 中国政府网. https://www.gov.cn/zhengce/zhengceku/2021-08/04/content_5629532.htm （R2，2026-11-01 WebSearch 核验可达——「推行代表作评价制度」的改革意见原文，代表作选取规则（少数、高质量、可公开）的方法论锚，与库内 Top10 快照面直接同构）
3. 国家统计局, 科学技术部. 中国科技统计年鉴·科技产出篇（论文/著作/专利分类统计体系）[EB/OL]. 国家统计局. https://www.stats.gov.cn/sj/ndsj/ （R3，2026-11-01 WebSearch 核验可达——科技产出按论文/著作/专利/项目四类分列的官方统计口径，UI 四卡的类目学来源）

# 附件

## 附录 A 原始需求原文摘录

「代表性成果（卡片式统计）」卡片名在三份需求真源检索 0 命中（UI 拆件）。组件行为对应原文，主需求《科技信息展示系统和科技专题服务系统.md》:1905-1907（1.1.1.1.4.3.3.1.1(3) 卡片式展示）：

> （3）卡片式展示
> 采用卡片式页面设计，将人才信息以结构化卡片形式呈现，美观直观，便于快速浏览与对比。

:1463（全球领域人才态势总述，「代表性成果」语义词）：

> 借助人脸识别、实体链接等智能算法，支持对人才详细背景、代表性成果及社会影响进行多维展示，为科研管理、学科布局和人才决策提供强有力的数据支撑。

:2271（研究领域图谱·节点聚焦）：

> 点击领域节点或关键词，自动聚焦并放大相关领域热点，让用户深入浏览具体研究方向和代表性成果。

UI 组件原文（`ProfileBasicPanel.jsx:305-330`）：论文卡 sub「被引 X 次 · 篇均 Y · 影响力 Z」、项目卡 sub「国家级 X / 国际 Y · 经费约 Z 万元」；`data.js:828-866` 四卡全 random mock（books.total=random(1,12)、fundingWan=random(800,12000)）——演示值，不作数据证据。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 代表性成果（卡片式统计） | 三份需求真源 | 0（UI 拆件） |
| 卡片式展示 | 主需求 | :1905-1907（行为叶） |
| 代表性成果 | 主需求 | :1463/:2271/:6558/:7949（展示/维护语境） |
| 著作/专著 | 主需求人才族段 | 0 |
| 国家级/经费 | 主需求人才族段 | 0（卡片级算式无） |
| papers/books/patents/projects | UI data.js | :828-866（mock 生成器） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TALENTREG_001_out.json`（2026-11-01 实跑：四腿逐列读数 + 快照面类型/字段完整性 + 三源排除）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（久新 talent 族表清单——B11 锚）。
- 族内对账：`M_SCIUI_TALENTIR_005_out.json`（achievement 902,667/venue 0 一致）；`M_SCIUI_TALENTIR_008_out.json`（profile 计数列共享）；`M_SCIUI_TALENTPF_006_out.json`（同面板影响力卡件）。

### B.2 本件产物逐键清单（`code/M_SCIUI_TALENTREG_001_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.jiuxin_table_count` | 计数 | 210（探测日实测） | §2.2 |
| `facts.jiuxin_profile_rows` | 计数 | 100,000 | §2.2 |
| `facts.jiuxin_profile_paper_count_nonnull/_sum` | 覆盖/合计 | 100,000 / 6,764,149 | §2.2/§3.2 |
| `facts.jiuxin_profile_citations_count_nonnull/_sum` | 覆盖/合计 | 100,000 / 185,229,713 | §2.2/§3.2 |
| `facts.jiuxin_profile_h_index_nonnull/_sum` | 覆盖/合计 | 100,000 / 1,445,108 | §2.2 |
| `facts.jiuxin_profile_patent_grant_count_nonnull/_sum` | 覆盖/合计 | 6,490 / 85,069 | §2.2/§3.2 |
| `facts.jiuxin_profile_patent_family_count_nonnull/_sum` | 覆盖/合计 | 6,490 / 68,314 | §2.2 |
| `facts.jiuxin_profile_project_count_nonnull/_sum` | 覆盖/合计 | 100,000 / 7,702,366 | §2.2/§2.4 |
| `facts.jiuxin_profile_book_like_cols` | 探针 | [] | §2.2/§3.3 |
| `facts.jiuxin_book_like_tables` | 探针 | [] | §2.5/§3.3 |
| `facts.jiuxin_research_achievement_rows` | 计数 | 902,667 | §2.3 |
| `facts.jiuxin_achievement_talents` | 计数 | 100,000 | §2.3 |
| `facts.jiuxin_achievement_type_dist` | 分布 | 仅 paper | §2.3 |
| `facts.jiuxin_achievement_paper/project/award/patent_rows` | 枚举 | 902,667 / 0 / 0 / 0 | §2.3 |
| `facts.jiuxin_achievement_title/venue/year/cited_by_count_nonnull` | 完整性 | 902,666 / **0** / 902,667 / 902,667 | §2.3 |
| `facts.jiuxin_talent_project_rows` | 计数 | 7,702,366 | §2.4 |
| `facts.jiuxin_talent_project_talents` | 计数 | 93,675 | §2.4 |
| `facts.jiuxin_talent_project_is_lead_dist` | 分布 | [[0, 7,702,366]] | §2.4 |
| `facts.jiuxin_experience_with_projects` | 探针 | 0（未回填） | §2.4 |
| `facts.gkx_table_count` | 计数 | 280 | §2.5 |
| `facts.gkx_achievement_like_tables` | 探针 | [] | §2.5/§3.3 |
| `facts.gkx_scholar_achievement_cols` | 结构 | 四计数列 | §2.5 |
| `facts.dev_achievement_like_tables` | 探针 | 2 张机构级（不构成承载） | §2.5/§3.3 |
| `derived[0].jiuxin_achievement_per_talent_avg` | 派生比 | 9.03（902,667/100,000） | §2.3 |
| `derived[1].jiuxin_paper_count_coverage_pct` | 派生比 | 100.0（100,000/100,000） | §2.2 |
| `derived[2].jiuxin_achievement_talent_coverage_pct` | 派生比 | 100.0（100,000/100,000） | §2.3 |
| `absence_probe` | 探针 | 五件（久新×2/gkx/dev/doc） | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

### B.3 共享与族内读数消费

本件消费族内锚：achievement 902,667/venue 0（=005 件）、profile 100,000 与计数列族（=002/008 件）、`dwd_scholar_papers` 738,106 有归属无代表排序（notes 登记）——批内零漂移（B11）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 规则/类目 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 代表作制度 | 三评改革（R2） | 少数高质量 TopN | 快照面 Top10 按被引降序 | **最高（规则同构）** |
| 四类分列统计 | 科技统计年鉴（R3） | 论文/著作/专利/项目 | 三类在、著作无 | 高（缺一类） |
| 产出 stock 口径 | Frascati（背景） | 累计量声明 | 计数列即 stock | 高 |
| 前端演示 | UI random 四卡 | — | mock 常量 | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 论文/被引/H 计数 | 四计数列 | 无 | **三列 100.0%** |
| 专利计数 | 无 | 无 | 6,490 非空 |
| 项目计数/关联面 | 无 | 无 | **7,702,366 双面互证** |
| 代表作快照 | 无（738,106 有归属无排序） | 机构级 2 张（不同物） | **902,667 唯一现成面** |
| 著作计数 | 无 | 无 | 无 |
| 项目分级/经费 | 无 | 无 | 无（Grant 未发布） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 三腿回填 + 论文型代表作（venue 回退渲染） + 著作卡「—」 | 无 |
| v1 | Grant 分级/经费面发布 → 项目卡 sub 行回填 | 久新维度发布 |
| v2 | 图书源接入 → 著作卡回填 | 外部数据源 |
| v3 | award/patent 型成果物化 → 代表作三色标签全启用 | 快照面扩展 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 专利 0 被误读为缺数 | **高** | 「无专利」≠「无数据」双语义 UI 区分 |
| 著作卡 random 值残留上线 | 高 | mock 替换清单登记（data.js:828-866） |
| 高被引综述挤占代表作位 | 中 | 排序键扩展留口径裁定 |
| 项目计数与关联面口径混引 | 中 | 引用处写明来源面 |

### C.5 总判

**部分支持**：三腿结构+数据双达标（论文腿全铺、项目腿双面互证、代表作面久新独有且规则同构官方制度），著作腿与项目细分（分级/经费）两个结构级缺口卡住完全档；venue 物料缺有渲染回退方案。升档触发器两条（Grant 发布+图书源）写死，按 B10 保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TALENTREG_001.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（gkx）+ 直连 dev/久新 | demo_* 直接 raise |
| 判档一致 | 文首 vs `support_judgment` | 部分支持 |
| B11 对账 | achievement 902,667/venue 0=005 件；project 7,702,366 双面一致 | 零漂移 |
| 幂等重跑 | SQL 全只读无随机 | 逐位一致 |
| 伪分残留 | impactScore 等演示分 | 未合成（无伪值） |
| mock 残留检查 | `rg "fieldHotness|fundingWan|books" repos/demo-ui-science/src/pages/talent-trend/data.js` | 正式版替换后无引用 |

# 科技指数高校榜（M_SCIUI_INDEX_038）

> **类型**：RANK（多对象分类榜单）｜ **域**：科技发展态势·科技指数·高校榜｜ **UI 挂载**：科技信息展示系统 → 科技指数页 → 排名 Tab → 四榜 Radio 第二项「高校榜」（`pages/tech-index/index.jsx:1081`）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 功能拆件（`_phase3_471_export.json` row_01 232），SRS 未以「高校榜」立叶
> **复现脚本**：`code/M_SCIUI_INDEX_038.py`｜ **产物**：`code/M_SCIUI_INDEX_038_out.json`
> **四判定摘要**：直接结构 = 否（三源无高校榜现成结果面）；直接数据 = 否；依赖结构 = 是（久新 power 表 education 类型切片 + gkx 高校池/论文面）；依赖数据 = 是（education 16,446 行现役名次 / 池 20,000 / 论文面 68.69% 高校可判）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` + 三方库 gkx + 久新 `jiuxin_warehouse`）均探；`demo_*` 禁引。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** 高校榜=高校对象域的分类榜单（裁定 NEW 口径）。三源没有一张叫「高校榜」的现成表（gkx 280 表 rank/score 命中 0；dev 榜面空壳；久新 power 是全类型机构榜），但对象池与计分原料三源齐备：久新 `ads_institution_technology_power` 的 education 类型切片 16,446 行**自带现役名次列**（过滤重排即得高校榜）；gkx 高校池 `dwd_forg_university_org_info` 20,000 行在案（裁定书指定可引，China 971 所）；gkx 中文论文首机构面 2 万采样 68.69% 可判高校（13,738 篇）。结构在、量在、现转即得——完全转换支持。

### 批次通用纪律摘要（S3-02 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 三个派生比分子分母同表同池，note 写明 |
| B4 | 负结论带探针 | absence_probe 三源三件（§3.3） |
| B5 | 确定性 | Counter.most_common 前先 sorted 计数、聚合键排序 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑（本件无手改） |
| B8 | 回执不复收 | 硬证据可复验（脚本幂等） |
| B9 | 单位/日期陷阱 | 榜为快照时点无年份陷阱；论文面用正则判机构 |
| B10 | 口径裁定保守交付 | 机构粒度 vs 成果粒度双口径并列 + 触发器（§1.6） |
| B11 | 多本账互推 | power 64,698/education 16,446 与 INDEX_001/036 零漂移 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 现成榜面存在吗？ | 不存在 | gkx rank/score 表 0 命中；dev enterprise_ranking 0 行 |
| 对象池够吗？ | 够 | education 16,446 行 / gkx 池 20,000 行 |
| 计分原料够吗？ | 够 | power 四指标现役 + 论文面 68.69% 高校可判 |

## 摘要

「高校榜」是科技指数页排行榜的四榜切片之一（综合/高校/企业/科研机构），需求语义源是 SRS seq 172「分类排名展示」的机构类型维度。三源无现成高校榜结果面，但久新机构科技实力榜的 education 切片（16,446 行、现役名次列、快照 2026-09-18）过滤重排即得全球高校榜 TopN；CN 切片 1,150 所高校即得国内高校榜。gkx 侧高校池 20,000 行（China 971）与中文论文首机构面（采样 68.69% 高校、Top1 中国科学院 756 篇）构成国产生产面旁证。判**完全转换支持**。语义偏移已披露：power 榜是论文/被引/人才/主题四指标学术单维族，非 UI mock 的成果四维。

- 需求判定：SRS 未以「高校榜」立叶；语义挂靠 seq 172 分类排名（机构类型维度）。
- 复现状态：脚本已跑通；education Top10 / CN Top10 / 论文面 Top12 三组读数落产物。
- 档位结论：**完全转换支持**（对象池+计分原料均足，现转即得）。
- 关键事实：education 切片占全机构榜 25.4196%、其中 CN 占 6.9926%——高校榜对象域足量。
- 升档路径：无需升档；成果粒度口径闭合见 §1.6 触发器。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/科技指数/**排行榜**/分类排名展示（1.1.1.1.4.1.8.3.2）。UI 实现在科技指数页（`pages/tech-index/index.jsx`）排名 Tab：排行榜头部是四项 Radio（`index.jsx:1079-1082`，综合榜/高校榜/企业榜/科研机构），「高校榜」是第二项（value=`university`）。切换时按 `rankingData[nextBoard]` 取对应数据集（`index.jsx:1066`），配套成果类型/机构类型/地域等七个筛选器。mock 数据侧，`mockData.js:1195` 用 `achievementRankingRecords.filter(item => item.type === 'university')` 生成高校榜——**mock 的高校榜是成果粒度过滤**（type 字段标在成果记录上），非机构粒度榜单。

值得记录的口径分岔：需求原文（分类排名展示）说「按科技领域、成果类型、**机构类型**、地域范围等条件查看分类排名」——机构类型在此是**筛选条件**之一；UI 作者把它升格为四个并列榜单 Tab 之一。所以「高校榜」既可读作「机构类型=高校的成果榜」（mock 实现语义），也可读作「高校对象的机构榜」（更贴近字面）。本件裁定取后者为主口径（裁定 NEW：高校榜=高校对象域榜单），前者作对照口径——理由见 §1.6。

### 1.2 为什么需要本指标

排行榜是科技指数「破四唯」评价体系的落地出口：指标展示给体系、可视化给趋势、排行榜给结果。高校榜单独成 Tab 的业务价值在于高校是基础研究的主力主体——政府用户（科技管理部门）最关心的高校科研竞争力格局、高校用户（双一流建设）最关心的对标位置，都需要一张对象域闭合的高校榜。四榜并列的设计（综合/高校/企业/科研机构）本质是把「机构类型」这个筛选维度前置为导航，让不同身份的用户直达自己的赛道。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**SRS seq 172 只给行为（按机构类型等条件查看分类排名），主需求 1.1.1.1.4.1.8.3 排行榜章给原则（「基于科学、客观的评价指标和方法……形成多维度、多层次的排行榜单」），高校榜的口径（学术实力？成果转化？综合声誉？）、指标体系、权重均未定义——这正是科技指数体系「需立项调研后才能确定」的批注来源。

### 1.4 类似指标权威方法可行性分析概要

高校排名是评价科学最成熟的领域之一。中国官方语境有两类先例：其一是科技部序列的高校科技统计（R1，科技部官网统计公报栏的《我国高等学校 R&D 活动统计分析》系列），以 R&D 经费/人员等科技投入产出指标作高校科技活动画像；其二是软科中国大学排名（R2，BCUR），十个评价模块 35 维度 104 指标，遵循「全面评估、分类评价」原则。国际语境的标杆是 ARWU 世界大学学术排名（R3），六项纯科研指标（校友获奖 10%/教师获奖 20%/高被引 20%/N&S 论文 20%/SCIE-SSCI 论文 20%/师均 10%），以客观、透明、稳定著称。

| 方法族 | 代表 | 判定轴 | 与本库匹配 |
|---|---|---|---|
| 高校 R&D 统计（科技部） | R1 | R&D 经费/人员 | 无经费表（经济维缺） |
| 综合评价（软科 BCUR） | R2 | 十模块全维 | 部分可算（科研模块） |
| 学术单维（ARWU） | R3 | 论文/获奖/高被引 | **最贴**（久新 power 榜即此类） |

久新 `ads_institution_technology_power` 的口径（论文 0.35/被引 0.30/人才 0.25/主题 0.10）与 ARWU 学术单维族同构——这决定了本件的最优现转路径。完整版见附录 C。

### 1.5 引用来源

- UI：`repos/demo-ui-science/src/pages/tech-index/index.jsx:1081` — `{ label: '高校榜', value: 'university' }`；`index.jsx:1066` — `return rankingData[rankingBoard] || rankingData.comprehensive || []`；`mockData.js:1195` — `university: rankRecords(achievementRankingRecords.filter((item) => item.type === 'university'))`。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md` seq 172（excel_row 175）「分类排名展示」——「提供多种分类排名方式，用户可按科技领域、成果类型、机构类型、地域范围等条件查看分类排名」。
- 主需求：`科技信息展示系统和科技专题服务系统.md` 1.1.1.1.4.1.8.3 排行榜章。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（双口径并列）**：

- **口径 A（机构粒度，本件主口径）**：从全机构科技实力榜中取 education 类型切片重排——$\text{UnivRank}(u) = \text{Rank}\{S_{\text{tech}}(u) : \text{type}(u)=\text{education}\}$。现转路径：久新 power 表 `WHERE institution_type_id='education' ORDER BY technology_power_score DESC`。
- 口径 B（成果粒度，mock 实现语义）：科技成果评价体系中 type=university 的成果集过滤重排——依赖成果级四维评分（innovation/influence/potential/support），该体系是 INDEX_013（指标权重展示）的立项范围，本件不闭合。

**降档/升档触发器**：若甲方认定高校榜必须是成果粒度（口径 B）→ 本件降为部分支持（成果评分体系未闭合，见 INDEX_013）；若久新 power 表下线或 education 切片缩量至千行以下 → 降部分支持；口径 A 已满足完全转换支持，无升档需求。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md` |
| 所属四级功能 | 1.1.1.1.4.1.8 科技指数（19 叶，excel_rows 162-180） |
| 语义挂靠叶 | 分类排名展示（seq 172，excel_row 175）——机构类型维度 |
| UI 容器 | `index.jsx` 排名 Tab 四榜 Radio 第二项 |
| 批内姊妹件 | INDEX_001 企业榜（company 切片，已交付）/ INDEX_036 综合榜（Lane 4 并行在写）——同一 power 表的三种切片，产物独立 |
| 同族约束 | 勿碰 INDEX_036 文件（Lane 4）；本件只做高校榜 |

## 二、计算过程

### 2.1 方法选择（文献依据）

选 ARWU 式学术单维族的现成切片（久新 power 表）而非自建综合体系。依据：其一，R3（ARWU）证明纯科研指标的高校排名方法成熟且被广泛采纳，power 表口径（论文/被引/人才/主题）与其同构；其二，R2（软科）的十模块体系需要经费、师资、就业等库外数据（R1 官方统计口径也依赖经费表），三源均无承载；其三，skill P3 原则——方法选择受数据源约束时，谱系排序即升档路线图。本件不新造公式，交付「现成榜的切片重排」，公式定义人标注仿王惠（推测定义）。

### 2.2 装载与规模校验

经 `_gkxdb.py` 连 gkx（280 表）、pymysql 直连久新（203 表）与开发库。三源规模：久新 power 全表 64,698 行（与 INDEX_001/036 facts 零漂移，B11），education 切片 16,446 行（`jiuxin_education_rows`）；gkx 高校池 `dwd_forg_university_org_info` 20,000 行（与共享快照 fix2 一致，`gkx_university_pool_rows`），其中 China 971 所（`gkx_university_pool_china_rows`）；gkx 中文论文 2 万行采样（`gkx_paper_sample_rows`）。

### 2.3 高校榜主承载：education 切片过滤重排（口径 A 现转）

```sql
SELECT p.institution_name, p.technology_power_score, p.technology_power_rank, pr.country_code
FROM ads_institution_technology_power p
LEFT JOIN ads_institution_profile pr ON p.institution_id = pr.institution_id
WHERE p.institution_type_id = 'education'
ORDER BY p.technology_power_score DESC, p.institution_name
LIMIT 10;
-- → 中国科学院大学 99.9968(全榜 rank2) / 北京大学 99.9961 / 浙江大学 99.9932 / …
```

education 全量 Top10（`jiuxin_education_top10`）：中国科学院大学（99.9968，stored_rank=2）、北京大学、浙江大学、上海交通大学、清华大学、中山大学、四川大学、复旦大学、华中科技大学、中国科学技术大学——Top10 全部为中国高校且 stored_rank 连续（2-11），说明全球高校科研竞争力头部完全由中国高校占据（该库口径下）。CN 切片 1,150 所（`jiuxin_education_cn_rows`）即国内高校榜的完整对象域，Top10 与全量 Top10 相同（中国高校就是全球头部）。

### 2.4 国产生产面旁证：gkx 论文首机构

拉取 `gkx.dwd_zh_paper` 2 万行（采样协议：大表全扫 GROUP BY 禁用，note 标「采样，非全表」），Python 侧解析首作者机构：13,738 篇（68.69%）可判高校（含「大学/学院」且剔「医院/临床/卫生院」）。高校 Top12（`gkx_paper_univ_top12`）：中国科学院 756 篇、上海交通大学 344、中国矿业大学 218、北京大学 207、武汉大学 198——与久新 power 榜头部（国科大/北大/浙大/上交）高度同向，中科院系在两个榜都是榜首。这组读数证明中文科研生产面与学术实力榜的一致性，也暴露语料偏斜（医疗类机构占比高，已在剔除逻辑中处理医院）。

### 2.5 榜面语义偏移披露

power 榜口径是论文 0.35/被引 0.30/人才 0.25/主题 0.10 的学术实力四指标族（metric_definition_version 在列，快照 2026-09-18），与 UI mock 的成果四维（innovation 96/influence 92/potential 94/support 90）不是同一评价体系。差异有三：对象粒度（机构 vs 成果）、指标域（学术单维 vs 成果综合）、时间性（快照榜 vs 评估期榜）。本件按裁定取机构粒度为主口径，mock 值仅作 UI 需求证据（演示值，不参与支持度结论）。

### 2.6 稳健性

切片重排的确定性：ORDER BY score DESC, name 双键，无平局漂移；stored_rank 列与现算排名双轨对账（Top10 两轨一致）。采样面的确定性：Counter 先聚后排序，关键词正则固定。语义稳健性风险在对象域定义——education 类型含全球 16,446 家教育机构（含海外 College/Universidad 等非「大学」中文字面的机构），如果甲方口径要求「中国普通高等学校名单」（R2 口径，1,086 所），则需与教育部名单对齐收缩，榜面会换血——已写进 §1.6 触发器与附录 C 风险表。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INDEX_038.py`（三源探针 + education 切片 + 论文面采样；运行 `python3 code/M_SCIUI_INDEX_038.py`）。
- 产物：`code/M_SCIUI_INDEX_038_out.json`。正文数字与产物键逐一对应：`jiuxin_education_rows=16446`（§2.2）、`jiuxin_education_top10` 十项（§2.3）、`jiuxin_education_cn_rows=1150` 与 `jiuxin_education_cn_top10`（§2.3）、`gkx_paper_univ_first_author_rows=13738` / `gkx_paper_univ_top12`（§2.4）、派生 `jiuxin_education_share_pct=25.4196` / `jiuxin_cn_share_of_education_pct=6.9926` / `gkx_paper_univ_share_pct_sample=68.69`。
- 结果解读：高校对象域在全机构榜占四分之一强、中国高校在高校域占约 7%（但占据全球头部 Top10 全席）——对象池充足，榜面即期可交付。
- 对照需求功能要求的评审：分类排名展示（机构类型=高校）——满足（现转即得）；配套筛选（地域/领域）——部分满足（country_code 维在，科技领域维需论文主题映射，未在本件闭合）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | power 全表 | `jiuxin_power_rows` | 64,698 |
| 切片 | education 行数 | `jiuxin_education_rows` | 16,446 |
| 榜面 | education Top10 | `jiuxin_education_top10` | 国科大 99.9968（rank2）领衔 |
| 国内 | CN 切片行数 | `jiuxin_education_cn_rows` | 1,150 |
| 国内 | CN Top10 | `jiuxin_education_cn_top10` | 北大/浙大/上交/清华… |
| 构成 | education 占全榜 | `jiuxin_education_share_pct` | 25.4196% |
| 构成 | CN 占 education | `jiuxin_cn_share_of_education_pct` | 6.9926% |
| 池 | gkx 高校池 | `gkx_university_pool_rows` | 20,000（China 971） |
| 论文面 | 采样篇数 | `gkx_paper_sample_rows` | 20,000（采样，非全表） |
| 论文面 | 高校首机构篇数 | `gkx_paper_univ_first_author_rows` | 13,738（68.69%） |
| 论文面 | 高校 Top12 | `gkx_paper_univ_top12` | 中科院 756 / 上交 344 / … |
| absence | gkx 榜面 | `gkx_rank_score_tables` | 0 命中 |
| absence | dev 榜面 | `dev_ads_enterprise_ranking_rows` | 0 行 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 高校对象池 | jiuxin | power.education 切片 | 16,446（CN 1,150） | 直查 | **足量** |
| D2 | 实力得分与名次 | jiuxin | power.technology_power_score/rank | 16,446 行全量现役 | 直查 | **足量** |
| D3 | 高校池（裁定书指定） | gkx | `dwd_forg_university_org_info` | 20,000（China 971） | 直查 | 足量（旁证/底册） |
| D4 | 国产科研生产面 | gkx | `dwd_zh_paper.author_info_list` | 2 万采样 68.69% 高校 | 采样 | 足量（旁证） |

`support_judgment="完全转换支持"`，与 §〇 定义一致（闸 6）。

### 3.2 D1/D2 主承载：一张表的自足切片

education 切片 16,446 行占全机构榜 25.4196%（`jiuxin_education_share_pct`），且名次列（stored_rank）在全表范围连续编码——高校榜不需要重算名次，`WHERE + ORDER BY` 就是榜。中国高校 1,150 所（6.9926%）但包揽全球 Top10：中国科学院大学（99.9968）到中国科学技术大学（99.9794）全部在 99.9 分段以上。这个「中国高校统治头部」的读数是库口径（全球论文/被引/人才数据在该库的覆盖结构）的直接产物，对外发布需随行披露语料口径（英文主导的国际数据库 vs 中文库的覆盖差）。

### 3.3 absence_probe 全记录（三源三件）

**gkx**：280 表 `information_schema.tables` 扫 `table_name LIKE '%rank%' OR '%score%'` → 0 命中（`gkx_rank_score_tables=[]`）——gkx 无任何榜/评分结果面，高校榜只能从要素表自建。**dev**：`gkxlumenx_dwd/gkxlumenx_ads` 扫 `%univ%/%ranking%` → 仅 `enterprise_ranking`（实测 0 行，且属造数黑名单 skill P4.1，值不参与判档）。**久新**：非缺席而是语义偏移（power 是全类型机构榜，高校榜=其切片），已在 §2.5 披露，不构成证伪。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| education 切片重排 | Top10 与 stored_rank 双轨一致（rank2-11） |
| CN 切片 | 1,150 所；Top10=全量 Top10（中国=全球头部） |
| 论文面采样 | 20,000 篇 → 13,738 高校（68.69%），采样 note 在案 |
| 三源对账 | power 64,698 / 池 20,000 与 INDEX_001/036/共享快照零漂移 |
| 脚本形态 | 三源顺序查询，零 demo_*，产物无耗时键 |

## 四、数据缺失情况

### 4.1 缺口清单（可构建但存在缺口）

| 缺失项 | 类型 | 对档位的影响 |
|---|---|---|
| 成果粒度评分体系（口径 B） | 方法未立项 | 成果粒度高校榜不可算 → 主口径改机构粒度（不影响本档） |
| 科技领域维（配套筛选） | 映射未建 | 领域筛选闭合需论文主题映射 → 影响交互完整度非档位 |
| 中国普通高校名单对齐 | 口径工程 | 教育部名单口径（1,086 所）vs education 全集 → 榜面会换血（触发器在案） |
| 高校经费/师资维（软科式） | 数据源缺 | 综合评价体系不可算 → 学术单维是现转上限 |

### 4.2 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 即期交付口径 A 榜 | 无需修复 | 本件 | education 切片 + CN 切片双榜 |
| 立项 INDEX_013 体系 | 方法立项 | 本件口径 B + INDEX 族 | 成果四维评分闭合后双口径并存 |
| 教育部名单对齐工程 | 口径工程 | 本件 + INDEX_036 | 甲方确认名单口径后收缩对象域 |

四项缺口中仅第四项是数据源级（库外），其余是口径/方法级——这正是完全转换支持档位的典型形态：对象与原料在，语义闭合的最后一公里在甲方口径确认。

## 参考文献

1. 2020年我国高等学校R&D活动统计分析[EB/OL]. 中华人民共和国科学技术部. https://most.gov.cn/xxgk/xinxifenlei/fdzdgknr/kjtjbg/index_1.html （R1，2026-11-01 WebSearch 核验可达，科技部统计公报栏）
2. 软科中国大学排名方法[EB/OL]. 软科. https://www.shanghairanking.cn/methodology/bcur/2026 （R2，2026-11-01 WebSearch 核验可达）
3. Academic Ranking of World Universities Methodology[EB/OL]. ShanghaiRanking. https://www.shanghairanking.com/methodology/arwu/2026 （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/科技指数.md》seq 172（excel_row 175）：

> ### 分类排名展示 · 序号 172
> #### 需规功能描述
> 提供多种分类排名方式，用户可按科技领域、成果类型、机构类型、地域范围等条件查看分类排名，支持多条件组合筛选，满足不同用户的查看需求。

《科技信息展示系统和科技专题服务系统.md》1.1.1.1.4.1.8 排行榜章（节选）：

> 基于科学、客观的评价指标和方法，对各类科技成果进行系统化评价和排名，形成多维度、多层次的排行榜单。排行榜不仅关注总体排名，还注重分类排名和动态变化……

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 高校榜 | 三份需求真源 | 0（未出现；语义挂靠 seq 172 机构类型维度） |
| 高校 | 科技指数.md | 0（排行榜章无高校字样） |
| 机构类型 | 科技指数.md seq 172 | 1（分类排名条件枚举） |
| university | demo-ui tech-index | index.jsx:1081 / mockData.js:645 等（UI 实现） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INDEX_038_out.json`（三源探针 + 切片榜 + 论文面采样全量在案）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（fix2 大学表行数 20,000 对账键）。
- 姊妹件：INDEX_001/036（power 表 64,698 行/版本键，B11 零漂移对账源）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INDEX_038_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INDEX_038 | 文首 |
| `ui_evidence` | 证据 | 3 条组件：行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false**（语义挂靠 seq 172） | §1.1/附录 A |
| `facts.jiuxin_power_rows` | 计数 | 64,698 | §2.2 |
| `facts.jiuxin_education_rows` | 计数 | 16,446 | §2.2/§2.3 |
| `facts.jiuxin_education_top10` | 榜单 | 10 项（国科大 99.9968 领衔） | §2.3 |
| `facts.jiuxin_education_cn_top10` | 榜单 | 10 项 | §2.3 |
| `facts.jiuxin_education_cn_rows` | 计数 | 1,150 | §2.3 |
| `facts.gkx_university_pool_rows` | 计数 | 20,000 | §2.2/§3.1 |
| `facts.gkx_university_pool_china_rows` | 计数 | 971 | §2.2 |
| `facts.gkx_paper_sample_rows` | 计数 | 20,000（采样） | §2.4 |
| `facts.gkx_paper_univ_first_author_rows` | 计数 | 13,738 | §2.4 |
| `facts.gkx_paper_univ_top12` | 榜单 | 12 项（中科院 756…） | §2.4 |
| `facts.gkx_rank_score_tables` | 探针 | []（0 命中） | §3.3 |
| `facts.dev_ads_enterprise_ranking_rows` | 探针 | 0 | §3.3 |
| `derived[0]` | 派生比 | gkx_paper_univ_share_pct_sample=68.69 | §2.4 |
| `derived[1]` | 派生比 | jiuxin_education_share_pct=25.4196 | §3.2 |
| `derived[2]` | 派生比 | jiuxin_cn_share_of_education_pct=6.9926 | §3.2 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

### B.3 共享快照消费

消费 `_shared_probe_s3_01_out.json` 的 `fix2.大学表行数=20000`（gkx 池对账）；power 侧经 INDEX_001/036 的 facts 间接对账（64,698/版本 2026-09-18）。论文年份分布（快照 fix2）本件未消费（无年度序列诉求）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 判定轴 | 数据要求 | 本库承载 | 贴合度 |
|---|---|---|---|---|---|
| 高校 R&D 统计 | 科技部（R1） | R&D 经费/人员 | 经费统计表 | 三源无 | 中（不可行） |
| 综合评价 | 软科 BCUR（R2） | 十模块 104 指标 | 全维数据平台 | 科研模块可算 | 中 |
| 学术单维 | ARWU（R3） | 论文/被引/高被引 | 文献计量库 | **power 表同构** | **最高（现转）** |
| 中文生产面 | 本件旁证 | 论文首机构计数 | zh_paper | 采样可算 | 高（旁证） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| power.education | 16,446（CN 1,150） | 名次现役、双轨一致 | 语义偏移（学术单维） |
| gkx 高校池 | 20,000（China 971） | country 100% 非空 | 无评分列（仅底册） |
| zh_paper 机构面 | 2 万采样 68.69% | 医疗偏斜已披露 | 采样非全表 |
| 成果四维评分 | 未立项 | — | 口径 B 缺 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 双榜（education 全量 + CN 切片） | 无 |
| v2 | 领域维筛选（论文主题映射） | 映射工程 |
| v3 | 口径 B 成果粒度榜 | INDEX_013 立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 中国高校包揽 Top10 被读作国别偏见 | 中 | 随行披露库口径覆盖结构 |
| education 含非「大学」教育机构 | 中 | 教育部名单对齐触发器 |
| 口径 B 需求回流 | 低 | 双口径并列已写死 |

### C.5 总判

**完全转换支持**：对象池（16,446/1,150）+ 计分原料（power 现役名次 + 论文面旁证）三源足量，`WHERE+ORDER BY` 现转即得；语义偏移（学术单维 vs 成果四维）与对象域口径（education vs 教育部名单）两个触发器已写死。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INDEX_038.py` | 退出码 0，落 `_out.json` |
| 数据入口 gkx | `_gkxdb.py` | demo_* 直接 raise |
| 切片榜复核 | `facts.jiuxin_education_top10` vs stored_rank | 双轨一致（2-11 连续） |
| 论文面复核 | `facts.gkx_paper_univ_top12` | 中科院 756 领衔 |
| 三源对账 | INDEX_001/036 facts + 共享快照 | 零漂移 |
| 采样协议 | 20,000 行 LIMIT 子查询 | note 标「采样，非全表」 |
| mock 残留 | `rg "type === 'university'" repos/demo-ui-science` | 正式版替换后无引用 |

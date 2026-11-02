# 科技指数企业榜（企业排名）（M_SCIUI_INDEX_001）

> **类型**：无业务逻辑数值类（榜单排名）｜ **域**：科技发展态势·科技指数·排行榜＞企业榜｜ **UI 挂载**：科技指数页 → 排行榜 Tab → 榜单切换 Radio「企业榜」
> **数据支持度**：**完全转换支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 拆件叶（`_phase3_471_export.json` row_01 183），三份需求说明书未出现「企业榜」独立叶
> **复现脚本**：`code/M_SCIUI_INDEX_001.py`｜ **产物**：`code/M_SCIUI_INDEX_001_out.json`
> **四判定摘要**：直接结构 = 否（三源无「科技指数四维」企业榜现成面）；直接数据 = 否；依赖结构 = 是（久新 `ads_institution_technology_power` 22 列含 rank/score/类型过滤键）；依赖数据 = 是（64,698 行全量，company 类 13,939 行）
> **数据源口径**：三源评估——开发库 `gkxlumenx_*` + 三方库 `gkx`（183.240.141.251:3318 只读）+ 久新库 `jiuxin_warehouse`（47.93.119.170:29030 只读）；本件主承载在久新。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** 三源无 UI 语义（四维加权科技成果综合榜、四榜 Radio 切换）的现成企业榜，dev 侧同名域表 `enterprise_ranking`/`enterprise_score` 属造数黑名单且实测 0 行（存在性披露、值不引用）；但久新 `ads_institution_technology_power`（64,698 行、22 列、含 `technology_power_rank`/`technology_power_score`/`institution_type_id`）按 company 类型过滤重排即得真实可读的企业科技实力榜——本件复现 Top10：Google (US) 98.9091 / BGI 华大 (CN) 98.8549 / 中石化 98.7811 / 腾讯 98.5585 / 华为 98.4349 等（facts `jiuxin_company_top10_by_tech_power` 全枚举）。判档压力仅在维度语义（科技实力四指标单维族 vs UI 四维综合）——结构、量、排名列三证齐备，现转即得。

### 批次通用纪律摘要（S3-02 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 企业占比分子分母同表；差值键分母=1 标注非比值 |
| B4 | 负结论带探针 | 三源榜面探针逐一留证（§3.3） |
| B5 | 确定性 | Top10 `ORDER BY score DESC, name` 双键破平局 |
| B6 | 闸门自身被闸 | 本批不自跑闸门 |
| B7 | 产物只由脚本产出 | 改脚本→重跑 |
| B8 | 回执不复收 | 派单方硬复验 |
| B9 | 单位/日期陷阱 | 得分 decimal(9,6) 精度保持；无年份列 |
| B10 | 口径裁定保守交付 | 维度双口径（实力榜/综合榜）+ 触发器（§1.6） |
| B11 | 多本账互推 | 64,698 与类型分布四和自洽在案 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 排名列存在吗？ | 存在 | `jiuxin_power_rows=64,698` 含 rank 列（facts） |
| 企业子池够大吗？ | 够 | `jiuxin_power_by_type.company.rows=13,939`（facts） |
| 榜单现转跑通了吗？ | 跑通 | `jiuxin_company_top10_by_tech_power` 十行（facts） |

## 摘要

「科技指数企业榜」是科技指数页排行榜 Tab 四榜 Radio（综合榜/高校榜/企业榜/科研机构）之一，语义源是 SRS 科技指数.md seq 172「分类排名展示」（「按科技领域、成果类型、机构类型、地域范围等条件查看分类排名」——机构类型筛选即四榜切分的语义根据）。数据侧判定：dev 同名域表为造数黑名单且 0 行、gkx 无任何 rank/score 结果面；久新 `ads_institution_technology_power` 64,698 行是三源唯一的企业可切排名面——company 类型 13,939 行，过滤重排一次跑通出真实 Top10（Google/华大/中石化/腾讯/华为/中石油/西电/阿里/微软/国家电网）。判**完全转换支持**；维度语义偏移（论文 0.35/被引 0.30/人才 0.25/主题 0.10 的科技实力单维族，非 UI 四维加权）按 B10 双口径披露。

- 需求判定：UI 拆件叶（「企业榜」非独立需求叶），语义挂 seq 171/172 排行榜族。
- 复现状态：脚本已跑通；规模/类型分布/Top10/分数分布/两个派生五组读数落产物。
- 档位结论：**完全转换支持**（结构+量+过滤重排在案）。
- 关键事实：dev `enterprise_ranking`/`enterprise_score` 实测 0 行——「表存在但 0 行」与「造数黑名单」双重披露，不得当结果面。
- 升档/降档触发器：见 §1.6（接受实力榜口径→现档即交付态；要求四维综合榜→需 INDEX 族权重件闭合后重算）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/科技指数/**排行榜**。UI 挂载点 `pages/tech-index/index.jsx:1082`：排名 Tab 的榜单切换 `Radio.Group`，options=`[{综合榜}, {高校榜}, {企业榜}, {科研机构}]`（`value='enterprise'`）——「企业榜」是企业类型机构对象的结果榜。切换时联动五维筛选（成果名称搜索/科技领域/成果类型/机构类型/地域）与导出（`exportRange` all/compare/current，mockData `rankingData.enterprise` 为数据源）。榜单行结构（mockData `applyEvaluationModel`）：`totalScore`（四维加权）+ 四维分 + `weightContributions`（分维贡献）——mock 注释明写「totalScore/weightContributions/evaluationMethod 一律由四维得分派生，禁止手写」，这是前端作者对榜单口径的自白：榜分必须可分解到维度。

### 1.2 为什么需要本指标

四榜切分回答「谁在领跑」的分对象叙事：综合榜给全景、企业榜给产业侧锚点——对招商/投资/供应链用户，企业榜的实操价值高于综合榜（专利密集度、成果转化活性直接可比）。分类排名是 SRS seq 172 的明文需求（「满足不同用户的查看需求」），企业榜是其机构类型维度的落地。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「企业榜」三字未独立出现在三份需求真源；seq 171「科技成果综合排名」与 seq 172「分类排名展示」给的是功能行为（TopN/筛选/排名变化趋势），对企业榜的得分构成（哪些维度、怎么加权、企业对象池怎么定）无一字定义。检索记录见附录 A。

### 1.4 类似指标权威方法可行性分析概要

企业创新能力排名的官方范式是国家创新调查制度（R1）的企业创新能力评价指标体系（科技部 2013 年发布、监测评价指标双轨）；国际侧 WIPO 全球创新指数（GII）的机构维度与企业研发记分牌提供方法参照。方法族对照：

| 方法族 | 代表 | 对象池 | 维度 | 与本库匹配 |
|---|---|---|---|---|
| 官方企业创新能力评价（R1） | 科技部/统计局 | 规上企业名录 | 多维加权 | **部分**（需企业名录+经济数据） |
| 学术实力榜（久新现役） | OpenAlex 机构体系 | 全球机构含企业 | 论文/被引/人才/主题 | **有（64,698 行现役）** |
| UI mock 四维模型 | buildForecast 族 | mock 记录 | 四维加权 | 演示值 |

久新现役面是企业子池可切的唯一现成榜。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-index/index.jsx:1082` — `{ label: '企业榜', value: 'enterprise' }`；`:1060-1070` 切换联动重置筛选。
- mockData：`repos/demo-ui-science/src/pages/tech-index/mockData.js:1196` — `enterprise: rankRecords(achievementRankingRecords.filter(item => item.type === 'enterprise'))`；`:1276` 排行类型枚举含「企业排行」；`:1166-1176` 四维派生注释（禁手写）。
- SRS：`…/科技发展态势/科技指数.md` seq 171/172（排行榜族），原文见附录 A。

### 1.6 推测原意与推测定义

**推测定义**：企业对象池 $E=\{o: type(o)=company\}$ 按综合得分降序的 TopN 榜，行含总分+分维分+名次。

- **口径 A（建议口径：科技实力企业榜）**：$E$=久新 power 表 company 类（13,939 家），总分=technology_power_score（论文 0.35/被引 0.30/人才 0.25/主题 0.10 加权）——现转即得，维度语义偏移须披露；
- 口径 B（UI 语义：四维科技成果综合榜）：维度=科技创新能力 0.4/影响力 0.3/潜力 0.2/保障 0.1，对象含企业的「科技成果」——需 INDEX 族权重件（M_SCIUI_INDEX_013）口径闭合后重算，现无现成面。

**降档/升档触发器（B10 模板）**：甲方接受口径 A → 维持完全转换支持且即期交付；坚持口径 B → 依赖 013 权重立项+四维分列建设，期间降**部分支持**（维度半缺）；若企业池要求国内注册口径（非 OpenAlex 全球体系）→ 需与 gkx/live 企业底册（189,116 行）映射，另立工程。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所属四级功能 | 科技指数（SRS seq 159–177） |
| 本件叶 | 企业榜（UI 拆件，row_01 183） |
| 同 Radio 姊妹叶 | 综合榜（INDEX_036）/ 高校榜（INDEX_038）/ 科研机构榜（本批外） |
| 榜单族相邻叶 | 排名历史变化（INDEX_019）/ 排名对比分析（INDEX_020）/ 筛选搜索（seq 176） |
| 权重侧联动件 | M_SCIUI_INDEX_013 指标权重展示（口径 B 前置） |

与 INDEX_036（综合榜）的分工：036 是全对象总榜（「多对象榜单非单指数读数」），本件是其企业切片——两件共享同一久新承载面与过滤重排路径，口径 A 下同源同构；差异在对象过滤键与叙事（产业侧 vs 全景）。

## 二、计算过程

### 2.1 装载与规模校验

pymysql 直连久新只读库。主面 `ads_institution_technology_power` 64,698 行、22 列（含四指标计数列、四分项得分列、四权重列、总分、总名次、基准池数），版本面：`metrics_as_of_date=2026-09-18`、`metric_definition_version=institution_technology_power_mvp_v1` 全表单版本（facts `jiuxin_power_version`）——单快照单口径，跨行可比性有版本保障。

### 2.2 类型分布与企业子池

`GROUP BY institution_type_id` 实测（facts `jiuxin_power_by_type`）：education 16,446 / **company 13,939** / healthcare 10,877 / facility 9,021 / government 及其余类型随产物全枚举。企业子池名次范围 [545, 64,693]——全类型榜首（中科院，rank 1）到榜尾之间企业占据中高段，企业榜榜首全球名次 545（Google），这与学术尺（论文/被引主导）下企业天然让位于高校/院所的结构一致，是口径 A 必须随行披露的榜单性质。

### 2.3 企业榜 Top10 复现（过滤+重排）

company 过滤 + `ORDER BY technology_power_score DESC, institution_name` 双键（B5）重排 Top10（facts `jiuxin_company_top10_by_tech_power` 全枚举）：Google (United States) 98.9091 / BGI Group (China) 98.8549 / Sinopec (China) 98.7811 / Tencent 98.5585 / Huawei 98.4349 / CNPC 98.3434 / China XD Group 98.2709 / Alibaba 97.9821 / Microsoft (United States) 97.8688 / State Grid 97.8588——中美头部企业交错、可读性强。每行随附 paper/cited_by/talent 计数与 global_rank（全类型名次），满足 mock 行结构「总分+分维+名次」的最小形态。

```sql
SELECT institution_name, technology_power_score, technology_power_rank
FROM ads_institution_technology_power
WHERE institution_type_id = 'company'
ORDER BY technology_power_score DESC, institution_name LIMIT 10;
-- → Google 98.9091 / BGI 98.8549 / Sinopec 98.7811 / …（十行）
```

### 2.4 分数分布与派生读数

企业子池分数 min/max/avg 落产物（facts `jiuxin_company_score_min_max_avg`）——分布非退化（非全体同分），区分度满足榜单可用性标准。两个派生（B3）：`jiuxin_company_share_pct`=21.5447%（13,939/64,698，同表同池占比）与 `jiuxin_company_top1_vs_alltype_top1_score_gap`=1.0901（全类型榜首分−企业榜首分，差值键分母=1 显式标注非比值——衡量企业在学术尺上的天花板落差）。

### 2.5 稳健性与口径敏感性

口径 A/B 的名次敏感性：两口径维度族不同（学术四指标 vs 创新四维），企业榜名次必然重排——本件 Top10 是口径 A 名次，不得当作 UI 综合榜名次对外。对象池敏感性：OpenAlex company 类型含全球企业（Google/Microsoft 在列），国内口径用户需再过滤国别——`institution_profile` 表有 country 维可切（本件未下钻，列为触发器③的工程面）。

### 2.6 复现代码结果展示

- 代码：`code/M_SCIUI_INDEX_001.py`（pymysql 直连久新 + `_gkxdb.py` 走 gkx 探针 + dev 造数面行数探针）；运行 `python3 code/M_SCIUI_INDEX_001.py`。
- 产物：`code/M_SCIUI_INDEX_001_out.json`。正文数字对应键：`jiuxin_power_rows=64698`、`jiuxin_power_by_type`（§2.2）、`jiuxin_company_top10_by_tech_power`（§2.3）、`jiuxin_company_score_min_max_avg`（§2.4）、两个 derived（§2.4）。
- 结果解读：三源唯一企业可切排名面过滤重排一次成功；Top10 真实可读、分布有区分度、企业子池量级 13,939 足够 TopN 任意深度。
- 对照需求功能要求的评审：企业榜 Tab 回填——**有条件通过**：口径 A 即期可供（Top10+全深榜+计数明细）；未通过点=维度语义与 UI 四维不同构、国内口径需国别二次过滤（触发器见 §1.6）。

### 2.7 分步证据对照表

| 步骤 | 证据项 | 产物键 | 数值 |
|---|---|---|---|
| 装载 | 榜面行数 | `jiuxin_power_rows` | 64,698 |
| 装载 | 版本快照 | `jiuxin_power_version` | 2026-09-18 × mvp_v1 |
| 子池 | company 行数 | `jiuxin_power_by_type.company.rows` | 13,939 |
| 子池 | 企业名次范围 | `jiuxin_power_by_type.company.{rank_min,rank_max}` | [545, 64,693] |
| 榜单 | Top10 | `jiuxin_company_top10_by_tech_power` | Google 98.9091 / BGI 98.8549 / … |
| 分布 | 企业分 min/max/avg | `jiuxin_company_score_min_max_avg` | （产物在案） |
| 派生 | 企业占比 | `jiuxin_company_share_pct` | 21.5447%（13,939/64,698） |
| 派生 | 榜首落差 | `jiuxin_company_top1_vs_alltype_top1_score_gap` | 1.0901（产物 derived[1]） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 机构排名结果面（企业可切） | jiuxin_warehouse | `ads_institution_technology_power`（22 列） | 64,698 | 直查 | **有**（company 13,939） |
| D2 | 机构类型维 | jiuxin_warehouse | `ads_institution_type`（OpenAlex 体系） | 全枚举 | 直查 | 有（company 定义在案） |
| D3 | UI 四维综合分 | 三源 | — | — | **不存在** | 缺（口径 B 障碍，§四） |
| D4 | 国内企业口径映射 | 三源 | OpenAlex↔国内底册 | — | **不存在** | 缺（触发器③） |

`support_judgment="完全转换支持"`，与文首同档（闸 6）。

### 3.2 D1/D2 质量面

排名列语义：`technology_power_rank` 是全类型基准名次（`benchmark_institution_count=64,698` 随行）——企业榜名次需过滤后重排（本件 §2.3 已做），直接用 global_rank 会得到「企业中全球第 545 名」的错位读数。类型维表含中文注释与 OpenAlex 官方类型 URL（`company`：参与科研活动的营利性企业），类型判定可溯源。

### 3.3 D3/D4 与 dev/gkx 的 absence_probe 全记录

- dev：`gkxlumenx_ads.enterprise_ranking` / `enterprise_score`——**造数黑名单**（skill P4.1 明列：分值禁止引用），且本批实测均 **0 行**（「表存在但 0 行」独立披露）；`svc_tech_power_score` 同为服务域造数面。absence_probe 在案（含行数实测值）。
- gkx：280 表 `table_name LIKE '%rank%'/'%score%'` **0 命中**（absence_probe 在案）——gkx 无任何排名结果面，企业榜需从明细自聚合（工程量大，非现转）。
- 条件与命中形态：D3/D4 均为「表/映射不存在」级——修复=建面/建映射，非补数据。

## 四、数据缺失情况

### 4.1 UI 四维综合分缺失（维度级，口径 B 障碍）

UI mock 的四维（创新 0.4/影响 0.3/潜力 0.2/保障 0.1）在久新榜面无对应分列（现有四分项=论文/被引/人才/主题，学术单维族）。「保障能力」（政策/资金维）在学术库体系中无承载（政策域 gkx 有表但企业粒度映射缺）——这是 INDEX 族共同的维度缺口，权重侧归 M_SCIUI_INDEX_013 件裁定。口径 A 先行可解即期用数。

### 4.2 国内企业口径映射缺失（对象池级）

OpenAlex company 池与国内企业底册（live `gkxlumenx_dwd.enterprise_base` 189,116 行）是两套体系（名称规范化/国别标注差异），映射层三源均无。若 UI 面向国内用户需国别切片，修复=名称模糊匹配+人工校验（工程量中等），或直接用 power 表 country 维（institution_profile 在案）先切国别再入榜。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 企业榜直供 v1 | 数据工程 | 本件即期 | TopN API + 维度语义标注 |
| 国别切片前置 | 数据工程 | 本件+036/038 | country 维过滤，免映射 |
| 四维分列建设 | 建模工程 | 本件+INDEX 族 | 与 013 权重件联动立项 |

## 参考文献

1. 关于征求国家创新调查监测与评价指标体系意见的通知[EB/OL]. 中华人民共和国科学技术部. https://most.gov.cn/tztg/201312/t20131204_110716.html （2026-11-01 WebSearch 核验可达；企业创新能力评价指标体系的官方发布口径）
2. 科技部、国家统计局联合印发《国家创新调查制度实施办法》[EB/OL]. 中华人民共和国科学技术部. https://www.most.gov.cn/ztzl/qgkjcxdhzkyzn/gcls/kjb/201705/t20170525_132970.html （2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/科技指数.md》seq 172（excel_row 175）——本件语义源：

> ### 分类排名展示 · 序号 172
> #### 需规功能描述
> 提供多种分类排名方式，用户可按科技领域、成果类型、机构类型、地域范围等条件查看分类排名，支持多条件组合筛选，满足不同用户的查看需求。

同文件 seq 171「科技成果综合排名」（「展示科技成果的综合排名榜单，用户可查看排名前N位的科技成果及其得分情况，系统提供排名变化趋势」）为四榜族父语境。「企业榜」三字未独立出现。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 企业榜 | 科技指数.md / 科技创新评估.md / 主需求文档 | 0（独立叶） |
| 分类排名 / 机构类型 | 科技指数.md | 1（seq 172，语义源） |
| 科技成果综合排名 | 科技指数.md | 1（seq 171，父语境） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INDEX_001_out.json`（2026-11-01 实跑）。
- 共享探针：`_probe_lane3_s302_out.json`（B 组）/ `_probe_lane3_s302_r2_out.json`（B3r/B5/B7）/ `_probe_lane3_s302_r3_out.json`（G4/G5）。
- dev 造数面行数实测：`_probe_lane3_s302_r2_out.json`（E7/E8，均 0 行）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INDEX_001 | 文首 |
| `ui_evidence` | 证据 | 3 条组件：行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | false（语义挂 seq 171/172） | §1.1/附录 A |
| `facts.jiuxin_power_rows` | 计数 | 64,698 | §2.1 |
| `facts.jiuxin_power_version` | 版本 | 2026-09-18×mvp_v1 | §2.1 |
| `facts.jiuxin_power_by_type` | 分布 | 全类型枚举含 company 13,939 | §2.2 |
| `facts.jiuxin_company_top10_by_tech_power` | 榜单 | 十行（名/分/计数/名次） | §2.3 |
| `facts.jiuxin_alltype_top5` | 对照 | 五行 | §2.2 |
| `facts.jiuxin_company_score_min_max_avg` | 分布 | 三读数 | §2.4 |
| `derived[0]` | 派生比 | jiuxin_company_share_pct | §2.4 |
| `derived[1]` | 差值 | 榜首落差（分母=1 标注） | §2.4 |
| `absence_probe` | 探针 | 三源 3 条 | §3.3 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 对象池 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 官方企业创新能力评价 | 国家创新调查制度（R1） | 规上企业 | 部分依赖经济数据 | 高（口径 B 方向） |
| 学术实力榜 | 久新现役（OpenAlex） | 全球机构 | **64,698 行** | **最高（口径 A）** |
| UI mock 四维 | index.jsx/mockData | mock | 演示值 | 仅证据 |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| institution_technology_power | 64,698 | 单版本/含 rank | 维度=学术单维族 |
| institution_type 维 | 全枚举 | OpenAlex 体系 | 国内口径映射缺 |
| dev enterprise_ranking/score | 0 | 黑名单 | 不可用 |
| gkx 排名面 | 0 | — | 需自聚合 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 企业榜 TopN API+标注 | 无 |
| v2 | 国别切片（country 维） | 过滤工程 |
| v3 | 四维综合榜（口径 B） | INDEX_013 权重立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 口径 A 名次被当综合榜名次 | **高** | 榜单标注「科技实力榜」 |
| 全球池混入国内叙事 | 中 | 国别切片 v2 |
| 学术尺企业天然低位误读 | 中 | 附 global_rank 联读 |

### C.5 总判

**完全转换支持**：承载面结构+量+过滤重排三证齐；维度语义偏移以双口径+触发器保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INDEX_001.py` | 退出码 0，落 `_out.json` |
| 类型和复核 | Σ type rows | =64,698（B11） |
| Top10 复核 | company 过滤重排 | Google 98.9091 居首 |
| 黑名单隔离 | dev 两表行数 | 0/0（值不引用） |
| 判档一致 | MD 文首 vs `support_judgment` | 完全转换支持 |

# 科技指数综合榜（M_SCIUI_INDEX_036）

> **类型**：无业务逻辑数值类（多对象榜单）｜ **域**：科技发展态势·科技指数·排行榜＞综合榜（Radio 首项）｜ **UI 挂载**：科技指数页 → 排行榜 Tab → 榜单切换 Radio「综合榜」（comprehensive，全对象总榜）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 拆件叶（`_phase3_471_export.json` row_01 230；**裁定 NEW**：多对象榜单非单指数读数）
> **复现脚本**：`code/M_SCIUI_INDEX_036.py`｜ **产物**：`code/M_SCIUI_INDEX_036_out.json`
> **四判定摘要**：直接结构 = 否（三源无「科技指数四维综合榜」现成面）；直接数据 = 否；依赖结构 = 是（久新 `ads_institution_technology_power` 64,698 行含 rank/score/类型键+profile 国别键）；依赖数据 = 是（全量在案，CN 切片 4,641 家）
> **数据源口径**：三源评估——开发库 `gkxlumenx_*`（10.50.11.76:3306）+ 三方库 `gkx`（183.240.141.251:3318 只读）+ 久新库 `jiuxin_warehouse`（47.93.119.170:29030 只读）；本件主承载在久新。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** 派单裁定 NEW 成立：综合榜是**多对象聚合榜单**（机构/城市等对象的 TopN 排名），不是单指数读数——与 TECHTRK_002（指标上行占比）不同物。按榜单要件盘点：久新 `ads_institution_technology_power` 64,698 行=全类型机构对象×科技实力总分+基准名次（版本 2026-09-18×mvp_v1，facts `jiuxin_power_rows`/`jiuxin_power_version`），配合 `ads_institution_profile` 国别键（JOIN 实测）——机构对象维的综合榜**现转即得**：全类型 Top10 复现首位中科院 99.999227（facts `jiuxin_alltype_top10`，重排序与存储名次双键核对一致）、CN 切片 Top10（facts `jiuxin_china_top10`，国内综合榜即期版）、九类型+国别分布全落产物。城市/国家对象维：geo 原始指标面 171,736 行在案（COUNTRY 5,081 行×27 年），但指数化承载表 `ads_geo_yearly_index` 实测 **0 行**——地理综合榜需从原始面自建指数化（聚合维在、得分列缺，非本件主口径的阻塞项）。机构榜结构+量+过滤重排三证齐，判完全转换支持；四维语义偏移与地理榜升档路径按 B10 披露。

### 批次通用纪律摘要（S3-02 批 Lane 4，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | CN 占比/极差分子分母同表同池；极差键分母标注 |
| B4 | 负结论带探针 | 地理指数榜/黑名单 absence 留证（§3.3） |
| B5 | 确定性 | TopN 按 score DESC,name 双键；分布按键排序 |
| B6 | 闸门自身被闸 | 本批不自跑闸门 |
| B7 | 产物只由脚本产出 | 改脚本→重跑 |
| B8 | 回执不复收 | 派单方硬复验 |
| B9 | 单位/日期陷阱 | 国别键 JOIN 显式；快照日期字符串化 |
| B10 | 口径裁定保守交付 | 实力榜/四维综合榜+机构榜/地理榜双轴披露（§1.6） |
| B11 | 多本账互推 | 64,698/类型分布/company 13,939 与 INDEX_001 零漂移 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 多对象排名面存在吗？ | 存在（机构维） | power 64,698 含 rank/score（facts） |
| 综合榜 TopN 跑通了吗？ | 跑通 | `jiuxin_alltype_top10`（与存储名次一致） |
| 地理对象维呢？ | 原始面在、指数面空（0 行） | `jiuxin_geo_yearly_index_rows` |

## 摘要

「科技指数综合榜」是排行榜 Tab 四榜 Radio 的首项（comprehensive——全对象总榜，区别于高校/企业/科研机构三个类型切片），语义源是 SRS seq 171「科技成果综合排名」（前 N 位及得分、排名变化趋势）+seq 172「分类排名展示」（机构类型等条件——四榜切分的语义根据）。派单裁定其为本体=多对象聚合榜单。数据侧判定：久新 power 表 64,698 行全类型基准名次现役，是三源唯一的机构对象总榜面——本件复现全类型 Top10（中科院 99.999227 / 国科大 / 北大 / 浙大 / 上交，头部极差仅 0.0167）、CN 切片 Top10（国内综合榜即期版）、九类型分布（education 16,446/company 13,939/…）与国别 Top10 分布（US 16,442/CN 4,641/…，CN 占比 7.1733%）；geo 面城市/国家级原始指标 171,736 行在案但指数化承载表 0 行（地理综合榜需自建指数化）。判**完全转换支持**（机构榜即期可得）；四维语义偏移（学术实力族 vs UI 创新四维）与 INDEX_001 同源，闭合待权重件。

- 需求判定：UI 拆件叶（Radio 首项）；语义挂 seq 171/172 排行榜族。
- 复现状态：脚本已跑通；全类型 Top10/CN 榜/类型分布/国别分布/geo 双面五组读数落产物。
- 档位结论：**完全转换支持**（机构对象维结构+量+重排三证齐）。
- 关键事实：mock「综合榜」实为按领域分组重排（comprehensive=groupBy field 后各组 rankRecords）——UI 的「综合」语义与「全对象单榜」有微妙差异，本件交付两种真实形态（全类型单榜+领域分组可由 region/field 切片复用）。
- 升档路径：地理综合榜指数化（geo 原始面→geo_yearly_index 落表）或四维语义闭合（权重件）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/科技指数/排行榜/**综合榜**（UI 拆件叶，row_01 230）。UI 挂载点 `index.jsx:1080`：排名 Tab 的榜单切换 `Radio.Group` options 首项 `{ label: '综合榜', value: 'comprehensive' }`——与高校榜/企业榜/科研机构三个类型切片并列，「综合」=不分对象类型的总榜。切换联动重置五维筛选（成果名称搜索/科技领域/成果类型/机构类型/地域）与导出。mock 数据形态的关键细节（mockData.js:1196）：`comprehensive: Object.values(buildGroupedRanking(achievementRankingRecords, 'field')).flatMap(rankRecords)`——mock 综合榜是**按领域分组后各组重排**的拼接榜，每行含 totalScore（四维加权 0.4/0.3/0.2/0.1）+四维分+weightContributions（applyEvaluationModel 派生，「禁止手写」）。榜单标题位（index.jsx:1049-1051）comprehensive 分支显示「科技成果综合排名」。

### 1.2 为什么需要本指标

四榜 Radio 的信息架构逻辑：综合榜给全景基线（谁整体最强），三个类型榜回答分赛道（高校/企业/科研机构各自领跑者）——用户先在综合榜定位标杆，再下钻类型榜找同类对标。对管理侧，综合榜+类型切片一起读才能区分「学术体系强」与「产业体系强」（INDEX_001 已证学术尺下企业让位——综合榜 Top10 全为院所/高校，类型榜正是矫正这种结构偏差的设计）。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「综合榜」三字未独立出现在三份需求真源；语义源 seq 171 给功能行为（「展示科技成果的综合排名榜单，用户可查看排名前N位的科技成果及其得分情况，系统提供排名变化趋势」）、seq 172 给分类条件（「按科技领域、成果类型、机构类型、地域范围等条件查看分类排名」）——但榜单得分构成（哪些维度、怎么加权）、对象池定义（成果？机构？）均无定义。mock 的四维加权与领域分组是实现选择。检索记录见附录 A。

### 1.4 类似指标权威方法可行性分析概略

综合榜的方法范式：学术体系以机构总榜为主流（Nature Index 全球机构榜 R1、Leiden Ranking R2——固定指标族全机构单榜+切片）；创新体系以多维加权综合为主流（GII 经济体榜 R3——支柱加权总分排名）。方法族对照：

| 方法族 | 代表 | 榜单结构 | 与本库匹配 |
|---|---|---|---|
| 机构总榜+切片（现役） | Nature Index（R1）/Leiden（R2） | 全机构单榜+类型/区域切片 | **有（power 64,698 现役）** |
| 多维加权综合榜（UI 语义） | GII（R3） | 支柱加权总分榜 | 分维待权重件 |
| mock 领域分组拼接 | 前端演示 | groupBy(field) 重排 | 演示值 |

完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-index/index.jsx:1080` — `{ label: '综合榜', value: 'comprehensive' }`；`:1049-1051` 标题位「科技成果综合排名」。
- mockData：`repos/demo-ui-science/src/pages/tech-index/mockData.js:1196` — `comprehensive: Object.values(buildGroupedRanking(…, 'field')).flatMap(rankRecords)`（领域分组拼接形态）；`:1166-1176` 四维派生。
- SRS：`…/科技发展态势/科技指数.md` seq 171/172（语义源），原文见附录 A。

### 1.6 推测原意与推测定义

**推测定义**：综合榜=全对象（不分类型）按综合得分降序的 TopN 榜，行含总分+分维分+名次+类型/地域键（供下钻切片）。

- **口径 A（建议口径：机构科技实力综合榜）**：对象=power 全池 64,698 机构（九类型），总分=technology_power_score（论文 0.35/被引 0.30/人才 0.25/主题 0.10）——现转即得，本件已实测（全类型 Top10+CN 榜+类型/国别切片）；mock 的领域分组形态可由 profile/学科维切片复用；
- 口径 B（UI 语义：四维科技成果综合榜）：维度=创新 0.4/影响 0.3/潜力 0.2/保障 0.1，对象=科技成果——需 INDEX_013 权重闭合+成果对象面建设；
- 口径 C（地理综合榜）：对象=城市/国家——geo 原始面 171,736 行→指数化落 `ads_geo_yearly_index`（结构已预留）→地理 TopN。

**降档/升档触发器（B10 模板）**：口径 A 被接受 → 维持完全转换支持且即期交付（学术尺标注）；坚持口径 B → 降档风险在权重/成果面两前置闭合前维持部分支持；口径 C 立项 → 地理榜从本件派生（指数化工程），两榜并存。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md` |
| 所属四级功能 | 科技指数·排行榜（seq 171–177） |
| 本件叶 | 综合榜（UI 拆件，row_01 230，Radio 首项） |
| 同 Radio 姊妹叶 | 高校榜（INDEX_038，Lane 5）/ 企业榜（INDEX_001，已交付）/ 科研机构榜（批外） |
| 榜单族相邻叶 | 排名历史变化（174=INDEX_019）/ 排名对比分析（175=INDEX_020）/ 筛选搜索（176）/ 结果导出（177） |
| 权重侧联动件 | M_SCIUI_INDEX_013（口径 B 前置） |

与 INDEX_001（企业榜）的分工：001 是本件的 company 切片（同一承载面、同一过滤重排路径、口径 A 同源同构）；本件补全对象轴（全类型+国别切片）与地理轴（geo 双面盘点）——两件构成「总榜+分榜」的完整判定，判档结论一致（完全转换支持）互为佐证（B11）。

## 二、计算过程

### 2.1 装载与榜单底座

pymysql 直连久新只读库。榜单底座 `ads_institution_technology_power`：64,698 行、版本 2026-09-18×institution_technology_power_mvp_v1 单快照（facts `jiuxin_power_rows`/`jiuxin_power_version`，与 INDEX_001/共享探针 B1/B2 零漂移）。国别键经 `ads_institution_profile`（60 列画像面，country_code 在列）JOIN 取得——profile 83,745 行覆盖 power 池的 JOIN 实测成功（CN 4,641 家命中）。

### 2.2 全类型综合 Top10 复现

`ORDER BY technology_power_score DESC, institution_name` 双键（B5）重排 Top10，与存储基准名次（technology_power_rank）双键核对：中科院（government）99.999227 双榜第 1 / 国科大（education）99.9968 / 北大 99.9961 / 浙大 99.9932 / 上交 99.9927 等（facts `jiuxin_alltype_top10` 十行全落，含 country）。头部读数：Top10 类型多样性 2（government+education——学术尺下企业缺席头部，与 INDEX_001「企业榜首全球名次 545」互证）；Top1 与 Top10 分差仅 0.0167（derived `jiuxin_top1_vs_top10_score_gap`——头部极度密集，百分位制的天花板效应）。

```sql
SELECT p.institution_name, p.institution_type_id, p.technology_power_score,
       p.technology_power_rank, pr.country_code
FROM ads_institution_technology_power p
LEFT JOIN ads_institution_profile pr ON p.institution_id = pr.institution_id
ORDER BY p.technology_power_score DESC, p.institution_name LIMIT 10;
-- → 中科院 99.999227 (rank 1, CN) / 国科大 / 北大 / 浙大 / 上交 / …
```

### 2.3 国别切片：CN 综合榜

`WHERE pr.country_code='CN'` 过滤重排 Top10（facts `jiuxin_china_top10`）：中科院 99.999227（全球 1）/ 国科大（全球 2）/ 北大 / 浙大 / 上交——国内榜与全类型榜头部重合（中国学术体系在 OpenAlex 尺上的统治性），随行 global_rank 供两榜联读。国别分布（facts `jiuxin_country_top10_distribution`）：US 16,442 / CN 4,641 / GB 4,023 / FR 3,449 / DE 3,253 / JP 2,611 / IN 2,503 / CA 1,902 / IT 1,450 / RU 1,345；CN 占比 7.1733%（4,641/64,698，derived `jiuxin_cn_institution_share_pct`——注意这是 OpenAlex 机构体系的国别构成，非国内口径全覆盖）。

### 2.4 类型分布（四榜 Radio 的对象供给）

九类型全枚举（facts `jiuxin_type_distribution`，与 INDEX_001 facts 逐键一致）：education 16,446 / company 13,939 / healthcare 10,877 / facility 9,021 / nonprofit 5,807 / government 4,136 / other 3,175 / archive 1,011 / funder 286——综合榜（全类型）与三类型榜（高校/企业/科研机构）的对象池分层齐备；Top10 类型多样性 2/9（derived `jiuxin_top10_type_diversity`，分子=Top10 出现类型数、分母=全榜类型数——计数键标注非比值）。

### 2.5 地理对象轴盘点（geo 双面）

geo 原始指标面 `ads_geo_yearly_metrics` 171,736 行（分布 CITY 132,975 / PROVINCE 33,518 / COUNTRY 5,081 / CONTINENT 162，facts `jiuxin_geo_level_distribution`；COUNTRY 级 2000-2026 二十七年跨度——共享探针 A1/A6）；指数化承载 `ads_geo_yearly_index` 14 列结构在（index_code/normalized_value/percentile/component_values/formula_snapshot）但实测 **0 行**（facts `jiuxin_geo_yearly_index_rows`）。地理综合榜的判定：聚合维（城市/国家对象）与原始指标（论文/被引/人才计数）均在案，缺的只是指数化得分列——从原始面归一合成即可填充预留表，工程为一条聚合管道（与 INDEX_028 口径 B 的落表工程同源）。

### 2.6 稳健性与口径敏感性

对象轴敏感：机构榜（现役）与地理榜（待建）是两个对象体系——同名「综合榜」在两轴上的读数不可互推（机构计数≠城市计数）。语义敏感：power 总分=学术四分族加权，UI「综合」=创新四维——两族名次相关性高但不恒等（INDEX_001 已披露企业段位差）。国别键敏感：profile JOIN 依赖画像面覆盖（83,745 行 vs power 64,698——池内机构画像覆盖高，CN 切片可信；未命中 JOIN 的行为 LEFT JOIN null，国别分布按命中计）。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INDEX_036.py`（久新直连，profile JOIN 切片）；运行 `python3 code/M_SCIUI_INDEX_036.py`。
- 产物：`code/M_SCIUI_INDEX_036_out.json`。正文数字对应键：`jiuxin_power_rows`/`jiuxin_power_version`（§2.1）、`jiuxin_alltype_top10`（§2.2）、`jiuxin_country_top10_distribution`/`jiuxin_china_top10`（§2.3）、`jiuxin_type_distribution`（§2.4）、`jiuxin_geo_level_distribution`/`jiuxin_geo_yearly_index_rows`（§2.5）、derived 三键（§2.2-2.3）。
- 结果解读：机构综合榜三视图（全类型/国别/类型）+地理轴双面（原始在/指数空）——「能交付什么」与「缺什么」两侧留证。
- 对照需求功能要求的评审：综合榜 Tab 回填——**有条件通过（口径 A）**：全类型 TopN+CN 榜+类型/国别切片即期可供；未通过点=四维语义（权重件）与地理榜（指数化工程）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 | 数值 |
|---|---|---|---|
| 底座 | 榜面规模 | `jiuxin_power_rows` | 64,698 |
| 底座 | 版本 | `jiuxin_power_version` | 2026-09-18×mvp_v1 |
| TopN | 全类型 Top10 | `jiuxin_alltype_top10` | 中科院 99.999227 首位 |
| TopN | 重排-存储名次核对 | `jiuxin_alltype_top10[].stored_rank` | 与 rank 一致 |
| 切片 | CN Top10 | `jiuxin_china_top10` | 中科院（全球 1）首位 |
| 切片 | 国别分布 | `jiuxin_country_top10_distribution` | US 16,442/CN 4,641/… |
| 分布 | 类型分布 | `jiuxin_type_distribution` | education 16,446/company 13,939/… |
| 地理 | geo 层级分布 | `jiuxin_geo_level_distribution` | CITY 132,975/COUNTRY 5,081 |
| 地理 | 指数承载 | `jiuxin_geo_yearly_index_rows` | 0（结构预留） |
| 派生 | CN 占比 | `jiuxin_cn_institution_share_pct` | 7.1733%（4,641/64,698） |
| 派生 | Top10 类型多样性 | `jiuxin_top10_type_diversity` | 2（/9） |
| 派生 | 头部极差 | `jiuxin_top1_vs_top10_score_gap` | 0.0167 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 机构对象总榜 | jiuxin_warehouse | `ads_institution_technology_power` | 64,698 | 直查 | **有**（rank/score 在列） |
| D2 | 国别切片键 | jiuxin_warehouse | `ads_institution_profile.country_code`（JOIN） | CN 4,641 | 直查 | 有 |
| D3 | 地理对象原始面 | jiuxin_warehouse | `ads_geo_yearly_metrics` | 171,736（COUNTRY 5,081） | 直查 | 有（计数无指数） |
| D4 | 地理指数化承载 | jiuxin_warehouse | `ads_geo_yearly_index`（14 列） | **0** | 结构在数据空 | 缺（待填充） |
| D5 | UI 四维综合分 | 三源 | — | — | 不存在 | 缺（权重件前置） |

`support_judgment="完全转换支持"`，与文首同档（闸 6）。

### 3.2 D1/D2 质量面

总榜三重可用性：基准名次随行（`technology_power_rank`+`benchmark_institution_count=64,698` 基准声明）、重排一致性（本件 ORDER BY 重排与存储名次双键核对一致——Top10 无错位）、版本单一（跨行可比）。国别键为 JOIN 增强维（非 power 原生）——profile 画像面覆盖决定切片完整性，CN 命中 4,641 家供国内榜即期使用。

### 3.3 D4/D5 absence_probe 全记录

否定性证据三件套：**查了什么**——①`SELECT COUNT(*) FROM ads_geo_yearly_index`（地理指数面现场复核，与 `_table_class` E-空表分类互证）；②dev `enterprise_ranking` 行数（综合榜候选黑名单表）；③gkx `%rank%`/`%score%` 表扫描。**条件**——地理级科技指数现成榜面/三源现成综合榜。**命中**——geo_index 0 行（表在数空）；dev 0 行（黑名单+空壳）；gkx 0 张。缺失情形归属：D4「表存在但 0 行」——修复=填充（聚合管道）而非建表；D5「语义未建设」——权重件管辖。

## 四、数据缺失情况

### 4.1 地理指数化缺失（表在数空，口径 C 阻塞项）

geo 原始面 171,736 行（城市/省级/国家级年度计数）已具备地理榜的全部原料，但 `ads_geo_yearly_index` 0 行——城市/国家级「科技指数」得分列从未生成。修复：归一管道（各指标百分位制→加权→落 index_code 编码行），与 INDEX_028 口径 B 落表工程同源（一张管道两件受益）。地理榜历史维原料充足（COUNTRY 27 年序列）。

### 4.2 四维综合语义缺失（权重件前置，与 001 同源）

UI 综合榜 totalScore=创新 0.4/影响 0.3/潜力 0.2/保障 0.1 四维派生；power 总分=学术四分族——维度族不同构（INDEX_001 §4.1 同述）。闭合路径=INDEX_013 口径 B 立项→四维分列建设→本件同面重排。成果对象池（UI 语义的「科技成果」）三源亦无独立承载，若口径 B 坚持成果粒度需另建对象面（工程量大于机构维复用）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 综合榜直供 v1 | 数据工程 | 本件即期 | 全类型/CN/类型/国别四视图 |
| geo 指数化管道 | 数据工程 | 本件+INDEX_028 | 原始面→geo_yearly_index 填充 |
| 四维分列建设 | 建模工程 | 本件+001/038+013 | 权重件联动 |
| 成果对象面（如需） | 建模工程 | 榜单族 | UI 成果粒度坚持时立项 |

## 参考文献

1. Nature Index 2024[EB/OL]. Springer Nature. https://www.nature.com/nature-index/ （2026-11-01 WebSearch 核验可达；全机构总榜+切片的学术榜范式）
2. CWTS Leiden Ranking 2024[EB/OL]. Universiteit Leiden. https://www.leidenranking.com/ （2026-11-01 WebSearch 核验可达；机构综合榜指标族与规模分层）
3. Global Innovation Index 2024[EB/OL]. WIPO. https://www.wipo.int/global_innovation_index/en/ （2026-11-01 WebSearch 核验可达；多维加权综合榜与经济体排名范式）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/科技指数.md》seq 171/172——本件语义源：

> ### 科技成果综合排名 · 序号 171
> #### 需规功能描述
> 展示科技成果的综合排名榜单，用户可查看排名前N位的科技成果及其得分情况，系统提供排名变化趋势，显示与上一期相比的上升或下降情况。

> ### 分类排名展示 · 序号 172
> #### 需规功能描述
> 提供多种分类排名方式，用户可按科技领域、成果类型、机构类型、地域范围等条件查看分类排名，支持多条件组合筛选，满足不同用户的查看需求。

「综合榜」三字未独立出现；四榜 Radio（综合/高校/企业/科研机构）是 seq 172「机构类型」条件的产品化拆分。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 综合榜 | 科技指数.md / 主需求文档 | 0（独立名） |
| 科技成果综合排名 | 科技指数.md | 1（seq 171，语义源） |
| 分类排名 / 机构类型 | 科技指数.md | 1（seq 172，四榜切分根据） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INDEX_036_out.json`（2026-11-01 实跑）。
- 共享探针：`_probe_lane4_s302_out.json`（A1-A6 geo 面；B1/B2 power 对账；E 组 dev 扫描/黑名单复核；D3 gkx 扫描）、`_probe_lane4_s302_r2_out.json`（geo_index 列结构）。
- 久新 schema 索引：`20261026_久新指标 gap 调研/…/_table_class.json`（geo_yearly_index=E-空表分类互证）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INDEX_036 | 文首 |
| `ui_evidence` | 证据 | 3 条组件行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | false（语义挂 seq 171/172） | §1.1/附录 A |
| `facts.jiuxin_power_rows` | 计数 | 64,698 | §2.1 |
| `facts.jiuxin_power_version` | 版本 | 2026-09-18×mvp_v1 | §2.1 |
| `facts.jiuxin_alltype_top10` | 榜单 | 10 行（含 stored_rank/country） | §2.2 |
| `facts.jiuxin_china_top10` | CN 榜 | 10 行（含 global_rank） | §2.3 |
| `facts.jiuxin_country_top10_distribution` | 分布 | 10 国 | §2.3 |
| `facts.jiuxin_type_distribution` | 分布 | 9 类 | §2.4 |
| `facts.jiuxin_geo_level_distribution` | 分布 | 4 层级 | §2.5 |
| `facts.jiuxin_geo_yearly_index_rows` | 缺格 | 0（14 列结构在） | §2.5 |
| `derived[0]` | 派生比 | CN 占比 7.1733%（4,641/64,698） | §2.3 |
| `derived[1]` | 计数 | Top10 类型多样性 2（/9） | §2.4 |
| `derived[2]` | 跨度 | 头部极差 0.0167 | §2.2 |
| `absence_probe` | 探针 | 三源 3 条 | §3.3 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 榜单结构 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 机构总榜+切片 | Nature Index（R1）/Leiden（R2） | 全机构单榜 | **power 64,698 现役** | **最高（口径 A）** |
| 多维加权综合 | GII（R3） | 支柱总分榜 | 分维待权重件 | 高（口径 B） |
| 地理指数榜 | GII 经济体维 | 城市/国家榜 | 原始面在/指数面空 | 中（口径 C，需管道） |
| mock 分组拼接 | 前端演示 | groupBy(field) | 演示值 | 仅证据 |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| power 总榜 | 64,698 | rank/score/基准数 | 维度=学术族 |
| profile 国别键 | CN 4,641 命中 | JOIN 增强 | OpenAlex 体系国别 |
| geo 原始面 | 171,736 | 4 层级×27 年（COUNTRY） | 无指数列 |
| geo_yearly_index | 0 | 14 列预留 | **数据空** |
| UI 四维分 | — | — | 权重件前置 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 四视图（全类型/CN/类型/国别） | 无 |
| v2 | geo 指数化→地理综合榜 | 聚合管道（与 028 共建） |
| v3 | 四维综合榜 | INDEX_013 权重闭合 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 学术尺综合榜被当四维综合榜 | **高** | 榜单标注「机构科技实力榜」 |
| OpenAlex 国别构成误读（CN 7.17%≠全球占比语义） | 中 | 切片口径随行披露 |
| 机构榜/地理榜对象混淆 | 中 | 两轴分榜呈现 |
| 头部极差过小（0.0167）致名次敏感 | 低 | 分维联读+基准数披露 |

### C.5 总判

**完全转换支持**：机构对象维结构+量+重排三证齐（即期交付）；地理维与四维语义两条升维路径明确（管道工程/权重件），保守交付不悬空。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INDEX_036.py` | 退出码 0，落 `_out.json` |
| power 对账 | `jiuxin_power_rows` vs INDEX_001/020 | 64,698 零漂移（B11） |
| 类型分布对账 | `jiuxin_type_distribution` vs INDEX_001 | 逐键一致（B11） |
| TopN 复核 | 全类型首位 | 中科院 99.999227=stored_rank 1 |
| geo 复核 | `jiuxin_geo_yearly_index_rows` | 0（与共享探针 A5 一致） |
| 判档一致 | MD 文首 vs `support_judgment` | 完全转换支持 |

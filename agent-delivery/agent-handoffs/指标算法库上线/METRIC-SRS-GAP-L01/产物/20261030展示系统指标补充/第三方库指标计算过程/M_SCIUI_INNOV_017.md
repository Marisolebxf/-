# 领域创新指标排名（M_SCIUI_INNOV_017）

> **类型**：RANK（领域分组排名，双口径 A 26 领域各自国别 Top3 / 口径 B 中/美领域居首数矩阵）｜ **域**：科技发展态势·全球创新监测·创新载体排行模式第 2 项｜ **UI 挂载**：`carrierRankModeModel.js:5`（`CARRIER_RANK_MODES { key: 'domain', label: '领域排名' }`）+ `:22`（`attachCarrierRankGroups` 领域分组重排）
> **数据支持度**：**完全直接支持**｜ **公式定义人**：上游已内置（snapshot 自带 output_rank，本件消费+JOIN 聚合）｜ **口径归属**：**SRS 正名叶**（seq 74『领域排名』逐字命中——本批少有的正名件）
> **复现脚本**：`code/M_SCIUI_INNOV_017.py`｜ **产物**：`code/M_SCIUI_INNOV_017_out.json`
> **四判定摘要**：直接结构 = 是（ads_topic_country_snapshot 自带 output_rank + ranked_country_count + 26 领域字典 JOIN 链全在）；直接数据 = 是（4,467 topics × 224 国全量、26 领域全覆盖）；依赖结构 = 不需要；依赖数据 = 不需要
> **数据源口径**：本件支持度按「开发库 gkxlumenx_*（禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin（47.93.119.170:29030 只读）」三源评估（20261101 三源铁律）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全直接支持。** 排名的三要件——排名键（output_rank）、分组维度（领域字典）、基数（ranked_country_count）——在久新**全链路内置**：`ads_topic_country_snapshot` 209,517 行自带 `output_rank`（topic 内国别排名）与 `ranked_country_count`，经 `ads_discipline_topic`（4,516 topics → 26 fields）+ `ads_discipline_field`（26 领域字典）两级 JOIN 即得领域×国排名——SRS seq 74『领域排名』**逐字命中**（本批少有的正名件，`named_in_srs=true`）。实测口径 A（26 领域各自国别 Top3）：中国在 **23 个领域**居首（**88.4615%**，`derived.jiuxin_cn_field_first_share_pct`），美国 3 个（健康专业/兽医学/心理学——医学与心理类），计算机科学 Top3 为 China 147,981 / United States 38,554 / United Kingdom 13,380（中国约为美 3.8 倍，复算 147,981/38,554）。口径 B（output_rank 直读）：中国论文量 Top5 主题（先进光催化 34,715 / 能源转换电催化剂 30,824 / 电池材料 13,176 等）**全部 output_rank=1**（`jiuxin_top5_topics_cn_rank1_share_pct=100.0`），ranked_country_count 103-121 国参与排名。语义对齐披露：UI 挂载是**载体粒度**（mock 八领域：合成生物/光载信息/量子信息等），上游是 26 学科领域（神经科学/化学/计算机科学等）——回填需建 UI 八领域→26 学科映射或换用学科枚举。判**完全直接支持**。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 居首占比分子分母同 JOIN 同 SUM（26 领域） |
| B4 | 负结论带探针 | gkx discipline/field/rank 0 表 + dev 论文 0 表（官方快照原值） |
| B5 | 确定性 | 榜单 ORDER BY SUM(paper_count) DESC；JOIN 幂等（同 SQL 同值） |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑 |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | 全窗 2015-2025（上游 analysis 窗）；排名为整数位次 |
| B10 | 口径裁定保守交付 | 双口径 + UI 领域↔学科映射披露 + output_rank topic 内语义声明 |
| B11 | 多本账互推 | snapshot 209,517 与 011/016 件同表同值；discipline_topic 4,516 与 016 件同值 |

### 判档自检三问（本件 = 完全直接支持）

| 问 | 答 | 证据 |
|---|---|---|
| 排名列是现成的吗？ | 是（output_rank 内置） | CN Top5 主题全 rank=1 |
| 领域分组维度全吗？ | 全（26 领域字典+4,516 映射） | 口径 A 26 领域全覆盖 |
| 需要重算排名吗？ | 领域级聚合需 SUM 重排（topic 内排名≠领域级） | 口径 A 即此重排（B5 幂等） |

## 摘要

「领域创新指标排名」是创新载体排行榜的**排名模式第 2 项**（`carrierRankModeModel.js:5`，总体/领域/地区三模式之一；`:22` 的 `attachCarrierRankGroups` 按领域分组后组内 `displayRank` 重排——「领域内排名」语义）。本件是全批少有的**双满配**件：SRS 正名（seq 74『提供创新载体的多维度排名，包括总体排名、领域排名、地区排名』**逐字命中**）+ 数据直读（久新 snapshot 自带 `output_rank` 排名列与 `ranked_country_count` 基数列）。实测口径 A（26 领域各自国别 Top3，SUM 论文重排）：**中国在 23 个领域居首（88.4615%）**——计算机科学 China 147,981 / US 38,554 / UK 13,380、能源、材料、化学等全线领跑；**美国仅 3 个领域居首（健康专业/兽医学/心理学）**——美方优势收缩至医学与心理类的格局在领域粒度上清晰可见。口径 B（output_rank 直读验证）：中国论文量 Top5 主题（先进光催化 34,715 / 能源转换电催化剂 30,824 / 电池材料 13,176 / 金属有机框架 11,970 附近 / 能源环境经济增长等）**100% output_rank=1**，每主题 103-121 国参与排名——上游排名的密度与广度双达标。语义适配披露：UI 领域分组键是 mock 八领域（合成生物/光载信息/量子信息/新材料/人工智能/新能源/智能制造/生命健康），上游是 OpenAlex 四级学科体系的 26 领域——**回填需建八领域→26 学科映射**（或 UI 改用学科枚举），映射是配置工作非数据缺口。判**完全直接支持**：排名键、分组维度、基数三件全内置，即期回填。

- 需求判定：**SRS 正名叶**（seq 74 逐字命中，`named_in_srs=true`；seq 73 指数计算与 seq 84 城市排名计算为姊妹锚）。
- 复现状态：脚本已跑通；26 领域 Top3 榜 + 居首矩阵 + output_rank 直读验证 + 三源负结论全部落产物。
- 档位结论：**完全直接支持**（排名三要件全内置 + SRS 正名）。
- 关键事实：中国 23/26 领域居首 + 美国 3 领域（健康专业/兽医学/心理学）——领域粒度的中美格局 headline 即可上屏。
- 升档路径：已满档；扩展方向是领域内年度双窗排名变化（`growth_rank` 列在，v2）与城市级领域排名（另立件）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**全球创新监测**/创新载体排行榜（排名模式）。挂载点实查：

- `src/pages/global-innovation/tabs/carrierRankModeModel.js:5`：`CARRIER_RANK_MODES { key: 'domain', label: '领域排名' }`——排名模式第 2 项（overall/domain/region 三选一）。
- `carrierRankModeModel.js:22`：`attachCarrierRankGroups`——rankMode='domain' 时按 `row.domain` 分组、组大小降序 + 组名 localeCompare 排组、组内 `displayRank` 重排——**「领域内排名」语义**（分组→组内重排两步）。
- 消费方 `InnovationRanking.jsx:44/:121`：rankMode state + 模式选择器；`:39` `RANK_SCORE_DIMENSION='score'`——排序底座是创新能力指数（014 姊妹件）。
- `src/pages/global-innovation/mockData.js:15`：`domains` 八领域枚举（合成生物/光载信息/量子信息/新材料/人工智能/新能源/智能制造/生命健康）——mock 载体行携带 domain 字段随机装配。

UI 的排名链路：score 排序 → domain 分组 → 组内重排——数据侧对应：领域聚合排名 → 领域分组 → 领域内国别排名。

### 1.2 为什么需要本指标

总体排名回答「谁最强」，领域排名回答「**强在哪一行**」——把综合榜拆成分领域榜，是排行榜的**结构透视镜**：中国总体第一（014 件产物键 90.7862）但领域排名揭示美方在健康专业/兽医学/心理学仍有壁垒——单总榜会抹平这种结构性差异。本指标承担三职：①**分组视图**（领域模式下的分组榜单）；②**强弱诊断**（哪领域垄断/哪领域胶着——`ranked_country_count` 佐证竞争密度）；③**导航筛选**（InnovationRanking 的领域筛选器与排名模式联动）。数据侧本件是「排名件」的直读代表：上游把排名（output_rank）做进 snapshot 列——这类件的判档是「排名键+分组维度是否双满配」，本件双满（排名列+26 领域字典）。

### 1.3 需求文档是否给出定义方法

**需求文档提及指标名但未给计算方法。** seq 74 原文：『提供创新载体的多维度排名，包括总体排名、领域排名、地区排名，用户可切换查看不同维度的排名情况』——**「领域排名」逐字命中**（`named_in_srs=true`），但只给了功能叙述（可切换查看），未给排序键（论文？专利？指数？）、分组学（领域怎么划）、粒度（载体级？国家级？）。姊妹锚 seq 73（『生成创新能力指数，用户可查看指数计算方法和权重设置』）暗示排序键应为指数；上游实际内置的是论文量排名（output_rank）——排序键的「指数 vs 论文量」分歧须披露（本件按上游论文量口径，指数变体留 v2）。本件的双口径构造即「直读上游 + 聚合重排」的保守方案。

### 1.4 类似指标权威方法可行性分析概要

领域排名的权威范式有三支。**SCImago 国别排名**（R1）：Scopus 27 学科分类 × 国别文档数排名，支持学科筛选+多指标排序（documents/citations/H-index）——「学科×国别」矩阵排名的公开标杆（2025 年中国 documents 1,352,563 居首（SCImago 官方数字，外部参照非本件产物））；**NSF NCSES 学科对比**（R2）：S&E 领域的国别产出对比（分数计数制），领域粒度的美国 vs 中国格局官方叙事；**UI 分组重排范式**（R3，本件挂载实现）：score 排序→domain 分组→组内 displayRank——分组学的「组大小降序+组名排序」是展示层规则（非数据层）。方法族对照：

| 方法族 | 分组学 | 排序键 | 三源承载 | 匹配度 |
|---|---|---|---|---|
| SCImago 学科×国别（R1） | Scopus 27 学科 | documents 等 6 键 | 26 领域字典+output_rank | **高（同构）** |
| NSF 学科对比（R2） | S&E 领域 | 分数计数产出 | 26 领域 SUM（whole） | 中高（计数制差异） |
| UI 分组重排（R3） | mock 八领域 | score（指数） | 映射待建+指数 v2 | 中（配置层） |

结论：上游 26 领域×output_rank 与 SCImago 范式同构度最高（学科字典+国别排名+基数列三对应）；UI 八领域映射与指数排序键是两个配置项（非数据缺口）。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankModeModel.js:5/:22`（模式枚举+分组重排）；`…/tabs/InnovationRanking.jsx:39/:44`（排序底座+消费方）；`…/mockData.js:15`（八领域枚举）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` seq 74（**正名锚**）、seq 73/84（姊妹锚）。
- 数据：`code/_snapshots/_probe_lane5_s3_01_out.json`（snapshot COUNT/DESC #2/#3——output_rank 列原值）。

### 1.6 推测原意与推测定义

**定义（上游内置 + 本件聚合，均须披露口径假设）**：

- **上游内置（topic 级）**：`output_rank` = 同 topic 内按 paper_count 的国别排名（1 = 最高）；`ranked_country_count` = 参与排名国数。实测：中国论文量 Top5 主题全部 rank=1、103-121 国参与。
- **口径 A（领域级·UI 同构分组排名）**：`rank(field, country)` = 按 SUM(paper_count)（4,516 topics 经 field_id 聚合到 26 领域）重排。实测中国 23 领域居首（88.4615%）、美国 3 领域（健康专业/兽医学/心理学）；计算机科学 Top3：China 147,981 / US 38,554 / UK 13,380。
- **口径 B（output_rank 直读验证）**：中国 Top5 主题的 rank 与基数——100.0% rank=1（`derived.jiuxin_top5_topics_cn_rank1_share_pct`）。
- **UI 映射披露**：mock 八领域 → 26 学科映射待建（如 人工智能→计算机科学/决策科学、生命健康→医学/神经科学/药理学等）——映射是回填配置项。

**降档/升档触发器（B10 模板）**：本件已满档（完全直接支持）。扩展触发器：①指数排序键变体（seq 73 语义——014 件评分作 rank 键）→ v2 增强不换档；②领域内年度排名变化（growth_rank 列在）→ v2；③城市级领域排名 → 另立件。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` |
| 所属四级功能 | 全球创新监测（33 叶）· 创新载体排行榜 |
| 本件挂载视图 | 排名模式第 2 项（主）+ InnovationRanking 消费 |
| 需求叶对应 | **seq 74 正名**（多维度排名展示——领域排名逐字命中） |
| 批内相邻件 | M_SCIUI_INNOV_014（能力评分——UI 排序底座 score 的数据侧）；M_SCIUI_INNOV_016（趋势对标——同池 growth_rank 是本件 output_rank 的增长版姊妹）；M_SCIUI_INNOV_011（区域论文数——本件排序键的存量源）；M_SCIUI_TECHTRK_019（维度得分 TOP5——技术跟踪侧同族排名件） |
| 跨模块参照 | 技术发展跟踪（维度排名语境） |

本件与 016 是「存量/增长」排名姊妹：011/017 消费 paper_count/output_rank（存量排名），016 消费 paper_growth_rate/growth_rank（增长排名）——「一池三吃」（存量榜/领域榜/增长榜）是 topic 池的核心价值。与 014 的分工：014 出 score（排序底座），本件出分组领域榜——UI 链路「score 排序→domain 分组→组内重排」的两半分别由 014/017 数据侧供给。

## 二、计算过程

### 2.1 装载与规模校验

久新 `ads_topic_country_snapshot` 209,517 行（`facts.jiuxin_topic_country_rows`，官方快照 #2 原值断言通过）；`ads_discipline_topic` 4,516 行（4,467 topics→26 fields 映射，`jiuxin_discipline_topic_rows`）；`ads_discipline_field` 26 行（领域字典，`jiuxin_discipline_field_rows`，断言 26）。排名三件套（output_rank / ranked_country_count / 26 领域字典）一次取齐。

### 2.2 gkx/dev 侧负结论（absence_probe）

gkx discipline/field/rank 三关键字表扫描：**0 表**；dev 论文表 0 张（官方共享快照原值消费，`dev_paper_tables=[]`）——两库均无领域排名承载，判档依据独落久新。

### 2.3 口径 A：26 领域各自国别 Top3（SUM 重排）

```sql
SELECT f.name_zh AS field, s.country_name_en AS country, SUM(s.paper_count) AS papers
FROM ads_topic_country_snapshot s
JOIN ads_discipline_topic t ON s.topic_id=t.topic_id
JOIN ads_discipline_field f ON t.field_id=f.field_id
GROUP BY f.name_zh, s.country_name_en
-- 组内按 papers DESC 取 Top3
```

26 领域全覆盖（`jiuxin_field_count=26`）；每领域 Top3 落 `jiuxin_field_country_top3`（26×3 行）。居首统计：中国 23 / 美国 3（健康专业/兽医学/心理学）——`jiuxin_cn_field_first_count` / `jiuxin_us_field_first_count`。

### 2.4 口径 B：output_rank 直读验证

```sql
SELECT dt.name_zh, s.output_rank, s.ranked_country_count, s.paper_count
FROM ads_topic_country_snapshot s JOIN ads_discipline_topic dt ON s.topic_id=dt.topic_id
WHERE s.country_code='CN' ORDER BY s.paper_count DESC LIMIT 5
```

→ 先进光催化技术 rank=1（121 国）/ 能源转换电催化剂 rank=1（118 国）/ 电池材料研究进展 rank=1（103 国）等（`jiuxin_cn_output_rank_sample_top5`）——**Top5 全 rank=1**，`derived.jiuxin_top5_topics_cn_rank1_share_pct=100.0`。

### 2.5 居首占比派生

`derived.jiuxin_cn_field_first_share_pct` = 23/26 = **88.4615%**（分子=中国居首领域数，分母=领域总数，同 JOIN 同 SUM，B3）。

### 2.6 复现代码结果展示

| 产物键 | 值（节选） |
|---|---|
| `jiuxin_field_count` | 26 |
| `jiuxin_field_country_top3['计算机科学']` | China 147,981 / US 38,554 / UK 13,380 |
| `jiuxin_cn_field_first_count` / `jiuxin_us_field_first_count` | 23 / 3 |
| `jiuxin_cn_output_rank_sample_top5[0..2]` | 先进光催化 rank=1（121 国）/能源转换电催化剂 rank=1（118 国）/电池材料 rank=1（103 国） |
| `derived.jiuxin_cn_field_first_share_pct` | 88.4615 |
| `derived.jiuxin_top5_topics_cn_rank1_share_pct` | 100.0 |

### 2.7 分步证据对照表

| 步骤 | SQL/操作 | 产物键 | 结果 |
|---|---|---|---|
| S1 规模断言 | COUNT 三表 | `jiuxin_topic_country_rows` 等 | 209,517/4,516/26 零漂移 |
| S2 gkx 探测 | 三关键字 LIKE | absence_probe | 0 表 |
| S3 dev 消费 | 官方快照论文表 | `dev_paper_tables` | [] |
| S4 口径 A | 三表 JOIN+SUM+组内 Top3 | `jiuxin_field_country_top3` | 26 领域全出 |
| S5 居首统计 | Top1 国别计数 | `jiuxin_cn/us_field_first_count` | 23 / 3 |
| S6 口径 B | output_rank 直读 | `jiuxin_cn_output_rank_sample_top5` | 全 rank=1 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 源表 | 行数 | 库别 | 状态 |
|---|---|---|---|---|
| D1 排名面 | ads_topic_country_snapshot | 209,517 | jiuxin | **全量内置（主承载）** |
| D2 主题→领域映射 | ads_discipline_topic | 4,516 | jiuxin | 全量（26 fields 覆盖） |
| D3 领域字典 | ads_discipline_field | 26 | jiuxin | 全量（name_zh/en 双名） |
| D4 gkx 领域类 | — | 0 表 | gkx | 三关键字 0 命中 |
| D5 dev 论文面 | — | 0 表 | dev | 空载（官方快照） |

### 3.2 D1 主承载明细

output_rank 与 ranked_country_count 全量非空（PARTIAL 覆盖行排名仍出——上游在可解析子集内排名）；4,467 topics 全部挂接领域（JOIN 无落空——口径 A 26 领域行数与 topic 分布一致）。

### 3.3 D2/D3 映射链明细

`ads_discipline_topic` 的 field_id 外键 100% 命中 `ads_discipline_field`（26/26）；topic 粒度 4,516 行（含少量同 topic 多行版本）→ 口径 A 的 SUM 聚合自动去重（GROUP BY field×country 幂等）。

### 3.4 D4/D5 负结论面

gkx 无 discipline/field/rank 任何承载；dev 论文面 0 表——两库领域排名面完全空载，负结论双登记。

### 3.5 现场复核清单

- `SELECT COUNT(*) FROM ads_discipline_field` → 26
- `SELECT COUNT(DISTINCT field_id) FROM ads_discipline_topic` → 26
- 计算机科学 Top1 复算：`SUM(paper_count)` where field=计算机科学 and country=China → 147,981
- 中国居首数复算：26 领域 Top1 国别遍历计数 → 23

## 四、数据缺失情况

### 4.1 UI 八领域↔26 学科映射缺位（配置级）

UI mock 八领域（合成生物/光载信息等）与上游 26 学科（计算机科学/神经科学等）粒度不同——映射表未建。**修复建议**：建八领域→26 学科多对多映射（如 生命健康→医学/神经科学/药理学/免疫学与微生物学），或 UI 改用学科枚举。**影响面**：不建映射则领域模式回填用 26 学科直出（UI 枚举替换）。

### 4.2 指数排序键变体缺位（口径级）

seq 73 暗示排序键应为创新能力指数，上游内置的是论文量排名——指数变体（014 件评分作 rank 键）待权重裁定后加算。**修复建议**：v2 出双键榜（论文量榜+指数榜）。**影响面**：单一论文量榜可能与 seq 73 语义有偏（披露在案）。

### 4.3 领域内年度排名变化缺位（时间级）

当前口径 A 是全窗存量榜；`growth_rank`（增长排名）列在但未主消费——领域内年度排名变化（谁在爬升）需双窗分年加算。**修复建议**：v2 接 growth_rank 出「进步榜」。**影响面**：静态榜先行，动态变化延后。

## 参考文献

1. SCImago Journal & Country Rank Help[EB/OL]. SCImago. https://www.scimagojr.com/help.php （R1，学科×国别排名方法论（27 学科分类+多指标排序），2026-11-01 WebSearch 核验可达）
2. SCImago Country Rankings 2025[EB/OL]. SCImago. https://www.scimagojr.com/countryrank.php?year=2025 （R3，2025 年国别科学产出排名实数据（中国 documents 居首），2026-11-01 WebSearch 核验可达）
3. Publications Output: U.S. Trends and International Comparisons[EB/OL]. NSF NCSES. https://ncses.nsf.gov/pubs/nsb20214/publication-output-by-country-region-or-economy-and-scientific-field （R2，学科领域国别产出对比官方叙事，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

**「领域排名」在 SRS 逐字命中（seq 74，本批正名件）。** 检索记录（2026-11-01）：

| 检索词 | 范围 | 命中 |
|---|---|---|
| 领域排名 | 全球创新监测.md | **seq 74**（多维度排名展示） |
| 领域 | 全球创新监测.md | seq 74/86 等多处 |
| domain | UI 源码 | carrierRankModeModel.js:5/:22 + mockData.js:15（本件挂载） |

正名原文：
- seq 74：『提供创新载体的多维度排名，包括总体排名、领域排名、地区排名，用户可切换查看不同维度的排名情况。』

姊妹锚：
- seq 73：『基于数据模型对各创新载体的创新成果数据进行计算，生成创新能力指数，用户可查看指数计算方法和权重设置。』
- seq 84：『基于数据模型分析计算各大城市的创新能力排名，用户可查看排名结果和计算方法。』

### A.2 检索记录逐行

（检索工具：ripgrep 于 SRS 目录与 repos/demo-ui-science/src；时间 2026-11-01；命中行号已实查 ±10 行上下文。）

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_017_out.json`（20261101 实跑：26 领域 Top3 + 居首矩阵 + output_rank 验证 + 三源负结论在案）。
- 本 lane 共享探针：`code/_snapshots/_probe_lane5_s3_01_out.json`（snapshot COUNT/DESC #2/#3——output_rank/ranked_country_count 列原值）。
- 官方共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（dev 论文表 0 张）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INNOV_017_out.json`，20261101 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `jiuxin_topic_country_rows` | 计数 | 209,517 | §2.1 |
| `jiuxin_discipline_topic_rows` | 计数 | 4,516 | §2.1 |
| `jiuxin_discipline_field_rows` | 计数 | 26 | §2.1 |
| `jiuxin_field_count` | 计数 | 26 | §2.3 |
| `jiuxin_field_country_top3` | 榜单 | 26 领域×Top3 | §2.3/§2.6 |
| `jiuxin_cn_field_first_count` | 计数 | 23 | §2.3/§〇 |
| `jiuxin_us_field_first_count` | 计数 | 3 | §2.3/§〇 |
| `jiuxin_cn_output_rank_sample_top5` | 验证 | 5 主题全 rank=1 | §2.4 |
| `derived.jiuxin_cn_field_first_share_pct` | 派生比 | 88.4615 | §2.5 |
| `derived.jiuxin_top5_topics_cn_rank1_share_pct` | 派生比 | 100.0 | §2.4 |
| `dev_paper_tables` | 负结论 | [] | §2.2 |
| `absence_probe` | 探针 | gkx 0 表 + dev 0 表 | §2.2 |
| `support_judgment` | 判档 | 完全直接支持 | §〇 |

### B.3 共享快照消费（B11 零漂移）

本件消费：官方 lane5 快照 #2（209,517）作规模登记值；#3（DESC——output_rank/ranked_country_count 列）作排名列证据；官方共享快照 dev 论文表探测（0 张）作 dev 侧负结论原值。全部引用原值零漂移。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 分组学 | 三源承载 | 贴合度 |
|---|---|---|---|
| SCImago 学科×国别（R1） | Scopus 27 学科 | 26 领域+output_rank | **高（同构）** |
| NSF 学科对比（R2） | S&E 领域 | 26 领域 SUM | 中高（计数制差异） |
| UI 分组重排（R3） | mock 八领域 | 映射待建 | 中（配置层） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| snapshot 排名面 | 209,517 | rank+基数列内置 | 无（topic 级） |
| 主题→领域映射 | 4,516 | 26 fields 全覆盖 | 无 |
| 领域字典 | 26 | 双名 | 无 |
| gkx 领域类 | 0 表 | — | 结构缺失 |
| dev 论文面 | 0 表 | — | 空载 |
| 八领域映射 | 未建 | — | 配置级（§4.1） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 26 领域国别榜（口径 A 直给）+ 中国 23/26 headline | 无 |
| v2 | 指数排序键变体 + growth_rank 进步榜 | 014 权重裁定 |
| v3 | 八领域映射 + 城市级领域榜 | UI 枚举决策 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 论文量榜被当指数榜 | 中 | 双键披露（seq 73 语义偏移在案） |
| 八领域映射误配 | 中 | 映射表评审（多对多） |
| PARTIAL 行排名密度误读 | 低 | ranked_country_count 并排展示 |
| 全窗榜与年度榜混读 | 低 | 统计窗标签 |

### C.5 总判

**完全直接支持**：排名三要件（键/维度/基数）全内置 + SRS 正名（seq 74 逐字命中）——即期回填件。八领域映射与指数键变体是配置级增强，不换档。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_017.py` | 退出码 0，落 `_out.json` |
| 数据入口 | jiuxin 直连只读；gkx 经 `_gkxdb.py` | demo_* 直接 raise |
| 居首占比复算 | 23/26×100 | 88.4615 |
| 计算机科学复算 | field JOIN SUM China | 147,981 |
| 判档一致 | MD 文首 vs 产物 `support_judgment` | 完全直接支持 |
| mock 残留检查 | `rg "domain: '" repos/demo-ui-science/src/pages/global-innovation/mockData.js` | 正式版替换后无 mock |

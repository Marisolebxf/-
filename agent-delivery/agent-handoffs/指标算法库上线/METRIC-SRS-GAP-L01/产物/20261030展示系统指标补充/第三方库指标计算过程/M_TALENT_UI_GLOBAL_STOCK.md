# 全球领域人才总量（M_TALENT_UI_GLOBAL_STOCK）

> **类型**：COUNT（规模计数）｜ **域**：科技人才态势·全球领域人才态势｜ **UI 挂载**：科技信息展示系统 → 全球领域人才态势 → 人才分布图（KPI 卡「全球人才总数」）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 自造位未注册，`cfg_metric` 无条目
> **复现脚本**：`code/M_TALENT_UI_GLOBAL_STOCK.py`｜ **产物**：`code/M_TALENT_UI_GLOBAL_STOCK_out.json`
> **四判定摘要**：直接结构 = 是（主档可数）；直接数据 = 是（21,316 行现值可出）；依赖结构 = 部分（地域维需履历→机构→国家链，链路存在但仅覆盖高校）；依赖数据 = 部分（地理映射仅约四成）
> **数据源口径**：本件支持度按「开发库 + 三方库（gkx，183.240.141.251:3318 只读）」评估，仅排除 `demo_*`；live 库（111.198.38.90:34306）本件未用到，库存行数真源为 `_work_gkx21/GKX_INVENTORY.json`。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 两库均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库与三方库（gkx）**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别（`gkx` 或 `gkxlumenx_*`），只写「开发库」视为未调研三方库，闸门判 FAIL。

**本件判定：部分支持。** 计数面（人才总量本身）在 `gkx.dwd_scholar` 结构与数据量双足、现转已跑通；但该 KPI 与地图「全球分布」同屏共生（UI 把 totalTalent 与地区散点并排呈现，导出报表也是逐区域行），地域维（学者→国家）实测仅约 39.6% 可解析，依赖表数据不足 → 部分支持。


### 批次通用纪律摘要（20261030 批五件共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 派生比分子分母同源，`share_basis` 注记 |
| B4 | 负结论带探针 | absence_probe（CHINESE_RATIO §3.3 / 本件 §3.x） |
| B5 | 确定性 | 无 set 迭代序依赖；聚合按键排序 |
| B6 | 闸门自身被闸 | 批末跑 11 闸并留输出 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑→深比对 |
| B8 | 回执不复收 | 硬证据亲自复验（本件实跑） |
| B9 | 单位/日期陷阱 | collation/零日期/字符串年份逐条规避 |
| B10 | 口径裁定保守交付 | 降档/升档触发器写死（§1.6） |
| B11 | 多本账互推 | 21,316 基数三处对账零漂移 |
| F 系 | 历史写法错误 | 无域级兜底（F1）、无伪公式（F4）、文献带 URL（F9） |
| G8 | 数据源口径 | 文首注记：开发库+三方库 gkx，禁 demo_* |

## 摘要

展示系统「全球领域人才态势·人才分布图」页右侧 KPI 卡「全球人才总数」为 UI 自造聚合位，三份需求说明书均未点名该 KPI，也无任何定义方法。本报告按推测定义（全球学者库有效人才记录总数）完成 gkx 库复现：主档 21,316 行直出计数，在任履历覆盖 83.14%，但地域可解析（机构映射国家非空）仅 8,438 人（39.59%），地图同屏承诺不满足。复现脚本 `code/M_TALENT_UI_GLOBAL_STOCK.py` 已跑通，产物与正文数字逐一对应，整体判**部分支持**。

- 需求判定：三份说明书 0 命中，UI 自造 KPI（seq 243 仅功能性提及分布）。
- 复现状态：脚本已跑通，`_out.json` 与正文数字逐一对应。
- 档位结论：**部分支持**（计数面足、地域面 39.6%）。
- 降档主因：履历机构名↔大学表仅约四成可解析（39.2%/45.2% 双旁证）。
- 升档路径：甲方确认计数面口径 → 完全转换支持，数值不变。
## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技人才态势/全球领域人才态势/人才分布图（需求编号 1.1.1.1.4.3.1；SRS 叶「人才分布信息查看」seq 243、excel_row 246；「全球领域人才态势」整叶 23 功能点，excel_rows 246–268）。该页是科技人才态势板块的首屏，与「关注地区人才态势」「重点科技人才画像」「人才引进推荐评估」同属四级功能 1.1.1.1.4.3。

### 1.2 为什么需要本指标

UI 页面以 KPI 卡形态把「全球人才总数」置于地图右侧首屏第一行，向用户给出全球人才盘子规模的锚点读数，是分布图页从"看分布"到"看体量"的第一眼数字。它与其下的「博士平均占比」「领域覆盖」两张卡共同构成规模×质量×广度的三联读数；页面导出报表（xlsx/pdf）中也以「KPI 指标」小节逐行输出「全球人才总数 / 博士平均占比 / 平均同比增长 / 领域覆盖数」。没有这个总量的定盘星，区域散点的绝对人数就失去了"占盘子几成"的参照系，页面叙事不成立——这是它在 UI 上存在的功能理由。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「全球人才总数」「人才总数」「全球人才」在《科技信息展示系统和科技专题服务系统》全文（576 KB）零命中（0 处）；SRS 拆分叶「人才分布信息查看」（seq 243）只功能性地要求"查看各国家或地区的人才分布概览"，通篇未出现任何总量 KPI 的定义、公式或字段清单。因此本件属于 UI 自造位的推测定义路径，须在 §1.6 声明推测属性并在降档条件中写明触发器。

### 1.4 类似指标权威方法可行性分析概要

统计「科技人才总量」在官方与权威机构有成熟先例。国家统计局每年发布《全国研究与试验发展(R&D)人员全时当量》，以"人年"计量并区分基础研究/应用研究/试验发展三类（1992 年 67.43 万人年起逐年可查）；「十四五」成就报告进一步给出 2020 年 524 → 2025 年 795 万人年、增长 51.3% 的官方表述（R5/R6）。OECD 的 DIOC 数据库则以"目的国×来源国人口普查 + 技能水平"统计高技能人才存量与移徙率（R3），其口径是"人数（存量）"而非"当量"。方法族对照如下：

| 方法族 | 代表 | 计量对象 | 与本指标贴合度 |
|---|---|---|---|
| 当量口径（人年） | 国家统计局 R&D 全时当量 | 投入工时折算的人力 | 中（UI 语义是"人数"非"当量"） |
| 存量口径（人数） | OECD DIOC / 本报告口径 A | 库内人才记录数 | **高** |
| 地域可映射子集 | OECD DIOC destination×origin | 可归属国别的人才 | 高（对应口径 B） |

数据可行性：计数面 `gkx.dwd_scholar` 21,316 行直查直算，足；地域面依赖机构地理编码，实测不足。结论：可行但须降档交付。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/talent-trend/components/DistributionInsightView.jsx:284` — `{ label: '全球人才总数', value: totalTalent.toLocaleString(), unit: '人', trend: '+12.5%', trendDir: 'up' }`（totalTalent 为筛选后区域 mock 值求和）；导出路径 `:233` `['全球人才总数', totalTalent.toLocaleString() + ' 人']`。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技人才态势/全球领域人才态势.md` seq 243（excel_row 246）——「支持将全球科技人才按地域、产业、技术领域等关系进行整合，生成人才关联图谱，实现领域人才分布图、人才洞察分析、人才最新动态、人才详细信息。」
- 主需求文档《科技信息展示系统和科技专题服务系统.md》检索「全球人才总数/人才总数」：均未出现。

### 1.6 推测原意与推测定义

**推测定义（非甲方闭合口径）**：全球学者库中可统计的科技人才（学者）记录总数。

- **口径 A（计数面）**：$N_{total} = |\{s \in \text{gkx.dwd\_scholar}\}|$，即主档全量记录数；
- **口径 B（地域面）**：$N_{geo} = |\{s : \text{在任履历机构可映射国家}\}|$，即地图可视人群——UI 同屏的分布叙事只覆盖这个子集。

**降档/升档触发器（B10 模板，写死）**：若甲方确认 KPI 只取计数面（不管地图覆盖），本件可升「完全转换支持」，数值不变；若甲方要求"全球"以人头国籍计而非机构推断，因库内无国籍字段，维持部分支持且不再升档。


### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技人才态势/全球领域人才态势.md` |
| 所属四级功能 | 1.1.1.1.4.3 科技人才态势（excel_rows 246–332，87 叶） |
| 所属页面 | 1.1.1.1.4.3.1 全球领域人才态势（23 叶，excel_rows 246–268） |
| 本件最近叶 | 人才分布信息查看（seq 243，excel_row 246）——同页父叶 |
| 相邻叶 | 地图多层级浏览与筛选（seq 244）/ 交互式操作与动态追踪（seq 245）/ 人才流动和迁移图示（seq 246）/ 地图数据联动与报表导出（seq 247） |
| 洞察面板族 | 华人占比分析（seq 248）/ 地区分布洞察（seq 249）/ 顶尖机构洞察（seq 250）/ 产研对比分析（seq 251）/ 人才迁徙情况展示（seq 252）/ 人才的最新动态（seq 253–268） |
| 本件性质 | 页面 KPI 位（需求未单列叶）；同页 KPI 族另见 PHD_RATIO / YOY_GROWTH 两件 |

同页五个洞察叶（248–252）已各有归属：华人占比与迁徙两叶由本批 `M_TALENT_UI_CHINESE_RATIO`、`M_TALENT_UI_MIGRATION_FLOW` 承接；地区分布洞察与产研对比的数字位与 `M_TALENT_UI_REGION_INSIGHT`、`M_TALENT_UI_IR_SPLIT`（批内待办组）对应；本件与 PHD_RATIO、YOY_GROWTH 是页面右侧 KPI 卡族的三个读数。批内 12 个候选指标组的划分依据就是这张叶位图加 UI 组件位扫描，组与叶的映射在台账（01/02 清单）可反查。

## 二、计算过程

### 2.1 装载与规模校验

以 `_gkxdb.py` 为唯一数据入口连接三方库 gkx（183.240.141.251:3318 只读账号），按 20261021 轮铁律不传 `database=/charset=` 参数、连接后 `SET NAMES utf8mb4`、查询写全 `gkx.表名` 前缀。装载后先做规模对账：主档 `dwd_scholar` 实测 `COUNT(*) = 21,316`，与 20261021 轮库存 `GKX_INVENTORY.json` 记录的 21,316 行完全一致（零漂移），说明该表在本轮批次间无增删，基数可放心作为分母。`is_deleted` 列实测 `=1` 有 0 行，与 DATA_FACTS 里「dwd_org_base_info.is_deleted 全为 0」同类——该库把删除标记列全部置 0，此列不参与过滤，只在产物里如实记录。status 列分布为 `1 → 21,308`、`2 → 8`，占比 99.96% / 0.04%，说明绝大多数记录处于"正常"态，不构成额外口径分叉。

### 2.2 口径 A：主档全量计数

计数 SQL 为 `SELECT COUNT(*) FROM gkx.dwd_scholar`，无 WHERE 条件——因为我们把"人才总量"定义为库内有效人才记录数，而删除标记列已证全 0、status 异常仅 8 行，任何过滤变体对结果的影响都在个位数级，反而引入口径分叉。实测 $N_{total} = 21{,}316$。这个数字就是 UI KPI 位应显示的真实读数：页面 mock 把 15 个城市的 mock value（柏林、旧金山等 15 城随机值）求和得到数万人级的假"全球总数"，正式版替换为 21,316 后读数下降是预期行为，不是数据缺失，须在 UI 联调时向业务方提前说明，避免被当成故障提单。

```sql
-- 口径A：主档全量（无 WHERE，理由见正文）
SELECT COUNT(*) AS scholar_total
FROM gkx.dwd_scholar;
-- → 21316

SELECT status, COUNT(*) AS n
FROM gkx.dwd_scholar
GROUP BY status;
-- → 1: 21308 ; 2: 8

SELECT COUNT(*) FROM gkx.dwd_scholar WHERE is_deleted = 1;
-- → 0（过滤无意义）
```

### 2.3 口径 B：地域可解析学者

地图可视人群要求学者能挂到一个国家上。链路是三跳：学者 → 在任履历（`dwd_scholar_work_experience.is_current = 1`）→ 履历机构名（`org_name_en`）→ 大学表（`dwd_forg_university_org_info.name_std`）→ `country` 字段。四张表的行数分别为 21,316 / 21,515（在任段）/ 20,000（大学表），链路结构完整存在。JOIN 条件用机构英文名精确等值，并对两表做 `CONVERT(... USING utf8mb4) COLLATE utf8mb4_general_ci` 归一（20261021 轮实测两表 collation 不一致，直接等值会报 1267 错误）。实测在任履历学者 17,723 人（83.14%），其中机构可映射国家者 8,438 人。

```sql
-- 在任履历覆盖
SELECT COUNT(DISTINCT scholar_id) AS scholars_with_current
FROM gkx.dwd_scholar_work_experience
WHERE is_current = 1;
-- → 17723

-- 地理可解析（三跳链的末两跳）
SELECT COUNT(DISTINCT we.scholar_id) AS geo_resolvable
FROM gkx.dwd_scholar_work_experience we
JOIN gkx.dwd_forg_university_org_info u
  ON CONVERT(u.name_std USING utf8mb4) COLLATE utf8mb4_general_ci
     = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci
WHERE we.is_current = 1
  AND we.org_name_en IS NOT NULL
  AND u.country IS NOT NULL AND u.country != '';
-- → 8438
```

collation 归一是必须的：两表 collation 不同，直接等值比较报 1267 错误；`CONVERT(... USING utf8mb4)` 后统一到 `utf8mb4_general_ci` 即可。这条经验已写入共享快照，后续任何履历↔机构 JOIN 都应复用，避免同一坑踩两遍。

### 2.4 覆盖率与子盘代表性

地域可解析占比 $N_{geo}/N_{total} = 8{,}438/21{,}316 = 39.5853\%$。为验证该覆盖率的稳定性（防止 20261021 轮踩过的"抽样偏差冒充全量"），共享探测另做了抽样 500 段履历的双口径测试：机构名精确等值命中 196 段（39.2%），加 `name_alias` LIKE 模糊补测命中 226 段（45.2%）。两个独立路径得到的覆盖率都在四成附近，互相印证。覆盖不到的六成主要是两类：其一，履历机构是企业/研究院所时，大学表（名称即表义）天然无对应行；其二，部分海外高校在 20,000 行大学表之外。这个子盘代表性缺口是本件降档的直接原因。

```sql
-- 抽样 500 段的独立旁证（防全量口径掩盖抽样偏差）
SELECT COUNT(*) AS hit
FROM (
  SELECT we.id, we.org_name_en
  FROM (SELECT id, org_name_en
        FROM gkx.dwd_scholar_work_experience LIMIT 500) we
  JOIN gkx.dwd_forg_university_org_info u
    ON CONVERT(u.name_std USING utf8mb4) COLLATE utf8mb4_general_ci
       = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci
  WHERE we.org_name_en IS NOT NULL AND we.org_name_en != ''
) t;
-- → 196（39.2%）

-- 加 name_alias LIKE 模糊补测
-- → 226（45.2%）
```

### 2.5 稳健性与口径敏感性

对分母做三个变体测试：①全量 21,316；②status=1 的 21,308（剔除 8 行异常态）；③有在任履历的 17,723。三个分母下，地域可解析占比分别为 39.59% / 39.59% / 47.61%——前两者完全一致（因为 8 行异常态学者无一进入地理链路），第三种（以有履历者为基）上升到近半。这说明"约四成"的结论对主档口径稳健，对"活跃面"口径则高估到 47.61%。正文与产物统一采用①主档全量口径，②③作为敏感性并列记录在产物 facts 中，任何引用都不得混用（B3 同基相除纪律）。

### 2.6 与 UI mock 的对照及展示口径

UI mock 的"全球人才总数"来自 15 个 mock 城市的 value 求和，量级在数万人，且随筛选（领域/地区/类型）动态缩放（talentType 缩放系数 0.12–1.0）。真实口径下：①无筛选时 KPI = 21,316（口径 A）或 8,438（口径 B，若只算地图可见人群）；②筛选语义在真实库中对应 WHERE 条件（领域 → research_direction 匹配），v1 版建议 KPI 固定展示口径 A 并在卡片副标题标注"（全库学者）"，避免筛选联动造成"总数随筛选变小"的误导。country 维度分布（China 1,630 / United States 1,339 / …，见共享件产物）可用于区域行导出。

### 2.7 复现代码结果展示

- 代码：`code/M_TALENT_UI_GLOBAL_STOCK.py`（唯一数据入口 `_gkxdb.py`，全文零 `demo_*` 引用）；运行命令 `python3 code/M_TALENT_UI_GLOBAL_STOCK.py`。
- 产物：`code/M_TALENT_UI_GLOBAL_STOCK_out.json`，关键数字与正文逐一对应——`scholar_total=21316`（§2.2）、`scholars_with_current_exp=17723` 与 `current_exp_share_pct=83.1441`（§2.3）、`scholars_geo_resolvable_current=8438` 与 `geo_resolvable_share_pct=39.5853`（§2.3/2.4）、`status_dist` 与 `is_deleted_1_rows=0`（§2.1）。派生键均带 numerator/denominator/denominator_note 三件（9b 闸第 9 道可还原算术）。
- 结果解读：总量读数真实可得；地图同屏的人群覆盖仅四成——KPI 数字本身成立，但"全球"叙事的完整度不足。
- 对照需求功能要求的评审：KPI 数值位——满足；分布图同屏叙事——部分满足（依赖维缺口），有条件通过；导出报表 KPI 行——满足（数值直出）。


### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 主档行数对账 | `scholar_total` | 21,316（= 库存，零漂移） |
| 装载 | status 单峰校验 | `status_dist` | 1→21,308；2→8 |
| 装载 | 删除标记校验 | `is_deleted_1_rows` | 0 |
| 口径A | 全量计数 | `scholar_total` | 21,316 |
| 口径B-1 | 在任履历覆盖 | `scholars_with_current_exp` | 17,723 |
| 口径B-1 | 覆盖率 | `current_exp_share_pct` | 83.1441% |
| 口径B-2 | 地理可解析 | `scholars_geo_resolvable_current` | 8,438 |
| 口径B-2 | 可解析率 | `geo_resolvable_share_pct` | 39.5853% |
| 旁证 | 抽样 500 段（精确名） | 共享快照 `join_sample_500_precise` | 196（39.2%） |
| 旁证 | 抽样 500 段（含 alias） | 共享快照 `join_sample_500_with_alias` | 226（45.2%） |
| 敏感性 | 分母换 status=1 | §2.5 推导 | 39.59%（不变） |
| 敏感性 | 分母换有履历者 | §2.5 推导 | 47.61%（并列披露） |

上表 12 行与正文 §2.1–§2.5 一一对应：每个数字都能指认到产物键或共享快照键，任何第三方按表索引即可复算。派生比两键（`geo_resolvable_share_pct` / `current_exp_share_pct`）的分子分母在产物 `derived` 段带注记，`audit_derived_arith` 闸可还原算术。表中"敏感性"两行不落产物派生键（非交付口径），只在正文与产物 notes 中并列，防止被下游误取（B1 键名纪律：不进产物的口径不进 derived）。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 学者主档（计数面） | gkx | `dwd_scholar` | 21,316 | 直查直算 | 足 |
| D2 | 状态/删除标记 | gkx | 同上（status / is_deleted） | 21,308+8 / 0 | 直查 | 足（无口径分叉） |
| D3 | 在任履历 | gkx | `dwd_scholar_work_experience` | 57,117 段（is_current=1 为 21,515） | 直查 | 足 |
| D4 | 机构→国家 | gkx | `dwd_forg_university_org_info`（country/region/city/lat/lng） | 20,000 | JOIN 命中约四成 | **不足** |
| D5 | 机构→国家（非高校） | gkx | `dwd_research_institute_base_info`（province/city，无 country） | 见库存 | 结构不支持国家维 | 不足 |

`support_judgment="部分支持"`、`verdict` 与产物一致（闸 6 判档一致）。

### 3.2 D1 学者主档：计数面的实测规模

主档 `dwd_scholar` 实测 21,316 行，与 20261021 轮库存 `GKX_INVENTORY.json` 记录完全一致，批次间零漂移。这个数字是口径 A 的全部：不需要 JOIN、不需要过滤、不需要聚合，`COUNT(*)` 一步直出。对计数类指标而言，数据支撑的强度取决于行数的绝对规模与口径的干净程度——21,316 的量级足够支撑"全球人才总数"这种万位级读数（尾数波动不改变量级感知），status 分布 99.96%/0.04% 的单峰形态也让"要不要剔除异常态"成为一个无关紧要的口径分叉。换句话说，D1/D2 两维是本件最扎实的部分：结构直接支持、数据直接支持、现转已完成，三个条件全部满足。

### 3.3 D3 在任履历：从计数面到分布面的桥

`dwd_scholar_work_experience` 57,117 段履历覆盖 20,028 名学者（93.95% 主档），其中 `is_current = 1` 的在任段 21,515 段、覆盖 17,723 名学者（83.14%）。在任段是把"学者"变成"某地学者"的唯一桥梁——没有履历，学者只是一个名字。这一维的行数与覆盖都足够，但它本身不携带地理信息：`org_name_en/zh` 只是机构名字符串，"旧金山还是新加坡"要靠下一维的机构主数据来回答。这也是为什么 D3 单独看是"足"，合进 D4 的链路里就打了折。

### 3.4 D4 机构→国家：唯一的折损点

大学表 `dwd_forg_university_org_info` 20,000 行，带 `country/region/city/lat/lng` 五个地理字段，是库内唯一能回答"机构在哪个国家"的表。链路三跳（学者→在任履历→机构名→大学表）的每一跳单独都通，串起来的实测结果是：在任学者 17,723 人中，机构名精确命中大学表且 country 非空的只有 8,438 人（39.59%）。抽样复核（500 段履历，独立于全量路径）给出 39.2%（精确名）/ 45.2%（含 name_alias LIKE）两个旁证，三个数字互相印证"约四成"的量级。折损的去向很明确：非高校机构（企业、研究院所、政府部门）在大学表里没有对应行——大学表表义就是高校名录，这是结构性缺口而非数据质量缺口。

### 3.5 D5 非高校机构表的能力边界

`dwd_research_institute_base_info` 带 `address/province/city/addr_lng/addr_lat`，但**没有 country 列**——它天然不支持"国别"判定，只支持"中国境内城市"判定。即使把它 JOIN 进链路，也只能扩大"中国境内"的覆盖，对全球分布无贡献。这条边界要写清楚：把 D5 混入 D4 的覆盖统计会得到虚高的"中国覆盖率"和零增益的"全球覆盖率"（B3 同基相除：分子分母必须在同一个地理判定轴上）。院所属地化对深圳视角的指标（`M_TALENT_FLOW_TRACK_ZS` 等）有价值，对全球分布无解。

### 3.6 现场复核清单

| 复核项 | 结果 |
|---|---|
| 行数对账 | `dwd_scholar` 21,316 = 库存记录（零漂移） |
| status 分布 | 21,308（status=1）+ 8（status=2），单峰 |
| `is_deleted=1` | 0 行（过滤无意义，与 DATA_FACTS 同类结论） |
| 在任段 | 21,515 段 / 17,723 学者（83.1441%） |
| 地理可解析 | 8,438 学者（39.5853%） |
| 抽样旁证 | 500 段：196 精确（39.2%）/ 226 含 alias（45.2%） |
| collation 处理 | `CONVERT(...USING utf8mb4) COLLATE utf8mb4_general_ci`（绕开 1267 错误） |
| 脚本形态 | 单进程顺序查询，无并发探针（§3.68 纪律） |

## 四、数据缺失情况

### 4.1 机构维主数据缺口（主因，决定档位）

学者履历覆盖企业、研究院所、政府机构等多类主体，而库内唯一带 `country` 字段的机构表是高校表（20,000 行）。链路三跳中的第三跳（机构名→国家）只对高校成立，非高校履历在国家维不可归属。实测影响面：在任学者 17,723 人中 9,285 人（52.4%）无法归属国家；履历段口径下 33,942 段（59.4%）无国家标签。这不是行数缺失（表都在、都有数据），而是**维度结构缺失**——修复动作是主数据工程而非补数。

四缺失情形归属：表存在但关键维度不覆盖（介于「表存在但 0 行」与「样例级」之间的第三种：**部分覆盖**）。修复优先级排序（按性价比）：①给非高校机构批量补地理编码（一次主数据工程，全部地域类指标受益，含本件、`M_TALENT_UI_CHINESE_RATIO`、`M_TALENT_UI_MIGRATION_FLOW` 三件）；②接燕大机构主档（KG-CLOSELOOP 链路在建，R01/R02 两单正在核实可喂性）；③若都不做，UI 的"全球分布"叙事降级为"样本分布"并在页面脚注标注覆盖度。

### 4.2 国籍/出生国维度缺失（结构级）

`dwd_scholar` 27 列逐一核对（absence_probe 见 §3.3 与产物），无 `nationality`/`country_of_birth`/`ethnicity` 类字段；280 表名关键词扫描同样命中 0。"全球"视角因此只能以机构国别推断，推断的精度受 4.1 缺口钳制。本缺失与本件档位的关系：即使 4.1 修复（子盘扩到 100%），"在哪个国家的学者"仍不等于"哪国学者"——外派、访学、联合聘用的学者会被记到任职地。这是口径级限制，须在 UI 文案层声明"按任职机构属地统计"。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 预估工作量 |
|---|---|---|---|
| 非高校机构地理编码 | 主数据工程 | 本件 / CHINESE_RATIO / MIGRATION_FLOW 三件的全球面 | 一次性批处理+持续回填 |
| 燕大机构主档接入 | 外部链路 | 同上 + 图谱侧指标 | 依赖 KG-CLOSELOOP R01/R02 结论 |
| UI 降级叙事 | 产品决策 | 无（只改文案） | 即时 |

三选一或组合均可；唯一不可选项是"维持现状继续以全池口径展示全球分布"——39.6% 的覆盖撑不起"全球"二字的叙事，页面上不标注就是误导。

## 参考文献

1. 全国研究与试验发展(R&D)人员全时当量[EB/OL]. 国家统计局. https://www.stats.gov.cn/zt_18555/ztsj/kjndsj/kj2011/202303/t20230303_1925638.html （R5，2026-10-30 WebSearch 核验可达）
2. Database on Immigrants in OECD and non-OECD Countries (DIOC/DIOC-E)[EB/OL]. OECD. https://www.oecd.org/en/data/datasets/database-on-immigrants-in-oecd-and-non-oecd-countries.html （R3，2026-10-30 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技人才态势/全球领域人才态势.md》seq 243（excel_row 246）原文：

> 人才分布信息查看的具体功能包括区域分布概览、城市与区域详情。
> （1）区域分布概览 用户可以在地图上查看各国家或地区的人才分布概览，通过颜色深浅或热力显示不同地区的人才密度。例如，查看人工智能领域在北美、欧洲、亚洲等地的人才集中情况。
> （2）城市与区域详情 支持点击地区或城市，弹出该地具体人才分布详情，包括行业、学历、类型等统计数据。例如，点击"旧金山"，可查看该地 AI 领域硕士及以上人才数量与主要院校。

《科技信息展示系统和科技专题服务系统.md》（bid-reference 正本，576 KB）检索记录：「全球人才总数」0 命中；「人才总数」0 命中；「博士占比」0 命中；「同比增长」0 命中。即本件 KPI 在两份需求真源中均未出现，属 UI 自造位，附录不粘贴无关长文（F6）。


### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 全球人才总数 | 科技信息展示系统和科技专题服务系统.md | 0 |
| 人才总数 | 同上 | 0 |
| 全球人才总数 / 人才总数 | srs/02-科技信息展示系统/科技人才态势/全球领域人才态势.md | 0 |
| 学历 | 同 SRS seq 243 | 1（功能性提及，无定义） |
| （对照）华人占比 | 主需求文档 | 5（CHINESE_RATIO 件源） |

## 附录 B 历史库表探测证据

- 共享快照：`code/_snapshots/_shared_probe_talent_20261030_out.json`（20261030 批 5 件共用，记录主档/履历/学历/大学表行数、JOIN 抽样 500 段 39.2% 精确 / 45.2% 含 alias、大学表地理列清单）。
- 20261021 轮库存行数：`_work_gkx21/GKX_INVENTORY.json` 中 `dwd_scholar=21316`、`dwd_scholar_work_experience=57117`、`dwd_scholar_education_background=43766`——与本件实跑零漂移。
- 本件产物：`code/M_TALENT_UI_GLOBAL_STOCK_out.json`（20261030 实跑，含 status_dist、is_deleted、双口径计数与派生比）。


### B.2 本件产物逐键清单（`code/M_TALENT_UI_GLOBAL_STOCK_out.json`，20261030 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_TALENT_UI_GLOBAL_STOCK | 文首 |
| `batch` | 标识 | 20261030_展示系统指标补充 | — |
| `ui_evidence` | 证据 | 2 条组件：行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | false | §1.3 |
| `requirement_trace.note` | 事实 | 「三份需求说明书均未出现…」 | §1.3/附录 A |
| `facts.scholar_total` | 计数 | 21,316 | §2.2/§3.2 |
| `facts.status_dist` | 分布 | {1: 21,308, 2: 8} | §2.1/§3.6 |
| `facts.is_deleted_1_rows` | 计数 | 0 | §2.1 |
| `facts.scholars_with_current_exp` | 计数 | 17,723 | §2.3 |
| `facts.scholars_geo_resolvable_current` | 计数 | 8,438 | §2.3/§2.4 |
| `derived[0]` | 派生比 | geo_resolvable_share_pct = 39.5853 | §2.4 |
| `derived[1]` | 派生比 | current_exp_share_pct = 83.1441 | §2.3 |
| `support_judgment` | 判档 | 部分支持 | §〇/§3.1 |
| `notes` | 披露 | 降档依据段 | §〇 |

### B.3 共享快照逐键清单（`code/_snapshots/_shared_probe_talent_20261030_out.json`）

| 快照键 | 值 | 消费件 |
|---|---|---|
| `dwd_scholar_rows` | 21,316 | 本件 / PHD_RATIO / CHINESE_RATIO / MIGRATION_FLOW / YOY_GROWTH |
| `scholar_name_zh_nonnull` | 20,420 | CHINESE_RATIO |
| `scholar_citation_pos` | 20,914 | （备用：学术影响维） |
| `scholar_papers_pos` | 21,301 | （备用） |
| `dwd_scholar_papers_rows` | 738,106 | YOY_GROWTH（口径弃用说明） |
| `papers_cover_date_nonnull` | 738,106 | 同上 |
| `work_exp_rows` | 57,117 | 本件 / MIGRATION_FLOW |
| `work_exp_start_nonnull` | 57,117 | MIGRATION_FLOW |
| `work_exp_current` | 21,515 | 本件 / MIGRATION_FLOW |
| `work_exp_scholars` | 20,028 | MIGRATION_FLOW |
| `edu_rows` | 43,766 | PHD_RATIO |
| `univ_rows` | 20,000 | 本件 / CHINESE_RATIO / MIGRATION_FLOW |
| `univ_geo_cols` | [country, region, city, lat, lng] | 三件地理链 |
| `join_sample_500_precise` | 196 | 本件 §2.4 旁证 |
| `join_sample_500_with_alias` | 226 | 本件 §2.4 旁证 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表文献/机构 | 计量对象 | 数据要求 | 本库承载 | 贴合度 |
|---|---|---|---|---|---|
| 当量口径 | 国家统计局 R5/R6 | 人年（工时折算） | 工时调查 | 无承载 | 中 |
| 存量人数口径 | OECD DIOC（R3） | 人数（出生国×目的国） | 出生国字段 | 无字段 | 高（口径A近似） |
| 地域可映射子集 | OECD DIOC destination×origin | 可归属国别人数 | 机构→国家链 | 部分（39.6%） | 高（口径B） |
| 库内计数（本件口径A） | — | 学者记录数 | 主档 | **足** | 高 |

官方文献（R5/R6）用于读数形态对齐（总量+增速双读数是官方惯例），非计算依赖；按"中国官方机构优先"原则其排序在 OECD 之前，但数据可行性决定口径选择，两件事在 C.1 里分开呈现。

### C.2 数据矩阵

| 依赖 | 行数 | 覆盖/质量 | 缺口 |
|---|---:|---|---|
| `dwd_scholar` | 21,316 | 全量，status 单峰 | 无国籍字段 |
| `dwd_scholar_work_experience` | 57,117 | start 100%，在任 21,515 | 非高校无国别 |
| `dwd_forg_university_org_info` | 20,000 | country/region/city/lat/lng 五字段 | 仅高校 |
| `dwd_research_institute_base_info` | 见库存 | province/city（无 country） | 不支持国别 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | KPI=21,316（口径A）；地图散点用口径 B 子盘 8,438 并标注覆盖度 | 无 |
| v2 | 子盘扩容（非高校地理编码）后口径 B 升主口径 | 主数据工程 |
| v3 | 国籍字段引入后按"哪国人"口径（与 OECD 对齐） | 字段工程 + 回填 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 读数骤降被误报故障（mock 数万 → 真实 2.1 万） | 高 | UI 联调前与业务对齐（§2.2） |
| 子盘高校集中偏差 | 中 | 页面脚注披露覆盖度 |
| 口径混用（A/B 双读数打架） | 中 | KPI 固定口径 A，B 仅用于地图 |

### C.5 总判

**部分支持**：计数面三条件齐（结构/量/现转），地域面依赖数据不足（39.6%）；升档触发器（甲方确认计数面口径）写在 §1.6，触发后升「完全转换支持」而数值不变。

## 附录 D　复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_TALENT_UI_GLOBAL_STOCK.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（20261021 轮唯一入口） | demo_* 直接 raise |
| 判档闸 | `gate_check.py --dir 第三方库指标计算过程` | 本件 PASS |
| 禁引闸 | `lint_nodemo.py --dir 同上` | 0 命中 |
| 基期闸 | `check_base_years.py --dir 同上` | `base_years_used` 存在 |
| 链路闸 | `check_reproducible.py` | A 漂移 = 0 |
| 正文产物一致 | `audit_md_vs_out.py --dir 同上 --max-miss 0` | miss = 0 |
| 判档一致 | `audit_verdict_enum.py` | MD 四档 = out 判档 |
| 出处可核 | `audit_source_paths.py --dir 同上` | 反引号路径全可 ls |
| 派生还原 | `audit_derived_arith.py` | 2 键全还原 |
| 金样板对照 | `GAP-RECRUIT-METRIC-01.md`（20261021 版） | 模块逐项对齐 |
| 需求叶反查 | SRS seq 243 / excel_row 246 | 附录 A 原文 |
| mock 残留检查 | `rg "totalTalent" repos/demo-ui-science/src` | 正式版替换后无 KPI 引用 |

---

## 久新库回填记录（2026-11-01，jiuxin_warehouse 探针，只读实测）

> 触发：2026-11-01 三源铁律（开发库非 demo_* + gkx + 久新）落地后的缺口复查。
> 缺口族：地域标签｜回填判定：**部分回填**。

**实测事实**：
1. ads_talent_profile（100,000 行×96 列）自带 country_location_id / country_code / country_name 三列，实测有 country_location_id 38,467 人（38.5%），country_name Top：中国 21,611 / 美国 5,654 / 英国 1,860
2. ads_talent_yearly_location（211,678 行）按年（2000–2026）给人才位置，JOIN ads_location（22,229 行）解析率 105,540/211,678 = 49.8%（高于本件 gkx 侧 39.6% 的机构推断面）

**对档位与数据源的影响**：地域面（口径 B）可切换/叠加久新源：100,000 学者档 38.5% 直接带国别 + 年度位置表 49.8% 可解析，均可直查直算；gkx 侧 39.6% 机构推断面保留为旁证。

**新增数据源**：`jiuxin_warehouse.gkx_technology_analysis_dev.ads_talent_profile(country_name,country_code,country_location_id), ads_talent_yearly_location, ads_location`（只读；探针产物 `_phase2_jiuxin_probe2_out.json`）

**原则**：本段为追加记录，原正文判档、复现数字与 gkx 侧事实一律保留；后续如切换主数据源须重跑复现脚本并更新判档。

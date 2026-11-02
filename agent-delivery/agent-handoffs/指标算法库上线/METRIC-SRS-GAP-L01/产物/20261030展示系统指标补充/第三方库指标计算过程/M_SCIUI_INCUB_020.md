# 载体平均增长率（年）（M_SCIUI_INCUB_020）

> **类型**：简单统计类（载体年度序列三源零承载）｜ **域**：科技信息展示系统·科技成果展示·科技时空演进展示·演进回放面板「平均增长率」（需求侧平行锚：科技创新生态展示·载体增量统计）｜ **UI 挂载**：`pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:1126`（growthRate 项）+ `:1042`（formatGrowthRate 环比实现）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（三份说明书未出现「平均增长率」指标名；语义锚 SRS 序号 486「载体年度与季度增量统计」+ 主需求 :3423 采集要求在案，平均口径无定义；UI 实现为回放快照序列逐期环比）｜ **口径归属**：UI 派生读数（mock 快照 events 272/434/600/774/894 演示序列）
> **复现脚本**：`code/M_SCIUI_INCUB_020.py`｜ **产物**：`code/M_SCIUI_INCUB_020_out.json`
> **四判定摘要**：直接结构 = 无（载体年度序列结果面三源无）；直接数据 = 无（同左）；依赖结构 = **缺**（dev `dim.carrier` 28 行 v1_approx 主档**无成立/备案年份列**；`enterprise_innovation_carrier`/`carrier_index` 结构齐但双 0 行）；依赖数据 = 无（gkx 0 命中；久新 218 表 live 复核 0 命中）
> **数据源口径**：三源（dev live `10.50.11.76` `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表复核）逐一探针留证；`demo_*` 禁引；UI mock 值仅作需求语义证据。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库与久新库**均无法构建 |

**四判定**：表结构直接支持 / 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。**增长率的计算前提是「载体年度序列」（存量逐年或新备案流水）——dev 唯一近似主档 `dim.carrier` 28 行 9 列（carrier_id/name/type/level/坐标/source=v1_approx）**无任何年份列**；两张序列预留面 `enterprise_innovation_carrier`（publish_date 列在）与 `carrier_index`（stat_period/index_score/rank 列在）**双 0 行**空壳；gkx 280 表 incub/carrier 词族 0 命中；久新 218 表 live 复核 0 命中。基期序列本身无承载，比率无从算起。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 环比分母=上一期快照值（mock 链实读） |
| B4 | 负结论带探针 | absence_probe 四件（dev 序列/gkx/久新/需求原文） |
| B5 | 确定性 | mock 序列按文件序；环比链确定性计算 |
| B7 | 产物只由脚本产出 | 本件 py 实探+实算产出 _out.json |
| B9 | 单位/日期陷阱 | 单位=%；mock 快照 label 为年字符串 |
| B10 | 口径裁定保守交付 | 逐期环比/均值/CAGR 三口径并列披露 |
| B11 | 多本账互推 | dev 载体表行数与共享快照零漂移 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成增长率结果面吗？ | 无 | absence_probe |
| 载体年度序列原料齐吗？ | **缺** | dim.carrier 无年份列；序列面双 0 行 |
| 现在就能算吗？ | 不能 | 基期序列无承载 |

## 摘要

「载体平均增长率（年）」挂在时空演进页「演进回放」面板：相邻回放快照的时空事件数环比变化率（`formatGrowthRate=(cur-prev)/prev`），mock 五年快照 272/434/600/774/894 对应逐期环比 59.6%/38.2%/29.0%/15.5%（均值 35.6%，KPI trendLabel 另示 18.4%）。数据侧判定：**完全不支持**——载体年度序列两层（存量年份维+增量流水）三源均无数据：dev `dim.carrier` 28 行 v1_approx 主档无年份列，`enterprise_innovation_carrier`/`carrier_index` 结构齐双 0 行；gkx/久新词族 0 命中。增长率天然依赖基期，基期序列无承载即无从算起。权威口径：Eurostat AAGR/BEA 复利式、OECD 年度环比式。

- 需求判定：指标名三份说明书未出现；语义锚序号 486「载体年度与季度增量统计」（主需求 :3423：自动采集年度/季度新建立和新备案载体+同比环比分析）。
- 复现状态：三源探针+mock 环比链实算已跑通。
- 档位结论：**完全不支持**（基期序列全缺）。
- 关键事实：dev 载体序列面是「schema 已建、数据未灌」双空壳（publish_date/stat_period 列齐）——升档只差灌数。
- 升档路径：载体备案年份落库 → 年度序列可构建 → 完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 科技时空演进展示 → 演进回放面板（`SpaceTimeEvolutionPage.jsx:1126`「平均增长率」＝`buildPlaybackFeatureItems` 的 growthRate 项，取 `formatGrowthRate(metrics.events, previousMetrics.events)`）；公式实现 `:1042-1048`：`((current-previous)/previous*100).toFixed(1)%`，previous=0 时显示「基准」。数据链：`spaceTimeEvolutionMock.js:436-520` `playback.snapshots.year[]` 五快照（2022-2026）。

**挂载点归属注记**：派单书将本件归 INCUB 族（l3=平均增长率），实际挂载组件在时空演进页回放面板——语义主锚是「时空事件增长率的回放呈现」，载体增量语义（序号 486）为需求侧平行锚。两锚共享「年度序列无承载」结论（产物 notes 登记）。

### 1.2 为什么需要本指标

回放面板要让管理者一眼看到「演进在加速还是放缓」：增长率是回放叙事的量化锚点（序号 486 语境：识别创新活跃区和政策带动成效；序号 501 语境：回溯演变历程自动生成趋势变化报告）。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**（序号 486 给出采集要求未定义平均口径；UI 实现为逐期环比。）

### 1.4 类似指标权威方法可行性分析概要

增长率口径方法族（完整版指向附录 C）：①Eurostat AAGR——复利式 (期末/期初)^(1/n)-1，跨期可比；②BEA 平均年增长——同复利式变体（periodicity 参数化）；③OECD 年度增长——本年四季和÷上年四季和-1（链式环比族）；UI 实现属③的单期形态，「平均」若取全期应为①或逐期均值（mock 均值 35.6% 参照）。

### 1.5 引用来源

1. Eurostat. Glossary: Annual average growth rate (AAGR). https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Annual_average_growth_rate_%28AAGR%29
2. U.S. Bureau of Economic Analysis. How is average annual growth calculated? https://www.bea.gov/help/faq/463
3. OECD. Methodological notes: OECD GDP growth. https://www.oecd.org/content/dam/oecd/en/data/methods/OECD-Quarterly-GDP-Growth-Methodology.pdf

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：回放相邻快照的事件量环比（UI 现形态）；需求侧平行锚为载体存量/增量年度增长率。
- **操作化定义（本件未实现）**：逐期环比 = (Vₜ-Vₜ₋₁)/Vₜ₋₁×100%；全期平均 = AAGR 复利式——**双口径并列**。
- **降档触发器**：已处最低档。
- **升档触发器**：载体年份维落库（dim.carrier 扩列或序列面灌数）→ 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：时空演进·演进回放（序号 501 地域流动明细与历史回溯语境）。
- 相近叶：INCUB_032（时空事件增长量，同 mock trendSections）/INCUB_033（时空事件趋势，同 regions.years.events 序列）——三件共享「mock 时空事件序列无真实承载」结论；需求侧与 ECOSYS_001 族（生态增量）语义相邻。

## 二、计算过程

从缺。本指标需载体年度序列（或真实事件快照序列）作基期（§1.4 权威式），三源探针（附录 B 四件）证明序列层无数据承载：dev 主档无年份列、序列面双 0 行；gkx/久新 0 命中——无基期即无除式，禁伪公式。mock 环比链 [59.6, 38.2, 29.0, 15.5]% 与均值 35.6% 仅为演示量级参照（产物键 `derived[1]`，B10 披露）。复现代码与证据对照见产物 `derived[0]`（负结论留空登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 载体存量主档（截面） | dev `dim.carrier` | 28 行 v1_approx（**无年份列**） |
| 载体年度序列（增量流水） | dev `enterprise_innovation_carrier` / `carrier_index` | 结构齐**双 0 行** |
| 时空事件快照序列（UI 锚） | 三源 | 无承载（mock only） |
| 要素侧 | gkx / 久新 | 0 命中 / 0 命中 |

### 3.2 现场复核清单

`dim.carrier` 样本（合肥科技大学/中科院北京先进技术研究院…source=v1_approx）9 列全读无年份；`carrier_org_rel` 57 行 rel_type=self。UI 公式链实读：`:1042` 环比式→`:1126` growthRate 项→`:1119` note「2025-2026 节点变化」。mock 快照 `metrics.events` 五值与 KPI trendLabel「18.4% 环比」、均值 35.6% 三口径差异已披露（B10）。

## 四、数据缺失情况

### 4.1 缺口清单

①载体年份维缺失（主档无列）；②序列面双 0 行（结构在数未灌）；③事件快照序列无真实承载（mock only）；④「平均」口径未定义（逐期/均值/CAGR 三候选）。

### 4.2 修复建议与影响面

短期：`dim.carrier` 扩 `established_year`/`registered_date` 列（28 行可从公开名录回填）；或 `enterprise_innovation_carrier` 灌数（publish_date 列已在）→ 年度序列可构建，本件与 INCUB_022（载体成果总览）联动受益。中期：载体增量按季落 `carrier_index`（stat_period 列已在）→ 序号 486 需求完整落地。

### 4.3 影响面

回放面板「平均增长率/热点转移/新兴领域」三卡全为 mock 演示态；回放动画本身读 mock snapshots 无后端。

## 参考文献

1. Eurostat. Glossary: Annual average growth rate (AAGR). https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Annual_average_growth_rate_%28AAGR%29
2. U.S. Bureau of Economic Analysis. How is average annual growth calculated? https://www.bea.gov/help/faq/463
3. OECD. Methodological notes referring to the OECD QNA press release: OECD GDP growth. https://www.oecd.org/content/dam/oecd/en/data/methods/OECD-Quarterly-GDP-Growth-Methodology.pdf

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 平均增长率` 三份说明书 + 主需求 → 指标名 0 命中。
- 语义锚原文（SRS 科技创新生态展示.md 序号 486「载体年度与季度增量统计」；主需求 :3423 同文）：「自动采集年度和季度内新建立和新备案的创新载体数据，按地区、载体类型等维度高亮显示增长速度和空间分布变化。包含同比、环比变化分析，趋势曲线及专属报表一键生成。」
- UI：`spaceTimeEvolutionMock.js:436-520` `snapshots.year[].metrics.events`（272/434/600/774/894，mock 演示值）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_020_out.json`）

facts（ui_mount/ui_formula_read/ui_mock_snapshot_events/ui_mock_snapshot_labels/ui_mock_yoy_series/ui_mock_yoy_mean=35.6/ui_mock_kpi_trendlabel/ui_mock_note/dev_table_total=542/dev_dim_carrier_rows=28/dev_dim_carrier_cols/dev_dim_carrier_note/dev_enterprise_innovation_carrier_rows=0/dev_enterprise_innovation_carrier_cols/dev_carrier_index_rows=0/dev_carrier_index_note/gkx_table_count=280/gkx_incub_word_tables/jiuxin_table_count_live=218/jiuxin_incub_word_tables/srs_anchor/named_in_srs/named_note/authoritative_formula）；derived[0]（负结论 null 登记）/derived[1]（mock_reference 35.6% 披露）；absence_probe（四件）；support_judgment=完全不支持；base_years 三键（基期维整体缺失为主因）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：Eurostat AAGR（复利式，跨期可比）→ BEA 变体（periodicity 参数）→ OECD 环比式（UI 现形态）。数据矩阵：载体年度序列三源无数据（主档无年份列+序列面双 0 行）。分期方案：一期年份维回填（完全转换支持）、二期季度增量流水（序号 486 完整落地）。风险登记：v1_approx 主档年份回填的数据质量、「平均」口径需产品裁定。总判：完全不支持（基期序列全缺，升档=灌数即活）。

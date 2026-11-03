# 指标趋势序列（M_SCIUI_TECHTRK_024）

> **类型**：SERIES（时间序列，存量计数）｜ **域**：科技发展态势·技术发展跟踪/科技发展规划·多维度指标体系展示｜ **UI 挂载**：科技信息展示系统 → 科技发展规划 → 多维度指标体系展示卡「统计库」分组第 3 张 KPI 卡（TechDevelopmentPlan.tsx:830 `{ label: '趋势序列', value: '84', change: '+3.8%' }`，mock 84，演示值不参与支持度结论）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 推导叶（筛选记录 row_01 31），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_TECHTRK_024.py`｜ **产物**：`code/M_SCIUI_TECHTRK_024_out.json`
> **四判定摘要**：直接结构 = 否（三源无「统计指标序列条数」结果面）；直接数据 = 否；依赖结构 = 是（久新 geo_yearly_metrics 171,736 行 + patent_analysis_jurisdiction 675 行年度序列）；依赖数据 = 部分（序列口径三源异构 + 开发库序列表全空载 + 「序列可用」阈值无需求定义）
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

**本件判定：部分支持。** 「趋势序列」在 UI 上是一张 KPI 计数卡（值 84、环比 +3.8%），语义是「统计库中可用作时间序列的指标条数」。三源没有任何表直接给出这个「序列条数」结果面（开发库 5 张序列类表 4 张 0 行、gkx 命中 0），但久新两张表的结构化年度序列完全可用：`ads_geo_yearly_metrics`（jiuxin_warehouse，171,736 行 = 13,445 个 location × 年，四列指标）与 `ads_patent_analysis_jurisdiction`（675 行，YEAR: 期年度序列）。降档根因有二：其一，**「序列」的计数口径无需求定义**——84 对应什么口径（哪些指标算、跨度几年算可用）三份说明书一字未提，任何复算都是口径假设；其二，**序列承载三源异构**——论文/项目/人才/机构序列在 geo 表（地理维）、专利序列在 jurisdiction 表（受理局维，非国家维），「统计库」语义下的统一序列目录须跨源拼装且维度不同源。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 本件为计数非比值；derived 登记分子分母说明 |
| B4 | 负结论带探针 | absence_probe：gkx 280 表序列面扫描 / dev 序列表逐表行数 |
| B5 | 确定性 | 跨度分布按 span 排序、中位数 Python 侧确定性计算 |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑（本件 3 次改脚本 3 次重跑） |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | statistics_year 为 smallint 直读；2026 残年剔除趋势解读 |
| B10 | 口径裁定保守交付 | 序列计数口径 A/B 并列 + 阈值待裁定触发器写死（§1.6） |
| B11 | 多本账互推 | geo_yearly_metrics 171,736 与 lane5 共享探针零漂移；gkx 专利 2,939,895 引用官方快照 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 有现成「序列条数」结果面吗？ | 无 | 三源 absence_probe：gkx 命中 0、dev 序列表 4/5 空载 |
| 年度序列本身可算吗？ | 可 | jiuxin geo_yearly_metrics 171,736 行 + jurisdiction 675 行 |
| 序列计数口径闭合吗？ | 不闭合 | mock 84 无口径定义；跨度阈值（本件设 ≥5 年）是假设 |

## 摘要

「趋势序列」是科技发展规划页「多维度指标体系展示」卡里统计库分组的第 3 张 KPI 卡，前端 mock 给 84（+3.8%）——按兄弟卡片（统计指标 186.7 亿、年度样本 3,260、空间指标 56）的构词法，它数的是「统计库中按年可比的指标序列条数」。三源探测：开发库序列类表 5 张中 4 张 0 行（仅 policy_timeseries 37 行政策时间点）；gkx 无任何指标年度序列结果面；久新 `ads_geo_yearly_metrics` 171,736 行（13,445 location × 2015-2026 × 论文/项目/人才/机构四列）与 `ads_patent_analysis_jurisdiction`（4 受理局 × 1990-2025 年序列）构成可用序列池。本报告以「跨度 ≥5 年」假设复算：可用序列 40,508 条（10,126 location × 4 列 + 4 条专利序列），序列跨度中位数 12 年（均值 12.77、最长 27）。降档双因：mock 84 的计数口径无需求定义（任何阈值都是假设）；序列承载三源异构（地理维 vs 受理局维）。判**部分支持**。脚本已跑通，正文与产物数字逐一对应。

- 需求判定：**UI 推导叶**（指标名三份说明书未出现；语义最近叶为科技发展规划.md seq 179「多维度指标体系展示」——本挂载点正是其 UI 实现）。
- 复现状态：脚本已跑通；序列池规模、跨度分布、US 示范序列 2014-2025 落产物。
- 档位结论：**部分支持**（序列计数口径假设 + 承载异构双因）。
- 关键事实：开发库 5 张序列表 4 张空载——「有表无数」是本件开发库侧的典型形态。
- 升档路径：甲方裁定序列入选口径（哪些指标维 + 跨度阈值）→ 统一序列目录发布 → 可升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**科技发展规划**/综合发展规划/多维度指标体系展示（SRS seq 179，excel_row 182）。UI 挂载点是 `TechDevelopmentPlan.tsx` 的 `multidimensionalIndicatorCategories` 常量：七个分类 Tab（技术发展/产业数据库/机构库/课题库/成果库/**统计库**/人才库），每个分类四张 KPI 卡。「趋势序列」在统计库分组第 3 位（`:830`），前有「统计指标 186.7 亿」「年度样本 3,260」，后有「空间指标 56」。渲染位置 `:2826-2832`（`activeIndicatorCategoryItem.metrics.map`），每卡显示 label / value / change 三读数，点击分类 Tab 联动切换。

mock 值语义推断：兄弟卡「空间指标 56」给的是一个明确的小整数，「趋势序列 84」与其并排，最合理的读法是「统计库中可按时间轴出序列的指标条数 84 条、环比新增 3.8%」。卡片是纯静态常量（无任何计算逻辑），**全部为前端硬编码，演示值，不参与支持度结论**。值得记录的组件行为：`linked: ['趋势对比', '区域统计', '指标口径']` 声明了联动入口但未实现跳转——「指标口径」入口的存在暗示前端作者预期这批数字将来需要口径披露页，与本报告 B10 双口径交付同向。

### 1.2 为什么需要本指标

规划场景的核心问题是「哪些指标能看趋势」：决策者做五年规划回溯时，只有跨年可比的指标序列才有分析价值，单点快照无法支撑「变好还是变坏」的判断。统计库分组把「趋势序列」做成独立 KPI 卡，就是在告诉用户：这个库不只是数字仓库，其中 84 条（mock）指标可以拉出时间曲线。它同时是数据治理读数——序列条数的环比变化（+3.8%）反映统计库的时序化覆盖率在提升还是停滞。

数据侧本件的张力在「序列」一词的三层含义：① 条数（UI 卡片语义，本件主体）；② 序列本身（哪 84 条、每条什么形状——由 M_SCIUI_INNOV_002 承接演进语义）；③ 序列质量（跨度、连续性、可比性）。本报告复算的是 ①+③：给出三源当前能产出的序列条数与跨度分布，让「84 是什么口径」的裁定有数据可依。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「趋势序列」该词未出现在三份说明书（《科技发展态势/技术发展跟踪.md》《科技全域态势.md》《全球创新监测.md》）及主需求文档《科技信息展示系统和科技专题服务系统.md》。语义最近的原文有三处，均为功能描述：科技全域态势.md seq 12「监测数据趋势变化查看功能」——『提供时间轴趋势展示，用户可查看特定要素随时间变化的趋势』（要素级趋势查看，非序列计数）；科技发展规划.md seq 179「多维度指标体系展示」——『在大屏上展示技术发展、产业数据库、机构库、课题库、成果库、统计库、人才库等指标体系』（本挂载点的需求出处，只列库名不给指标口径）；全球创新监测.md seq 71『用户可查看预测结果和趋势分析』。三处都没有「序列怎么计数、什么指标入选、跨度门槛」的任何定义。

### 1.4 类似指标权威方法可行性分析概要

「指标序列可用性」在官方统计体系有成熟先例。OECD MSTI 明确以 148 个关键指标的**年度时间序列**监测成员国 S&T 表现，序列口径（参考年、国别归属、分数计数）逐指标发布元数据（R4）；欧盟 RIS 复合指数要求每指标至少 8 年数据窗并显式做插补与异常值处理（R5）；Hyndman & Athanasopoulos 的预测实践则把「序列足够长」（通常 ≥2 个季节周期或 ≥8-10 个观测点）作为可建模的门槛（R3）。方法族对照：

| 方法族 | 序列可用门槛 | 数据要求 | 与三源匹配 |
|---|---|---|---|
| OECD MSTI 式指标目录 | 逐指标元数据发布，序列即产品 | 指标注册表+年度值 | **无（三源无指标注册表）** |
| 欧盟 RIS 式数据窗 | ≥8 年窗+插补 | 长窗年度面板 | **部分（geo 序列中位 12 年达标，短序列 1-4 年占 24.5%）** |
| 预测建模门槛（Hyndman） | ≥2 周期/8-10 点 | 同上 | **部分（同上）** |
| 本件口径 A（跨度 ≥5 年） | 保守门槛假设 | location×年计数 | **有（可直查）** |

结论：权威体系的「序列目录」需要指标注册表承载，三源均无；但序列本体（geo 四列 + 专利受理局）结构齐全、量足，按假设门槛可即时产出条数。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/TechDevelopmentPlan.tsx:830` — `{ label: '趋势序列', value: '84', change: '+3.8%' }`；`:824-834` 统计库分组常量全貌；`:2826-2832` KPI 卡渲染；`:833` `linked: ['趋势对比', '区域统计', '指标口径']` 联动声明。
- SRS：`…/科技发展态势/科技发展规划.md` seq 179（excel_row 182）多维度指标体系展示——本挂载点需求出处（未定义指标口径，附录 A）；`…/科技全域态势.md` seq 12 监测数据趋势变化查看功能（要素级趋势，非计数）。
- 主需求文档：《科技信息展示系统和科技专题服务系统.md》「趋势序列」0 处命中（检索记录附录 A）。
- 久新 schema：表结构以本批探针 DESC 实查为准（`code/_snapshots/_probe_lane5_s3_01_out.json`）。

### 1.6 推测原意与推测定义

**推测定义（B10 双口径并列，均须披露口径假设）**：

- **口径 A（可产出序列条数·保守门槛）**：$N_{series} = |\{l : span(l) \ge 5\}| \times 4 + N_{jurisdiction}$，span 为 location 的去重年份数。实测 **40,508**（10,126 location × 4 指标列 + 4 条受理局年序列）。读数语义「三源当前可直查的跨年可比序列总条数」。
- **口径 B（序列质量·跨度中位数）**：对口径 A 的 geo 序列取跨度中位数 = **12 年**（均值 12.77，min 1，max 27），衡量「序列有多长」，服务 RIS 式 8 年窗达标判断（中位序列达标，短尾 1-4 年共 3,319 个 location 不达标）。
- 口径 C（统计库目录口径·mock 84 的可能语义）：须有指标注册表（哪些指标入选统计库），三源无承载，**不可构建**。

**降档/升档触发器（B10 模板）**：若甲方裁定接受口径 A 的 5 年门槛 → 仍部分支持但语义闭合（「84 条统计库序列」与「40,508 条三源序列」的差异需口径说明页消化）；若久新发布统一指标注册/序列目录表 → 可升**完全转换支持**；若甲方要求对齐 OECD MSTI 式逐指标元数据 → 三源无注册表，维持部分支持不升档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技发展规划.md` |
| 所属四级功能 | 科技发展规划（19 叶，seq 178–196） |
| 本件挂载视图 | 多维度指标体系展示卡（统计库分组第 3 卡） |
| 需求叶对应 | 无同名叶；最近叶 seq 179 多维度指标体系展示（挂载点需求出处） |
| 批内相邻件 | M_SCIUI_TECHTRK_023（技术趋势判断结论，同页趋势叙事）；M_SCIUI_INNOV_002（全球创新趋势演进——序列本体的演进读数，与本件「条数」互补）；M_SCIUI_INNOV_008（趋势预测值——序列的前瞻段） |
| 批内已证事实复用 | gkx 专利 2,939,895 行（官方共享快照）；jiuxin geo 表结构（本 lane 共享探针） |

本件与 INNOV_002/008 构成「序列三件套」：024 数序列（有多少条）、002 读演进（序列长什么样）、008 做预测（序列往哪走）。三件共享 geo_yearly_metrics 主承载但切面不同，本件是唯一以「条数」为交付物的，也因此是三件中最依赖口径裁定的一件。

## 二、计算过程

### 2.1 装载与规模校验

久新 Doris 只读连接（批次统一入口）。主承载 `ads_geo_yearly_metrics` 171,736 行、13,445 个去重 location（facts.jiuxin_geo_yearly_metrics_rows / jiuxin_geo_yearly_metrics_locations），与本 lane 共享探针（`_probe_lane5_s3_01_out.json`）零漂移；专利维 `ads_patent_analysis_jurisdiction` 675 行（4 受理局 × ALL/YEAR 期）。开发库与 gkx 侧按 absence_probe 协议逐一留证（§2.6）。

### 2.2 序列跨度分布（口径 B 输入）

对 13,445 个 location 逐一计算去重年份数 span，分布落产物 `jiuxin_geo_series_span_dist`（按键排序，B5）：span=1 的 1,113 个、span=2 的 915 个、…、span=12 的 537 个、最长 span=27。跨过 5 年门槛的 10,126 个（75.3%），短尾 1-4 年 3,319 个（24.7%）。中位数 12、均值 12.77——中位序列满足 RIS 式 8 年窗（R5），短尾序列连 Hyndman 门槛（R3）都够不着，序列质量两极分化明显。

```sql
-- 跨度分布（B5：按 span 排序输出，Python 侧确定性算中位数）
SELECT span, COUNT(*) c FROM (
  SELECT location_id, COUNT(DISTINCT statistics_year) AS span
  FROM ads_geo_yearly_metrics GROUP BY location_id
) t GROUP BY span ORDER BY span;
-- → span=1:1113 … span=12:537 … span=27（中位数 12，均值 12.77）
```

### 2.3 口径 A 汇总：可产出序列条数

跨度 ≥5 年的 location 10,126 个 × 4 指标列（paper_count / project_count / talent_count / institution_count）= 40,504 条 geo 序列，加 4 条受理局专利年序列（CN/EP/US/WO，1990-2025），合计 **40,508**（facts.jiuxin_total_derivable_series）。注意分子分母说明：derived 键登记 numerator=40,504+4 的构成而非相除关系（本件是计数不是比值，B3 以说明承载）。

```sql
-- 跨度≥5年的 location 数
SELECT COUNT(*) FROM (
  SELECT location_id FROM ads_geo_yearly_metrics
  GROUP BY location_id HAVING COUNT(DISTINCT statistics_year) >= 5
) t;  -- → 10126
-- 受理局年序列清单
SELECT jurisdiction_code, COUNT(*) yrs, MIN(statistics_year), MAX(statistics_year)
FROM ads_patent_analysis_jurisdiction WHERE period_key LIKE 'YEAR:%'
GROUP BY jurisdiction_code ORDER BY jurisdiction_code;
-- → CN:2000-2025 / EP:1990-2025 / US:1990-2025 / WO:1990-2025
```

### 2.4 示范序列：US 年度专利（成品形态展示）

序列池里抽 US 受理局年度专利数作「趋势序列」成品形态：2014-2025 连续 12 年无缺口（facts.jiuxin_patent_us_yearly_series）：44,428 → 44,839 → 43,751 → 45,213 → 43,590 → 50,779 → 53,773 → 53,038 → 61,361 → 67,519 → 46,358 → 46,885。曲线形态可读：2018 前平台期（4.3-4.5 万）、2019-2023 爬升（+33%）、2024 骤降 31%（采集口径切换或滞后入库，需与 002 件同因解读）。这条序列证明「趋势序列」的展示语义在三源有真值可回填——卡片的 84 是计数，卡片背后的曲线是这条。

### 2.5 序列质量钳制

geo 序列可用性受两个质量列钳制：`coverage_status`（样例 loc_000CE1D2… 2006 年 paper 维 NOT_AVAILABLE——早期年覆盖率不足）与 `location_resolved_ratio`。这意味着「跨度 12 年」不等于「12 年全可比」：部分序列的早期点是部分覆盖下的计数，正式交付的序列目录须把 coverage_status 一并带出。此外 jurisdiction 表同 run 内多 topic 快照重复（同一年多行），年序列必须 `GROUP BY statistics_year` 去重后取值——本件 US 序列即按此口径（MAX 去重）。

### 2.6 三源负结论探针

- **gkx**（absence_probe `gkx 280 表指标年度序列结果面扫描`）：`information_schema.tables` 按 metric/series/yearly/trend 四关键词扫描，命中 **0** 表——gkx 280 表全是要素底表（dwd_*），无任何指标年度序列结果面。
- **开发库**（absence_probe `dev gkxlumenx_dwd+ads 序列/趋势类表扫描` + facts.dev_series_table_rows）：命中 6 张表逐一 COUNT——`industry_chain_metric_series`=0、`policy_metric_timeseries`=0、`policy_timeseries`=37、`svc_metric_series`=0、`enterprise_growth_trend`=0、`policy_time_series_indicator`=0。除政策时间点 37 行外全部空载，「有表无数」。
- **久新**：主承载成立，无负结论需求；但登记异构事实——geo 表无专利列（四列见 §2.3），专利序列必须走受理局维表。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TECHTRK_024.py`（久新直连 + gkx 经 `_gkxdb.py`，零 demo_*；跨度分布 SQL 排序 + Python 中位数）。运行 `python3 code/M_SCIUI_TECHTRK_024.py`。
- 产物：`code/M_SCIUI_TECHTRK_024_out.json`。正文数字与产物键逐一对应：`jiuxin_geo_yearly_metrics_rows=171736`（§2.1）、`jiuxin_geo_yearly_metrics_locations=13445`、`jiuxin_geo_locations_span_ge5y=10126`（§2.3）、`jiuxin_total_derivable_series=40508`（§2.3/derived）、`jiuxin_geo_series_span_median=12` / `jiuxin_geo_series_span_avg=12.77` / `jiuxin_geo_series_span_max=27`（§2.2/口径 B）、`jiuxin_patent_us_yearly_series` 十二年逐点（§2.4）、`jiuxin_patent_jurisdiction_yearly` 四序列清单（§2.3）、`dev_series_table_rows` 六表行数（§2.6）。
- 结果解读：一个可用读数（40,508 条三源可直查序列 + 中位跨度 12 年的质量面）、一个不可用读数（mock 84 无口径不可对标）、一组负结论（gkx 0 表、dev 4/5 空载）。
- 对照需求功能要求的评审：KPI 卡回填——部分满足（条数可按假设口径回填，但「统计库序列」的目录语义须甲方裁定）；趋势曲线展示——满足（US 序列证明真值可得）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | geo 序列池行数 | `jiuxin_geo_yearly_metrics_rows` | 171,736 |
| 装载 | 去重 location 数 | `jiuxin_geo_yearly_metrics_locations` | 13,445 |
| 跨度 | span≥5 的 location | `jiuxin_geo_locations_span_ge5y` | 10,126（75.3%） |
| 跨度 | 跨度中位数/均值/最长 | `jiuxin_geo_series_span_median` 等 | 12 / 12.77 / 27 |
| 计数 | 口径 A 总序列条数 | `jiuxin_total_derivable_series`（derived） | 40,508 |
| 计数 | 受理局年序列 | `jiuxin_patent_jurisdiction_yearly` | CN/EP/US/WO × 1990-2025 |
| 示范 | US 年度专利序列 | `jiuxin_patent_us_yearly_series` | 2014-2025 十二点 |
| 负结论 | gkx 序列面 | absence_probe | 命中 0 表 |
| 负结论 | dev 序列表行数 | `dev_series_table_rows` | 4/5 空载（37 行仅政策） |
| 质量钳制 | coverage 早期缺口 | `jiuxin_narrative…` 同批 geo 样例 | 2006 年 NOT_AVAILABLE |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 地理维年度序列 | jiuxin_warehouse | `ads_geo_yearly_metrics`（paper/project/talent/institution 四列） | 171,736（13,445 location） | 直查 | **有**（主承载） |
| D2 | 专利维年度序列 | jiuxin_warehouse | `ads_patent_analysis_jurisdiction`（YEAR: 期） | 675（4 局 × 36 年） | 直查 | 有（受理局维非国家维） |
| D3 | 序列目录/指标注册表 | 三源 | — | — | **不存在** | **缺**（mock 84 的口径锚点） |
| D4 | 开发库序列承载 | dev | `industry_chain_metric_series` 等 6 表 | 0/0/37/0/0/0 | 空载 | 缺（有表无数） |
| D5 | gkx 序列结果面 | gkx | —（280 表扫描） | 0 | **不存在** | 缺 |

`support_judgment="部分支持"` 与产物一致（闸 6）。

### 3.2 D1 主承载明细

geo_yearly_metrics 的四列即「趋势序列」的最小完备集：论文（产出）、项目（投入）、人才（载体）、机构（主体），13,445 个 location 覆盖 COUNTRY/PROVINCE/CITY/CONTINENT 四级（本 lane 探针：CITY 132,975 行 / PROVINCE 33,518 / COUNTRY 5,081 / CONTINENT 162）。按 5 年门槛 75.3% 的 location 可产序列，序列量与跨度双达标——这是本件不落入「完全不支持」的支柱。质量钳制见 §2.5。

### 3.3 D2 专利维的维度错位

jurisdiction 表的序列是**受理局**年度序列（US/EP/CN/WO），不是国家创新属地序列：US 序列度量「向 USPTO 递交的申请」，其逐年变化混合了属地创新与受理局选择行为（OECD R1 明确以专利族+发明人属地规避此偏差，三源无对齐承载）。序列可用，但并读 geo 序列时须标注维度差异。

### 3.4 D3 目录缺口（主降档因）

mock 84 隐含一个「统计库指标目录」：哪些指标入选、每条的跨度要求、可比性规则。三源无任何指标注册表（gkx 是要素底表集合、久新是分析结果表集合、开发库 cfg 侧无指标目录），本件的 5 年门槛与四列入选都是假设。没有目录，条数读数就无法与 84 对标——这不是数据工程能闭合的缺口，是产品裁定缺口。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| geo 序列池 | 171,736 行 / 13,445 location / 四列 |
| 跨度门槛复算 | span≥5 → 10,126（75.3%）；中位 12 年 |
| 口径 A | 10,126×4 + 4 = 40,508 |
| US 示范序列 | 2014-2025 十二点连续（2024 骤降 31% 待口径核） |
| gkx 序列面 | 280 表关键词扫描命中 0 |
| dev 序列表 | 6 表 COUNT：0/0/37/0/0/0 |
| 脚本形态 | 单进程顺序查询，零 demo_*，产物无耗时键 |

## 四、数据缺失情况

### 4.1 指标目录缺失（结构级，主因）

「统计库趋势序列」需要一个指标注册表（入选规则 + 跨度门槛 + 口径元数据）作为计数锚点，三源均无（D3，absence_probe：gkx 0 表、dev 空载、jiuxin 无注册类表）。四缺失情形归属：**表不存在**。修复动作：产品侧定义目录 schema → 工程侧按目录从 geo/jurisdiction 两表物化序列视图。影响面：不止本件——INNOV_002（演进读哪些序列）、INNOV_008（预测哪些序列）共享此目录缺口，一份目录三件受益。

### 4.2 开发库序列表空载（数据级）

6 张序列类表 4 张 0 行，`policy_timeseries` 37 行仅为政策发布时间点。空载意味着开发库当前不能作为任何序列读数的回退源。修复与影响：属数据回填工程，优先级低于目录裁定（目录未定，回填无靶）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 甲方裁定序列口径（指标维+跨度门槛） | 产品决策 | 本件即期 | 5 年门槛为保守假设可先行 |
| 建指标序列目录表（注册+元数据） | 结构工程 | 本件 + INNOV_002/008 | 一表三件受益 |
| geo 表补专利列或物化国家维专利序列 | 数据工程 | 本件 + INNOV_001/002 | 消除受理局/地理维度错位 |

三条路径的档位后果：口径裁定 → 仍部分支持但语义闭合；目录表建成 → 可升**完全转换支持**；geo 专利列补齐 → 序列四维完备（论文/项目/人才/机构+专利）。推荐组合：即期走口径裁定 + 目录表立项。

## 参考文献

1. Forecasting: Principles and Practice (3rd ed) §8 Exponential smoothing[EB/OL]. Hyndman & Athanasopoulos. https://otexts.com/fpp3/exponential-smoothing.html （R3，2026-11-01 WebSearch 核验可达）
2. Main Science and Technology Indicators | OECD[EB/OL]. https://www.oecd.org/en/data/datasets/main-science-and-technology-indicators.html （R4，2026-11-01 WebSearch 核验可达）
3. Regional Innovation Scoreboard 2025 – Methodology Report[EB/OL]. European Commission. https://research-and-innovation.ec.europa.eu/document/download/f6019e31-2927-4802-ae56-5f2fd92cb6c3_en （R5，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

「趋势序列」未出现在三份说明书与主需求文档，无原文可摘。语义最近的三段：

SRS《02-科技信息展示系统/科技发展态势/科技发展规划.md》seq 179（excel_row 182）：

> 在大屏上展示技术发展、产业数据库、机构库、课题库、成果库、统计库、人才库等指标体系，用户可自定义展示内容和布局，支持指标间的联动分析。

SRS《02-科技信息展示系统/科技发展态势/科技全域态势.md》seq 12：

> 提供时间轴趋势展示，用户可查看特定要素随时间变化的趋势；支持趋势预测功能，基于历史数据预测未来发展趋势；提供异常监测功能，自动识别和标记数据异常点和突变点。

UI 组件 `TechDevelopmentPlan.tsx:830`（本件挂载，mock 演示值）：

> `{ label: '趋势序列', value: '84', change: '+3.8%' }`

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 趋势序列 | 技术发展跟踪/科技全域态势/全球创新监测.md | 0 |
| 趋势序列 | 科技信息展示系统和科技专题服务系统.md | 0 |
| 趋势（语义扫描） | 科技发展规划.md | 3（seq 178/180/182 功能叙述） |
| 时间轴趋势 | 科技全域态势.md | 1（seq 12，要素级非计数） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_024_out.json`（20261101 实跑：序列池/跨度分布/口径 A/US 示范序列/三源负结论在案）。
- 本 lane 共享探针：`code/_snapshots/_probe_lane5_s3_01_out.json`（geo_yearly_metrics DESC/年份分布/等级分布、patent_analysis_jurisdiction ALL/YEAR 序列、dwd_patent 列清单与 20 万采样、dev 序列表扫描）。
- 官方共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（gkx 专利 2,939,895、论文按年分布）。

### B.2 本件产物逐键清单（`code/M_SCIUI_TECHTRK_024_out.json`，20261101 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_TECHTRK_024 | 文首 |
| `ui_evidence` | 证据 | 3 条组件行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.jiuxin_geo_yearly_metrics_rows` | 计数 | 171,736 | §2.1/§3.2 |
| `facts.jiuxin_geo_yearly_metrics_locations` | 计数 | 13,445 | §2.1 |
| `facts.jiuxin_geo_locations_span_ge5y` | 计数 | 10,126 | §2.3/口径 A |
| `facts.jiuxin_geo_series_span_dist` | 分布 | span 1→27 逐年计数 | §2.2 |
| `facts.jiuxin_geo_series_span_median` | 统计 | 12 | 口径 B |
| `facts.jiuxin_geo_series_span_avg` | 统计 | 12.77 | §2.2 |
| `facts.jiuxin_geo_series_span_max` | 统计 | 27 | §2.2 |
| `facts.jiuxin_total_derivable_series` | 计数 | 40,508 | §2.3（derived 同名登记构成） |
| `facts.jiuxin_patent_jurisdiction_yearly` | 清单 | CN/EP/US/WO 四序列 | §2.3/§3.3 |
| `facts.jiuxin_patent_us_yearly_series` | 序列 | 2014-2025 十二点 | §2.4 |
| `facts.dev_series_table_rows` | 计数 | 6 表（0/0/37/0/0/0） | §2.6/§4.2 |
| `derived.jiuxin_total_derivable_series` | 派生 | 40,508（构成说明） | §2.3 |
| `absence_probe` | 探针 | gkx 0 表 / dev 6 表行数 | §2.6/§3.1 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `notes` | 披露 | 口径假设+异构+残年 | §〇/§4 |

### B.3 共享快照消费（B11 零漂移）

本件消费：官方快照 `dims.gkx[2]`（dwd_patent 2,939,895——正文 §1.7/§3 引用原值）；本 lane 探针 `ads_geo_yearly_metrics COUNT=171,736`（本件实跑 assert 对账一致）；`ads_patent_analysis_jurisdiction COUNT=675`（024 与 002 两件同值，批内互推一致）。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 门槛/口径 | 三源承载 | 贴合度 |
|---|---|---|---|---|
| 指标目录制 | OECD MSTI（R4） | 148 指标年度序列+逐指标元数据 | 无注册表 | 高（目标态） |
| 数据窗制 | 欧盟 RIS（R5） | ≥8 年窗+插补+异常处理 | geo 中位 12 年达标 | 中高（可即时套用） |
| 建模门槛制 | Hyndman FPP（R3） | ≥2 周期/8-10 点 | 同上 | 中（预测侧由 008 承接） |
| 本件口径 A | 保守假设 | span≥5 | 直查可得 | 即期交付 |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| geo_yearly_metrics | 171,736 行 | coverage 早期缺口 | 无专利列 |
| patent_analysis_jurisdiction | 675 行 | 同 run 重复需去重 | 受理局维非属地 |
| 指标注册表 | 不存在 | — | 结构缺失（主因） |
| dev 序列表 | 4/5 空载 | — | 数据级空载 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 序列条数 40,508 + 跨度质量面 + US 示范曲线回填 | 甲方接受 5 年门槛假设 |
| v2 | 指标序列目录表 + 序列视图物化 | 目录 schema 裁定 |
| v3 | OECD MSTI 式逐指标元数据 + geo 专利列 | 数据工程 + 目录运营 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 40,508 被误读为「统计库 84 的真值」 | **高** | 卡片注记「三源可产序列，口径假设 5 年」 |
| 受理局序列被当国家序列 | 中 | 维度标签随行 |
| 短尾序列（24.7%）入目录拉低可比性 | 中 | 目录带 span 与 coverage 双列 |

### C.5 总判

**部分支持**：序列本体量大质足（171,736 行、中位 12 年），但计数口径（目录）三源无承载、开发库侧空载、专利维错位三因叠加。升档路径（目录表）写死在 §1.6 触发器，按 B10 保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_024.py` | 退出码 0，落 `_out.json` |
| 数据入口 | gkx 经 `_gkxdb.py`；jiuxin 直连只读 | demo_* 直接 raise |
| 序列池对账 | 产物 `jiuxin_geo_yearly_metrics_rows` vs lane5 探针同键 | 171,736 = 171,736 |
| 口径 A 复算 | 10,126×4+4 | 40,508 |
| US 序列连续性 | `jiuxin_patent_us_yearly_series` | 2014-2025 无缺年 |
| 判档一致 | MD 文首 vs 产物 `support_judgment` | 部分支持 |
| mock 残留检查 | `rg "趋势序列" repos/demo-ui-science/src` | 正式版替换后 KPI 卡无 mock 值 |

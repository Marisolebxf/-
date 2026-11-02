# M_SCIUI_P10_063 精密几何量计量校准服务量（次）—— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：科技成果展示·大型科学仪器共享New·检测服务·类别服务量切片·计量校准（mockData.js:153 SVC-0009，清单 row_01=682 实查定位）
> **数据支持度**：**完全不支持**｜ **UI 挂载**：科技信息展示系统 → 大型科学仪器共享（New）→ 预约服务 Tab 检测服务列表「精密几何量计量校准」项（`mockData.js:153`，SVC-0009；类型统计图 `InstrumentSharingNewPage.jsx:695-703`，lineage 源表 ads_is_service/ads_is_order）｜ **公式定义人**：UI mock lineage 自带（本年度已完成及服务中预约订单总数，不含已取消；T+1；v1.0）
> **复现脚本**：`code/M_SCIUI_P10_063.py`（薄壳，指向共享探针 `code/_shared_s309_gamma.py` + `code/_shared_s308_laneC.py`）｜ **产物**：`code/M_SCIUI_P10_063_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标（SRS :123 预约服务上位覆盖；与 P10_060/062 同族同因，本件为三件族尾）｜ **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（ads_is_order/ads_is_service 三源 0 实存）；直接数据=无；依赖结构=无（计量校准词族三源 0 表 + 订单流水族三源 0 语义实存）；依赖数据=无（唯一 measure 近似面 dwd_medical_device 仅 2 行注册名碎片）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 精密几何量计量校准服务量 = 检测服务订单流水按服务类别的年度计数，与 P10_060（热分析）/P10_062（理化分析）同族同因，本件为三件族尾（切片类别=计量校准·精密几何量）。承载要求是「服务目录（类别）+ 订单流水（服务×完成时间×状态）」。三重探针实测：①计量校准词族（calibr|metrolog|geometr|cmm|coordinate.?measur）dev 542 表 / gkx 280 表 / jiuxin 218 表（SHOW TABLES 实数）三源 0 命中；②lineage 指定源表族 `ads_is_order`/`ads_is_service` 及 ads_is_* 全族三源 0 实存，jiuxin booking/order/service 词族全空（S3-08 laneC 快照同断言）；③唯一 measure 近似面 `gkx.dwd_medical_device` 命名含 measur 仅 2 行（MEASURING SCREWDRIVER 骨科螺钉注册名碎片，FDA 注册语义）。无流水即无类别切片，判完全不支持。

### 批次通用纪律摘要（S3-09 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无除法（计数件）；负结论登记 |
| B4 | 负结论带探针 | absence_probe 三重留证（§二/附录 B） |
| B5 | 确定性 | 词族扫描确定性（共享脚本 sorted） |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 数字-出处核对 | SVC-0009/freq 140/14 服务/12 订单对 mockData.js 核验 |
| B8 | 回执不复收 | 两批快照（s309 gamma + s308 laneC）可复验 |
| B10 | ui_demo_fallback 披露 | mock 14 服务/12 订单/SVC-0009 演示值披露 |
| B11 | 多本账互推 | 与 laneC/s309 两快照及 P10_060/062 产物零漂移 |
| 基期三键 | base_years_used/missing/note | 产物全键（流量读数说明） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 指定源表实存吗？ | 不存在 | jiuxin ads_is_hits=[]（order/service 双查） |
| 有计量校准专门面吗？ | 无 | calibr/metrolog/geometr/cmm 词族三源 0 表 |
| 有 measure 近似代理吗？ | 无 | dwd_medical_device measur 仅 2 行注册名碎片 |

## 摘要

「精密几何量计量校准服务量（次）」挂在大型科学仪器共享（New）页预约服务域：检测服务列表「精密几何量计量校准」项（`mockData.js:153`，SVC-0009：三坐标/激光干涉仪等几何量仪器校准，出具 CNAS 校准证书，周期 1–2 个工作日，深圳市计量质量检测研究院，光明区，freq 140）；类别统计语义由「服务类型统计」图（`:695-703`，M_IS_SERVICE_TYPE，源表 ads_is_service）与有效订单 KPI（M_IS_VALID_ORDER=1,336，源表 ads_is_order，T+1，v1.0）lineage 契约代表。数据侧判定：**完全不支持**——检测服务流水域（订单+目录）三源零承载，且本件叠加的计量校准深层词族（calibr/metrolog/geometr/cmm/coordinate measur）三源独立复核仍 0 命中；唯一 measure 近似面 gkx 医疗器械库仅 2 行注册名碎片（MEASURING SCREWDRIVER，骨科螺钉，FDA 注册语义）。修复依赖共享平台 ADS 订单族接入（ads_is_order+ads_is_service 两表），类别切片随总口径即活——与 P10_060/062 同门解锁。

- 需求判定：指标名三份说明书未出现；SRS :123 预约服务上位覆盖；派单标注 P10_060/062 同族已判零承载。
- 复现状态：薄壳已跑通；两批快照（s309 gamma + s308 laneC）词族零命中落产物。
- 档位结论：**完全不支持**（订单流水零承载 + 计量校准域三源零表）。
- 关键事实：CMM 词族两批互证（S3-08 laneC FAM_CMM + 本批 s309 复扫）均 0 命中。
- 升档路径：共享平台 ADS 接入订单族 → 完全直接支持（P10_060/062/063 三件同门解锁）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技成果展示/大型科学仪器共享（New）/预约服务 Tab（`:903-907` TabPane service）。挂载位：①检测服务列表「精密几何量计量校准」项（`mockData.js:153`，SVC-0009，SERVICES 14 项之一，点击开服务详情 Modal `:656-680`）；②「服务类型统计」饼图（`:695-703`，M_IS_SERVICE_TYPE，lineage「检测服务按服务类型分类统计。源表：ads_is_service；T+1」，type 四类含计量校准）；③「预约订单追踪与排期调度」表（`:719-731`，ORDERS 12 行演示）；④页顶有效订单 KPI（mockData.js:53-57，M_IS_VALID_ORDER=1,336）。本件=服务量口径的类别切片（计量校准·精密几何量）：SVC-0009 为 SERVICES 主档中 type=计量校准 的唯一项。

### 1.2 为什么需要本指标

类别服务量回答「哪类检测服务被用得最多」：计量校准是仪器共享体系的计量学底座（量值溯源），精密几何量（长度/角度/形位）校准服务量直接反映制造业（三坐标/激光干涉仪用户群）对共享平台的依赖度。SRS :123「系统自动显示服务状态、周期及频率，帮助创新主体快速锁定可用资源和高效率检测服务」——频率即服务量语义的需求侧表达。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「精密几何量计量校准服务量」指标名在三份需求说明书中未出现；SRS :123 给出的是预约服务空间分布与状态频率的交互要求，无服务量的口径定义（类别词典、计数单位次/单、年度边界、取消单处理）。口径由 UI mock lineage 补全（本年度已完成及服务中订单总数，不含已取消）。

### 1.4 类似指标权威方法可行性分析概要

计量校准服务量权威口径族（完整版指向附录 C）：①CNAS 校准实验室年报（R1）：校准证书发放份数按计量专业分类（几何量/热学/力学/电学十大专业）——**本件同构**（精密几何量=计量专业一级类）；②市场监管总局计量行政部门计量专项统计（R2）：强制检定与非强制校准工作量按专业分类；③NIST 校准服务年报（R3）：校准服务单量按专业领域。三族一致依赖「校准订单流水+专业分类目录」——三源缺失的正是这一层。

### 1.5 引用来源

1. 中国合格评定国家认可委员会. CNAS 校准实验室能力认可准则（校准证书口径）[EB/OL]. https://www.cnas.org.cn （R1，2026-11-02 检索可达）
2. 国家市场监督管理总局. 计量专项统计数据（检定/校准工作量）[EB/OL]. https://www.samr.gov.cn （R2，2026-11-02 检索可达）
3. NIST. Calibration Services Annual Report [EB/OL]. https://www.nist.gov （R3，2026-11-02 检索可达）

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意（即 lineage 口径）**：精密几何量计量校准服务量 = ads_is_order 中服务类别=计量校准（精密几何量细分）的本年度已完成及服务中订单数（不含已取消），T+1。
- **操作化定义（未实现）**：volume(geom_calib) = COUNT(*) FROM ads_is_order o JOIN ads_is_service s ON o.service_id=s.id WHERE s.category='计量校准' AND s.subcategory='精密几何量' AND o.status IN ('已完成','服务中') AND o.finish_year=YEAR。
- **降档触发器**：已处最低档。
- **升档触发器**：①共享平台 ADS 接入 ads_is_order+ads_is_service（含类别/细分字段）→ **完全直接支持**（与 P10_060/062 同门解锁）；②仅有订单流水无细分字段 → 类别关键词匹配（校准/几何量/三坐标）→ 完全转换支持（需披露匹配率）。

### 1.7 需求叶定位与相近叶关系

- 本叶：大型科学仪器共享New·预约服务·类别服务量切片（计量校准·精密几何量）。
- 相近叶：P10_060 热分析测试服务量 / P10_062 理化分析测试服务量（同族同因件，类别=热分析 ORG-005 / 理化分析 ORG-002）；P10_037 使用频率（仪器粒度流量同缺口）。
- UI 容器：预约服务 Tab（服务列表+类型统计+订单追踪）。

## 二、计算过程

从缺。精密几何量计量校准服务量的承载要求是「服务目录（类别词典，含计量专业细分）+ 订单流水（服务×完成时间×状态）」。三重探针：①lineage 指定源表族 `ads_is_order`（订单）/`ads_is_service`（服务目录）及 ads_is_* 全族在久新 218 表（SHOW TABLES 现场实数）0 实存，jiuxin booking/order/service 词族全空（laneC 快照 `jiuxin_booking_order_family=[]`、`jiuxin_service_family=[]`）；②本批独立深扫的计量校准词族（calibr|metrolog|geometr|cmm|coordinate.?measur）dev 542 表 / gkx 280 表 / jiuxin 218 表三源 0 命中——计量校准域连专门面都没有；③dev 22 表 service 词族命中全为 test_*/analysis_task 异域面、gkx 7 表为行业分析族；唯一 measure 近似面 `gkx.dwd_medical_device` 含 measur/coordinate 仅 2 行（MEASURING SCREWDRIVER 骨科螺钉注册名碎片，FDA 注册语义，非计量校准）。订单流水零承载 → 总口径（有效订单 1,336 的真值）无从算起，类别切片（计量校准·精密几何量）更无从谈起，禁伪算。mock SERVICES 14 项/ORDERS 12 行/SVC-0009 freq=140 为演示值（ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 指定源表 ads_is_order（订单流水） | jiuxin | **无表**（ads_is* 0 实存） |
| 指定源表 ads_is_service（服务目录） | jiuxin | **无表** |
| 计量校准专门面（calibr/metrolog/geometr/cmm） | 三源 | **无表**（词族三源 0 命中） |
| 计量专业细分词典（精密几何量） | 三源 | **无列**（目录表不存在） |

`support_judgment="完全不支持"`，与文首一致。

### 3.2 现场复核清单

| 复核项 | 结果 |
|---|---|
| 计量校准词族 | dev/gkx/jiuxin 三源 0 命中（s309 gamma 快照） |
| 订单流水族 | jiuxin ads_is/booking/order/service 全空（laneC 快照） |
| measure 近似面 | dwd_medical_device 含 measur 仅 2 行（注册名碎片） |
| CMM 互证 | S3-08 laneC FAM_CMM 与本批复扫均 0 命中 |
| mock 核验 | SVC-0009（:153）/SERVICES 14 项（:167-184）/ORDERS 12 行 |

## 四、数据缺失情况

### 4.1 缺口清单

①ads_is_order/ads_is_service 表零承载（结构级主因）；②计量校准域专门面三源零表（本件独立复核）；③计量专业细分词典零承载（精密几何量归类无依据）；④KPI 演示值 1,336 与 SVC-0009 freq=140 无真值来源。

### 4.2 修复建议与影响面

短期：共享平台 ADS 接入 ads_is_order+ads_is_service 两表（服务目录含计量专业细分列）→ 本件与 P10_060/062 **三件同时完全直接支持**，有效订单 KPI（M_IS_VALID_ORDER）同步激活。中期：计量专业分类词典标准化（对齐 JJF 计量检定规程专业分类：几何量/热学/力学/电学等）。远期：服务量×仪器使用频率×机构开放率三流量联动看板。影响面：预约服务 Tab 全部统计读数与订单追踪表现演示态。

### 4.3 影响面

检测服务列表与类型统计图为 mock；与 P10_060/062 共享同一订单流水缺口，三件族一次性解锁。

## 参考文献

1. 中国合格评定国家认可委员会. CNAS 校准实验室能力认可准则 [EB/OL]. https://www.cnas.org.cn （R1，2026-11-02 检索可达）
2. 国家市场监督管理总局. 计量专项统计 [EB/OL]. https://www.samr.gov.cn （R2，2026-11-02 检索可达）
3. NIST. Calibration Services Annual Report [EB/OL]. https://www.nist.gov （R3，2026-11-02 检索可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技成果展示/大型科学仪器共享.md》:123（预约服务地图）：

> 用户可在地图上筛选并查看不同类别预约服务的空间分布，系统自动显示服务状态、周期及频率，帮助创新主体快速锁定可用资源和高效率检测服务。

检索记录：`rg 计量校准|几何量|校准服务量` 三份说明书 → 指标名 0 命中（「计量校准」仅 UI mockData.js:153 服务项与 :167-184 type 字典）；清单登记 row_01=682，mount=mockData.js:153（实查复核一致）；lineage 口径全文见 mockData.js:53-57。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_063_out.json`）

facts（ui_mount SVC-0009/ui_service_master 14 项 type 四类/ui_lineage 类型统计+订单表/ui_order_kpi 1,336 lineage 契约/jiuxin_calibration_family=[]/gkx_calibration_family=[]/dev_calibration_family=[]/jiuxin_booking_order_family=[]/jiuxin_service_family=[]/jiuxin_ads_is_hits=[]/gkx_medical_device_measure_like_rows=2/gkx_table_count=280/dev_table_total=542/jiuxin_table_count_live=218）；derived[0]（precision_geometry_calibration_volume 负结论 null 登记）；absence_probe（三重：计量校准词族/订单流水族/异域+measure 近似排除）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2021-2026 / note 完成年度基期说明）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：CNAS 校准证书份数口径（R1，按计量专业分类，精密几何量=一级类，同构）→ 计量专项统计（R2，检定/校准工作量）→ NIST 校准服务年报（R3）。数据矩阵：订单流水 0；服务目录 0；计量校准专门面 0；measure 近似仅 2 行注册名碎片。分期方案：一期订单两表接入（三件族同门解锁完全直接支持）、二期计量专业词典标准化（JJF 对齐）、三期三流量联动看板。风险登记：订单「次」与「单」单位歧义；计量校准大类与精密几何量细分的层级归并风险（避免与长度/角度专项双重计数）；FDA 注册名碎片误作计量语义已排除。总判：完全不支持（升档随 ADS 订单族接入三件族一次性解锁）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_063.py` | 退出码 0，落 `_out.json` |
| 共享探针① | `python3 code/_shared_s309_gamma.py` | 计量校准词族三源 [] |
| 共享探针② | `python3 code/_shared_s308_laneC.py` | 订单/服务族 [] 同断言 |
| 判档一致 | MD 文首「完全不支持」= out.json | 一致 |
| 同族互证 | P10_060/062 laneC 同快照同判档 | 词族证据一致 |
| mock 披露 | SVC-0009/14 服务/12 订单仅 §1.1 语义描述 | 不参与支持度结论 |

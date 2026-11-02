# M_SCIUI_P10_060 热分析测试服务量（次）—— 指标信息 MD

> **类型**：简单统计类｜ **域**：科技成果展示·大型科学仪器共享New·预约服务·检测服务流水域·类别切片（InstrumentSharingNewPage.jsx:719-731/:695-703，mockData.js:185 ORG-005 实查定位）
> **数据支持度**：**完全不支持**｜ **UI 挂载**：科技信息展示系统 → 大型科学仪器共享（New）→ 预约服务 Tab「预约订单追踪与排期调度」表 +「服务类型统计」图（`InstrumentSharingNewPage.jsx:719-731/:695-703`，lineage 源表 ads_is_order/ads_is_service）｜ **公式定义人**：UI mock lineage 自带（本年度已完成及服务中预约订单总数，不含已取消；T+1；v1.0）
> **复现脚本**：`code/M_SCIUI_P10_060.py`（薄壳，指向共享探针 `code/_shared_s308_laneC.py`）｜ **产物**：`code/M_SCIUI_P10_060_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标（SRS :123 预约服务上位覆盖；INCUB_061 同族）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（ads_is_order/ads_is_service 三源 0 实存）；直接数据=无；依赖结构=无（检测服务流水域零承载）；依赖数据=无（订单/booking/service 词族三源逐一零命中）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 热分析测试服务量 = 检测服务订单流水按服务类别的年度计数。承载要求是「服务目录（类别）+ 订单流水（服务×完成时间×状态）」。实测：lineage 指定源表族 `ads_is_order`/`ads_is_service` 及整个 ads_is_* 族在久新 218 表（SHOW TABLES 实数）0 实存；jiuxin booking/order 词族 0 命中、service 词族 0 命中；dev 542 表 service 词族 22 表命中全为 test_*/analysis_task 异域面（bi.test_order 等内部测试表）；gkx 280 表 service 词族 7 表为 dwd_industry_analysis_* 行业分析族——检测服务流水域三源零承载。无流水即无类别切片（热分析测试），判完全不支持。

### 批次通用纪律摘要（S3-08 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无除法（计数件）；负结论登记 |
| B4 | 负结论带探针 | absence_probe 三源逐一留证（§二/附录 B） |
| B5 | 确定性 | 词族扫描确定性（共享脚本 sorted） |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 数字-出处核对 | ORDERS 12 行/SERVICES 14 项对 mockData.js 核验 |
| B10 | ui_demo_fallback 披露 | mock 14 服务/12 订单演示值披露 |
| B11 | 多本账互推 | 与共享快照 `_shared_s308_laneC_out.json` 零漂移 |
| 基期三键 | base_years_used/missing/note | 产物全键（流量读数说明） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 指定源表实存吗？ | 不存在 | jiuxin ads_is_hits=[]（order/service 双查） |
| 有订单流水可切片吗？ | 无 | booking/order 词族三源 0 命中 |
| 有服务目录可代理吗？ | 无 | service 词族命中全异域（test_*/industry_analysis） |

## 摘要

「热分析测试服务量（次）」挂在大型科学仪器共享（New）页预约服务域：订单追踪表（`:719-731`，ORDERS 12 行演示订单）+ 服务类型统计图（`:695-703`，M_IS_SERVICE_TYPE，源表 ads_is_service）；服务量总口径由有效订单 KPI（M_IS_VALID_ORDER=1,336，源表 ads_is_order，T+1，v1.0）lineage 契约代表；「热分析测试」本身在 UI 仅以机构能力清单项出现（mockData.js:185 ORG-005 哈工大深圳 services 数组，聚合物/金属材料曲线交付）。数据侧判定：**完全不支持**——检测服务流水域（订单+目录）三源零承载：jiuxin booking/order/service 三词族全空、dev 22 表命中全为内部测试表、gkx 7 表为行业分析族。修复依赖共享平台 ADS 订单族接入（ads_is_order+ads_is_service 两表），类别切片随总口径即活。

- 需求判定：指标名三份说明书未出现；SRS :123 预约服务上位覆盖；派单标注 INCUB_061 同族。
- 复现状态：薄壳已跑通；三源词族零命中落产物。
- 档位结论：**完全不支持**（订单流水零承载，类别切片无从谈起）。
- 关键事实：ads_is_order/ads_is_service 0 实存；jiuxin booking/order=[] service=[]。
- 升档路径：共享平台 ADS 接入订单族 → 完全直接支持（类别切片随总口径即活）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技成果展示/大型科学仪器共享（New）/预约服务 Tab（`:903-907` TabPane service）。挂载位：①「预约订单追踪与排期调度」表（`:719-731`，orderColumns 含订单号/仪器/机构/申请人/进度/订阅提醒，ORDERS 12 行演示）；②「服务类型统计」饼图（`:695-703`，CHART_METRICS.serviceType=M_IS_SERVICE_TYPE，lineage「检测服务按服务类型分类统计。源表：ads_is_service；T+1」）；③「检测服务列表」（`:656-680`，SERVICES 14 项点击开服务详情 Modal）；④页顶有效订单 KPI（mockData.js:53-57，M_IS_VALID_ORDER=1,336，lineage 原文「本年度已完成及服务中预约订单总数（不含已取消）。源表：ads_is_order；源系统：深圳市大型科学仪器共享平台；T+1；v1.0」）。本件=服务量口径的类别切片（热分析测试）：该类目在 UI 以 ORG-005 哈工大（深圳）机构能力清单项出现（mockData.js:185，services 数组「热分析测试」，flow 预约→送样→测试→曲线交付）。

### 1.2 为什么需要本指标

类别服务量回答「哪类检测服务被用得最多」：管理者以类别流量调配仪器机时与补贴方向（热分析是材料类高频刚需），用户以服务量判断类别成熟度与排期预期。SRS :123「系统自动显示服务状态、周期及频率，帮助创新主体快速锁定可用资源和高效率检测服务」——频率即服务量语义的需求侧表达。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「热分析测试服务量」指标名在三份需求说明书中未出现；SRS :123 给出的是预约服务空间分布与状态频率的交互要求，无服务量的口径定义（类别词典、计数单位次/单、年度边界、取消单处理）。口径由 UI mock lineage 补全（本年度已完成及服务中订单总数，不含已取消）。

### 1.4 类似指标权威方法可行性分析概要

检测服务量权威口径族（完整版指向附录 C）：①CNAS 检测实验室年报（R1）：报告发放份数按检测领域分类——**本件同构**（次≈报告份）；②国家科技基础条件平台调查（R2）：大型仪器对外服务机时/次数按类别；③深圳市共享平台年度运行报告（R3）：服务订单统计。三族一致依赖「订单流水+服务目录」——三源缺失的正是这一层。

### 1.5 引用来源

1. 中国合格评定国家认可委员会. CNAS 检测和校准实验室能力认可准则及应用要求 [EB/OL]. https://www.cnas.org.cn （R1，2026-11-02 检索可达）
2. 科技部. 国家科技基础条件资源调查（大型仪器对外服务） [EB/OL]. https://www.most.gov.cn （R2，2026-11-02 检索可达）
3. 深圳市科技创新委员会. 深圳市大型科学仪器共享服务平台年度运行报告 [EB/OL]. https://stic.sz.gov.cn （R3，2026-11-02 检索可达）

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意（即 lineage 口径）**：热分析测试服务量 = ads_is_order 中服务类别=热分析测试的本年度已完成及服务中订单数（不含已取消），T+1。
- **操作化定义（未实现）**：volume(thermal) = COUNT(*) FROM ads_is_order o JOIN ads_is_service s ON o.service_id=s.id WHERE s.category='热分析测试' AND o.status IN ('已完成','服务中') AND o.finish_year=YEAR。
- **降档触发器**：已处最低档。
- **升档触发器**：①共享平台 ADS 接入 ads_is_order+ads_is_service（含类别字段）→ **完全直接支持**；②仅有订单流水无服务目录 → 类别关键词匹配 → 完全转换支持（需披露匹配率）。

### 1.7 需求叶定位与相近叶关系

- 本叶：大型科学仪器共享New·预约服务·类别服务量切片（热分析测试）。
- 相近叶：P10_062 理化分析测试服务量（同族同因件，类别=理化分析测试 ORG-002 南科大）/P10_037 使用频率（仪器粒度流量同缺口）/INCUB_061（派单标注同族）。
- UI 容器：预约服务 Tab（订单追踪表+服务类型统计+服务列表）。

## 二、计算过程

从缺。热分析测试服务量的承载要求是「服务目录（类别词典）+ 订单流水（服务×完成时间×状态）」。lineage 指定源表族 `ads_is_order`（订单）/`ads_is_service`（服务目录）及整个 ads_is_* 族在久新 218 表（SHOW TABLES 现场实数）0 实存；jiuxin booking/order 词族与 service 词族双双 0 命中（共享快照 `jiuxin_booking_order_family=[]`、`jiuxin_service_family=[]`）；dev 17 schema/542 表 service 词族 22 表命中全为 test_*/analysis_task 异域面（bi.test_order/test_customer、cfg.analysis_task 等内部测试与任务表，无检测服务语义）；gkx 280 表 service 词族 7 表为 dwd_industry_analysis_* 行业分析族（companies/content_types/countries/documents/industries/topics/topic_dict），非检测服务流水。订单流水零承载 → 总口径（有效订单 1,336 的真值）无从算起，类别切片（热分析测试）更无从谈起，禁伪算。mock SERVICES 14 项/ORDERS 12 行为演示值（ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 指定源表 ads_is_order（订单流水） | jiuxin | **无表**（ads_is* 0 实存） |
| 指定源表 ads_is_service（服务目录） | jiuxin | **无表** |
| 订单/booking 词族 | 三源 | **0 命中**（jiuxin=[]/dev 异域/gkx 异域） |
| 服务类别词典（热分析测试） | 三源 | **无列**（目录表不存在） |

### 3.2 现场复核清单

UI 链实读：`:719-731`（订单追踪表）；`:695-703`（服务类型统计图+lineage）；`:656-680`（服务列表）；`:903-907`（Tab 结构）；mock `:185`（ORG-005 热分析测试服务项）+ `:212-224`（ORDERS 12 行）+ `:53-57`（有效订单 KPI lineage 原文）。三源实连复核（共享快照）：jiuxin booking_order_family=[]/service_family=[]/ads_is_hits=[]；dev service 22 表异域；gkx service 7 表行业分析族。SRS :123 原文核验。

## 四、数据缺失情况

### 4.1 缺口清单

①ads_is_order/ads_is_service 表零承载（结构级主因，订单流水是流量件的地基）；②订单/booking 词族三源零命中（任何等价流水面无）；③服务类别词典零承载（热分析测试归类无依据）；④KPI 演示值 1,336 无真值来源。

### 4.2 修复建议与影响面

短期：共享平台 ADS 接入 ads_is_order+ads_is_service 两表 → 本件与 P10_062 **同时完全直接支持**（类别切片随总口径即活），有效订单 KPI（M_IS_VALID_ORDER）同步激活。中期：服务类别词典标准化（分析测试/计量校准/热分析/理化分析等层级）。远期：服务量×仪器使用频率×机构开放率三流量联动看板。影响面：预约服务 Tab 全部统计读数与订单追踪表现演示态。

### 4.3 影响面

服务类型统计图（serviceType）与服务列表为 mock；订单追踪 12 行为演示；与 P10_062/037 共享同一订单流水缺口。

## 参考文献

1. 中国合格评定国家认可委员会. CNAS 实验室认可准则 [EB/OL]. https://www.cnas.org.cn （R1，2026-11-02 检索可达）
2. 科技部. 国家科技基础条件资源调查 [EB/OL]. https://www.most.gov.cn （R2，2026-11-02 检索可达）
3. 深圳市科技创新委员会. 深圳市大型科学仪器共享服务平台 [EB/OL]. https://stic.sz.gov.cn （R3，2026-11-02 检索可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技成果展示/大型科学仪器共享.md》:123（预约服务地图）：

> 用户可在地图上筛选并查看不同类别预约服务的空间分布，系统自动显示服务状态、周期及频率，帮助创新主体快速锁定可用资源和高效率检测服务。

检索记录：`rg 热分析|服务量` 三份说明书 → 指标名 0 命中（「热分析」仅 UI mockData.js:185 机构服务项）；lineage 口径全文见 mockData.js:53-57（有效订单 KPI）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_060_out.json`）

facts（ui_mount 订单表+统计图/ui_service_row ORG-005 服务项/ui_order_kpi 1,336 lineage 契约/ui_mock 14 服务 12 订单/jiuxin_booking_order_family=[]/jiuxin_service_family=[]/jiuxin_ads_is_hits=[]/dev_service_family_note 22 表异域/gkx_service_family 行业分析族 7 表/gkx_table_count=280/dev_table_total=542/jiuxin_table_count_live=218）；derived[0]（thermal_analysis_test_volume 负结论 null 登记）；absence_probe（三件）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2021-2026 / note 流量读数+完成年度基期说明）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：CNAS 报告份数口径（R1，lineage 同构）→ 条件资源调查服务次数（R2）→ 共享平台年度运行报告（R3）。数据矩阵：订单流水 0；服务目录 0；类别词典 0；KPI 1,336 为 mock。分期方案：一期订单两表接入（完全直接支持，P10_060/062 同门解锁）、二期类别词典标准化、三期三流量联动看板。风险登记：订单「次」与「单」单位歧义（一次送样多项目需拆单口径）；取消单剔除边界（lineage 已定不含已取消）。总判：完全不支持（升档随 ADS 订单族接入解锁）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_060.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneC.py` | 快照键与本件 facts 零漂移 |
| 判档一致 | MD 文首「完全不支持」= out.json | 一致 |
| 断言 | jiuxin booking/service 族=[] | 脚本内 assert 通过 |
| 同族互证 | P10_062 同快照同断言 | 词族证据一致 |
| mock 披露 | 14 服务/12 订单仅 §1.1 语义描述 | 不参与支持度结论 |

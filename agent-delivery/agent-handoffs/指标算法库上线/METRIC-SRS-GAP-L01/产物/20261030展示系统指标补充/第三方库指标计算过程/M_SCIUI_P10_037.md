# M_SCIUI_P10_037 入网仪器月均使用频率（次/月）—— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：科技成果展示·大型科学仪器共享New·仪器/机构详情与使用频率Top10（InstrumentSharingNewPage.jsx:952+1066+623，清单序号 551 实查定位）
> **数据支持度**：**完全不支持**｜ **UI 挂载**：科技信息展示系统 → 大型科学仪器共享（New）→ 仪器详情 Modal/机构详情 Modal「使用频率」+ 使用频率 Top10 图（`InstrumentSharingNewPage.jsx:952/:1066/:623`）｜ **公式定义人**：UI mock lineage 自带（源表 ads_is_instrument_usage；月均频次口径）
> **复现脚本**：`code/M_SCIUI_P10_037.py`（薄壳，指向共享探针 `code/_shared_s308_laneC.py`）｜ **产物**：`code/M_SCIUI_P10_037_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标（SRS :75/:107/:235 三处「使用频率」上位覆盖）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（指定源表 ads_is_instrument_usage 三源 0 实存）；直接数据=无；依赖结构=无（预约/订单流水族 order/book/reserv 三源 0；usage/freq/机时列命中全为异域语义）；依赖数据=无（无流水即无频率）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 月均使用频率 = Σ月内预约完成单 ÷ 台（或机时折算），承载要求是预约/订单流水。UI lineage 指定源表 `ads_is_instrument_usage` 在久新 218 表（SHOW TABLES 实数）**0 实存**（ads_is_* 前缀族整体缺失，P10_040 同根因）；dev 542 表 usage/freq/机时列词族命中全为异域语义（config.group_capacity.usage 容量配额 / chain_hotspot.news_freq_score 资讯热度 / policy_subscription.push_frequency 推送频率）；jiuxin order/book/reserv 预约流水词族 0 命中；gkx 280 表仪器族 0 命中（dwd_medical_device 注册库 15 列无 usage/机时/预约列）。无流水即无频率，判完全不支持——与 S3-07 批 INCUB_008 同根因复判一致，本件独立留证。

### 批次通用纪律摘要（S3-08 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 频率=月度单量÷台数同台账同月（口径注记）；负结论登记 |
| B4 | 负结论带探针 | absence_probe 三源逐一留证（§3.2/附录 B） |
| B5 | 列表 sorted() | base_years/ctx_refs sorted |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 数字-出处核对 | 32 仪器/38-260 次/月/mock 值对 mockData.js 核验 |
| B10 | ui_demo_fallback 披露 | mock 38-260 次/月演示值披露 |
| 基期三键 | base_years_used/missing/note | 产物全键（月度口径说明） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 指定源表实存吗？ | 不存在 | jiuxin `SHOW TABLES LIKE 'ads_is%'`=0（218 表实数） |
| 有预约流水可转换聚合吗？ | 无 | jiuxin order/book/reserv 0；dev bi.test_order 为积木报表测试单语义 |
| 有机时/频率列可代理吗？ | 无 | dev usage/freq 列命中全为容量/资讯/推送异域语义 |

## 摘要

「入网仪器月均使用频率（次/月）」在大型科学仪器共享（New）页有三个挂载位：仪器详情 Modal（`:952`「使用频率 {usageFreq} 次/月」）、机构详情 Modal（`:1066` 同字段）、服务统计域「使用频率 Top10（含使用评价）」图（`:623`，CHART_METRICS.usageFreq，lineage 指定源表 ads_is_instrument_usage，T+1）。mock 给 32 台仪器 38-260 次/月、14 家机构 65-260 次/月。数据侧判定：**完全不支持**——频率的原料是预约/订单流水：指定源表族 ads_is_* 在久新 218 表零实存；dev 542 表 usage/freq/机时词族命中全为异域语义（容量配额/资讯热度/推送频率）；jiuxin 预约流水词族 0；gkx 仪器族 0（注册库无 usage 列）。需规背景仅有 2020-12 底有效订单总量 1,336 个（单时点总量，无单机口径）。与 INCUB_008（S3-07）同根因复判一致。

- 需求判定：指标名三份说明书未出现；SRS :75/:107/:235 三处「使用频率」上位覆盖。
- 复现状态：薄壳已跑通；三源负结论落产物。
- 档位结论：**完全不支持**（预约流水零承载，频率不可算）。
- 关键事实：ads_is_instrument_usage 0 实存；dev usage 列 4 处全为异域。
- 升档路径：共享平台 ADS 接入（order+usage 两表）→ 完全直接支持；仅 order 表 → 转换聚合完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技成果展示/大型科学仪器共享（New）/三挂载位：①仪器列表/地图点 → 仪器详情 Modal（`:930-960`，`:952` Descriptions 第 11 项「使用频率 {activeInstrument.usageFreq} 次/月」，紧邻 `:953-955` 使用评价 rating）；②机构列表/地图点 → 机构详情 Modal（`:1058-1068`，`:1066` 使用频率项）；③服务统计域使用频率 Top10 图（`:623` SectionCard，`:194-197` freqTop 排序切片 `sort((a,b)=>b.usageFreq-a.usageFreq).slice(0,10)`，`:332-359` freqOption 横向条形图，tooltip 双值「使用频率 + 使用评价」）。mock 数据源：INSTRUMENTS 32 台（`:109-141`，每条 usageFreq 字段）+ INSTITUTIONS 14 家（`:180-196`）+ CHART_METRICS.usageFreq（`:245-248` lineage）。

### 1.2 为什么需要本指标

使用频率是仪器共享的需求热度读数：管理者看 Top10 判断资源紧张度与排期策略（SRS :75「掌握仪器开放情况和可预约资源，提升利用效率」）；创业者按频率避让拥挤仪器、选高效机构（SRS :235「为用户快速锁定高效服务机构提供辅助」）。它与开放率（供给可用性）、共享率（开放意愿）构成仪器共享运营三角。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「入网仪器月均使用频率」指标名在三份需求说明书中未出现；SRS 三处上位句（:75 系统自动统计共享率及使用频率 / :107 自动收集使用后的反馈评价及使用频率 / :235 实时动态统计开放率活跃状态及使用频率）均为功能要求，无频率的公式（单量口径 vs 机时口径、月度窗口、剔除取消单与否）。公式实际由 UI mock lineage（源表 ads_is_instrument_usage，月均频次）补全。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①科技部《开放共享评价考核实施细则》（R1）：年均运行机时/共享机时（小时口径）——**机时台账**依赖；②高校仪器共享平台通行口径（R2）：月均预约完成单量（次/月，UI mock 同构）；③原值利用率口径（机时÷标准机时 1600h/年，R3 财政部口径）：复合依赖。三族一致依赖「预约/机时流水」——三源缺失的正是这一层。

### 1.5 引用来源

1. 科技部办公厅. 国家重大科研基础设施和大型科研仪器开放共享评价考核实施细则. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2026/202601/t20260116_195736.html （R1，2026-11-02 可达；运行机时/共享机时考核指标）
2. 教育部. 高等学校科研仪器开放共享评价考核（机时口径通行实践）[EB/OL]. https://www.moe.gov.cn （R2，2026-11-02 检索可达）
3. 财政部. 大型科研仪器设备利用率统计（原值利用率口径）[EB/OL]. https://www.mof.gov.cn （R3，2026-11-02 检索可达）

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意（即 UI lineage 口径）**：单台仪器月均使用频次（次/月）= 当月预约完成单量（不含取消）；机构级为成员仪器均值。
- **操作化定义（未实现）**：usageFreq(仪器,月) = COUNT(预约单 WHERE 仪器 AND 月 AND 状态∈{已完成,服务中})；机构值 = 成员仪器按台均。
- **降档触发器**：已处最低档。
- **升档触发器**：①共享平台 ADS 接入（ads_is_order + ads_is_instrument_usage）→ 完全直接支持；②仅 ads_is_order → 月度单量转换聚合 → 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：大型科学仪器共享New·仪器/机构详情·使用频率 + Top10 图（三挂载位）。
- 相近叶：INCUB_008 入网仪器月均使用频率（S3-07 同根因件——预约流水零承载已证，本件复判独立留证）；SOFTSCI_015 热门仪器利用率排行（usageRate 同字段族）；P10_040 共享率/P10_055 开放率/P10_041 评分（同 ads_is_* 表族缺口）；INCUB_035 仪器月度预约趋势（预约流水同根因，路A 件）。
- UI 容器：两个 Modal + 服务统计 Top10 图。

## 二、计算过程

从缺。使用频率的原料是预约/订单流水（或机时台账）：UI lineage 指定源表 `ads_is_instrument_usage` 在久新 218 表（SHOW TABLES 现场实数）0 实存——ads_is_* 前缀族整体缺失（P10_040 同根因）；jiuxin order/book/reserv 预约流水词族 0 命中。dev 17 schema/542 表词族双扫：usage 列命中仅 `config.group_capacity.usage`/`tenant_capacity.usage`（容量配额语义）；freq 命中 `chain_hotspot.news_freq_score`（资讯热度）/`policy_subscription.push_frequency`（推送频率）；`bi.test_order`（order_name/order_sign_date）为积木报表测试单语义——均非仪器使用。gkx 280 表仪器族 0（dwd_medical_device 15 列：dwd_id/id/device_name/device_type/device_id_issuing_agency/brand_name/company_name/created_time/updated_time/…，无 usage/机时/预约列）。无流水即无频率，禁伪算。mock 32 仪器 38-260 次/月 + 14 机构 65-260 次/月为演示值（ui_demo_fallback 披露）；需规背景仅 2020-12 底有效订单 1,336 个总量。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 指定源表 ads_is_instrument_usage（频率面） | jiuxin | **无表**（ads_is* 0 实存） |
| 预约/订单流水（转换原料） | jiuxin | **无表**（order/book/reserv 0） |
| 机时/频率列（代理候选） | dev | **异域语义**（容量/资讯/推送 4 处） |
| 仪器台账（关联键） | 三源 | **无表**（P10_040 同缺口） |
| 测试单表（代理候选） | dev bi.test_order | **语义错位**（积木报表测试单） |

### 3.2 现场复核清单

UI 链实读：`:952/:953-955`（仪器 Modal 频率+评价双项）；`:1066`（机构 Modal 频率项）；`:623`（Top10 卡头）；`:194-197`（freqTop 排序链）；`:332-359`（freqOption 图配置，tooltip「使用频率：{value} 次/月 + 使用评价：{rating} 分」）；mock `:109` 起 32 台 usageFreq 值 + `:245-248` lineage 原文。三源实连复核（共享探针快照）：jiuxin ads_is_hits=[]/booking_order_family=[]；dev instrument_family_hits 4 异域列逐名核验；gkx instrument_family=[]；dwd_medical_device 15 列清单核验（无 usage 族）。需规 3565 行有效订单 1,336 复核。

## 四、数据缺失情况

### 4.1 缺口清单

①预约/订单流水零承载（结构级主因——ads_is_order/ads_is_instrument_usage 均未接入）；②仪器台账零承载（频率的关联键，P10_040 同缺口）；③机时台账零承载（考核细则口径的替代原料同样缺失）；④月度窗口/剔除规则口径未立项（完成单口径 vs 含取消口径需裁定）。

### 4.2 修复建议与影响面

短期：共享平台 ADS 接入 order + instrument_usage 两表 → 本件**完全直接支持**（Top10/详情双位即活），同族 P10_040/041/055 及 INCUB_008/035、SOFTSCI_015 整族升档。中期：机时口径并行（考核细则对齐，需机时台账）。远期：频率×开放率×评分联动画像（机构运营三维）。

### 4.3 影响面

仪器/机构两个 Modal 频率项与 Top10 图均为 mock 演示态；服务统计域四宫格中本图与「月度预约趋势」（INCUB_035 同根因）共缺预约流水。

## 参考文献

1. 科技部办公厅. 国家重大科研基础设施和大型科研仪器开放共享评价考核实施细则 [EB/OL]. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2026/202601/t20260116_195736.html （R1，2026-11-02 可达）
2. 教育部. 高等学校科研仪器开放共享评价考核 [EB/OL]. https://www.moe.gov.cn （R2，2026-11-02 检索可达）
3. 财政部. 大型科研仪器设备利用率统计口径 [EB/OL]. https://www.mof.gov.cn （R3，2026-11-02 检索可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技成果展示/大型科学仪器共享.md》三处上位句：

:75（仪器资源状态与预约展示）：

> 仪器资源按空闲、排期协调、忙碌等服务状态以多种图标形式标识，系统自动统计共享率及使用频率，用户可随时掌握仪器开放情况和可预约资源，提升利用效率。

:107（使用评价收集）：

> 自动收集用户对仪器使用后的反馈评价及使用频率，生成实时分析报告，让高校、科研单位和创新企业参考历史数据，提高选择决策和服务满意度。

:235（资源状态与实时活跃度）：

> 实时动态统计各服务机构仪器资源开放率、当前活跃状态及使用频率，系统高亮显示热门资源，为用户快速锁定高效服务机构提供辅助。

检索记录：`rg 入网仪器月均使用频率|使用频率` 三份说明书 → 指标名 0 命中（「使用频率」仅功能句）；UI lineage 口径全文见 mockData.js:245-248。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_037_out.json`）

facts（ui_mount 三挂载位/ui_compute_chain 排序链/ui_mock 32 仪器 38-260/ui_lineage_note 源表契约/probe_jiuxin_ads_is=[]/probe_jiuxin_booking_order=[]/probe_dev_usage_cols 4 异域列/probe_gkx_instrument_family=[]/probe_dev_table_total=542/probe_gkx_table_count=280/probe_jiuxin_table_count_live=218/family_note INCUB_008 复判）；derived[0]（instrument_monthly_avg_usage_freq 负结论 null 登记）；absence_probe（三件）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2021-2026 / note 月度口径）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：考核细则机时口径（运行/共享机时，R1）→ 平台单量口径（月均预约完成单，UI 同构，R2）→ 财政利用率口径（机时÷1600h，R3 复合）。数据矩阵：ads_is_* 表族 0；预约流水 0；机时台账 0；异域列 4 处（容量/资讯/推送/测试单）。分期方案：一期 ADS 接入 order+usage（完全直接支持）、二期机时口径并行、三期三维联动画像。风险登记：单量口径 vs 机时口径的数值量级差（需口径标注）；月度窗口滚动规则未定。总判：完全不支持（升档随共享平台 ADS 表族接入整族解锁）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_037.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneC.py` | 快照键与本件 facts 零漂移 |
| 判档一致 | MD 文首「完全不支持」= out.json | 一致 |
| 断言 | jiuxin ads_is=[] / booking=[] / gkx instrument=[] | 脚本内 assert 通过 |
| mock 披露 | 38-260 次/月仅 §1.1 语义描述 | 不参与支持度结论 |

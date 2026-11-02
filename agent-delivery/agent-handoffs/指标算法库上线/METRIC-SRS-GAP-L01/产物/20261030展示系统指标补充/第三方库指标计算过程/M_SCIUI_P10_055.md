# M_SCIUI_P10_055 机构入网仪器开放率（openRate%）—— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：科技成果展示·大型科学仪器共享New·服务机构·机构开放率（InstrumentSharingNewPage.jsx:1065+809，清单序号 579 实查定位）
> **数据支持度**：**完全不支持**｜ **UI 挂载**：科技信息展示系统 → 大型科学仪器共享（New）→ 机构详情 Modal「开放率」+「机构开放率 TopN」图 + 地图点/进度条位（`InstrumentSharingNewPage.jsx:1065/:809/:241/:829`）｜ **公式定义人**：UI mock lineage 自带（机构开放率 = 开放共享仪器数 ÷ 入网仪器数 × 100%；源表 ads_is_org_open_rate）
> **复现脚本**：`code/M_SCIUI_P10_055.py`（薄壳，指向共享探针 `code/_shared_s308_laneC.py`）｜ **产物**：`code/M_SCIUI_P10_055_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标（SRS :187/:235 上位覆盖）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（指定源表 ads_is_org_open_rate 三源 0 实存）；直接数据=无；依赖结构=无（机构-仪器台账+开放标志对零承载；open_rate 列全库 0 命中）；依赖数据=无（分子分母均无承载）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 机构开放率是 P10_040 平台共享率的机构粒度下钻：lineage 公式 = 机构开放共享仪器数 ÷ 机构入网仪器数 × 100%，承载要求是「机构-仪器台账 + 开放标志对」（或现成 org_open_rate 结果表）。实测：指定源表 `ads_is_org_open_rate` 及整个 ads_is_* 族在久新 218 表（SHOW TABLES 实数）0 实存；dev 542 表 open_rate/open_share 列词族 0 命中（机构侧唯一 capability 表 realdata_research_org_stat 0 行空壳且无仪器关联）；gkx 280 表仪器族 0 命中（dwd_medical_device 的 company_name 是 FDA 注册商语义，非入网管理机构）。分子分母两依赖均无承载，公式无法执行，判完全不支持。

### 批次通用纪律摘要（S3-08 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | lineage 公式分子分母须同机构台账（口径注记）；负结论登记 |
| B4 | 负结论带探针 | absence_probe 三源逐一留证（§3.2/附录 B） |
| B5 | 确定性 | TopN 排序 openRate 降序（:257 sort 链） |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 数字-出处核对 | 14 机构 48-90% 对 mockData.js 核验 |
| B10 | ui_demo_fallback 披露 | mock 48-90% 演示值披露 |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 指定源表实存吗？ | 不存在 | jiuxin `SHOW TABLES LIKE 'ads_is%'`=0（218 表实数） |
| 机构-仪器台账可拼装吗？ | 不可 | org×instrument×open_flag 结构三源 0 表 |
| 有代理面吗？ | 无 | dwd_medical_device 注册商语义错位；org_stat 空壳 |

## 摘要

「机构入网仪器开放率（openRate%）」在大型科学仪器共享（New）页服务机构域有四挂载位：机构详情 Modal（`:1065`「开放率 {openRate}%」）、「机构开放率 TopN」图（`:809`，CHART_METRICS.orgOpenRate，lineage 指定源表 ads_is_org_open_rate）、地图点副题（`:241`「{type} · 开放率 {openRate}% · {activeStatus}」）、活跃度列表进度条（`:829` Progress percent={o.openRate}）。mock 给 14 家机构 48-90%（深圳计量院 90 最高/比亚迪 48 最低），TopN 图取 openRate 降序前 8（`:256-259`）。数据侧判定：**完全不支持**——指定源表族 ads_is_* 三源 0 实存；机构-仪器台账与开放标志对零承载；gkx 唯一 device 表（dwd_medical_device）的 company_name 是 FDA 注册商语义非入网机构。修复依赖共享平台 ADS 表族接入（P10_040 主缺口），org+org_open_rate 两表即活。

- 需求判定：指标名三份说明书未出现；SRS :187/:235 上位覆盖。
- 复现状态：薄壳已跑通；三源负结论落产物。
- 档位结论：**完全不支持**（机构粒度分子分母零承载）。
- 关键事实：ads_is_org_open_rate 0 实存；open_rate 列全库 0 命中。
- 升档路径：共享平台 ADS 接入 → 完全直接支持（TopN/进度条/地图副题即活）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技成果展示/大型科学仪器共享（New）/服务机构域。四挂载位：①机构地图点/列表 → 机构详情 Modal（`:1058-1068`，`:1065` 开放率项，同 Modal 含 `:1063` 入网仪器 instrumentCount 台套、`:1066` 使用频率、`:1067` 共享能力评分——机构运营四联读数）；②服务机构统计三宫格之一「机构开放率 TopN」（`:809-811`，`:256-259` orgOpenRateTop 排序切片前 8，`:423` 条形图数据）；③机构地图点副题（`:241`）；④资源状态与实时活跃度列表（`:828-830` Progress 进度条渲染 openRate）。mock 数据源 INSTITUTIONS 14 家（`:180-196` openRate 字段）+ CHART_METRICS.orgOpenRate（`:261-264` lineage 原文）。

### 1.2 为什么需要本指标

机构开放率度量单个服务机构「入网之后开放了多少」：管理者以 TopN 识别开放标杆与滞后机构（政策激励依据），用户以进度条快速筛选高可得性机构（SRS :235「为用户快速锁定高效服务机构提供辅助」）。它是平台共享率（P10_040）的机构粒度分解——两档读数构成「总量-结构」验证链。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「机构入网仪器开放率」指标名在三份需求说明书中未出现；SRS :187「自动在地图高亮展示各服务机构的地理分布及资源状态」/:235「实时动态统计各服务机构仪器资源开放率、当前活跃状态及使用频率」为功能要求，无机构开放率的公式与统计时点。公式实际由 UI mock lineage 补全（机构开放率 = 开放共享仪器数 ÷ 入网仪器数 × 100%，源表 ads_is_org_open_rate，T+1）。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①科技部考核细则（R1）：管理单位开放率（单位机组开放数÷单位机组总数）——**本件 lineage 同构**，依赖单位-机组台账；②深科技创新〔2017〕117 号（R2）：入网+开放义务的机构粒度执行率；③教育部高校考核（R3）：校级机组开放率通报口径。三族一致依赖「机构×仪器×开放标志」三层结构——三源缺失的正是这一层。

### 1.5 引用来源

1. 科技部办公厅. 国家重大科研基础设施和大型科研仪器开放共享评价考核实施细则. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2026/202601/t20260116_195736.html （R1，2026-11-02 可达；管理单位开放率考核）
2. 深圳市科技创新委员会. 深圳市促进重大科研基础设施和大型科学仪器共享管理暂行办法实施细则（深科技创新〔2017〕117 号）. https://stic.sz.gov.cn （R2，2026-11-02 检索可达）
3. 教育部. 高等学校科研仪器开放共享评价考核结果通报 [EB/OL]. https://www.moe.gov.cn （R3，2026-11-02 检索可达）

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意（即 lineage 口径）**：机构开放率 = 该机构开放共享仪器数 ÷ 该机构入网仪器数 × 100%，T+1。
- **操作化定义（未实现）**：openRate(org) = COUNT(instrument WHERE org AND open_flag=1) ÷ COUNT(instrument WHERE org) × 100；TopN 按值降序取 8。
- **降档触发器**：已处最低档。
- **升档触发器**：①共享平台 ADS 接入（ads_is_org + ads_is_org_open_rate）→ **完全直接支持**；②仅机构-仪器台账（org×instrument×open_flag）→ 自算转换 → 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：大型科学仪器共享New·服务机构·机构开放率（四挂载位）。
- 相近叶：P10_040 平台共享率（总量口径，路C 同族主缺口件）/P10_041 共享能力评分（openRate 为评分输入维）/P10_037 使用频率（同 Modal 四联读数之一）。
- UI 容器：机构详情 Modal + TopN 图 + 地图副题 + 活跃度进度条。

## 二、计算过程

从缺。机构开放率的承载要求是「机构-仪器台账 + 开放标志对」（org×instrument×open_flag 三层结构）或现成 org_open_rate 结果表：指定源表 `ads_is_org_open_rate` 及整个 ads_is_* 族在久新 218 表（SHOW TABLES 现场实数）0 实存；dev 17 schema/542 表 open_rate/open_share 列词族 0 命中，机构侧唯一统计表 `ads.realdata_research_org_stat`（capability_score 语义）0 行空壳且无仪器关联；gkx 280 表仪器族 0 命中——`dwd_medical_device.company_name` 为 FDA 注册厂商语义（Highridge Medical 等），非共享平台入网管理机构，且无开放标志列（S3-07 批共享探针已证，本件独立留证）。分子分母两依赖均无承载，公式无法执行，禁伪算。mock 14 机构 48-90% 为演示值（ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 指定源表 ads_is_org_open_rate（结果面） | jiuxin | **无表**（ads_is* 0 实存） |
| 机构-仪器台账（org×instrument） | 三源 | **无表** |
| 开放标志列（open_flag） | 三源 | **无列**（open_rate 词族 0 命中） |
| 机构维（14 家服务机构名单） | dev/gkx | **语义错位**（org_stat 空壳；dwd_medical_device 注册商≠入网机构） |

### 3.2 现场复核清单

UI 链实读：`:1065`（Modal 开放率项）；`:809-811`（TopN 卡）；`:256-259`（orgOpenRateTop sort 链）；`:423`（orgOpenRateOption 数据位）；`:241`（地图副题）；`:829`（Progress）；mock `:180-196`（14 机构 openRate 值域 48-90）+ `:261-264`（lineage 原文）。三源实连复核（共享探针快照）：jiuxin ads_is_hits=[]；dev ads_is_hits=[] + open_rate 列 0 命中 + instrument_family_hits 4 异域列；gkx instrument_family=[]；jiuxin instrument_family=[]。SRS :187/:235 原文核验。

## 四、数据缺失情况

### 4.1 缺口清单

①ads_is_org / ads_is_org_open_rate 表零承载（结构级主因）；②机构-仪器台账零承载（自算路径同堵）；③开放标志列零命中（任何等价物无）；④机构名单维错位（mock 14 家 vs 库内 org 域无仪器共享机构面）。

### 4.2 修复建议与影响面

短期：共享平台 ADS 接入 org + org_open_rate 两表 → 本件**完全直接支持**（四挂载位即活），同族 P10_040/041/037 整族升档。中期：机构开放率月度序列（T+1 滚动，补时序维度）。远期：开放率×频率×评分机构画像（`:1063-1067` 四联读数联动）。

### 4.3 影响面

机构详情 Modal 四联读数中「入网仪器 instrumentCount」同为 mock（台账缺）；TopN 图与进度条均为演示态；机构地图副题开放率位无真数。

## 参考文献

1. 科技部办公厅. 国家重大科研基础设施和大型科研仪器开放共享评价考核实施细则 [EB/OL]. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2026/202601/t20260116_195736.html （R1，2026-11-02 可达）
2. 深圳市科技创新委员会. 深科技创新〔2017〕117 号实施细则 [EB/OL]. https://stic.sz.gov.cn （R2，2026-11-02 检索可达）
3. 教育部. 高等学校科研仪器开放共享评价考核通报 [EB/OL]. https://www.moe.gov.cn （R3，2026-11-02 检索可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技成果展示/大型科学仪器共享.md》:187（服务机构地图展示）：

> 按照科研院所、高校、企业、检测机构等类别，自动在地图高亮展示各服务机构的地理分布及资源状态。用户可一目了然了解机构服务布局，便于寻找合作与申请服务。

:235（资源状态与实时活跃度）：

> 实时动态统计各服务机构仪器资源开放率、当前活跃状态及使用频率，系统高亮显示热门资源，为用户快速锁定高效服务机构提供辅助。

检索记录：`rg 机构入网仪器开放率|开放率` 三份说明书 → 指标名 0 命中（「开放率」仅 :235 功能句）；UI lineage 口径全文见 mockData.js:261-264。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_055_out.json`）

facts（ui_mount 四挂载位/ui_compute_chain sort 链/ui_mock 14 机构 48-90/ui_lineage_note 源表契约/probe_jiuxin_ads_is=[]/probe_dev_ads_is=[]/probe_gkx_instrument_family=[]/probe_jiuxin_instrument_family=[]/probe_dev_open_rate_cols 0 命中/probe_dev_table_total=542/probe_gkx_table_count=280/probe_jiuxin_table_count_live=218/family_note）；derived[0]（org_instrument_open_rate 负结论 null 登记）；absence_probe（三件）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2021-2026 / note 截面读数说明）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：考核细则管理单位开放率（R1，lineage 同构）→ 117 号入网义务执行率（R2）→ 教育部校级通报（R3）。数据矩阵：ads_is_org 族 0；org×instrument×open_flag 0；代理面双错位（org_stat 空壳/注册商语义）。分期方案：一期 ADS 两表接入（完全直接支持）、二期月度序列、三期机构画像联动。风险登记：机构名单口径（mock 14 家与平台 499 管理单位的范围差）；开放率与共享率的术语混用风险（UI 两卡并存需口径标注）。总判：完全不支持（升档随 ADS 表族接入解锁）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_055.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneC.py` | 快照键与本件 facts 零漂移 |
| 判档一致 | MD 文首「完全不支持」= out.json | 一致 |
| 断言 | jiuxin/dev ads_is=[] / gkx instrument=[] | 脚本内 assert 通过 |
| mock 披露 | 48-90% 仅 §1.1 语义描述 | 不参与支持度结论 |

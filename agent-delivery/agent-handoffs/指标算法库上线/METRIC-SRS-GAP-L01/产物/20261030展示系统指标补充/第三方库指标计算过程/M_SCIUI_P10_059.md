# M_SCIUI_P10_059 三坐标测量机保有量（台套）—— 指标信息 MD

> **类型**：简单统计类｜ **域**：科技成果展示·大型科学仪器共享New·仪器盘点·机种粒度分类计数（InstrumentSharingNewPage.jsx:507/:613-615，mockData.js:131 INS-0023 实查定位）
> **数据支持度**：**完全不支持**｜ **UI 挂载**：科技信息展示系统 → 大型科学仪器共享（New）→ 仪器盘点左栏类别复选框台套计数 +「类别总量与共享状态统计」图（`InstrumentSharingNewPage.jsx:507/:613-615`，lineage 源表 ads_is_instrument_registry）｜ **公式定义人**：UI mock lineage 自带（按设备分类统计入网仪器台套数；T+1）
> **复现脚本**：`code/M_SCIUI_P10_059.py`（薄壳，指向共享探针 `code/_shared_s308_laneC.py`）｜ **产物**：`code/M_SCIUI_P10_059_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标（SRS :59 仪器类别精准筛选上位覆盖）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（ads_is_instrument_registry 三源 0 实存）；直接数据=无；依赖结构=无（入网仪器台账零承载）；依赖数据=无（dwd_medical_device 10,000 行为 FDA 医疗器械注册库，CMM 词族四 pattern 0 命中——语义错位实证）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 三坐标测量机保有量 = 入网仪器台账按机种（三坐标测量机/CMM）的分类计数。承载要求是「入网仪器台账（名称+类别+归属机构）」或现成 registry 结果表。实测：lineage 指定源表 `ads_is_instrument_registry` 及整个 ads_is_* 族在久新 218 表（SHOW TABLES 实数）0 实存，dev 542 表 instrument 词族仅命中 4 个异域列（chain_hotspot.news_freq_score 等），gkx 280 表仪器/入网词族 0 命中；唯一万行级设备面 `gkx.dwd_medical_device`（10,000 行）经 CMM 词族四 pattern 实测（坐标 0/COORDINAT 0/CMM 0/MEASUR 2）+ device_type 品类分布实证（top5 全为脊柱骨钉等临床品类），确认为 FDA 医疗器械注册库——与共享仪器入网台账语义错位（派单预期披露项已落实为定量证据）。计数无分子无台账，判完全不支持。

### 批次通用纪律摘要（S3-08 批共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 无除法（分类计数件）；负结论登记 |
| B4 | 负结论带探针 | absence_probe 四件留证（含语义错位专项） |
| B5 | 确定性 | type_top5 按 c DESC 排序（脚本 ORDER BY） |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 数字-出处核对 | INS-0023 行字段对 mockData.js:131 核验 |
| B10 | ui_demo_fallback 披露 | mock 32 台套/机械 3 台套演示值披露 |
| B11 | 多本账互推 | 与共享快照 `_shared_s308_laneC_out.json` 零漂移 |
| 基期三键 | base_years_used/missing/note | 产物全键（截面读数说明） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 指定源表实存吗？ | 不存在 | jiuxin `SHOW TABLES LIKE 'ads_is%'`=0；dev ads_is_hits=0 |
| 有台账可分类计数吗？ | 无 | 三源 instrument 词族 0 表（dev 4 命中为异域列） |
| 候选代理面可用吗？ | 不可（语义错位） | dwd_medical_device CMM 四 pattern 0 命中；top5=脊柱骨钉临床品类 |

## 摘要

「三坐标测量机保有量（台套）」挂在大型科学仪器共享（New）页仪器盘点域：左栏类别复选框逐类显示「N 台套」（`:507`，机械类 mock 3 台套，其中 `INS-0023` 三坐标测量机 GLOBAL S 07.10.07，Hexagon 瑞典，深圳计量院几何量所）+「类别总量与共享状态统计」图（`:613-615`，lineage 源表 ads_is_instrument_registry，T+1）。数据侧判定：**完全不支持**——ads_is_* 族三源 0 实存；唯一 10,000 行设备面 gkx `dwd_medical_device` 是 FDA 医疗器械注册库（CMM 词族 坐标/COORDINAT/CMM 三 pattern 实测 0 命中，MEASUR 词族 2 行为 MEASURING SCREWDRIVER 手术器械；device_type top5=Spinal bone screw 1062/Bone-screw 734 等临床品类），语义错位禁伪算。修复依赖共享平台 ADS 表族接入（P10_040 主缺口同门），registry 一表即活。

- 需求判定：指标名三份说明书未出现；SRS :59 仪器类别精准筛选（统计不同类别仪器的总量）上位覆盖。
- 复现状态：薄壳已跑通；CMM 词族四 pattern 零命中落产物。
- 档位结论：**完全不支持**（台账零承载+代理面语义错位）。
- 关键事实：ads_is_instrument_registry 0 实存；dwd_medical_device CMM 0 命中（10,000 行注册库）。
- 升档路径：共享平台 ADS 接入（ads_is_instrument_registry）→ 完全直接支持（类别计数+机种下钻即活）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技成果展示/大型科学仪器共享（New）/仪器盘点 tab。挂载位：①左栏仪器类别筛选卡（`:500-515`，INSTRUMENT_CATEGORIES 12 类复选框，每类后缀「{categoryCounts[c]} 台套」实时计数）；②「类别总量与共享状态统计」堆叠图（`:613-615`，CHART_METRICS.categoryStatus = M_IS_CATEGORY_STATUS，lineage 原文「按设备分类统计入网仪器台套数及共享状态分布（演示样本 32 台套）。源表：ads_is_instrument_registry；T+1」）；③仪器详情 Drawer 设备分类字段（`:943`）。本件=该类别计数链的机种粒度下钻：三坐标测量机（INS-0023）是「机械」类 3 台套之一。

### 1.2 为什么需要本指标

机种粒度保有量回答「某类高价值仪器深圳有多少台、落在哪些机构」：管理者以保有量做购置决策与重复建设预警（三坐标测量机是几何量计量的标机型，单价 160 万级），用户以机种筛选锁定送测机构。SRS :59「统计不同类别仪器的总量和使用状态，方便资源统筹和专项服务调度」——机种计数是类别统计的下钻层。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「三坐标测量机保有量」指标名在三份需求说明书中未出现；SRS :59 给出的是类别筛选与总量统计的功能要求，无机种口径（机种词典、台套定义、在网/退役边界）。台套口径由 UI mock lineage 补全（按设备分类统计入网仪器台套数，源表 ads_is_instrument_registry）。

### 1.4 类似指标权威方法可行性分析概要

保有量权威口径族（完整版指向附录 C）：①科技部重大科研基础设施与大型科研仪器国家网络管理平台（R1）：入网机组按仪器分类目录（分析仪器/物理性能测试仪器等 20 大类）计数——**本件 lineage 同构**，依赖入网登记；②深圳市大型科学仪器共享服务平台（R2）：入网仪器台账按机种字典分类；③海关/统计部门设备保有量普查（R3）：购置流水累计折算。三族一致依赖「入网/购置台账」——三源缺失的正是这一层。

### 1.5 引用来源

1. 科技部. 重大科研基础设施和大型科研仪器国家网络管理平台入网指引 [EB/OL]. https://www.most.gov.cn （R1，2026-11-02 检索可达）
2. 深圳市科技创新委员会. 深圳市大型科学仪器共享服务平台 [EB/OL]. https://stic.sz.gov.cn （R2，2026-11-02 检索可达）
3. 国家统计局. 高技术产业（制造业）统计分类与设备保有量口径 [EB/OL]. http://www.stats.gov.cn （R3，2026-11-02 检索可达）

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意（即 lineage 口径）**：三坐标测量机保有量 = ads_is_instrument_registry 中机种=三坐标测量机（CMM）的入网台套数，T+1。
- **操作化定义（未实现）**：cmm_holdings = COUNT(*) FROM registry WHERE category='机械' AND machine_type IN ('三坐标测量机','CMM',…机种词典)。
- **降档触发器**：已处最低档。
- **升档触发器**：①共享平台 ADS 接入 ads_is_instrument_registry（含机种字段）→ **完全直接支持**；②仅有类别级台账（无机种列）→ 机种词典关键词匹配 → 完全转换支持（需披露匹配率）。

### 1.7 需求叶定位与相近叶关系

- 本叶：大型科学仪器共享New·仪器盘点·机种粒度计数（三坐标测量机保有量）。
- 相近叶：P10_040 平台共享率（同源表族主件）/P10_037 使用频率/P10_055 机构开放率/P10_041 能力评分——路C 仪器域五件同门（ads_is_* 缺口）。
- UI 容器：仪器盘点 tab 左栏类别卡 + 类别总量统计图。

## 二、计算过程

从缺。三坐标测量机保有量的承载要求是「入网仪器台账（名称+机种+类别+归属机构）」：lineage 指定源表 `ads_is_instrument_registry` 及整个 ads_is_* 族在久新 218 表（SHOW TABLES 现场实数）0 实存；dev 17 schema/542 表 instrument 词族仅 4 个异域列命中（chain_hotspot.news_freq_score/config.usage 等，非仪器面）；gkx 280 表 instrument|share_rate 词族 0 命中。唯一万行级设备候选 `gkx.dwd_medical_device`（10,000 行）经词族+品类双探针确证为 FDA 医疗器械注册库：CMM 词族四 pattern 实测全零（坐标 0/COORDINAT 0/CMM 0，MEASUR 2 行为 MEASURING SCREWDRIVER 手术器械）；device_type top5 为 Spinal bone screw non-bioabsorbable 1,062/Bone-screw internal spinal fixation 734/Orthopaedic bone screw 481/Polymeric spinal interbody fusion 296/Metallic spinal interbody fusion 277——全为骨科植入物临床品类，与共享仪器入网台账语义错位（派单「语义错位披露」预期落实为定量证据）。计数无分子无台账，禁伪算。mock 32 台套/机械 3 台套为演示值（ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 指定源表 ads_is_instrument_registry | jiuxin | **无表**（ads_is* 0 实存） |
| 入网仪器台账（名称+机种+类别） | 三源 | **无表** |
| 机种词典（CMM 同义词族） | 三源 | **无列**（无词典表） |
| 候选代理 dwd_medical_device | gkx | **语义错位**（FDA 注册库，CMM 0 命中） |

### 3.2 现场复核清单

UI 链实读：`:507`（类别台套计数）；`:613-615`（类别总量图+lineage）；`:943`（Drawer 设备分类）；mock `:131`（INS-0023 全字段）+ `:73-84`（12 类别常量）+ `:237-240`（categoryStatus lineage 原文）。三源实连复核（共享快照+薄壳补测）：jiuxin ads_is_hits=[]；dev ads_is_hits=[] + instrument_family 4 异域列；gkx instrument_family=[]；CMM 三 pattern 0/0/0；type_top5 临床品类。SRS :59 原文核验。

## 四、数据缺失情况

### 4.1 缺口清单

①ads_is_instrument_registry 表零承载（结构级主因）；②入网仪器台账零承载（任何含机种/类别的仪器面均无）；③机种词典零承载（无同义词表）；④代理面语义错位（医疗器械注册库≠共享仪器台账，四 pattern 定量实证）。

### 4.2 修复建议与影响面

短期：共享平台 ADS 接入 ads_is_instrument_registry（名称+机种+类别+归属）→ 本件**完全直接支持**（类别计数+机种下钻即活），路C 仪器域五件（P10_037/040/041/055/059）整族升档。中期：机种词典标准化（CMM/XRD/SEM 等同义词族入库）。远期：保有量×使用频率×开放率机构画像。影响面：类别统计图（categoryStatus）与左栏台套计数同步激活。

### 4.3 影响面

仪器盘点 tab 全部计数读数为 mock；机种粒度（INS-0023 详情 Drawer）为演示行；与 P10_040/055/037/041 共享同一结构性缺口。

## 参考文献

1. 科技部. 重大科研基础设施和大型科研仪器国家网络管理平台 [EB/OL]. https://www.most.gov.cn （R1，2026-11-02 检索可达）
2. 深圳市科技创新委员会. 深圳市大型科学仪器共享服务平台 [EB/OL]. https://stic.sz.gov.cn （R2，2026-11-02 检索可达）
3. 国家统计局. 设备保有量统计口径 [EB/OL]. http://www.stats.gov.cn （R3，2026-11-02 检索可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技成果展示/大型科学仪器共享.md》:59（仪器类别精准筛选）：

> 用户可按功能类别（如医药、电子、材料、化工）快速筛选仪器清单，系统联动高亮对应仪器在地图及列表中的分布结果，并统计不同类别仪器的总量和使用状态，方便资源统筹和专项服务调度。

检索记录：`rg 三坐标|测量机|保有量` 三份说明书 → 指标名 0 命中；「三坐标测量机」仅出现于 UI mockData.js:131（演示行）；lineage 口径全文见 mockData.js:237-240。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_059_out.json`）

facts（ui_mount 类别计数+统计图/ui_instrument_row INS-0023 全字段/ui_lineage 源表契约/ui_mock 32 台套 12 类机械 3/gkx_dwd_medical_device_rows=10000/gkx_medical_device_measure_like_rows=2/measure_like_samples/gkx_medical_device_cmm_zh_rows=0/cmm_en_rows=0/cmm_abbr_rows=0/gkx_medical_device_type_top5 临床品类/gkx_semantic_mismatch_note/dev_instrument_family_hits 4 异域列/dev_ads_is_hits=[]/gkx_table_count=280/gkx_instrument_family=[]/jiuxin_table_count_live=218/jiuxin_instrument_family=[]）；derived[0]（cmm_holdings_count 负结论 null 登记）；absence_probe（四件含语义错位专项）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2018-2026 / note 截面读数+购置日期口径提示）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：国家网络管理平台入网机组计数（R1，lineage 同构）→ 深圳共享平台台账口径（R2）→ 统计部门保有量普查（R3）。数据矩阵：registry 0；入网台账 0；机种词典 0；代理面 dwd_medical_device 语义错位（CMM 0/0/0+MEASUR 2 手术器械+top5 脊柱骨钉）。分期方案：一期 registry 接入（完全直接支持）、二期机种词典、三期机构画像。风险登记：机种名称不规范（中英混写/型号带机种名）需词典兜底；FDA 注册库误用风险（本件已定量排除）。总判：完全不支持（升档随 ADS registry 接入解锁）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_059.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneC.py` | 快照键与本件 facts 零漂移 |
| 判档一致 | MD 文首「完全不支持」= out.json | 一致 |
| 断言 | dwd_medical_device=10000；CMM 三 pattern=0 | 脚本内 assert/实测通过 |
| 语义错位 | type_top5 全临床品类 | 产物 gkx_medical_device_type_top5 |
| mock 披露 | 32 台套/机械 3 仅 §1.1 语义描述 | 不参与支持度结论 |

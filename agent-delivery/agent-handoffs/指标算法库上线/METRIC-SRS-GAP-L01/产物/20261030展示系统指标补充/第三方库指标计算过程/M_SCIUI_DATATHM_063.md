# 资源总数（M_SCIUI_DATATHM_063）

> **类型**：无业务逻辑数值类（渠道×资源条数登记面三源零承载，表级近似可交付）｜ **域**：科技信息展示系统·科技数据资源·接入视窗·资源来源分析和详情·汇总区「资源总数」｜ **UI 挂载**：`AccessSourceAnalysisDetail.jsx:373`（Statistic title="资源总数" value={channels.reduce((s, c) => s + c.count, 0)} suffix="个"）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（「资源总数」字面三份说明书 0 命中；语义锚 seq 351 渠道归集数据量统计——条数维总计无定义）｜ **口径归属**：UI 派生读数（渠道汇总的条数维总计），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_DATATHM_063.py`｜ **产物**：`code/M_SCIUI_DATATHM_063_out.json`
> **四判定摘要**：直接结构 = 无（渠道×资源条数登记面三源零命中：dev 542 表 resource/catalog/inventory/metadata/registry 词族 0 命中；gkx 280 表唯一近邻 `dwd_dim_source_code` 数据源维度表 4 行——语义排除；久新 live 215 张 resource 命名 7 张全为论文计量年表——语义排除）；直接数据 = 无（同左）；依赖结构 = 有（表级近似侧三源表清单面完整：dev information_schema/gkx SHOW TABLES/久新 SHOW TABLES）；依赖数据 = 有（表级近似读数 1,032/剔备份 930——036 件先例复用）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证（本件 2026-11-02 三源实跑复核 + 036 件计数产物复用，B11 漂移已登记）；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 口径（推测定义，§1.6）：渠道归集资源条数的总计——`Σ count(c) FROM 渠道资源登记面 GROUP BY channel`。渠道×资源口径登记面逐一排除：**dev** 542 表 resource/catalog/inventory/metadata/registry 词族 **0 命中**（information_schema 全文正则实跑）；**gkx** 280 表 resource/catalog/collect/inventory/registry 词族唯一命中 `dwd_dim_source_code`（数据源维度表 4 行——登记数据来源编码 source_code/source_name，非资源条目）**语义排除**；**久新** live 215 张（2026-11-02 实跑，快照 210 + 新增 5 张 ads_talent_*）resource 词族 7 张命中全为论文计量年表（`ads_city_subfield_resource_yearly` 27,720 行 city×subfield×year 论文计数 / `ads_institution_subfield_resource_yearly` 985,555 行 institution×subfield×year——「resource」指论文计量资源）**语义排除**。**降档不到底的原因**：表级近似侧三源结构+数据双在（036 件先例：三源表 1,032 张/剔备份 930 张）——若甲方裁定「资源≈数据表」可转正，但**一资源可多表，语义不等价**。`resource_total_by_channel = null`（B10）。**本件最重要的口径发现：mock 汇总-明细量级断裂**——汇总卡资源总数 1,256（Σ channels.count）vs 同组件 seq 352 明细面仅 12 行（asd-001~012），1,244 条差额无登记面承载——汇总卡与明细表非同一台账，正式版须先建资源目录再谈总数。

### 批次通用纪律摘要（S3-05 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 本件为计数总计（无可算派生比）；share 分布 38.6+28.3+19.5+9.6+4.0=100.0% 自洽核对；指标值 null 留空 |
| B4 | 负结论带探针 | 三件 absence_probe（dev/gkx/jiuxin，§3.3）+ 三处语义排除登记 |
| B5 | 确定性 | 词族命中 sorted()（gkx 表清单/久新表清单）；mock 读数正则实算 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 本件 py 已跑出 _out.json；产物零手改 |
| B8 | 回执不复收 | lane7 快照 + 036 件计数产物复用（不重跑计数）；本件三源词族探针为 063 新增（062 未覆盖 resource/catalog/inventory 词族） |
| B9 | 单位/日期陷阱 | 资源总数单位「个」（条数维）；同区「归集总量 33,670」为数据量维（volume）勿混——同名「归集」双维并存；久新 metrics_as_of_date 是快照日非统计期 |
| B10 | 口径裁定保守交付 | 指标值 null；汇总-明细断裂披露；count/volume 双维披露；触发器写死 |
| B11 | 多本账互推 | dev 542/gkx 280 与 lane7 快照零漂移；久新快照 210（2026-11-01）→ 本件实跑 215（2026-11-02，+5 张 ads_talent_*）——活库增长漂移已登记，resource 词族命中数不变 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有渠道×资源条数登记面可 Σ 吗？ | 无 | dev 0 命中 / gkx 1 张语义排除（维度表）/ 久新 7 张语义排除（论文计量）（§3.3） |
| 表级近似（资源≈表）可交付吗？ | 可 | 036 件先例：1,032/剔备份 930（须资源-表映射，§1.6） |
| mock 的 1256 能当资源总数吗？ | 不能 | 汇总-明细断裂：1256 vs 明细 12 行（1,244 差额无承载，§3.2） |

## 摘要

「资源总数」是接入视窗·资源来源分析和详情（组件注释自标「需规 seq 351–355」）汇总三卡排的第三卡：`AccessSourceAnalysisDetail.jsx:373` `<Statistic title="资源总数" value={channels.reduce((s,c)=>s+c.count,0)} suffix="个"/>`（1,256 个）——与「渠道数 5 类」（:363）、「归集总量 33,670」（:371，Σ volume 数据量维）并列，三卡共享渠道汇总前提。数据侧判定分两层：**渠道×资源条数口径**（本件正式口径）三源零承载——resource/catalog/collect/inventory/registry 词族命中全为语义排除（dev 0 命中/gkx 维度表 1 张/久新论文计量 7 张）；**表级近似**（资源≈数据表）可交付——036 件先例三源表计数 1,032/剔备份 930 张（gkx 99 张 bak + dev 3 张 tmp/copy 已剔）。判**部分支持**（登记面缺位+表级近似）。本件核心披露：**mock 汇总-明细量级断裂**——汇总卡 1,256（Σ 五渠道 count 485/356/245/120/50，share 合计 100.0% 自洽）vs 同组件 seq 352 明细面 12 行（asd-001~012，五渠道全覆盖但仅演示采样）——1,244 条差额在 mock 中同样无台账承载，演示数据的汇总层是手写分布而非明细聚合。脚本已跑通（三源排除证据+036 计数复用+久新活库漂移登记+mock 断裂实证落产物）。

- 需求判定：**UI 派生读数**（「资源总数」字面 0 命中；seq 351 渠道归集数据量统计语境的条数维总计卡）。
- 复现状态：脚本已跑通；三源词族排除 + 三处语义排除 + 036 计数复用 + 久新 215 漂移登记 + mock 断裂实证全落产物。
- 档位结论：**部分支持**（渠道×资源登记面零承载 ⇒ 正式口径不可交付；表级近似 930/1,032 可交付但须裁定）。
- 关键事实：**汇总-明细量级断裂**（1,256 vs 12）+ count/volume 双维并存——本件最重要的口径发现。
- 升档路径：资源目录立项 → 完全直接支持；裁定资源≈表 + 资源-表映射 → 完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技数据资源·接入视窗。挂载：资源来源分析和详情（1.1.1.1.4.4.2；组件注释自标「需规 seq 351–355」）——`AccessSourceAnalysisDetail.jsx:361-377` 汇总三卡排之第三卡：`:371-375` `<Col span={8}><Statistic title="资源总数" value={channels.reduce((s,c)=>s+c.count,0)} suffix="个"/></Col>`；同排第一卡「渠道数」（channels.length=5 类，:363）、第二卡「归集总量」（Σ volume=33,670，:367-369）——三卡同为 mock `accessSourceAnalysis.channels`（`mockData.js:101-107` 五渠道：科研院所 485/企业 356/第三方平台 245/高等院校 120/政府部门 50）的客户端 reduce 派生。同组件下方明细表（seq 352）dataSource 是 `accessSourceAnalysis.details` 12 行（:134-145）——汇总与明细**非同一数据源**（§3.2）。

### 1.2 为什么需要本指标

资源总数回答「平台归集了多少个数据资源」：它是接入视窗的**基数读数**——渠道贡献度对比（seq 351）以它为全量背景（科研院所 485 个占 38.6% vs 政府部门 50 个占 4.0%），多维筛选（seq 354）以它为筛选前全集，明细浏览（seq 352）以它为「能翻到多少条」的预期。没有总数，渠道占比无分母、明细表无完备性承诺。需求语义锚 SRS 接入视窗 seq 351「自动统计并展示各渠道归集的数据量，支持按时间、业务类型、来源类别进行细分」——各渠道细分（GROUP BY channel）与总计（Σ）是同一登记面的两级读数。权威对应物是 DAMA-DMBOK 数据资产管理：资产目录的条目计数是资产盘点的第一读数（catalog inventory count）——目录在，计数是 SELECT COUNT(*) 一行的事。本库场景下，该读数要求资源目录/归集台账存在——没有目录，任何「资源总数」都是无根之数。

### 1.3 需求文档是否给出定义方法

**需求文档未给出总数的定义方法。**「资源总数」字面三份说明书 0 命中——本读数仅见 UI 卡名。语义锚 SRS 接入视窗 seq 351「渠道归集数据量统计」（各渠道归集的数据量统计展示）——「数据量」一词本身双义（条数 vs 体量），UI 用 count/volume 双卡分列（资源总数 1,256 个 / 归集总量 33,670）恰是把双义拆开呈现，但哪一维是 seq 351 的「主维」无定义。**资源口径三无**：资源语义边界（数据集？数据表？API？文件？——与 036「数据表总数」的边界问题同根）、渠道枚举域（mock 五渠道 vs 主需求 :2613 渠道归集语境的渠道清单无登记）、时间快照规则（存量时点 vs 累计口径）均无定义。UI 的 1,256 是 mock 手写分布的 reduce 结果，不构成口径证据。

### 1.4 类似指标权威方法可行性分析概要

资源总数的权威方法分三层。其一，数据资产管理口径（R1 DAMA-DMBOK）：资产目录条目计数——`SELECT COUNT(*) FROM 资产目录`，前提是目录存在且登记粒度=资源粒度；其二，数据治理平台工程口径（R2 Dataphin/Atlas）：资产盘点以元数据采集为准——采集器扫表登记元数据，资产数=已采集元数据条目数（表级粒度，一表一资产）；其三，国家标准统计口径（R3 GB/T 33850 服务数据）：资源统计以登记台账为准——登记什么算什么，口径边界先行。方法族对照：

| 方法族 | 原料 | 计数机制 | 与三源匹配 |
|---|---|---|---|
| 资产目录计数（R1） | 资源目录表 | COUNT(*) | **无目录**（词族 0 命中/语义排除，§3.3） |
| 元数据采集盘点（R2） | 元数据库 | 采集条目数 | **表级近似有**（三源表清单 1,032——036 件先例） |
| 登记台账统计（R3） | 归集台账 | COUNT(*) | **无台账**（与目录同缺） |
| 前端演示 | mock 常量 | 手写分布 reduce | 结构披露（不作源） |

结论：三条权威路径的第一层原料（资源目录/归集台账）三源均无承载——资源粒度口径不可交付；表级近似（元数据盘点口径）结构+数据双在（1,032/剔备份 930）——「一表一资产」的 Dataphin 式口径可近似交付，但资源-表映射未登记（一资源可多表）。「目录缺、表清单在」构成本件部分支持的判定结构。与 036（数据表总数——表级口径的正面件）、064（数据资源条数——同族明细侧件）同根，与 056（覆盖资源数——流量侧对照件）构成「覆盖 vs 总量」对。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:373`（资源总数卡）、`:361-377`（三卡排）、`:165`（seq 351-355 注释锚）；mock 语义源 `mockData.js:101-107`（channels 五渠道）、`:134-145`（details 12 行明细）。
- 需求：SRS `bid-reference/srs/02-科技信息展示系统/科技数据资源/接入视窗.md` seq 351（渠道归集数据量统计语境），原文见附录 A。
- 权威方法：R1 DAMA-DMBOK（dama.org）；R2 阿里云 Dataphin 资产盘点口径（developer.aliyun.com）；R3 GB/T 33850-2017（openstd.samr.gov.cn）。
- 族内先例：`M_SCIUI_DATATHM_036.md`（三源表计数多口径 1,032/930）；`M_SCIUI_DATATHM_056.md`（覆盖 vs 总量对照件——mock 口径混同实证）；`_lane7_shared_probe_out.json`（三源表数 B11 锚）。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**：按 R1→R3 路径推测，资源总数是资源目录的条目计数（渠道汇总形态）——

$$N_{\text{total}} = \sum_{c \in C} \text{count}(c) = \text{COUNT}(\*) \; \text{FROM 资源目录}\; R \; \text{GROUP BY channel} \; \text{then} \; \Sigma$$

其中 $C$ 为渠道枚举域（mock 五渠道：科研院所/企业/第三方平台/高等院校/政府部门），count(c) 为渠道 c 的资源条数。**表级近似**（若甲方裁定资源≈数据表）：$N_{\text{total}} \approx$ 三源表计数（全口径 1,032 / 剔备份 930——036 件先例），但一资源可多表（一张库表 vs 一个数据集），须再乘资源-表映射。**口径三未裁**：资源语义边界（数据集/表/API/文件）、渠道枚举域（五渠道 vs 其他）、时间快照规则（存量时点 vs 累计）。**前提是资源目录存在，三源实测无（§3.3）**——公式列示仅作口径锚（F4：本件 §二 从缺）。

**降档/升档触发器（B10 模板）**：①资源目录/归集台账立项（含渠道字段）→ `COUNT(*) GROUP BY channel` 直查 → 升**完全直接支持**；②甲方裁定「资源≈数据表」+ 资源-表映射登记 → 表级近似转正（值=映射后资源数）→ 升**完全转换支持**；③维持现状 → 部分支持（UI 建议改挂表级口径并披露边界，或「暂无数据」）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技数据资源/接入视窗.md` seq 351（渠道归集数据量统计语境——条数维总计卡） |
| 所属四级功能 | 1.1.1.1.4.4 科技数据资源（接入视窗挂载） |
| 本件挂靠 | **UI 派生读数**——渠道归集语境的基数卡 |
| 同窗 siblings 卡 | 渠道数（5 类）/ 归集总量（33,670——**volume 维，067 数据资源总量同族**） |
| 跨族近件 | 036（数据表总数——表级口径正面件，近似源）；064（数据资源条数——明细侧件）；056（覆盖资源数——流量对照件）；066/067（类型数/总量——计数组连坐） |
| UI 容器 | 资源来源分析和详情汇总三卡排（§1.1） |

本件是 S3-05 资源计数组的**存量侧正面件**：与 056（覆盖——流量侧）构成「覆盖 vs 总量」对照对（056 的 mock 混同实证恰好反证总量值的存在感）；与 036（表级口径）是「资源粒度 vs 表粒度」的同根件——资源目录立项则本件与 064 双升（触发器①），表级映射裁定则与 036 合流（触发器②）。

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

本件读数「资源总数」存在三个口径，B10 并列登记：**口径 A（正式口径）**——渠道×资源条数登记面总计 $\sum_c \text{count}(c)$；三源无资源目录（§2.2），**不可得**，指标键 `resource_total_by_channel = null` 留空。**口径 B（表级近似·全口径）**——若裁定资源≈数据表，$N \approx 1{,}032$（derived `resource_total_table_approximation_all`）；**口径 C（表级近似·剔备份）**——$N \approx 930$（derived `resource_total_table_approximation_no_backup`）。B/C 两读数可交付但资源-表语义不等价（一资源可多表），登记 derived 带注记不冒充正式值；**mock 1,256 演示值**不作任何口径原料（B10）。

### 2.2 排除实测：资源目录词族三源逐一留证

判「无承载」前的三源探针（本件 2026-11-02 实跑）：**dev** 542 表 resource/catalog/inventory/metadata/registry 词族命中 3 张（`facts.three_source.dev_registry_hits`）——`gkxlumenx_cfg.cfg_model_registry`（模型配置注册，25 行）/`gkxlumenx_cfg.model_registry`（0 行）/`gkxlumenx_job.xxl_job_registry`（调度执行器注册，0 行）——均为**系统配置/调度注册**语义非资源目录登记面，语义排除；**gkx** 280 表词族命中 0 张（`facts.three_source.gkx_hits=[]`），最近邻 `dwd_dim_source_code`（source_code 词族补查）4 行（`facts.three_source.gkx_dwd_dim_source_code_rows`，13 列维度表 `gkx_dwd_dim_source_code_cols_sorted`）——数据来源编码维度表，语义排除；**久新** live 215 张（`facts.three_source.jiuxin_table_total`，快照 210+5 漂移已登记）resource 词族命中 7 张（`facts.three_source.jiuxin_resource_hits_sorted`）——DESC 实查两张代表表均含 paper_count 列（`facts.three_source.jiuxin_desc_paper_count_present=true`），论文计量年表语义排除。三源结论：资源目录面 0（语义级）。

### 2.3 表级近似读数落盘（036 件先例复用）

口径 B/C 读数复用 036 件产物（B8 不重跑，`facts.table_level_approximation_from_036`）：全口径 **1,032** = dev 542 + gkx 280 + 久新 210（探测日 2026-11-01，`three_source_all_asof` 注记）；剔备份 **930** = 1,032 − gkx 备份 99 − dev 备份 3（配置 schema 与空表未剔——边界需裁定）。两读数进 derived（`resource_total_table_approximation_all/no_backup`）带「非资源条目口径」注记——语义边界（表≠资源）与映射缺位是转正阻断件。

### 2.4 mock 汇总-明细断裂核对（同基与量纲核对）

mock 汇总层正则实算：五渠道 count 485/356/245/120/50（`facts.ui.mock_channels_count_5=true` 五行解析），Σ=**1,256**（`facts.ui.mock_resource_total_sum`）；share 五值合计 **100.0%**（`facts.ui.mock_share_sum_pct`，同基自洽核对）；并列卡归集总量 Σ volume=**33,670**（`facts.ui.mock_volume_total_sum`——数据量维，与 count 维同名「归集」双量纲并存，B9）。**断裂实证**：同组件 seq 352 明细面 `details` 仅 **12 行**（`facts.ui.mock_detail_rows`，五渠道全覆盖 `mock_detail_channel_distinct=5`）——汇总 1,256 vs 明细 12，差额 **1,244**（`facts.ui.mock_detail_vs_channels_total_gap`）无台账承载：汇总层是手写分布非明细聚合。

### 2.5 稳健性与口径敏感性

三点敏感性：其一，**资源语义边界**——数据集/表/API/文件四候选粒度下单资源计数可差数量级，表级近似（930/1,032）只是「一表一资产」的 Dataphin 式口径；其二，**备份/配置剔除边界**——930 vs 1,032 的差（102 张）随备份判定规则浮动（gkx bak 后缀 99 张为显性，隐性备份无规则）；其三，**mock 双卡量纲混读**——count（个）与 volume（体量）同名「归集」并列，正式版不拆双卡则总数读数必被误读为体量。

### 2.6 需求符合性预评

seq 351 渠道归集数据量统计的「条数维总计」——**不满足**（渠道×资源登记面无承载）；「平台资源基数」——部分满足（表级近似 930/1,032 可挂，须披露表≠资源口径差异）。预评与触发器对齐：目录立项则本件与 064/066/067 连升。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_DATATHM_063.py`（三源词族实跑探针 + DESC 语义核对 + 036/lane7 复用 + mock 正则实算；零 `demo_*`）；运行 `python3 code/M_SCIUI_DATATHM_063.py`。
- 产物：`code/M_SCIUI_DATATHM_063_out.json`。正文数字与产物键逐一对应：`three_source.dev_registry_hits`（3 张语义排除，§2.2）、`three_source.gkx_dwd_dim_source_code_rows=4`（§2.2）、`three_source.jiuxin_resource_hits_sorted`（7 张，§2.2）、`table_level_approximation_from_036.three_source_all=1032` / `three_source_no_backup=930`（§2.3）、`ui.mock_resource_total_sum=1256` / `mock_volume_total_sum=33670` / `mock_share_sum_pct=100.0` / `mock_detail_rows=12` / `mock_detail_vs_channels_total_gap=1244`（§2.4）、derived `resource_total_by_channel=null` + 两近似键 1,032/930（B10 注记，§2.1/§2.3）。
- 结果解读：目录词族三源排除 + 表级近似双口径落盘 + 汇总-明细断裂实证——「资源粒度不可数、表级近似可交付」。
- 对照需求功能要求的评审：渠道条数总计——不满足；资源基数——部分满足（§2.6 预评）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 排除 | dev registry 词族 | `three_source.dev_registry_hits` | 3 张（模型/调度注册，语义排除） |
| 排除 | gkx 目录词族/近邻 | `three_source.gkx_hits` / `gkx_dwd_dim_source_code_rows` | [] / 4 行（维度表排除） |
| 排除 | 久新 resource 词族 | `three_source.jiuxin_resource_hits_sorted` | 7 张（paper_count 实证，语义排除） |
| 近似 | 表级全口径 | derived `resource_total_table_approximation_all` | 1,032 |
| 近似 | 表级剔备份 | derived `resource_total_table_approximation_no_backup` | 930 |
| mock | 汇总层 Σ count | `ui.mock_resource_total_sum` | 1,256（share 100.0%） |
| mock | 并列卡 Σ volume | `ui.mock_volume_total_sum` | 33,670（双量纲） |
| mock | 明细层行数 | `ui.mock_detail_rows` | 12（差额 1,244 断裂） |
| 指标 | 正式口径 | `resource_total_by_channel` | null（B10） |

九行对照中，断裂三元组（1,256 / 12 / 1,244）是全件最重要的负价值证据：mock 汇总层与明细层非同一登记面，正式版照抄即得无源总数；表级近似 930/1,032 是即期可交付的基数骨架，等待资源-表映射与语义裁定（§1.6 触发器）。


## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 资源目录/归集台账面（资源条目+渠道字段） | 三源 | — | — | **不存在** | **缺（正式口径判定性）** |
| D2 | 资源-表映射（表级近似转正要件） | 三源 | — | — | **不存在** | 缺（近似转正阻断） |
| D3 | 表级近似：三源表清单 | 三源 | information_schema/SHOW TABLES | 1,032 张（剔备份 930） | 直查 | 近似可得（036 件先例） |
| D4 | 最近邻：gkx `dwd_dim_source_code` | gkx | source_code/source_name | 4 行 | 直查 | **语义排除**（数据源维度表非资源条目） |
| D5 | UI 演示值 | UI | mock accessSourceAnalysis | 2 层（channels/details） | mock | 边界证据（不作源） |

`support_judgment="部分支持"`、产物与文首一致（闸 6）。

### 3.2 D5 mock 侧证据（汇总-明细量级断裂——本件核心披露）

mock 汇总层：`accessSourceAnalysis.channels`（`mockData.js:101-107`）五渠道 count 485/356/245/120/50——资源总数卡 1,256 = Σ（正则实算）；share 五值 38.6/28.3/19.5/9.6/4.0 合计 100.0% 自洽（手写圆润值）。**量级断裂实证**：同组件 seq 352 明细面 `details`（:134-145）仅 **12 行**（asd-001~asd-012，五渠道全覆盖——科研院所 3/企业 3/第三方平台 2/高等院校 2/政府部门 2）——汇总 1,256 vs 明细 12，**1,244 条差额在 mock 中同样无台账承载**。这说明演示作者的两层结构（汇总层手写分布 + 明细层演示采样）不是同一登记面的两级聚合——正式版若照此实现，汇总卡将是无源之数。**披露**：1,256 不作资源总数原料（B10）；「归集总量 33,670」（Σ volume）与本件 count 维并列——同名「归集」双维并存（volume 维归 M_SCIUI_DATATHM_067）。

### 3.3 D1 的 absence_probe 全记录（含三处语义排除专段）

否定性证据三件套：**查了什么**——①dev 542 表 resource/catalog/inventory/metadata/registry 词族（2026-11-02 information_schema 实跑正则：**0 命中**——dev 侧 gkxlumenx_* 十六 schema 无任何资源目录登记面）；②gkx 280 表 resource/catalog/collect/inventory/registry 词族（经 `_gkxdb.py` SHOW FULL TABLES 实跑：唯一命中 `dwd_dim_source_code`——DESC 实查 13 列（dwd_id/source_code/rid/source_name/table_data_source/is_deleted 等）4 行，**数据来源编码维度表**（登记专利/论文等数据从哪来），非接入资源条目——**语义排除**）；③久新 live 215 张（2026-11-02 SHOW TABLES 实跑；lane7 快照 210 + 新增 5 张 `ads_talent_honor_detail`/`ads_talent_integrity_score_demo`/`ads_talent_media_sentiment_assessment`/`ads_talent_topic_value_evidence`/`ads_talent_topic_value_summary`——人才面扩充，0 张消失）resource 词族 7 张命中（`ads_city_subfield_resource_yearly` 27,720 行/`ads_institution_subfield_resource_yearly` 985,555 行/`ads_recommendation_resource_direction`/`ads_research_resource_shortage_yearly`/`ads_resource_benchmark_city`/`ads_resource_optimization_recommendation`(+`_evidence`)）——DESC 实查前两张：列族为 paper_count/paper_fractional_count/citation_count/talent_count/project_count/funding_amount_cny——**城市/机构×子领域×年度的论文计量计数表**（「resource」=科技论文资源布局语义），≠接入数据资源条目——**语义排除**；④三份需求真源（「资源总数」0 命中；seq 351 渠道归集语境在）。**条件**——表级存在性+语义核对（三处最近邻过语义关）。**命中**——0（语义级）。四缺失情形归属：D1 属「**表不存在**」（资源目录/归集台账三源均无——修复动作是资产目录立项，与 064/066/067/056 共享）；D2 属「**表不存在**」（资源-表映射无登记——表级近似转正的阻断件，与 036/056 共享）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| dev 目录词族 | 542 表 0 命中（information_schema 正则实跑） |
| gkx 同词族 | 280 表唯一命中 dwd_dim_source_code（维度表 4 行，语义排除） |
| 久新 resource 词族 | 215 张（实跑）命中 7 张全为论文计量（DESC 实查 2 张，语义排除） |
| 久新活库漂移 | 快照 210（11-01）→ 实跑 215（11-02）：+5 张 ads_talent_*，0 消失——B11 登记 |
| 表级近似 | 1,032（542+280+210）/剔备份 930（036 件复用，B8；036 口径沿用其探测日） |
| UI 挂载 | 三卡排第三卡（:373）；siblings 渠道数/归集总量 |
| mock 断裂 | 汇总 1,256 vs 明细 12 行（1,244 差额无承载）；share 合计 100.0% |
| 脚本形态 | 三源实跑探针 + lane7/036 产物复用；mock 正则实算；零 demo_* |

## 四、数据缺失情况

### 4.1 资源目录面零承载（结构级，正式口径判定性缺口）

资源目录/归集台账三源零承载（§3.3）——dev 十六 schema 无任何 resource/catalog/inventory/metadata/registry 命名面，gkx 唯一近邻是数据来源维度表，久新 resource 命名全为论文计量。**本件的连坐面**：计数组五件（056/063/064/066/067）+ 表级正面件 036 共享「资源登记粒度缺位」——目录立项则 063/064 双升（资源条数），066/067（类型数/总量）随目录的字段扩展（类型/行数字段）连带受益。**四缺失情形归属「表不存在」**：修复动作是资产目录立项（资源条目：名称/类型/渠道/所属领域/登记时间——seq 352 明细面的字段清单可直接作目录 schema 底稿：dataType/collectTime/qualityLevel/relatedProject/field/volume 六元组）。

### 4.2 资源语义边界未裁（口径级，近似转正的阻断件）

本件降档的口径层根因：**资源 ≠ 表**——表级近似（1,032/930）是 Dataphin 式「一表一资产」口径，但业务语境的「资源」（mock 明细面形态：高能物理实验数据集/基因变异数据库）是**数据集粒度**，一资源可多表、一表可属多资源。正式版须裁定：①资源语义边界（数据集/表/API/文件）；②渠道枚举域（mock 五渠道是否即正式渠道清单——主需求 :2613 渠道归集语境无清单登记）；③count/volume 双维的主从（seq 351「数据量」一词双义，UI 已拆双卡但未裁主维）。此裁定与目录立项解耦，可先行。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 资源目录/归集台账立项 | 数据工程立项 | 本件 + 064/066/067 + 056（覆盖分母） | 触发器①（seq 352 明细六元组可作 schema 底稿） |
| 资源语义边界裁定（数据集/表/API） | 口径裁定 | 本件 + 036 + 计数组 | mock 断裂实证在前，可先行 |
| 资源-表映射登记 | 数据工程配套 | 本件 + 036/056 | 表级近似转正的阻断件，目录立项附带交付 |
| UI 汇总卡改挂或空态 | 展示规范 | 本件 UI | 1,256 演示值建议撤下（明细 12 行撑不起汇总层） |

档位后果：目录 → **完全直接支持**（COUNT(*) 直查）；映射转正 → **完全转换支持**；现状 → 部分支持。推荐顺序：口径裁定先行（即期一纸）→ 资源目录立项（seq 352 底稿）→ 资源-表映射（目录配套）。

## 参考文献

1. DAMA International. DAMA-DMBOK: Data Management Body of Knowledge[M]. 2nd ed. Technics Publications. https://www.dama.org/cp/body-of-knowledge （R1，2026-11-02 WebSearch 核验可达——资产目录条目计数是资产盘点第一读数，目录粒度=资产粒度是计数前提）
2. 阿里云开发者社区. Dataphin资产盘点与元数据采集口径[EB/OL]. https://developer.aliyun.com/article/1480319 （R2，2026-11-02 WebSearch 核验可达——元数据采集式资产盘点「一表一资产」工程口径，表级近似的权威形态）
3. GB/T 33850-2017 信息技术服务 质量评价指标体系[EB/OL]. 国家标准全文公开系统. https://openstd.samr.gov.cn/bzgk/std/index （R3，2026-11-02 WebSearch 核验可达——服务资源统计以登记台账为准，口径边界先行的国标锚）

# 附件

## 附录 A 原始需求原文摘录

**「资源总数」字面三份说明书未出现**（检索记录见 A.2）。语境原文：

SRS `bid-reference/srs/02-科技信息展示系统/科技数据资源/接入视窗.md` seq 351（渠道归集数据量统计）：

> ### 渠道归集数据量统计 · 序号 351
> #### 需规功能描述
> 自动统计并展示各渠道（如科研院所、企业、第三方平台）归集的数据量，支持按时间、业务类型、来源类别进行细分，帮助用户全面了解不同渠道的数据贡献度。

（SRS 原文渠道举例「科研院所、企业、第三方平台」三项 vs mock 五渠道——高等院校/政府部门是 UI 作者扩展，渠道枚举域无登记的实证。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 资源总数 | 主需求/核增/算法库 + SRS 分册 | 0 |
| 渠道归集数据量统计（语境锚） | SRS 接入视窗 | seq 351 |
| channels（count 字段） | mockData.js | :101-107（五渠道 485/356/245/120/50） |
| 资源总数 | AccessSourceAnalysisDetail.jsx | :373（Statistic 卡，Σ count reduce） |
| details（明细对照） | mockData.js | :134-145（12 行——断裂实证） |

## 附录 B 历史库表探测证据

### B.1 探针与快照

- 本件产物：`code/M_SCIUI_DATATHM_063_out.json`（2026-11-02 实跑：三源词族排除 + 三处语义排除 + 036 计数复用 + 久新活库漂移登记 + mock 断裂实证）。
- 共享探针：`code/_snapshots/_lane7_shared_probe_out.json`（三源表数 B11 锚）；`M_SCIUI_DATATHM_036_out.json`（表级计数先例复用，B8）。
- 族内对账：dev 542/gkx 280 与 lane7/036 逐键一致；久新 210（快照）→ 215（本件实跑）漂移已登记（+5 张 ads_talent_*，resource 命中数不变）。

### B.2 本件产物逐键清单（`code/M_SCIUI_DATATHM_063_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.ui.mock_channels_count_5` | 实算 | true（五渠道） | §3.2 |
| `facts.ui.mock_resource_total_sum` | 实算 | 1,256 | §3.2 |
| `facts.ui.mock_volume_total_sum` | 实算 | 33,670（volume 维对照） | §3.2 |
| `facts.ui.mock_share_sum_pct` | 实算 | 100.0（自洽核对） | §3.2 |
| `facts.ui.mock_detail_rows` | 实算 | 12（asd-001~012） | §3.2 |
| `facts.ui.mock_detail_vs_channels_total_gap` | 实算 | 1,244（断裂差额） | §3.2 |
| `facts.three_source.dev_table_total` | 探针 | 542（实跑复核） | §3.3 |
| `facts.three_source.gkx_table_total` | 探针 | 280（实跑复核） | §3.3 |
| `facts.three_source.jiuxin_table_total` | 探针 | 215（实跑；快照 210+5） | §3.3 |
| `facts.three_source.gkx_dwd_dim_source_code_rows` | 探针 | 4（维度表，语义排除） | §3.3 |
| `facts.table_level_approximation_from_036.three_source_all` | 计数 | 1,032（036 复用） | §3.1/§1.6 |
| `facts.table_level_approximation_from_036.three_source_no_backup` | 计数 | 930（036 复用） | §3.1/§1.6 |
| `derived[0].resource_total_by_channel` | 负结论 | null（B10） | §1.6/§二 |
| `absence_probe` | 探针 | 三件（dev/gkx/jiuxin） | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 原料 | 计数机制 | 贴合度 |
|---|---|---|---|---|
| 资产目录计数 | R1（DAMA-DMBOK） | 资源目录表 | COUNT(*) | 高（正式口径锚） |
| 元数据采集盘点 | R2（Dataphin） | 元数据库 | 采集条目数（一表一资产） | 高（表级近似形态） |
| 登记台账统计 | R3（GB/T 33850） | 归集台账 | COUNT(*) | 高（口径边界先行） |
| 前端演示 | mock 常量 | — | 手写分布 reduce | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 资源目录/台账 | 无（词族 0 命中） | 无（1 张语义排除） | 无（7 张语义排除） |
| 资源-表映射 | 无 | 无 | 无 |
| 表级表清单（近似） | 有（542） | 有（280） | 有（215 实跑/210 快照） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 资源粒度口径无可交付；表级近似登记（930/1,032 表数） | — |
| v1 | 资源语义边界+渠道枚举域裁定（一纸） | 口径裁定先行 |
| v2 | 资源目录立项（seq 352 六元组底稿）→ COUNT(*) 直查 | 触发器①（063/064 双升） |
| v3 | 资源-表映射登记 → 表级近似转正 | 触发器②（与 036 合流） |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| mock 1256 被当真实总数 | **高** | §3.2 断裂实证（vs 明细 12 行）+ B10 禁用注记 |
| 表数当资源数（一资源多表漏除） | **高** | §1.6 映射要件披露；§4.2 边界裁定先行 |
| count/volume 双维混用 | 中 | §3.2 双卡披露（volume 归 067）；B9 单位注记 |

### C.5 总判

**部分支持**：资源目录/归集台账面三源零承载（资源粒度口径不可交付），表级近似可交付但语义不等价（930/1,032 表数，须映射转正）；mock 汇总-明细断裂实证（1,256 vs 12）。本件是资源计数组存量侧正面件，与 064 连坐（目录立项双升）、与 036 合流（映射转正）、与 056 对照（覆盖 vs 总量）——目录立项是计数组五件的最大公约数修复动作。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_DATATHM_063.py` | 退出码 0，落 `_out.json` |
| 数据入口 | 三源实跑探针（dev/gkx/久新）+ lane7/036 产物复用 + mock 正则实算 | 本件新探针三源直连 |
| 判档一致 | 文首 vs `support_judgment` | 部分支持 |
| B11 对账 | dev 542/gkx 280 零漂移；久新 210→215 漂移登记 | 漂移键在产物 |
| mock 对账复核 | Σ channels.count=1256；details=12 行；share=100.0% | 断裂差额 1,244 |
| 幂等重跑 | 探针确定性 + 正则确定性 | 逐位一致（活库表数随探测日浮动，产物已带 asof 注记） |
| 伪指标值残留 | `resource_total_by_channel` | null（无伪值） |
| §二 从缺 | 指标本体（资源粒度口径） | 无伪公式（F4） |

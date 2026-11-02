# 数据资源条数（M_SCIUI_DATATHM_064）

> **类型**：无业务逻辑数值类（供应方/渠道×资源登记面三源零承载，表级近似可交付）｜ **域**：科技信息展示系统·科技数据资源·应用视窗·数据供应方数据被调用情况「资源数」列 + 接入视窗·资源来源分析和详情「资源数」列（一名两挂）｜ **UI 挂载**：`ApplicationWindow.jsx:214`（supplierColumns 资源数列）/ `AccessSourceAnalysisDetail.jsx:238`（channelColumns）/ `:317`（groupColumns）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（「数据资源条数/资源数」字面三份说明书 0 命中；语义锚 seq 388 供应方归集 + seq 351 渠道归集双语境——分组计数无定义）｜ **口径归属**：UI 派生读数（供应方/渠道分组的资源计数列），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_DATATHM_064.py`｜ **产物**：`code/M_SCIUI_DATATHM_064_out.json`
> **四判定摘要**：直接结构 = 无（供应方×资源/渠道×资源登记面三源零命中：dev 唯一命中 `gkxlumenx_dwd.enterprise_supply_chain` 企业供应链关系空表——语义排除；gkx 双词族唯一命中 `dwd_dim_source_code` 数据源维度表——语义排除；久新 live 215 张供应方词族 0 命中、resource 7 张全为论文计量——语义排除）；直接数据 = 无（同左）；依赖结构 = 有（表级近似侧三源表清单面完整）；依赖数据 = 有（表级近似读数 1,032/剔备份 930——036 件先例复用）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证（本件 2026-11-02 三源实跑：供应方词族为 064 新增探针 + resource 词族排除复用 063 件结论，B11 漂移承 063 登记）；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 口径（推测定义，§1.6）：按归属维度分组的资源计数——供应侧面 `COUNT(*) FROM 资源目录 GROUP BY supplier`、渠道侧面 `GROUP BY channel`。归属×资源口径登记面逐一排除：**dev** 542 表 supplier/provider/vendor/supply 词族唯一命中 `gkxlumenx_dwd.enterprise_supply_chain`——DESC 实查 9 列（org_id/related_org_id/relation_type/relation_strength/is_core_supplier/risk_level 等）**0 行**——企业供应链关系图谱空表（is_core_supplier 是「核心供应商」关系标记，主体是机构间供应链关系非数据供应方×资源登记），**语义排除**；资源目录词族 0 命中承 063 件；**gkx** 280 表双词族（供应方+资源目录+source_code）唯一命中 `dwd_dim_source_code`（063 件 DESC 实查语义排除）；**久新** live 215 张供应方词族 0 命中、resource 词族 7 张全为论文计量年表（063 件语义排除）。**降档不到底的原因**：表级近似侧三源结构+数据双在（036 件先例：1,032 张/剔备份 930 张）——但归属字段缺位，分组维度不可得，仅全库总量近似。`data_resource_count_by_supplier = null`、`data_resource_count_by_channel = null`（B10）。**本件最重要的口径发现：mock 同库双面 865 差**——供应侧面 Σ resourceCount = 391 vs 渠道侧面 Σ count = 1,256，同一演示库内「资源条数」两个口径层差 865——供应方口径与渠道口径非同一台账（且 mock 内部三层自洽：供应方 5 行 = 区域组 2 组 = 部门嵌套，逐值 391 一致），正式版须先统一资源归属维度。

### 批次通用纪律摘要（S3-05 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 本件为分组计数（无可算派生比）；share 双面各合计 100.0% 自洽核对；指标值 null 留空 |
| B4 | 负结论带探针 | 三件 absence_probe（dev/gkx/jiuxin，§3.3）+ 三处语义排除登记 |
| B5 | 确定性 | 词族命中 sorted()；mock 读数正则实算（supplierStats/supplierRegionGroups/channels 三块独立解析） |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 本件 py 已跑出 _out.json；产物零手改 |
| B8 | 回执不复收 | resource 词族排除复用 063 件（DESC 实查不重跑）；lane7 快照 + 036 计数产物复用；供应方词族为 064 新增 |
| B9 | 单位/日期陷阱 | 资源数单位「个/项」双形（供应侧「项资源」/渠道侧「个」）；totalCalls 285.6 万次是调用维勿混；久新 metrics_as_of_date 是快照日 |
| B10 | 口径裁定保守交付 | 双键 null；双面 865 差披露；三层自洽披露；触发器写死 |
| B11 | 多本账互推 | dev 542/gkx 280 零漂移；久新 210→215 漂移承 063 登记；mock 三层 391 逐值对账（156+89+34=279 华北 / 67+45=112 华南） |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有供应方/渠道×资源登记面可 GROUP BY 吗？ | 无 | dev 1 张语义排除（供应链空表）/ gkx 1 张语义排除（维度表）/ 久新 0+7 张语义排除（§3.3） |
| 表级近似（资源≈表）可交付分组读数吗？ | 仅总量 | 036 件先例 1,032/930——归属字段缺位，分组维度不可得 |
| mock 的 391/1256 能当资源条数吗？ | 不能 | 同库双面差 865——两口径非同一台账（§3.2） |

## 摘要

「数据资源条数」是一名两挂的分组计数列：**供应侧面**（应用视窗·数据供应方数据被调用情况，seq 388 语境）——`ApplicationWindow.jsx:214` supplierColumns「资源数」列（dataIndex=resourceCount，:582 Table 消费）+ `:491` 区域组「{g.resourceCount} 项资源」行内读数，mock 是 `supplierStats`（`mockData.js:909-915` 五供应方 156/89/67/45/34）与 `supplierRegionGroups`（:918-941 华北 279/华南 112）；**渠道侧面**（接入视窗·资源来源分析和详情，seq 351 语境）——`AccessSourceAnalysisDetail.jsx:238` channelColumns「资源数」列 + `:317` groupColumns「资源数」列（分组聚合消费），mock 是 `channels` 五渠道（Σ=1,256，与 063 同源）。数据侧判定：归属×资源口径登记面三源零承载——供应方词族唯一命中是 dev 企业供应链空表（语义排除），资源目录词族排除承 063 件；表级近似可交付总量（036 件 1,032/930）但分组维度不可得。判**部分支持**。本件核心披露：**mock 同库双面 865 差**——供应侧 391 vs 渠道侧 1,256（同一演示库、同一「资源」一词），且供应侧内部三层（供应方 5 行/区域组 2 组/部门嵌套 6 行）逐值自洽 391——两套手写数据各自圆融、互不对账，正式版「资源归属维度」（供应方/渠道/部门是否同一登记面字段）是最先要裁的口径。脚本已跑通（供应方词族三源新探针 + 063 复用 + 三块 mock 正则实算落产物）。

- 需求判定：**UI 派生读数**（「数据资源条数/资源数」字面 0 命中——列名级读数非立项项；seq 388/351 双语境锚）。
- 复现状态：脚本已跑通；供应方词族三源排除 + 063 复用 + 双面 mock 实算 + 三层自洽对账全落产物。
- 档位结论：**部分支持**（归属×资源登记面零承载 ⇒ 分组口径不可交付；表级近似仅总量）。
- 关键事实：**同库双面 865 差**（391 vs 1,256）+ 供应侧三层自洽——本件最重要的口径发现。
- 升档路径：资源目录立项（含供应方/渠道归属字段）→ 完全直接支持；表级映射 → 仅总量近似（分组仍缺归属）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技数据资源。**一名两挂**：①应用视窗·数据供应方数据被调用情况·部门名称自动归集展示（1.1.1.1.4.4.4；mock 注释自标「seq 388 含部门/区域归集字段」）——`ApplicationWindow.jsx:211-219` supplierColumns 第 4 列「资源数」（`:214` dataIndex=resourceCount，align center），`:582` Table 消费渲染五供应方行；`:481-495` 部门归集卡区域组行内读数「{g.resourceCount} 项资源」（`:491`）——mock 是 `supplierStats` 五行（中科院 156/清华大学 89/深圳市政府 67/华为公司 45/北京大学 34）与 `supplierRegionGroups` 两组（华北 supplierCount 3/resourceCount 279、华南 2/112，departments 嵌套逐供应方）；②接入视窗·资源来源分析和详情（seq 351 语境）——`AccessSourceAnalysisDetail.jsx:238` channelColumns「资源数」列（dataIndex=count，渠道明细表）与 `:317` groupColumns「资源数」列（分组汇总表——GROUP_OPTIONS 选非 none 时切换消费，分组聚合逻辑 `:195-205` 对 details 12 行客户端 map 累加）——mock 是 `channels` 五渠道 count 485/356/245/120/50（与 063 资源总数卡同源）。

### 1.2 为什么需要本指标

资源数列回答「每个供应方/渠道各贡献多少个资源」：供应侧面它是 seq 388 归集摘要的计数维——管理者看中科院 156 项 vs 北京大学 34 项定位供应主力（与调用总量 125 万 vs 15.8 万次并排，资源规模与活跃规模对照）；渠道侧面它是 seq 351 渠道贡献度的条数维（与归集数据量 volume 列并列）。没有分组计数，供应方排名（supplierRankColumns）与渠道对比（channelColumns）都退化为纯调用读数——「谁贡献的资源多」与「谁被调用得多」是两个问题。权威对应物是 DAMA-DMBOK 数据资产管理：资产目录按来源域分组的条目计数（stewardship 报表的标准列）——前提是目录有归属字段。本库场景下，该读数要求资源目录含供应方/渠道归属——没有归属字段，任何分组计数都无从 GROUP BY。

### 1.3 需求文档是否给出定义方法

**需求文档未给出计数的定义方法。**「数据资源条数/资源数」字面三份说明书 0 命中——本读数仅见 UI 列名与行内读数。语义锚双语境：SRS 应用视窗 seq 388「对所有供应方进行智能归类，对调用数据的部门归属自动识别和展示」（供应方/部门/区域三轴归集——资源数是归集摘要列）；SRS 接入视窗 seq 351「自动统计并展示各渠道归集的数据量……支持按时间、业务类型、来源类别进行细分」（渠道轴——count 维与 063 同根）。**归属口径三无**：归属维度轴（供应方/部门/区域/渠道四轴在 mock 并存但关系无定义——supplierStats 带 department+region 双字段，区域组是 region 轴的二次归集）、资源语义边界（承 063：数据集/表/API 未裁）、同一台账否（mock 双面 391 vs 1,256——供应方口径与渠道口径显然非同一登记面，差额 865 无解释）均无定义。UI 的两套列是前端作者的演示约定，不构成口径证据。

### 1.4 类似指标权威方法可行性分析概要

资源数分组的权威方法分三层。其一，数据资产管理口径（R1 DAMA-DMBOK）：资产目录按 steward/source domain 分组计数——`GROUP BY source` 的标准报表列，前提是目录+归属字段；其二，主数据管理口径（R2 Dataphin/Atlas 资产地图）：资产按项目/数据源分组——元数据采集附带归属登记，分组计数随采集落地；其三，统计口径国标（R3 GB/T 33850）：分类统计以登记台账的类目字段为准——分组维度先行登记。方法族对照：

| 方法族 | 原料 | 计数机制 | 与三源匹配 |
|---|---|---|---|
| 目录分组计数（R1） | 资源目录+归属字段 | GROUP BY source | **无目录**（词族命中全语义排除，§3.3） |
| 元数据采集归属（R2） | 元数据库+归属登记 | 采集附带 | **表级近似有**（1,032 表清单）**但归属缺位** |
| 台账分类统计（R3） | 归集台账+类目 | GROUP BY 类目 | **无台账** |
| 前端演示 | mock 常量 | 手写两套 | 结构披露（不作源） |

结论：三条权威路径的第一层原料（含归属字段的资源目录/台账）三源均无承载——分组口径不可交付；表级近似只有表清单（无归属字段）——分组读数不可得，仅全库总量（930/1,032）。「目录缺、归属字段更缺」构成本件部分支持的判定结构（比 063 更紧一档：063 总量近似可交付，本件分组近似也不可交付）。与 063（总量——同族正面件）、036（表级口径）、066/067（类型数/总量——计数组连坐）同根。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:214`（supplierColumns 资源数列）、`:582`（Table 消费）、`:481-495`（区域组归集卡）；`AccessSourceAnalysisDetail.jsx:238`（channelColumns）、`:317`（groupColumns）；mock 语义源 `mockData.js:909-915`（supplierStats）、`:918-941`（supplierRegionGroups）、`:101-107`（channels）。
- 需求：SRS `bid-reference/srs/02-科技信息展示系统/科技数据资源/应用视窗.md` seq 388（部门名称自动归集展示）+ `接入视窗.md` seq 351（渠道归集数据量统计），原文见附录 A。
- 权威方法：R1 DAMA-DMBOK（dama.org）；R2 阿里云 Dataphin 资产盘点口径（developer.aliyun.com）；R3 GB/T 33850-2017（openstd.samr.gov.cn）。
- 族内先例：`M_SCIUI_DATATHM_063.md`（资源总数——resource 词族三源排除+DESC 语义核对复用源）；`M_SCIUI_DATATHM_036.md`（表级计数先例）；`_lane7_shared_probe_out.json`（三源表数 B11 锚）。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露口径不闭合）**：按 R1→R3 路径推测，资源数是资源目录按归属维度的分组计数——

$$N_{\text{res}}(s) = \text{COUNT}(\*) \; \text{FROM 资源目录}\; R \; \text{WHERE}\; R.\text{supplier} = s \qquad \text{或} \qquad N_{\text{res}}(c) = \text{COUNT}(\*) \; \text{WHERE}\; R.\text{channel} = c$$

供应侧面按供应方 s（可二次归集到部门/区域——mock 的 supplierRegionGroups 形态：region 组内 Σ 供应方计数），渠道侧面按渠道 c（063 同源）。区域/部门归集是分组键的层级上卷（supplier → department → region），同一登记面的三级 GROUP BY。**表级近似**（若资源≈表）：仅全库总量 $\sum_s N_{\text{res}}(s) \approx 930/1{,}032$——归属字段缺位，分组不可得。**口径三未裁**：归属维度轴（供应方/部门/区域/渠道四轴关系）、资源语义边界（承 063）、双面台账统一否（391 vs 1,256 的差额解释）。**前提是含归属字段的资源目录存在，三源实测无（§3.3）**——公式列示仅作口径锚（F4：本件 §二 从缺）。

**降档/升档触发器（B10 模板）**：①资源目录立项（含 supplier/channel/department/region 归属字段）→ `GROUP BY` 直查 → 升**完全直接支持**；②表级映射登记（表→资源）+ 归属字段补登 → 分组近似转正 → 升**完全转换支持**；③仅表级映射（无归属）→ 总量近似可得、分组仍缺 → 维持部分支持；④维持现状 → 部分支持（UI 两处列建议「暂无数据」）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `应用视窗.md` seq 388（供应方归集语境）+ `接入视窗.md` seq 351（渠道归集语境）——一名两挂 |
| 所属四级功能 | 1.1.1.1.4.4 科技数据资源（应用/接入双视窗挂载） |
| 本件挂靠 | **UI 派生读数**——归集摘要的计数列（供应侧+渠道侧） |
| 同窗 siblings | 供应侧：调用总量/占比/区域（supplierColumns）；渠道侧：归集数据量/贡献度/业务类型（channelColumns） |
| 跨族近件 | 063（资源总数——总量正面件，渠道侧同源）；036（表级口径）；066/067（类型数/总量——计数组连坐）；057（调用频率——同 seq 388-389 调用语境） |
| UI 容器 | supplierColumns 表 + 部门归集卡 + channelColumns/groupColumns 表（§1.1） |

本件是 S3-05 资源计数组的**分组侧件**：与 063（总量）是「Σ vs GROUP BY」的同根对——目录立项（含归属字段）则两件双升；比 063 更紧一档的是表级近似在 063 可交付总量、在本件连分组也不可得（归属缺位）。渠道侧挂载与 063 共享 channels 数据源——两件同判部分支持、共享升档触发器①。

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

本件读数「数据资源条数」是一名两挂的分组计数，B10 并列登记三个口径：**口径 A（供应侧面·正式）**——`COUNT(*) GROUP BY supplier`（含 department/region 上卷）；**口径 B（渠道侧面·正式）**——`GROUP BY channel`（与 063 同源）；两正式口径均因归属×资源登记面缺位（§2.2）**不可得**，指标键 `data_resource_count_by_supplier` / `data_resource_count_by_channel` 双 null 留空。**口径 C（表级近似·仅总量）**——若裁定资源≈表，全库总量 ≈ **930**（剔备份，derived `data_resource_count_table_approximation_no_backup`）；归属字段缺位致**分组近似不可得**——口径 C 只给 Σ 不给 GROUP BY。

### 2.2 排除实测：归属词族三源逐一留证

判「无承载」前的三源探针（本件供应方词族为 064 新增实跑 + resource 词族复用 063，B8）：**dev** 542 表 supplier/provider/vendor/supply 词族唯一命中 `gkxlumenx_dwd.enterprise_supply_chain`（`facts.three_source.dev_supplier_hits`）——DESC 实查 9 列（org_id/related_org_id/relation_type/is_core_supplier 等）**0 行**——企业供应链关系图谱空表（is_core_supplier 是机构间供应链关系标记非数据供应方×资源登记），语义排除；**gkx** 280 表双词族（供应方+资源目录）唯一命中 `dwd_dim_source_code`（`facts.three_source.gkx_dual_family_hits`）——063 件 DESC 语义排除复用（`facts.three_source.resource_family_exclusion_ref`）；**久新** live 215 张（`facts.three_source.jiuxin_table_total`）供应方词族 0 命中（`jiuxin_supplier_hits=[]`）、resource 词族 7 张语义排除（`jiuxin_resource_hits_count=7`，承 063）。三源结论：归属×资源登记面 0（语义级）。

### 2.3 表级近似与 mock 双面读数落盘

口径 C 读数复用 036 件（`facts.table_level_approximation_from_036`）：全口径 1,032 / 剔备份 **930**（探测日注记同 063）——仅全库 Σ，供应商/渠道分组维不可得。mock 双面正则实算：**供应侧面** `supplierStats` 五行 resourceCount 156/89/67/45/34（`facts.ui.supplier_side.mock_rows=5`），Σ=**391**（`mock_resource_count_sum`，share 合计 `mock_share_sum_pct=100.0` 同基自洽）；区域归集面华北 279/华南 112（`mock_region_groups`），Σ=**391**（`mock_region_group_sum`）；部门嵌套六行 Σ=**391**（`mock_dept_nested_sum`）——**三层自洽**（供应方行→区域组→部门嵌套逐值对账一致）。**渠道侧面** `channels` Σ=**1,256**（`facts.ui.channel_side.mock_count_sum`，与 063 同源）；分组聚合面明细基座 12 行（`facts.ui.grouped_detail_rows`）。

### 2.4 双面断裂核对（同基与量纲核对）

**同库双面 865 差**：供应侧 391 vs 渠道侧 1,256（`facts.ui.cross_side_gap=865`）——同一演示库、同一「资源」一词，两口径层互不对账（供应侧三层内部 391 逐值一致、渠道侧 share 100.0% 自洽——两套手写数据各自圆融）。量纲注记（B9）：供应侧「项资源」/渠道侧「个」双单位形态并存；`mock_srs_anchor` 双语境键（seq 388 供应侧 / seq 351 渠道侧）登记两侧的需求锚——正式版须先统一资源归属维度（§1.6）再谈分组计数。

### 2.5 稳健性与口径敏感性

三点敏感性：其一，**归属四轴关系**——supplier/department/region/channel 四轴是否同一登记面的视图（渠道=供应方的类型上卷？中科院→科研院所？）无登记，双面 865 差即轴错位的实证；其二，**表级近似的分组盲区**——930/1,032 只有 Σ，任何分组尝试都因归属字段缺位而不可复现（比 063 更紧一档）；其三，**mock 三层自洽的误导性**——供应侧内部三层逐值一致是「同一份手写数据的三次上卷」，不能作为台账存在的旁证。

### 2.6 需求符合性预评

seq 388 部门归集展示的「资源数」列——**不满足**（供应方×资源登记面无承载）；seq 351 渠道条数列——不满足（同 063）；「全库资源总量」——部分满足（表级近似 930 可挂，分组维须空态）。预评与触发器对齐：目录立项（含归属四字段）则本件与 063 双升。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_DATATHM_064.py`（供应方词族三源新探针 + 063/036 复用 + 三块 mock 正则实算；零 `demo_*`）；运行 `python3 code/M_SCIUI_DATATHM_064.py`。
- 产物：`code/M_SCIUI_DATATHM_064_out.json`。正文数字与产物键逐一对应：`three_source.dev_supplier_hits`（1 张空表语义排除，§2.2）、`three_source.gkx_dual_family_hits`（承 063，§2.2）、`ui.supplier_side.mock_resource_count_sum=391` / `mock_region_group_sum=391` / `mock_dept_nested_sum=391` / `mock_share_sum_pct=100.0`（§2.3）、`ui.channel_side.mock_count_sum=1256`（§2.3）、`ui.cross_side_gap=865`（§2.4）、derived `data_resource_count_by_supplier=null` / `by_channel=null` + `table_approximation_no_backup=930`（B10，§2.1）。
- 结果解读：归属词族三源排除 + 表级近似仅总量 + mock 三层自洽与双面断裂并证——「分组口径不可算、总量近似可交付」。
- 对照需求功能要求的评审：供应方/渠道分组列——不满足；全库总量——部分满足（§2.6 预评）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 排除 | dev 供应方词族 | `three_source.dev_supplier_hits` | [enterprise_supply_chain]（0 行空表排除） |
| 排除 | gkx 双词族 | `three_source.gkx_dual_family_hits` | [dwd_dim_source_code]（承 063 排除） |
| 排除 | 久新供应方/resource | `jiuxin_supplier_hits` / `jiuxin_resource_hits_count` | [] / 7 张（排除） |
| 近似 | 表级总量（剔备份） | derived `data_resource_count_table_approximation_no_backup` | 930（仅 Σ 无分组） |
| mock | 供应侧 Σ | `ui.supplier_side.mock_resource_count_sum` | 391（share 100.0%） |
| mock | 区域/部门上卷 | `mock_region_group_sum` / `mock_dept_nested_sum` | 391 / 391（三层自洽） |
| mock | 渠道侧 Σ | `ui.channel_side.mock_count_sum` | 1,256 |
| mock | 双面差额 | `ui.cross_side_gap` | 865（轴错位实证） |
| 指标 | 正式口径（双侧） | `data_resource_count_by_supplier` / `by_channel` | null（B10 双键） |

九行对照中，三键同值 391（供应侧三层）与差额 865 并列是全件最重要的结构证据：mock 内部上卷链完整而跨面对账断裂——正式版须先裁归属四轴关系；表级近似 930 只有总量骨架，分组读数等待目录归属字段（§1.6 触发器①）。


## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 含归属字段的资源目录（supplier/channel/department/region） | 三源 | — | — | **不存在** | **缺（分组口径判定性）** |
| D2 | 表级近似：三源表清单+归属映射 | 三源 | information_schema/SHOW TABLES + 归属字段 | 1,032 张（清单有/归属无） | 半 | 近似仅总量（分组阻断） |
| D3 | 最近邻：dev `enterprise_supply_chain` | dev | org_id/related_org_id/is_core_supplier | 0 行 | 直查 | **语义排除**（供应链关系空表） |
| D4 | resource 词族（063 复用） | 三源 | dwd_dim_source_code 等 | — | 排除承 063 | 语义排除（复用） |
| D5 | UI 演示值 | UI | mock supplierStats/RegionGroups/channels | 三块 | mock | 边界证据（不作源） |

`support_judgment="部分支持"`、产物与文首一致（闸 6）。

### 3.2 D5 mock 侧证据（同库双面 865 差——本件核心披露）

mock 供应侧面三块解析（正则实算）：`supplierStats` 五行 resourceCount 156/89/67/45/34——**Σ=391**，share 43.8/23.8/16.0/10.9/5.5 合计 100.0%；`supplierRegionGroups` 华北 279（=156+89+34）/华南 112（=67+45）——**Σ=391**；departments 嵌套六行逐供应方——**Σ=391**。**三层自洽**：供应方行 → 区域组 → 部门嵌套逐值对账一致（mock 作者在供应侧面内部做了完整的层级上卷）。**双面断裂实证**：渠道侧面 `channels` 五渠道 Σ count = **1,256**（与 063 同源）——同一演示库、同一「资源」一词，供应侧 391 vs 渠道侧 1,256，**差 865 无解释**（两套手写数据各自圆融：供应侧三层 391 一致、渠道侧 share 100.0% 自洽，但互不对账）。这说明演示作者从未把「供应方的资源」与「渠道的资源」当作同一登记面——正式版若照此双轨实现，资源台账将分裂。**披露**：391/1,256 均不作资源条数原料（B10）；「调用总量 2,856,000」（Σ totalCalls，与 056 累计调用 285.6 万次同值——mock 全局复用）是调用维勿混。

### 3.3 D1 的 absence_probe 全记录（含三处语义排除专段）

否定性证据三件套：**查了什么**——①dev 542 表 supplier/provider/vendor/supply 词族（2026-11-02 information_schema 实跑正则：唯一命中 `gkxlumenx_dwd.enterprise_supply_chain`——DESC 实查 9 列 org_id/related_org_id/relation_type/relation_strength/is_core_supplier/risk_level/create_time/update_time 等、**0 行**——企业供应链关系图谱空表，is_core_supplier 是机构间供应链关系的「核心供应商」标记，主体是机构关系非「数据供应方×资源」登记，**语义排除**；资源目录词族 resource/catalog/inventory/metadata/registry 0 命中承 063 件）；②gkx 280 表双词族（供应方 + resource/catalog/collect/inventory/registry + source_code，经 `_gkxdb.py` 实跑：唯一命中 `dwd_dim_source_code`——数据来源编码维度表 4 行，063 件 DESC 实查语义排除——供应方×资源双缺）；③久新 live 215 张（2026-11-02 实跑，漂移承 063 件登记）supplier/provider/vendor/supply 词族 **0 命中**；resource 词族 7 张全为论文计量年表（063 件语义排除复用）；④三份需求真源（「数据资源条数/资源数」0 命中——列名级读数；seq 388/351 双语境锚在）。**条件**——表级存在性+语义核对（三处最近邻过语义关）。**命中**——0（语义级）。四缺失情形归属：D1 属「**表不存在**」（含归属字段的资源目录三源均无——修复动作是资产目录立项，与 063/066/067/056 共享，本件追加要求：目录 schema 须含 supplier/channel/department/region 归属字段）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| dev 供应方词族 | 1 张语义排除（enterprise_supply_chain 空表，DESC 实查） |
| gkx 双词族 | 1 张语义排除（dwd_dim_source_code 承 063） |
| 久新供应方词族 | 215 张 0 命中；resource 7 张语义排除（承 063） |
| 表级近似 | 1,032/剔备份 930（036 复用，B8）——归属缺位仅总量 |
| UI 挂载 | 三处：:214（supplierColumns）/:238（channelColumns）/:317（groupColumns）+ :491 区域组 |
| mock 双面 | 供应侧三层 391 逐值一致 vs 渠道侧 1,256——差 865 |
| 脚本形态 | 三源实跑（供应方新探针）+ 063/036 复用 + 三块 mock 正则实算；零 demo_* |

## 四、数据缺失情况

### 4.1 含归属字段的资源目录零承载（结构级，分组口径判定性缺口）

供应方/渠道×资源登记面三源零承载（§3.3）——dev 最近邻是供应链空表，gkx 最近邻是来源编码维度表，久新 0 命中。**本件的连坐面**：计数组五件（056/063/064/066/067）共享资源目录缺位，其中本件与 063 是最近邻（Σ vs GROUP BY）——但本件要求更强：目录**必须含归属字段**（063 只要求条目存在）。**四缺失情形归属「表不存在」**：修复动作是资产目录立项且 schema 含归属四字段（supplier/channel/department/region——mock supplierStats 的字段清单可直接作底稿：name/department/resourceCount/share/region 五元组，即目录行的归属+计数控件投影）。

### 4.2 归属维度轴与双面台账未裁（口径级）

本件降档的口径层根因：**归属四轴关系无定义**——mock 供应侧面 supplier 带 department+region 双字段（一供应方一部门一区域，无多对多），渠道侧面 channel 是另一轴（科研院所/企业/第三方平台/高等院校/政府部门——主体类型语义 vs 供应侧的具体机构语义），两轴是否同一登记面的两个视图（渠道=供应方的类型上卷？中科院→科研院所？）无登记；**双面 865 差**（391 vs 1,256）在 mock 内也无解释。正式版须裁定：①归属维度轴清单与层级（supplier→department→region 上卷 + channel 独立轴还是类型轴）；②资源语义边界（承 063）；③双台账统一规则（供应方口径与渠道口径的对账键）。此裁定与目录立项解耦，可先行。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 资源目录立项（含归属四字段） | 数据工程立项 | 本件 + 063/066/067/056 | 触发器①（supplierStats 五元组可作 schema 底稿） |
| 归属维度轴裁定（四轴关系+对账键） | 口径裁定 | 本件 | 双面 865 差实证在前，可先行 |
| 表级映射+归属补登 | 数据工程配套 | 本件 + 036/063 | 触发器②（分组近似转正） |
| UI 双侧列改挂或空态 | 展示规范 | 本件 UI | 391/1,256 演示值建议撤下 |

档位后果：目录（含归属）→ **完全直接支持**（GROUP BY 直查）；表级+归属 → **完全转换支持**；现状 → 部分支持。推荐顺序：归属轴裁定（即期一纸）→ 目录立项（含四字段）→ 归属补登。

## 参考文献

1. DAMA International. DAMA-DMBOK: Data Management Body of Knowledge[M]. 2nd ed. Technics Publications. https://www.dama.org/cp/body-of-knowledge （R1，2026-11-02 WebSearch 核验可达——资产目录按来源域/steward 分组计数是治理报表标准列，归属字段是分组前提）
2. 阿里云开发者社区. Dataphin功能Tips系列（10）-质量分计算口径[EB/OL]. https://developer.aliyun.com/article/1480319 （R2，2026-11-02 WebSearch 核验可达——资产按项目/数据源分组归集的元数据采集口径，归属登记随采集落地）
3. GB/T 33850-2017 信息技术服务 质量评价指标体系[EB/OL]. 国家标准全文公开系统. https://openstd.samr.gov.cn/bzgk/std/index （R3，2026-11-02 WebSearch 核验可达——分类统计以登记台账类目字段为准，分组维度先行登记的国标锚）

# 附件

## 附录 A 原始需求原文摘录

**「数据资源条数/资源数」字面三份说明书未出现**（检索记录见 A.2）。双语境原文：

SRS `bid-reference/srs/02-科技信息展示系统/科技数据资源/应用视窗.md` seq 388（部门名称自动归集展示）：

> ### 部门名称自动归集展示 · 序号 388
> #### 需规功能描述
> 对所有供应方进行智能归类，对调用数据的部门归属自动识别和展示，帮助管理者快速定位数据供应源，清晰呈现各部门在数据提供上的角色和分工。

SRS `bid-reference/srs/02-科技信息展示系统/科技数据资源/接入视窗.md` seq 351（渠道归集数据量统计）：

> ### 渠道归集数据量统计 · 序号 351
> #### 需规功能描述
> 自动统计并展示各渠道（如科研院所、企业、第三方平台）归集的数据量，支持按时间、业务类型、来源类别进行细分，帮助用户全面了解不同渠道的数据贡献度。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 数据资源条数/资源数 | 主需求/核增/算法库 + SRS 分册 | 0（列名级读数） |
| 部门名称自动归集展示（供应侧锚） | SRS 应用视窗 | seq 388 |
| 渠道归集数据量统计（渠道侧锚） | SRS 接入视窗 | seq 351 |
| resourceCount | mockData.js | :910-914（supplierStats 五行）+ :918-941（RegionGroups） |
| 资源数 | ApplicationWindow.jsx | :214（supplierColumns）+ :491（区域组） |
| 资源数 | AccessSourceAnalysisDetail.jsx | :238（channelColumns）+ :317（groupColumns） |

## 附录 B 历史库表探测证据

### B.1 探针与快照

- 本件产物：`code/M_SCIUI_DATATHM_064_out.json`（2026-11-02 实跑：供应方词族三源新探针 + resource 词族排除复用 063 + 036 计数复用 + 双面 mock 实算）。
- 共享探针：`code/_snapshots/_lane7_shared_probe_out.json`（三源表数 B11 锚）；`M_SCIUI_DATATHM_036_out.json`（表级计数先例）；`M_SCIUI_DATATHM_063_out.json`（resource 词族三源排除+DESC 语义核对——本件复用，B8）。
- 族内对账：dev 542/gkx 280 与 lane7/036 逐键一致；久新 210→215 漂移承 063 件登记；mock 三层 391 逐值对账一致。

### B.2 本件产物逐键清单（`code/M_SCIUI_DATATHM_064_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.ui.supplier_side.mock_resource_count_sum` | 实算 | 391（Σ supplierStats） | §3.2 |
| `facts.ui.supplier_side.mock_share_sum_pct` | 实算 | 100.0 | §3.2 |
| `facts.ui.supplier_side.mock_region_groups` | 实算 | 华北 279/华南 112 | §3.2 |
| `facts.ui.supplier_side.mock_region_group_sum` | 实算 | 391（三层一致） | §3.2 |
| `facts.ui.supplier_side.mock_dept_nested_sum` | 实算 | 391 | §3.2 |
| `facts.ui.channel_side.mock_count_sum` | 实算 | 1,256（与 063 同源） | §3.2 |
| `facts.ui.cross_side_gap` | 实算 | 865（双面断裂差额） | §3.2 |
| `facts.three_source.dev_supplier_hits` | 探针 | ['gkxlumenx_dwd.enterprise_supply_chain']（空表语义排除） | §3.3 |
| `facts.three_source.gkx_dual_family_hits` | 探针 | ['dwd_dim_source_code']（承 063 排除） | §3.3 |
| `facts.three_source.jiuxin_supplier_hits` | 探针 | []（0 命中） | §3.3 |
| `facts.table_level_approximation_from_036.three_source_all` | 计数 | 1,032（036 复用） | §3.1 |
| `derived[0/1].data_resource_count_by_supplier/by_channel` | 负结论 | null（B10 双键） | §1.6/§二 |
| `derived[2].data_resource_count_table_approximation_no_backup` | 近似 | 930（仅总量） | §3.1 |
| `absence_probe` | 探针 | 三件（dev/gkx/jiuxin） | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 原料 | 计数机制 | 贴合度 |
|---|---|---|---|---|
| 目录分组计数 | R1（DAMA-DMBOK） | 目录+归属字段 | GROUP BY source | 高（正式口径锚） |
| 元数据采集归属 | R2（Dataphin） | 元数据+归属登记 | 采集附带 | 中（表级近似但归属缺位） |
| 台账分类统计 | R3（GB/T 33850） | 台账+类目 | GROUP BY 类目 | 高（分组维度先行） |
| 前端演示 | mock 常量 | — | 手写两套（391/1,256） | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 含归属字段的资源目录 | 无（1 张供应链空表语义排除） | 无（1 张维度表语义排除） | 无（0+7 张语义排除） |
| 表级表清单 | 有（542） | 有（280） | 有（215 实跑/210 快照） |
| 归属字段/映射 | 无 | 无 | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 分组口径无可交付；表级近似仅总量（930/1,032） | — |
| v1 | 归属维度轴裁定（四轴关系+对账键一纸） | 口径裁定先行 |
| v2 | 资源目录立项（含归属四字段）→ GROUP BY 直查 | 触发器①（063/064 双升） |
| v3 | 表级映射+归属补登 → 分组近似转正 | 触发器② |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| mock 391/1,256 被当真实分组读数 | **高** | §3.2 双面断裂实证 + B10 禁用注记 |
| 双台账分轨（供应方/渠道永不对账） | **高** | §4.2 对账键裁定先行 |
| 表级总量误当分组值（归属缺位遗忘） | 中 | derived[2] 注记「仅全库总量」 |

### C.5 总判

**部分支持**：含归属字段的资源目录三源零承载（分组口径不可交付——比 063 更紧一档：表级近似连分组也不可得）；mock 同库双面 865 差（391 vs 1,256）+ 供应侧三层自洽是本件核心披露。目录立项（含归属四字段）是与 063 共享的触发器①，归属轴裁定是本件独有前置——修复顺序：裁定 → 目录 → 补登。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_DATATHM_064.py` | 退出码 0，落 `_out.json` |
| 数据入口 | 三源实跑（供应方新探针）+ 063/036/lane7 复用 + 三块 mock 正则实算 | 供应方词族首次登记 |
| 判档一致 | 文首 vs `support_judgment` | 部分支持 |
| B11 对账 | dev 542/gkx 280 零漂移；久新漂移承 063；mock 三层 391 一致 | 对账键在产物 |
| mock 对账复核 | Σ supplierStats=391=Σ RegionGroups=Σ dept 嵌套；Σ channels=1,256；差 865 | 断裂差额在产物 |
| 幂等重跑 | 探针确定性 + 正则确定性 | 逐位一致（活库表数带 asof 注记） |
| 伪指标值残留 | `data_resource_count_by_supplier/by_channel` | null（无伪值） |
| §二 从缺 | 指标本体（分组口径） | 无伪公式（F4） |

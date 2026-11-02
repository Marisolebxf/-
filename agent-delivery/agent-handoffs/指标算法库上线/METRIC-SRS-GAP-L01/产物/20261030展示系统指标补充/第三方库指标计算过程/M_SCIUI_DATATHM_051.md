# 接入渠道数量（M_SCIUI_DATATHM_051）

> **类型**：无业务逻辑数值类（渠道维度的资源登记面三源缺位——基数无分母面；UI 双套渠道词混用是口径级前置缺口）｜ **域**：科技信息展示系统·科技数据资源·接入视窗·资源来源分析和详情「渠道数」Statistic（挂靠 seq 361/363 渠道维度族）｜ **UI 挂载**：`components/AccessSourceAnalysisDetail.jsx:363`（`Statistic title="渠道数" value={channels.length} suffix="类"`）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（指标名级三份真源 0 命中；「渠道数」为 UI Statistic 题名；渠道 taxonomy 无定义——UI 自身两套渠道词混用）｜ **口径归属**：UI 派生读数（挂靠 seq 361/363），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_DATATHM_051.py`｜ **产物**：`code/M_SCIUI_DATATHM_051_out.json`
> **四判定摘要**：直接结构 = 无（dev channel 词族 16 列全业务语义——支付/导出/反馈；gkx 来源标签三面空）；直接数据 = 无（同左）；依赖结构 = 无（资源×渠道归属列不存在）；依赖数据 = 无（基数无分母面）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev`）逐一探针留证；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 语义是「接入渠道的分类基数」（DISTINCT 渠道数）——一个看似最简单的计数指标，但其分母面（资源×渠道归属登记）三源缺位，且**渠道 taxonomy 本身在前端就是两套混用词**：本挂载所在卡「资源来源分析」的 mock 渠道=**来源机构分类**（科研院所/企业/第三方平台/高等院校/政府部门，`accessSourceAnalysis.channels`），而 019/044/053 挂载的 mock 渠道=**传输方式**（API接口/文件传输/数据库同步/人工录入/物联网采集，`updateCycleStats`/`accessChannelStats`）——同一前端两套五类互斥词。三源逐一排除：**dev** 本件新探针——全库列级 channel 词族命中 **16 列**逐条语义核对**全为业务字段**（`gkxlumenx_pay` 支付渠道 13 列：pay_channel/pay_trade_order/pay_refund_order 的 channel_id/mch_id/order_no 族；`jimu_report_export_log.export_channel` 报表导出通道（值分布单值 script/118 行）；`policy_public_opinion.feedback_channel` 反馈渠道；`policy_subscription.push_channels` 推送通道）——**无一列登记「资源经哪个渠道接入」**；**gkx** 来源标签三面全空（scholar 单值/patent NULL 100%/zh_paper 空 100%——lane3 复用，048 同锚）；**久新** 215 表快照单期无资源×渠道登记。判完全不支持。`access_channel_count = null`（B10）。

### 批次通用纪律摘要（S3-05 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 本件无比值；mock 合计 33,670/1,256 为同源求和 |
| B4 | 负结论带探针 | 四件 absence_probe（dev/gkx/jiuxin/doc，§3.3）+16 列逐条语义排除+值分布佐证 |
| B5 | 确定性 | 列扫描 information_schema 自然序；mock 五渠道按 volume 降序（=原序）；值分布按 c DESC |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 本件 py 已跑出 _out.json；产物零手改 |
| B8 | 回执不复收 | lane3/042 快照复用不重跑 |
| B9 | 单位/日期陷阱 | 「类」单位；两套渠道词分叉披露（来源机构 vs 传输方式） |
| B10 | 口径裁定保守交付 | 正式口径 null；taxonomy 裁定列为前置；触发器写死 |
| B11 | 多本账互推 | gkx 来源标签=lane3（048 同锚）；词族=042；mock 五渠道=042 首段同款 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 资源×渠道归属有登记列吗？ | 无 | dev 16 列全业务语义（§3.3） |
| gkx/久新有渠道面吗？ | 无 | 标签三面空/快照无登记（§3.3） |
| 渠道 taxonomy 有定义吗？ | 无（两套混用） | 来源机构五类 vs 传输方式五类（§3.4） |

## 摘要

「接入渠道数量」挂在资源来源分析和详情卡的汇总行：`AccessSourceAnalysisDetail.jsx:363` Statistic「渠道数」（value=channels.length 动态计数，mock=5 类）。mock 五渠道（`mockData.js:100-106`）：科研院所（12,580/485/38.6%）、企业（8,920/356/28.3%）、第三方平台（6,240/245/19.5%）、高等院校（4,120/120/9.6%）、政府部门（1,810/50/4.0%）——归集总量 33,670、资源总数 1,256。数据侧：渠道基数的前提是「资源挂渠道」的登记面——dev channel 词族 16 列全业务语义（支付渠道 13+导出/反馈/推送通道 3）、gkx 来源标签三面全空、久新快照无登记，三源零承载。且口径级前置缺口：前端两套渠道词混用（本卡=来源机构分类；019/044/053 卡=传输方式）——「渠道数」连数什么都没定义。判**完全不支持**。脚本已跑通，产物与正文数字逐一对应。

- 需求判定：**UI 派生读数**（挂靠 seq 361/363；题名在、taxonomy 无）。
- 复现状态：脚本已跑通；channel 列级新探针（16 列+值分布）+ lane3/042 复用落产物。
- 档位结论：**完全不支持**（登记面缺位+taxonomy 未裁定双缺口）。
- 关键事实：16 列 channel 里 13 列是支付系统（pay_channel 族）——「渠道」一词在库内最强存在感是支付渠道；「资源从哪来」的接入渠道反而零登记。这与 048（来源机构标签全空）同病同根：供给侧元数据登记整体缺位。
- 升档路径：渠道 taxonomy 裁定（两套词二选一或并存分列）+资源登记面加渠道列 → 完全直接支持（与 048 共享标签登记触发器）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技数据资源/接入视窗·资源来源分析和详情（L6 段，挂靠 seq 361/363 渠道维度族）。UI 实际挂载（派单 mount 行 363，实查确认）：`AccessSourceAnalysisDetail.jsx:363` `<Statistic title="渠道数" value={channels.length} suffix="类" />`——渠道归集数据量统计卡汇总行三 Statistic 之首（:364 归集总量/:366 资源总数）；数据源 `accessSourceAnalysis.channels`（`:30` 解构）。mock 语义源 `mockData.js:99-106`：五渠道 name/volume/count/share/color/bizTypes。mock 结构披露：五类=来源机构分类（与 042 首段「五类来源结构」同款 mock——`overviewSourceAnalysis.sourceTypes` 的国内数据库/开源平台等是另一套六类词，前端实际三套来源词）；动态计数（channels.length）使 Statistic 随 mock 数组长度自动变化——纯演示联动。

### 1.2 为什么需要本指标

渠道数量是接入供给结构的**基数读数**：与渠道归集量分布（同卡 byTime/byBizType 维度）构成「多少类渠道、各类多少量」的结构视图；基数变化（新渠道接入/渠道下线）是供给侧治理的信号。权威对应物：数据目录的 distribution/endpoint 类型计数（DCAT——获取渠道形态）；ETL 的 source system 计数（数据仓库来源系统登记——标准建模维度）；供应链的供应商分级计数（SRM）。

### 1.3 需求文档是否给出定义方法

**指标名级三份真源 0 命中。**SRS 接入视窗的渠道相关功能句多见（seq 361「各渠道、数据表的历史更新周期」/363 渠道对比功能段）——「按渠道」作为**分析维度词**在，但「渠道数量」作为**基数指标**无定义；更关键的是渠道 taxonomy 无定义（渠道=来源机构？传输方式？数据类型？——前端三套词并存：来源机构五类/传输方式五类/来源六类）。核增需求与算法库 0 命中（附录 A.2）。

### 1.4 类似指标权威方法可行性分析概要

「渠道数量」的权威方法锚分三层。其一，数据目录（R2，DCAT）：`dcat:Distribution` 按 accessService/endpointType 分组计数——获取渠道的标准建模；其二，数据仓库建模（R1，Kimball 维度建模）：source system 维度表（数据来源系统登记）——`COUNT(DISTINCT source_system)`，ETL 侧标准做法；其三，API 管理（R3，Kong/APISIX）：route/service/upstream 分组计数——接入端点形态。方法族对照：

| 方法族 | 代表 | 原料 | 与三源匹配 |
|---|---|---|---|
| 目录 endpoint 类型 | R2（DCAT） | distribution 元数据 | **无登记**（16 列排除） |
| 来源系统维度 | R1（Kimball） | source_system 维表 | **无维表**（标签三面空） |
| API 端点分组 | R3（网关） | route/service | 无网关面（调用族同锚） |
| 前端演示 | UI mock | 五类常量 | 三套词混用（不作源） |

结论：计数指标的分母面（资源挂渠道的登记）在三源全面缺位——与 048 同根（供给侧元数据登记缺位家族）。完整版见附录 C。

### 1.5 引用来源

- 组件：`AccessSourceAnalysisDetail.jsx:363`（Statistic）、`:30`（channels 解构）；mock 语义源 `mockData.js:99-106`。
- 需求：SRS 接入视窗.md seq 361/363（渠道维度功能段）。
- 权威方法：R1 Kimball & Ross. The Data Warehouse Toolkit（维度建模 source system）；R2 W3C DCAT 2（w3.org）；R3 Kong Gateway（konghq.com）。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（须披露 taxonomy 未裁定）**：按来源系统维度建模推测

$$C = |\{\text{distinct } c : c = \text{channel}(r),\ r \in \text{资源登记面}\}|$$

即资源登记面上渠道字段的去重基数。**前提有二：taxonomy 裁定（渠道分哪几类）+资源×渠道登记面，三源实测双双缺席**（§3.3）——前端三套词（来源机构/传输方式/来源六类）说明 taxonomy 连演示层都未统一。公式列示仅作口径锚（F4：本件 §二 从缺）。

**降档/升档触发器（B10 模板）**：①taxonomy 裁定（一纸文件，建议双轴并存：来源机构轴+传输方式轴分列）+资源登记面加渠道双列 → 升**完全直接支持**（COUNT DISTINCT 即得）；②无登记面但按 es_sync 模块名近似（15 模块——模块≠渠道，语义分叉登记）→ 至多**部分支持**；③维持现状 → 完全不支持（Statistic 显示 0 或「—」）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技数据资源/接入视窗.md` |
| 所属 L5 | 资源来源分析和详情（L6 段；挂靠 seq 361/363 渠道维度族） |
| 本件 | **UI 派生读数**（Statistic 动态计数） |
| 同卡并列 | 归集总量（:364）/资源总数（:366）——同 mock 求和位 |
| 跨族近件 | 048（来源机构标签——同根：供给侧登记缺位）；019/044（传输方式渠道族）；042（五类来源结构同款 mock） |
| UI 容器 | `AccessSourceAnalysisDetail.jsx:352-368` |

本件与 048 构成**供给侧登记缺位双件**：048 要「来源机构标签」（活跃度聚合轴）、051 要「渠道归属列」（基数分母轴）——同一根因（资源登记环节无来源/渠道标注）的两个下游。与 019/044/053 的传输方式渠道族是**同名异轴**： taxonomy 裁定时须双轴分列（来源机构轴挂 048/051、传输方式轴挂 019/044/053），否则五类+五类会混成十类假分类。

## 二、计算过程

从缺（分母面（资源×渠道登记）三源缺位+taxonomy 未裁定，见 §3.3。按 F4 纪律不写伪计算过程；mock 计数联动与求和核验进 §三/附录 B）。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 资源×渠道归属列 | dev | channel 词族 16 列 | 16 列 | 语义排除 | **缺（判定性）** |
| D2 | 渠道/来源标签面 | gkx | dwd_* 来源列 | 三面全空（lane3） | 语义缺位 | **缺（判定性）** |
| D3 | 资源渠道登记 | jiuxin | ads_* | 快照单期 | 无登记 | 缺 |
| D4 | 渠道 taxonomy | — | —（需求无/前端三套词） | — | **不存在** | 缺（口径前置） |
| D5 | UI 演示值 | UI | mock 五渠道 | 5 类 | mock | 边界证据 |

`support_judgment="完全不支持"`、产物与文首一致（闸 6）。

### 3.2 dev 16 列逐类排除与值分布佐证

本件新探针①：channel 词族 16 列（`dev_channel_column_scan`）逐条排除——**支付渠道 13 列**（`gkxlumenx_pay.pay_channel` channel_id/name/mch_id 3 列+`pay_trade_order` channel_id/mch_id/order_no 3 列+`pay_refund_order` channel_id/mch_id/user/order_no/err_code/err_msg 7 列：支付系统自身的渠道商户体系）、**报表导出通道 1 列**（`gkxlumenx_bi.jimu_report_export_log.export_channel`——新探针②值分布实测**单值 `script`/118 行**：报表脚本导出，非数据接入）、**反馈渠道 1 列**（`policy_public_opinion.feedback_channel`——舆情反馈途径）、**推送通道 1 列**（`policy_subscription.push_channels`——订阅推送）——**无一列回答「资源经哪个渠道接入」**。16 列里支付占 13 列：「渠道」在库内最强存在感是支付渠道，接入渠道零登记。

### 3.3 absence_probe 全记录

否定性证据三件套：**查了什么**——①dev 列级 channel 词族 16 列+值分布（§3.2）——资源渠道归属列不存在；②gkx 来源标签三面（lane3 复用，048 同锚）：dwd_scholar 全量单值 gkx_ods/dwd_patent 采样 NULL 100%/dwd_zh_paper 空 100%——供应商库无渠道标注；③久新 215 表快照单期（as_of 2026-09-18）无资源×渠道登记；④需求真源指标名 0 命中（「按渠道」维度词多见、「渠道数量」基数指标无；taxonomy 无定义——前端三套词并存证据在案）。**条件**——列级+标签级+口径级三层核对。**命中**——0。四缺失情形归属：D1「**结构不存在**」（列不存在）；D2「**结构在但语义缺位**」（来源列在但全空）；D4「**口径缺位**」（taxonomy 未裁定）。

### 3.4 UI 三套渠道词并存（口径混乱证据）

前端 mock 渠道词实测三套互斥：①**来源机构五类**（本卡 `accessSourceAnalysis.channels`：科研院所/企业/第三方平台/高等院校/政府部门）；②**传输方式五类**（`updateCycleStats`/`accessChannelStats`：API接口/文件传输/数据库同步/人工录入/物联网采集——019/044/053 挂载）；③**来源六类**（`overviewSourceAnalysis.sourceTypes`：国内数据库/国外数据库/开源平台/科研院所/企业——042/053 挂载）。三套词各自五/五/六类，两两重叠不完全（「科研院所」「企业」在①③都出现但分类体系不同）——「渠道数」按①是 5、按②是 5、按③是 5（六类 mock 实给 5），演示层自身未统一。mock 求和核验（B1）：归集总量 33,670（`ui_mock_volume_total`）、资源总数 1,256（`ui_mock_count_total`）——与 :364/:366 Statistic 联动值一致。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| channel 词族 | 16 列（支付 13/导出 1/反馈 1/推送 1） |
| export_channel 值 | 单值 script/118 行（业务语义佐证） |
| gkx 标签 | 三面全空（lane3 复用，048 同锚） |
| 久新登记 | 快照单期无渠道面 |
| mock 三套词 | 来源机构 5/传输方式 5/来源 6（并存披露） |
| mock 求和 | 33,670/1,256（与 Statistic 联动一致） |
| 脚本形态 | 列级+值分布新探针；幂等重跑逐位一致 |

## 四、数据缺失情况

### 4.1 资源×渠道登记面缺位（结构级，与 048 同根）

基数指标的分母面（资源挂渠道）三源缺位（§3.2/3.3）。**四缺失情形归属「结构不存在」**：修复动作与 048 共享——资源登记环节加渠道双列（来源机构轴+传输方式轴，taxonomy 裁定后落地）；历史数据按供库合同回填（与 048 的标签回填同一工程）。

### 4.2 渠道 taxonomy 缺位（口径级，最前置）

「渠道」在三套前端词里三义（§3.4）。建议裁定**双轴并存**：①来源机构轴（科研院所/高等院校/企业/政府部门/第三方平台——挂 048/051）；②传输方式轴（API/文件传输/DB 同步/物联网/人工录入——挂 019/044/053）——两轴独立登记独立计数，UI 按挂载位取轴。一纸 taxonomy 文件先行，登记列随轴落。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 渠道 taxonomy 双轴裁定 | 口径裁定 | 本件 + 048 + 019/044/053 | 一纸文件（最前置） |
| 资源登记面加渠道双列 | 数据工程 | 本件 + 048 | 触发器①（供给侧登记族共用） |
| 存量渠道回填（合同溯源） | 数据工程 | 本件 + 048 | 与 048 标签回填同工程 |
| Statistic 暂无数据态 | 展示规范 | 本件 | mock 5 替换 |

档位后果：taxonomy+登记列 → **完全直接支持**（COUNT DISTINCT）；es_sync 模块近似（15）→ 至多**部分支持**（模块≠渠道）；现状 → 完全不支持。推荐：taxonomy 即期（一纸文件解锁全族口径），登记列随供给侧主线。

## 参考文献

1. Kimball R, Ross M. The Data Warehouse Toolkit 3rd ed — source system 维度建模[M]. Wiley. 中英文版公开书录见 Wiley. https://www.wiley.com/en-us/The+Data+Warehouse+Toolkit%3A+The+Definitive+Guide+to+Dimensional+Modeling%2C+3rd+Edition-p-9781118530801 （R1，2026-11-01 WebSearch 核验可达——来源系统维表与 COUNT DISTINCT 基数口径）
2. Data Catalog Vocabulary (DCAT) 2 — W3C Recommendation[EB/OL]. W3C. https://www.w3.org/TR/vocab-dcat-2/ （R2，2026-11-01 WebSearch 核验可达——dcat:Distribution 按 accessService/endpoint 分组的渠道建模）
3. Kong Gateway — Routing & Service 管理（route/service 分组计数）[EB/OL]. Kong Inc. https://developer.konghq.com/ （R3，2026-11-02 WebSearch 核验可达——接入端点分组计数的工程形态）

# 附件

## 附录 A 原始需求原文摘录

指标名级三份真源 0 命中。渠道维度功能句近邻：

SRS《02-科技信息展示系统/科技数据资源/接入视窗.md》seq 361（历史更新周期统计与分析，节选）：

> 能够精准统计并展示各渠道、数据表的历史更新周期……

（「各渠道」维度词在；「渠道数量」基数指标与 taxonomy 无定义。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 接入渠道数量 / 渠道数（指标名级） | 主需求/核增/算法库 + SRS 分册 | 0 |
| 渠道数 | UI AccessSourceAnalysisDetail.jsx | :363（Statistic 题名） |
| 渠道（维度词） | SRS 接入视窗.md seq 361/363 | 2（分析维度语境） |
| channels | UI mockData.js | :100-106（五渠道） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_DATATHM_051_out.json`（2026-11-02 实跑：channel 列级+值分布新探针 + lane3/042 复用）。
- 复用产物：`M_SCIUI_DATATHM_042_out.json`（词族）；共享快照 `_snapshots/_probe_lane3_s304c_out.json`（来源标签三面，048 同锚）。
- 族内对账：gkx 标签=lane3=048 同键；mock 五渠道与 042 首段同款。

### B.2 本件产物逐键清单（`code/M_SCIUI_DATATHM_051_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.dev_channel_column_scan` | 列扫描 | 16 列（支付 13/导出 1/反馈 1/推送 1） | §3.2 |
| `facts.dev_channel_dist_probe` | 值分布 | export_channel 单值 script/118（佐证） | §3.2 |
| `facts.ui_mock_channels` | mock | 五渠道（volume 降序） | §3.4 |
| `facts.ui_mock_channel_count` | mock | **5** 类 | §3.4 |
| `facts.ui_mock_volume_total` | mock | **33,670**（脚本求和） | §3.4 |
| `facts.ui_mock_count_total` | mock | **1,256**（脚本求和） | §3.4 |
| `derived[0]` | 负结论 | access_channel_count = null（B10） | §1.6 |
| `absence_probe` | 探针 | 四件（dev/gkx/jiuxin/doc） | §3.3 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 原料 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 目录 endpoint 类型 | R2（DCAT） | distribution 元数据 | **无登记** | 高（标准建模） |
| 来源系统维度 | R1（Kimball） | source_system 维表 | **无维表** | 高（ETL 标准） |
| API 端点分组 | R3（网关） | route/service | 无网关面 | 中（端点形态） |
| 前端演示 | UI mock | 三套词并存 | 5/5/5（六类实给五） | 结构披露（不作源） |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 渠道归属列 | 16 列全业务语义 | 0 | 0 |
| 来源标签 | — | 三面全空 | — |
| taxonomy | 需求无（前端三套词） | — | — |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | Statistic 暂无数据态 | — |
| v1 | taxonomy 双轴裁定（一纸文件） | 口径裁定 |
| v2 | 登记面双列+回填 → COUNT DISTINCT 上线 | 触发器①（与 048 共享） |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| mock 5 类沿用（taxonomy 未裁先上线） | **高** | §3.4 三套词披露+双轴裁定前置 |
| es_sync 15 模块被当「渠道数」 | 中 | 模块≠渠道语义分叉登记（§1.6） |
| 支付渠道 13 列误导扫描命中 | 低 | §3.2 逐类排除（值分布佐证） |

### C.5 总判

**完全不支持**：分母面（资源×渠道登记）三源缺位（16 列全业务语义/标签三面空/快照无登记）+taxonomy 未裁定（前端三套词并存）；与 048 同根（供给侧登记缺位家族）——taxonomy 双轴文件+登记双列两步解锁全族（048/051/019/044/053）。

## 附录 D　复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_DATATHM_051.py` | 退出码 0，落 `_out.json` |
| 数据入口 | dev information_schema 列扫描+值分布 | 16 列/单值幂等 |
| 判档一致 | 文首 vs `support_judgment` | 完全不支持 |
| B11 对账 | 标签=lane3=048；词族=042 | 零漂移 |
| 幂等重跑 | 列扫描/分布确定性 | 逐位一致 |
| §二 从缺 | 完全不支持档 | 无伪公式（F4） |
| 伪值残留 | `access_channel_count` | null（无伪值） |

# 实时投资金额（M_SCIUI_INNOV_007）

> **类型**：AMOUNT（金额累计读数，含刷新语义）｜ **域**：科技发展态势·全球创新监测·全球创新实时数据＞数据指标分类展示＞实时投资金额｜ **UI 挂载**：科技信息展示系统 → 全球创新监测 → 创新实时监测（`InnovationRealtime.jsx:85` KPI 卡「实时投资金额 456 亿美元 +23.1%」）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：推测定义（非招标原文闭合口径）｜ **口径归属**：UI 推测叶（SRS 未出现该指标名；近似叶 seq 67 数据指标分类展示将"投资金额"列为举例指标）
> **复现脚本**：`code/M_SCIUI_INNOV_007.py`｜ **产物**：`code/M_SCIUI_INNOV_007_out.json`
> **四判定摘要**：直接结构 = 否（三源无"实时流"金额面）；直接数据 = 否；依赖结构 = 是（三源各有金额列：gkx 中文格式 varchar / dev 数值万元 / 久新 DECIMAL+CNY 换算列）；依赖数据 = 是（gkx 8,826 行全解析 / dev 8,294 行 / 久新 63,122+160,822 行）——**现在就能加工得到可刷新的累计读数**，故入转换档
> **数据源口径**：开发库（gkxlumenx_*，10.50.11.76，禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新库（jiuxin Doris 47.93.119.170:29030，gkx_technology_analysis_dev，只读）

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库 gkx+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全转换支持。** "实时投资金额"拆成两半看："投资金额"半边三源承载充足——gkx 融资表 8,826 行金额（中文格式六形态**全解析成功**，累计 4,790.45 亿元 CNY）、dev `enterprise_invest` 8,294 行数值万元（合计 18.20 亿元）、久新项目表 amount 63,122 行 + amount_cny 160,822 行（含固定汇率换算状态列）；"实时"半边三源均无 30 秒流式承载（dev 事件流三表 0 行；gkx/久新为批量快照，久新最近 update_time 2026-10-30——昨日级调度刷新可实现）。本件按"定时增量刷新的累计投资金额读数"口径判**完全转换支持**：无现成结果面（没有一张表叫"实时投资金额"），但金额列结构+数据量现在就够算；若甲方咬定 30 秒流式 CDC 语义，则降部分支持（触发器写死 §1.6）。

### 批次通用纪律摘要（20261101 批 S3-01 Lane 6 五件共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 覆盖率分子分母同表同池 |
| B4 | 负结论带探针 | dev 事件流三表 0 行 absence_probe 留证 |
| B5 | 确定性 | 解析规则六形态闭合；聚合键排序 |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 改脚本→重跑，产物零手改 |
| B8 | 回执不复收 | 硬证据本件实跑（三源连接记录在案） |
| B9 | 单位/日期陷阱 | 中文金额单位（万/亿）逐形态解析；零日期排除；汇率固定口径披露 |
| B10 | 口径裁定保守交付 | "定时刷新 vs 30s 流式"双口径并列 + 降档触发器写死 |
| B11 | 多本账互推 | 25,654 基数对账共享快照零漂移；8,826 解析数与 lane6 探针形态计数互证 |
| W2-1 | 先读资产再发 SQL | 共享快照 + lane6 探针消费后才写复现脚本 |
| W2-2 | 引用不漂移 | 快照数字原值引用 |
| W2-3 | 篇幅深度对标 | 13 章节齐全 ≥20KB |
| W2-4 | 三源探针不省略 | dev/gkx/jiuxin 三源逐一留证（§三/附录 B） |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 有现成"实时投资金额"结果面吗？ | 无 | 三源无此表（absence_probe + 探针） |
| 金额列现在够算吗？ | 够 | gkx 8,826 全解析 / dev 8,294 / 久新 63,122（facts 键） |
| "实时"语义可满足吗？ | 调度级可 / 流式不可 | 久新 update_time 2026-10-30（昨日级）；30s CDC 三源无承载 |

## 摘要

「实时投资金额」是全球创新监测·实时监测 Tab 的四张 KPI 卡之一（`InnovationRealtime.jsx:85`，mock 456 亿美元 +23.1%，30 秒扰动刷新），组件自带的实时状态标注（`realtimeModel.js:3`）明写"演示刷新非真源流……不接正式 ADS"——前端作者已自行披露流式语义是演示级的。数据侧实测：三源各有金额承载但物理形态迥异——gkx 是中文格式 varchar（"8320.0万人民币"，六形态解析规则 8,826/8,826 全闭合，累计 4,790.45 亿元 CNY）、dev 是数值万元列（8,294 行，18.20 亿元）、久新是 DECIMAL 原币 + CNY 换算双列（63,122/160,822 行，换算状态 `CONVERTED_TO_CNY_FIXED_RATE` 披露在案）。"实时"按定时增量刷新理解（分钟/小时调度）三源均可实现（久新 update_time 2026-10-30 证明日级新鲜度在跑），30 秒流式无承载。判**完全转换支持**：金额可算性已证、现成面没有、口径触发器写死。

- 需求判定：**UI 推测叶**（SRS 未出现「实时投资金额」；近似叶 seq 67 将"投资金额"列为指标分类举例，seq 72"实时数据更新"给通用实时语义）。
- 复现状态：脚本已跑通；三源金额覆盖/解析/汇总读数落产物。
- 档位结论：**完全转换支持**（金额三源可算 + 无现成面 + 流式语义触发器待裁定）。
- 关键事实：gkx 金额六形态解析 100% 闭合（8,826/8,826）——中文格式不是障碍而是已闭合的工程事实；累计 4,790.45 亿元 CNY（美元口径 665.36 亿美元 est，仅量级对照）。
- 升降档路径：甲方接受调度刷新 → 维持本档交付；咬定 30s 流式 → 降部分支持；接 CB Insights/PitchBook 全球源 → 升完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/全球创新监测/全球创新实时数据/**数据指标分类展示**（SRS seq 67；UI `InnovationRealtime.jsx`）。实时监测 Tab 顶部是 `MetricKpiGrid` 四联 KPI 卡：实时专利公开（128,456 件）、实时论文收录（89,234 篇）、**实时投资金额（456 亿美元，+23.1%）**、实时新增机构（2,456 家）。mock 值是 UI 需求证据（演示值，不参与支持度结论）：量级取"全球年度 VC 总量"的月度量级、单位取"亿美元"、附环比趋势百分比。组件内有 30 秒 `setInterval` 对四卡数值做 ±1% 随机扰动（`InnovationRealtime.jsx:119-128`），模拟实时心跳——这个细节把"实时"的 UI 语义定义为**持续变动的活读数**，而非静态快照。

尤为关键的是 `realtimeModel.js:3` 的 `realtimeStatus` 对象——前端作者主动写下的口径披露："演示刷新非真源流。基于全球创新监测专题样本，按 30 秒频率扰动新增专利公开、论文收录、投资事件与机构动态，不接正式 ADS。" 这句话是三重证据：其一，正式版应接 ADS（与久新 ads_* 表的对接预期一致）；其二，"投资事件"在实时流的事件类型清单里（投资金额与事件数同屏语义）；其三，30 秒是演示选择而非需求约束。

### 1.2 为什么需要本指标

实时监测页的业务叙事是"全球创新的心跳"：专利、论文、投资、机构四类信号里，投资金额是唯一带金钱单位的读数——它把创新活动直接换算成资本强度，是四卡中最直观的"市场用钱投票"信号。对用户（科创决策者）而言，投资金额的实时变动回答"资本正在流向哪里"：金额上行说明融资环境回暖，下行说明收紧——这比专利/论文数的变动更领先（资本市场的反应时滞通常短于成果产出）。与 INNOV_009（领域投资规模）/INNOV_010（区域投资额）构成"总量/切片"三件套：本件是总量卡，另两件是它的领域维与区域维下钻。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「实时投资金额」全称在三份 SRS 与《科技信息展示系统和科技专题服务系统.md》rg 检索未命中。近似叶两处：SRS seq 67「数据指标分类展示」原文"将全球创新数据按照关键数据指标进行分类，如专利数量、论文引用率、投资金额，用户可选择查看不同类别的数据指标"——投资金额是其举例指标之一，但"实时"未定义（无刷新频率、无时窗）；SRS seq 72「实时数据更新」原文"实时更新全球创新数据，用户可查看最新数据变化，了解全球创新动态"——给的是通用实时语义，同样无频率定义。三份说明书未出现该指标名的固定句式适用于本件全称；"投资金额"单词级命中见附录 A 检索记录。

### 1.4 类似指标权威方法可行性分析概要

"投资金额"统计在权威体系有三条先例，口径差异集中在**事件范围**与**披露金额处理**：其一，CB Insights《State of Venture》全球口径——只算 VC 支持的股权融资事件，"对未公开具体数值的金额进行估计并纳入统计"（投中研究院转述其方法论），2025 年全球 4,693 亿美元/29,501 笔（R3）；其二，PitchBook Q4 2025 Global VC First Look——同为 VC 口径但收录更宽（含部分 growth equity），2025 年 5,126 亿美元（R4）；其三，科技部战略院《中国创业投资发展报告》——中国官方口径按创投机构调查统计，2023 年管理资本 15,196.3 亿元（R5）。方法族对照：

| 方法族 | 事件范围 | 金额处理 | 与本库匹配 |
|---|---|---|---|
| CB Insights 全球 VC | VC 股权融资轮 | 未披露金额估计纳入 | gkx 池有轮次字段可筛（funding_round） |
| PitchBook 全球 VC 宽口径 | VC+growth | 同上 | 同上 |
| 中国官方创投调查 | 创投机构年报 | 调查填报 | 无（需调查数据源） |

结论：本件无需新建方法论——金额累计读数 = 事件范围筛选 + 金额解析 + 币种归一 + 时窗聚合，三步全是工程动作；唯一的方法层决策是事件范围（全轮次 vs 仅 VC 轮），gkx 轮次字段（股权投资/新三板/A轮/天使轮等 12 类）支持任意筛选。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/global-innovation/tabs/InnovationRealtime.jsx:85` — `investment: { value: 456, trend: '+23.1%', label: '实时投资金额', unit: '亿美元', metricId: 'M_INNOV_INVEST_RT' }`（演示值，不作数据证据；metricId 为前端自编标识）；`InnovationRealtime.jsx:119-128` 30 秒扰动逻辑。
- 组件：`repos/demo-ui-science/src/pages/global-innovation/tabs/realtimeModel.js:3` — `realtimeStatus.tooltip`："演示刷新非真源流……不接正式 ADS"。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` seq 67（投资金额举例）/seq 72（实时数据更新）；主文档 505 行同文复述。

### 1.6 推测定义与降档/升档触发器

**推测定义（分两半口径）**：

- **金额半边（主口径）**：实时投资金额 = 窗口 W 内融资事件的金额合计（万元 CNY 归一），W ∈ {近 30 天, 近 90 天, 年初至今}；事件范围默认全轮次（可选仅 VC 轮：股权投资/天使/A/B/C 轮等）；金额解析六形态规则（§2.3）；币种归一 USD/CNY=7.2、HKD/CNY=0.92 固定汇率（交付版应接汇率服务）。
- **实时半边（工程口径）**：刷新语义 = 定时增量调度（分钟/小时级重算窗口合计），非 30 秒流式 CDC。

**降档/升档触发器（B10 模板）**：若甲方咬定 30 秒流式（真 CDC）→ 三源无承载，**降部分支持**；若接受调度刷新 → 维持**完全转换支持**（本档，金额可算性已证）；若接 CB Insights/PitchBook API 作真源 → **升完全直接支持**（外部源直查）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` |
| 所属四级功能 | 1.1.1.1.4.1 全球创新监测（33 叶） |
| 本件挂靠叶 | 数据指标分类展示（seq 67，excel_row 70）——投资金额为其举例指标 |
| 相近叶 | 实时数据更新（seq 72，实时语义源）；可视化数据呈现（seq 68，图表形态） |
| UI 容器 | `InnovationRealtime.jsx` MetricKpiGrid 四卡之三 |
| 批内姊妹件 | INNOV_009（领域投资规模=领域下钻）、INNOV_010（区域投资额=区域下钻）、INNOV_006（增长率=趋势读数） |

本件是 Lane 6 投资三件套的**总量件**：009/010 的金额解析规则、池口径注记、汇率口径全部在本件定义并复用（B11 批内一致），本件 MD 的 §2.3 解析规则是三件共享的方法基座。

## 二、计算过程

### 2.1 装载与规模校验

三源装载：gkx 经 `_gkxdb.py`（融资表 25,654 行对账共享快照零漂移）；dev `enterprise_invest` 46,967 行；久新 `ads_project_profile` 1,838,841 行。金额面规模分层核验：gkx 非空 8,826 行（34.40%）、dev 非零 8,294 行（17.66%）、久新 amount 63,122 行（3.43%）+ amount_cny 160,822 行（8.75%）。三个池的金额覆盖率排序 gkx > dev > 久新，但池语义各异（gkx=广东企业融资、dev=股权关系、久新=全球科研项目资助），不能直接互比——这是三源三本账的典型情形，本件以 gkx 为主算面（事件语义最贴"投资"），另两源作对照面。

### 2.2 dev 侧：股权关系快照，无事件流

dev 投融资 5 表中三张事件流表全空（`chain_investment`/`industry_chain_investment_event`/`industry_chain_investment_participant` 均 0 行，absence_probe 留证）；有数的两张是股权关系快照：`enterprise_invest`（46,967 行，invest_amount 万元列 8,294 行非零、合计 182,032 万元 = 18.20 亿元）与 `enterprise_forg_invest`（40,043 行外资股东关系）。金额读数可取（`facts.dev_enterprise_invest_amount_sum_wan_cny=182032.0`），但语义是"对外股权投资出资额"非"融资事件金额"，且 event_date 0 覆盖（INNOV_006 同款缺席）无法做时间窗。结论：dev 侧作金额对照面，不作主算面。

### 2.3 gkx 侧：中文金额六形态解析（方法基座）

gkx `funding_amount` 是中文格式 varchar，实测 8,826 非空行全部落在六种形态内，解析规则闭合（`facts.gkx_financing_amount_parse_fail=0`）：

| 形态 | 行数 | 解析式（→ 万元 CNY） |
|---|---|---|
| N万人民币 | 4,510 | N |
| N亿人民币 | 3,814 | N × 10,000 |
| N万美元 | 263 | N × 7.2 |
| N亿美元 | 134 | N × 72,000 |
| N万港元/万港币 | 105（港元港币系） | N × 0.92 |
| N亿港元/亿港币 | （并入上系） | N × 9,200 |
| 其他 | **0** | — |

六形态计数与 lane6 探针 `_probe_lane6_gkx_fin2_out.json` 的 SQL REGEXP 分布（万人民币 4,510/亿人民币 3,814/万美元 263/亿美元 134/港系 105）**完全互证零漂移**（B11）。累计金额 4,790,451.44 万元 CNY（`facts.gkx_financing_amount_sum_wan_cny=479045143.63`）；美元口径估算 665.36 亿美元（`derived.gkx_financing_amount_usd_bn_est`，除以 7.2 再除以 10,000）——与 UI mock 456 亿美元同量级（mock 为演示值不作数据证据，但量级巧合说明前端作者对全球 VC 月度/滚动窗口量级有正确直觉）。

```python
# 六形态解析（Python 侧，B5 确定性：无正则歧义，endswith 链式匹配）
def parse_cny(s):
    if s.endswith("万人民币"): return float(s[:-4])
    if s.endswith("亿人民币"): return float(s[:-4]) * 10000
    if s.endswith("万美元"):   return float(s[:-3]) * 7.2
    if s.endswith("亿美元"):   return float(s[:-3]) * 72000
    if s.endswith("万港元") or s.endswith("万港币"): return float(s[:-3]) * 0.92
    if s.endswith("亿港元") or s.endswith("亿港币"): return float(s[:-3]) * 9200
    return None  # 实测 0 行落到这里
```

### 2.4 近端窗口读数（"实时"的现实语义）

"实时"的工程可行形态是滚动窗口重算：最近完成年 2025 年 618 事件（`facts.gkx_financing_events_2025`）；最近 90 天窗口（2026-11-01 回溯）**0 事件**（`facts.gkx_financing_events_last90d_from_20261101=0`）——gkx 池最新 completion_date 为 2026-07-17（`facts.gkx_financing_max_completion_date`），说明 gkx 源的更新节奏是月级滞后，"实时"读数在 gkx 侧只能做到 T+30 天级。久新侧新鲜度更好：`ads_project_profile` 最大 update_time **2026-10-30 10:45**（`facts.jiuxin_project_profile_max_update_time`，昨日级）——若实时卡以久新项目资金为源，日级刷新已实现。两源新鲜度分层是"实时"口径裁定的重要输入：分钟级需求两源都不满足，小时/日级久新满足，月级 gkx 满足。

### 2.5 久新侧：科研项目资助金额（对照面）

久新 `ads_project_profile` 是 OpenAlex Grant 型科研项目池（1,838,841 行），金额面三层：amount 原值 63,122 行（3.43%）、amount_cny 换算值 160,822 行（8.75%）、换算状态列 `amount_cny_normalization_status`（样例值 `CONVERTED_TO_CNY_FIXED_RATE`——久新同样用**固定汇率**换算，与本件 7.2/0.92 口径同族，交付版接即期汇率的建议对两源一致）。另有问题维资金证据表 `ads_research_problem_funding_evidence` 5,123 行，其中仅 252 行有金额（`funding_amount_status`: AVAILABLE 252 / AMOUNT_MISSING 4,871）——问题维金额覆盖率 4.9%，作对照面时覆盖率须随行披露。

### 2.6 稳健性与口径敏感性

金额读数的三个敏感性逐一披露：**汇率**——USD/CNY 取 7.2 为 2024–2026 区间中枢近似，正式交付应接汇率服务并记录汇率日（久新 `amount_cny_exchange_rate_date` 列即此设计）；**事件范围**——全轮次 vs 仅 VC 轮差异显著（gkx 轮次分布：股权投资 8,597/新三板 3,349/战略投资 2,061/被收购 1,767…，"仅 VC 轮"口径会把新三板/并购类剔出，金额读数预计缩水四成以上，B10 双口径并列待裁定）；**池语义**——gkx 是广东企业池（INNOV_010 详证省份 100% 广东省），累计 4,790 亿元的语义是"广东样本池历史累计融资额"，**不是全球读数**；全球读数需外部源（CB Insights 2025 年 4,693 亿美元，R3）或久新全球项目池。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INNOV_007.py`（gkx 经 `_gkxdb.py`；dev/jiuxin 直连只读；六形态解析内嵌；运行 `python3 code/M_SCIUI_INNOV_007.py`）。
- 产物：`code/M_SCIUI_INNOV_007_out.json`。正文数字与产物键逐一对应：`dev_enterprise_invest_amount_sum_wan_cny=182032.0`（§2.2）、`gkx_financing_amount_nonnull=8826` / `gkx_financing_amount_parseable=8826` / `gkx_financing_amount_parse_fail=0`（§2.3）、`gkx_financing_amount_shapes`（§2.3 表）、`gkx_financing_amount_sum_wan_cny=479045143.63`（§2.3）、`gkx_financing_events_2025=618` / `gkx_financing_events_last90d_from_20261101=0` / `gkx_financing_max_completion_date`（§2.4）、`jiuxin_project_amount_nonnull=63122` / `jiuxin_project_amount_cny_nonnull=160822` / `jiuxin_project_profile_max_update_time`（§2.5）、`jiuxin_funding_evidence_amount_rows=252`（§2.5）、派生键 `gkx_financing_amount_coverage_pct=34.4` / `gkx_financing_amount_parseable_pct=100.0` / `gkx_financing_amount_usd_bn_est=665.36`（§2.1/§2.3）。
- 结果解读：金额可算性三源三证（累计额、覆盖率、解析闭合率全落产物）；"实时"分层新鲜度证据在案（gkx 月级 / 久新日级）。
- 对照需求功能要求的评审：KPI 卡金额读数——可交付（调度刷新 + 窗口口径披露）；30 秒流式——不可交付（触发器 §1.6）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| dev | 事件流三表行数 | `dev_chain_investment_rows` 等 | 0/0/0（absence_probe） |
| dev | 股权金额合计 | `dev_enterprise_invest_amount_sum_wan_cny` | 182,032 万元（18.20 亿元） |
| gkx | 金额非空 | `gkx_financing_amount_nonnull` | 8,826 |
| gkx | 解析闭合 | `gkx_financing_amount_parseable` / `parse_fail` | 8,826 / **0** |
| gkx | 六形态分布 | `gkx_financing_amount_shapes` | 4,510/3,814/263/134/105/0 |
| gkx | 累计金额 | `gkx_financing_amount_sum_wan_cny` | 4,790,451.44 万元 CNY |
| gkx | 美元口径 est | derived `gkx_financing_amount_usd_bn_est` | 665.36 亿美元 |
| gkx | 近端窗口 | `gkx_financing_events_2025` / `last90d` | 618 / 0 |
| gkx | 池新鲜度 | `gkx_financing_max_completion_date` | 2026-07-17 |
| 久新 | 项目金额覆盖 | `jiuxin_project_amount_nonnull` / `_cny_nonnull` | 63,122 / 160,822 |
| 久新 | 池新鲜度 | `jiuxin_project_profile_max_update_time` | 2026-10-30 10:45 |
| 久新 | 问题资金覆盖 | `jiuxin_funding_evidence_amount_rows` | 252/5,123（4.9%） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 融资事件金额 | gkx | `dwd_org_financing_info.funding_amount` | 8,826 非空（34.40%） | 转换（六形态解析） | **足** |
| D2 | 股权投资金额 | dev | `enterprise_invest.invest_amount` | 8,294 非零（17.66%） | 直查 | 足（对照面） |
| D3 | 项目资助金额 | jiuxin | `ads_project_profile.amount/amount_cny` | 63,122 / 160,822 | 直查 | 足（对照面） |
| D4 | 事件日期（窗口） | gkx | `completion_date` | 25,654（100%） | 直查 | **足** |
| D5 | 事件日期（dev） | dev | `enterprise_invest.event_date` | 0 覆盖 | **不可得** | 缺（对照面受累） |
| D6 | 实时流（CDC/30s） | 三源 | — | — | **不存在** | **缺（触发器主项）** |

`support_judgment="完全转换支持"`，与文首同档（闸 6 对齐）。

### 3.2 D1 gkx 金额列：中文格式是已闭合工程

8,826/8,826 解析闭合（§2.3 表）证明中文金额格式不是数据质量障碍——六形态覆盖完备、无游离形态（"其他"计数 0）。覆盖率 34.40%（8,826/25,654）意味着三分之二事件未披露金额，这与 VC 市场常态一致（CB Insights 方法论同样需要对未披露金额做估计，R3）；若甲方要求全事件金额，需引入估计模型（外部方法论先例存在），但基础读数（有金额子集合计）现在就能交付。

### 3.3 D4 事件日期：窗口读数的骨架

completion_date 100% 覆盖（零日期 0 行）使任意时间窗聚合可行：近 30 天/90 天/YTD/滚动年——本次实测近 90 天 0 事件暴露的是 gkx 源的**更新滞后**（最新 2026-07-17）而非日期列缺陷。窗口读数的源选择因此明确：近端窗口用久新（日级新鲜度），历史累计用 gkx（11 年纵深）。

### 3.4 D6 实时流缺席：absence_probe 全记录

否定性证据三件套：**查了什么**——dev 侧事件流三表（`chain_investment`/`industry_chain_investment_event`/`industry_chain_investment_participant`）行数；**条件**——全表 COUNT；**命中**——0/0/0。gkx/久新侧为批量快照表（无 binlog 订阅、无消息队列表、无流式视图），30 秒 CDC 无承载。缺失情形归属：**表不存在（事件流面）+ 列数据全空（dev event_date）**。这是"实时"半边的唯一降档源，触发器写死（§1.6）。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 六形态解析互证 | 脚本计数 = lane6 探针 SQL REGEXP 分布（零漂移） |
| 汇率口径披露 | 7.2/0.92 固定汇率，与久新 CONVERTED_TO_CNY_FIXED_RATE 同族 |
| 零日期协议 | completion_date > '1000-01-01' 生效 |
| 池口径披露 | gkx=广东池注记全程随行 |
| 新鲜度分层 | gkx 2026-07-17 / 久新 2026-10-30（实测 max 值落产物） |
| 脚本形态 | 三源只读；无 demo_*；无耗时键 |

## 四、数据缺失情况

### 4.1 实时流承载缺失（源级，触发器主项）

三源无 30 秒流式承载（§3.4）。修复路径两条：接消息队列/CDC 管道（工程立项，源系统侧改造）；或口径降级为调度刷新（分钟/小时级重算，本档交付形态）。影响面：本件 KPI 卡的"心跳感"由前端扰动兜底（演示），正式版读数将是准实时的调度值——需与甲方对齐预期。

### 4.2 gkx 金额覆盖率 34.40%（数据级，披露项）

三分之二事件无金额。修复路径：估计模型（CB Insights 先例，R3）或维持"有金额子集"口径并随行披露覆盖率。影响面：累计额读数语义是"披露金额子集合计"，偏低估。

### 4.3 全球池缺失（池语义级，三件套共同缺口）

gkx 是广东池、dev 是股权关系、久新是全球科研项目（资助非 VC）——三源无一覆盖"全球 VC 融资事件"语义。修复：接 CB Insights/PitchBook API（升完全直接支持）或甲方接受"广东池/科研项目池"的替代语义。影响面：本件 + INNOV_009/010 三件共享。

### 4.4 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径裁定：调度刷新 vs 30s 流式 | 口径裁定 | 本件 | B10 触发器，决定档位走向 |
| 接 CB Insights/PitchBook API | 外部数据源 | 本件+009+010 | 升完全直接支持；2025 全球 4,693 亿美元（R3）可作校准锚 |
| dev event_date 回填 | 数据回填 | 本件+006+009+010 | 源系统侧补数 |
| 汇率服务接入 | 工程项 | 本件+009+010 | 替换固定 7.2/0.92；久新 exchange_rate_date 列设计可参照 |

## 参考文献

1. BVK Global Venture Capital Report 2025（数据源 CB Insights）[EB/OL]. BVK. https://www.bvkap.de/files/content/Studien/Studien%20Archiv/20260126_BVK%20Global%20Venture%20Capital%20report%202025_FINAL.pdf （R3，2025 全球 VC 4,690 亿美元/+47% YoY，2026-11-01 WebSearch 核验可达）
2. Q4 2025 Global VC First Look[EB/OL]. PitchBook. https://pitchbook.com/news/reports/q4-2025-global-vc-first-look （R4，2025 全球 5,126 亿美元口径，2026-11-01 WebSearch 核验可达）
3. State of Venture 2025 Annual Report[EB/OL]. CB Insights. https://www.cbinsights.com/reports/CB-Insights_Venture-Report-2025.pdf （R3b，2025 年报原出处，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

「实时投资金额」在三份 SRS 与主文档均未出现（`named_in_srs=false`）。近似叶原文：

SRS《02-科技信息展示系统/科技发展态势/全球创新监测.md》seq 67（excel_row 70）：

> 将全球创新数据按照关键数据指标进行分类，如专利数量、论文引用率、投资金额，用户可选择查看不同类别的数据指标。

seq 72（excel_row 75）：

> 实时更新全球创新数据，用户可查看最新数据变化，了解全球创新动态。

主文档 505 行与 seq 67 同文。UI 组件 `InnovationRealtime.jsx:85` 的 KPI 卡定义（演示值，不作数据证据）：`investment: { value: 456, trend: '+23.1%', label: '实时投资金额', unit: '亿美元', metricId: 'M_INNOV_INVEST_RT' }`。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 实时投资金额 | 三份 SRS + 主文档 | 0 |
| 投资金额 | 全球创新监测.md:183 / 主文档:505 | 2（均为 seq 67 举例句） |
| 实时 | 全球创新监测.md | 8（seq 60/72 实时叶 + 全球创新实时数据分组名） |
| 实时投资 | 主文档 | 0（3733/3739 行为孵化载体系统投资监控，另语境） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_007_out.json`（20261101 实跑：三源金额覆盖、六形态解析、累计额、窗口读数、新鲜度、dev 事件流缺席探针）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（dev 投融资 5 表清单 + gkx 融资 25,654 行，零漂移引用）。
- lane 级探针：`code/_probe_lane6_gkx_fin_out.json`（列清单）/`_probe_lane6_gkx_fin2_out.json`（形态分布互证）/`_probe_lane6_dev_fin_out.json`（5 表行数与列）/`_probe_lane6_jiuxin3_out.json`（久新金额覆盖）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INNOV_007 | 文首 |
| `ui_evidence` | 证据 | 3 条组件行号 | §1.1/§1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.dev_enterprise_invest_rows` | 计数 | 46,967 | §2.2 |
| `facts.dev_enterprise_invest_amount_rows` | 计数 | 8,294 | §2.2 |
| `facts.dev_enterprise_invest_amount_sum_wan_cny` | 金额 | 182,032.0 万元 | §2.2 |
| `facts.dev_chain_investment_rows` 等 | 计数 | 0/0/0 | §2.2/§3.4 |
| `facts.gkx_financing_amount_nonnull` | 计数 | 8,826 | §2.3 |
| `facts.gkx_financing_amount_parseable` / `parse_fail` | 计数 | 8,826 / 0 | §2.3 |
| `facts.gkx_financing_amount_shapes` | 分布 | 六形态计数 | §2.3 |
| `facts.gkx_financing_amount_sum_wan_cny` | 金额 | 479,045,143.63 万元 | §2.3 |
| `facts.gkx_financing_events_2025` | 计数 | 618 | §2.4 |
| `facts.gkx_financing_events_last90d_from_20261101` | 计数 | 0 | §2.4 |
| `facts.gkx_financing_max_completion_date` | 日期 | 2026-07-17 | §2.4 |
| `facts.jiuxin_project_profile_rows` | 计数 | 1,838,841 | §2.5 |
| `facts.jiuxin_project_amount_nonnull` / `_cny_nonnull` | 计数 | 63,122 / 160,822 | §2.5 |
| `facts.jiuxin_project_profile_max_update_time` | 时间 | 2026-10-30 10:45:00 | §2.4/§2.5 |
| `facts.jiuxin_funding_evidence_rows` / `_amount_rows` | 计数 | 5,123 / 252 | §2.5 |
| `derived[0]` | 派生比 | gkx_financing_amount_coverage_pct = 34.4 | §3.2 |
| `derived[1]` | 派生比 | gkx_financing_amount_parseable_pct = 100.0 | §2.3 |
| `derived[2]` | 派生比 | gkx_financing_amount_usd_bn_est = 665.36 | §2.3 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |
| `notes` | 披露 | 五条（口径/演示自认/三物理形态/池语义/汇率） | §1.6/§四 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表机构 | 事件范围 | 金额处理 | 本库承载 | 贴合度 |
|---|---|---|---|---|---|
| 全球 VC 口径 | CB Insights（R3） | VC 股权轮 | 未披露金额估计纳入 | gkx 轮次字段可筛 | 高（需外部源补全球池） |
| 全球 VC 宽口径 | PitchBook（R4） | VC+growth | 同上 | 同上 | 高（同上） |
| 中国官方调查口径 | 科技部战略院（R5） | 创投机构年报 | 调查填报 | 无调查数据源 | 低 |
| 库内直算口径 | 本项目 | gkx 全轮次 | 有金额子集合计 | **现在可算** | **交付基线** |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| gkx 金额列 | 8,826/25,654 | 解析 100% 闭合 | 覆盖 34.40%；广东池 |
| dev 金额列 | 8,294/46,967 | 数值万元直查 | 语义为股权出资；日期 0 覆盖 |
| 久新 amount | 63,122/1,838,841 | 3.43% | 资助语义非 VC |
| 久新 amount_cny | 160,822 | 8.75% | 固定汇率 |
| 实时流 | 三源无 | — | CDC 缺失（触发器） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | gkx 累计额 + 窗口读数（调度刷新 + 池口径注记） | 无 |
| v2 | 事件范围双口径（全轮次/仅 VC 轮）+ 覆盖率随行披露 | 甲方裁定范围 |
| v3 | CB Insights API 接入（全球池 + 估计模型） | 外部源立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 4,790 亿被误读为全球读数 | **高** | 广东池注记 + UI 文案「广东样本池」 |
| 30s 流式预期落差 | 高 | 口径裁定前置；前端扰动过渡 |
| 固定汇率漂移 | 中 | 汇率服务接入排期 |
| 覆盖率 34.40% 低估 | 中 | 披露 + 估计模型（v3） |

### C.5 总判

**完全转换支持**：金额半边三源可算（gkx 主算面解析闭合、累计额落产物），实时半边调度级可实现、流式级无承载（触发器写死）；无现成结果面故不入直接档，依赖侧结构+数据量足额故入转换档。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_007.py` | 退出码 0，落 `_out.json` |
| 数据入口 | gkx 经 `_gkxdb.py`；dev/jiuxin 直连只读 | demo_* 直接 raise |
| 解析闭合 | `gkx_financing_amount_parse_fail` | 0 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 完全转换支持 |
| 负证据探针 | `absence_probe[0]`（dev 事件流 0/0/0） | hits=0 留证 |
| 共享快照对账 | 25,654 行 fix2 键 | 零漂移 |
| 形态互证 | 脚本 shapes vs `_probe_lane6_gkx_fin2_out.json` | 计数一致 |
| mock 残留检查 | `rg "M_INNOV_INVEST_RT" repos/demo-ui-science/src` | 正式版替换后无引用 |

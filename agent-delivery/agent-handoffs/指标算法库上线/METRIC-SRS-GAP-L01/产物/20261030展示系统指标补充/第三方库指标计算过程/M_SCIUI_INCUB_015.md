# 供需匹配率（载体-企业）（M_SCIUI_INCUB_015）

> **类型**：无业务逻辑数值类（政策供需匹配面三源零承载）｜ **域**：科技信息展示系统·科技成果展示·创新载体孵化载体·总览 KPI 卡「政策匹配率」+ 政策资源匹配面板分｜ **UI 挂载**：`pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:114`（KPI「政策匹配率」）/ `:254`（匹配对象面板「匹配率」）/ `:627`（SoftMatchResultPanel 匹配分）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（三份说明书未出现「匹配率/供需匹配率」指标名；语义锚 SRS 序号 549「载体对接政策资源」+ 主需求 :3717 仅描述匹配行为，比率口径无定义）｜ **口径归属**：UI 派生读数（mock `policyMatchRate` 92/86/79/74 演示常数），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_INCUB_015.py`｜ **产物**：`code/M_SCIUI_INCUB_015_out.json`
> **四判定摘要**：直接结构 = 无现成匹配结果数据（dev `ads.policy_match` 结构面齐但 0 行空壳；gkx/久新无匹配面）；直接数据 = 无（同左）；依赖结构 = **缺**（dev 载体主档 `dim.carrier` 28 行无画像标签维——匹配前提输入缺失；gkx 0 列命中；久新 match 命中全为科技要素推荐语义排除）；依赖数据 = 无（政策库适配条件未结构化，匹配 run 无从运行）
> **数据源口径**：三源（dev live `10.50.11.76` `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live 218 表复核）逐一探针留证；`demo_*` 禁引；UI mock 值仅作需求语义证据。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库与久新库**均无法构建 |

**四判定**：表结构直接支持 / 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。**匹配率的计算三层前提——①政策资源库适配条件结构化、②载体/企业画像标签面、③匹配结果面——三源逐一探测：dev `gkxlumenx_ads.policy_match` 是唯一结构承载（`match_score`/`rank_no`/`model_version` 列齐）但 **0 行**且载体侧 `dim.carrier`（28 行，`source=v1_approx`）无任何画像标签列，匹配 run 无输入无从运行；gkx 280 表 incub/match 词族表名+列名双零命中；久新 218 表 live 复核 match 命中 15 表全为 `ads_recommendation_*` 科技要素推荐（论文/人才/技术方向），无政策资源库语义排除。指标及关键依赖三源均无法构建。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（§2.8/附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 分母口径缺失已披露（负结论无除式） |
| B4 | 负结论带探针 | absence_probe 五件（dev 匹配面/载体标签维/gkx/久新/需求原文） |
| B5 | 确定性 | 词族命中列表 sorted()；mock 值按文件序 |
| B7 | 产物只由脚本产出 | 本件 py 实探产出 _out.json |
| B9 | 单位/日期陷阱 | 单位=%（比率）；mock 分值「92分」带单位后缀 |
| B10 | 口径裁定保守交付 | 负结论留空登记（derived value=null） |
| B11 | 多本账互推 | dev 表行数与 `_lane7_shared_probe_out.json` 快照零漂移 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成匹配结果面吗？ | 无 | dev 0 行空壳/gkx 0 命中/久新语义排除（absence_probe） |
| 匹配前提维（政策库+画像）结构数据齐吗？ | **缺** | 载体主档无标签列；政策库适配条件未结构化 |
| 现在就能算吗？ | 不能 | 匹配 run 无输入 |

## 摘要

「供需匹配率（载体-企业）」是孵化载体页的政企匹配读数：载体当前可匹配政策资源的比率（%），KPI 显示全市载体均值、匹配面板显示单载体分。UI mock 4 载体 92/86/79/74（均值 83%）、面板 92/88/84 分。数据侧判定：**完全不支持**——dev 唯一结构承载 `ads.policy_match`（13 列含 match_score/rank_no）0 行空壳，载体主档 `dim.carrier` 28 行 v1_approx 近似源无画像标签维，政策库（`dwd.policy_base_info` 35,758 行）适配条件未结构化；gkx 零命中；久新 match 命中全为科技要素推荐语义排除。匹配率业界口径（惠企政策平台「免申即享」）需企业标签库×政策事项颗粒化拆解两前提，三源均无。

- 需求判定：指标名三份说明书未出现；语义锚序号 549「载体对接政策资源」（匹配行为有需求、比率口径无定义）。
- 复现状态：三源探针脚本已跑通；五件 absence_probe 留证。
- 档位结论：**完全不支持**（三层前提全缺）。
- 关键事实：dev `ads.policy_match` 是「schema 已建、数据未灌」的预留面——升档只差政策库拆解+载体标签建设两步。
- 升档路径：政策库颗粒化+载体标签面 → 匹配 run 落 `ads.policy_match` → 部分支持；接深圳市惠企政策平台接口 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 创新载体孵化载体 → ①总览 KPI 卡（`IncubationCarrierPage.jsx:114`「政策匹配率」＝当前筛选载体 `policyMatchRate` 均值，`buildKpis()` L103-105 `Math.round(ΣpolicyMatchRate/items.length)`）；②匹配对象面板（`:254`「匹配率」＝当前载体单值 `${item.policyMatchRate}%`）；③政策资源匹配阶段（`:627` `SoftMatchResultPanel score={activeCarrier?.policyMatchRate}` 匹配总分 + policyMatches 明细 92/88/84 分）。三级读数同源一个 mock 字段。

### 1.2 为什么需要本指标

载体运营方需知道「我园区的企业能吃到多少政策红利」：匹配率越高＝政策覆盖越好、申报辅导越精准。SRS 序号 549 的功能定位（高亮载体可申领资金补贴、专家辅导、技术支持等政策红利）需要一个量化总分来排序和追踪，匹配率就是这个总分的展示形态。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）；主需求 :3717 仅功能分句。**固定句式：三份说明书未给出该指标的计算方法。**

### 1.4 类似指标权威方法可行性分析概要

业界政企匹配口径（方法族表，完整版指向附录 C）：①厦门「免申即享」范式——政策要素管理（一策一案拆解适用主体/条件）+ 企业画像标签（600+ 标签）+ 一策一模型比对；②黑龙江惠企平台——企业标签 158 个×政策事项标签 106 个双向匹配，推送率/兑现率分层监测；③火炬中心孵化器评价体系（2019）无「政策匹配率」直接指标——服务能力维度考察投融资/导师/中介服务，佐证该指标是平台派生读数非法定报表指标。

### 1.5 引用来源

1. 福建省发改委《厦门市利用大数据实现"政策精准找人"》（2025）：政策要素解构+企业画像 600 标签+一策一模型。https://fgw.fujian.gov.cn/ztzl/fjys/dxjy/202503/t20250304_6771822.htm
2. 国家发改委《黑龙江省：打造全流程政策服务新模式》（2025）：企业标签 158×政策事项标签 106 双向匹配、网办率 94.13%/兑现率监测。https://www.ndrc.gov.cn/xwdt/ztzl/xhyshj/dfdt/202509/t20250910_1400392.html
3. 科技部火炬中心《科技企业孵化器评价指标体系》（国科火字〔2019〕239 号）。http://www.chinatorch.gov.cn/fhq/zcfg/202602/bf58a7e77266425e94fa7cc512518095.shtml

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：载体画像（行业/阶段/需求标签）× 政策库适配条件的匹配命中面，以比率呈现。
- **操作化定义（业界通行式，本件未实现）**：匹配率 = 命中政策事项数 ÷ 适用于该载体的政策事项总数 × 100%（厦门/黑龙江口径的标签命中率）。
- **降档触发器**：已处最低档（完全不支持）。
- **升档触发器**：政策库适配条件结构化 + 载体标签面落库 → 匹配 run 灌 `ads.policy_match` → 部分支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：创新载体孵化载体·政策资源匹配（UI 阶段三），SRS 序号 549「载体对接政策资源」。
- 相近叶：序号 548「各级政策自动归集」（政策库建设——本件匹配前提的上游）；序号 550「政策申报流程与材料管理」（匹配结果的下游消费）。INCUB_011（成长分）同为载体画像派生读数，其画像缺失结论与本件互证。

## 二、计算过程

从缺。本指标需「政策资源库适配条件结构化 + 载体画像标签面 + 匹配结果面」三层依赖（§1.4 业界口径），三源探针（附录 B 五件）证明三层均无承载：dev 匹配面 0 行空壳且载体主档无标签维、gkx 零命中、久新语义排除——无原料即无除式，禁伪公式。复现代码与证据对照见产物 `derived[0]`（负结论留空登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 政策资源库（适配条件结构化） | dev `dwd.policy_base_info`（35,758 行，快照键） | **未结构化**（政策正文面，无适用条件颗粒化拆解列） |
| 载体画像标签面 | dev `dim.carrier`（28 行 v1_approx） | **缺**（9 列无标签维） |
| 匹配结果面 | dev `ads.policy_match` | **0 行**（13 列结构齐） |
| 要素侧匹配承载 | gkx 280 表 / 久新 218 表 | 0 命中 / 语义排除 |

### 3.2 现场复核清单

dev `dim.carrier` 样本（合肥科技大学/中科院北京先进技术研究院…，carrier_type=university/research，source=v1_approx）与 `carrier_org_rel` 57 行（rel_type=self 归属）均无画像/需求标签——匹配计算输入侧物理缺失；`ads.policy_match` 列结构（subject_type/subject_id/policy_id/match_score/match_reasons/rank_no/model_version）证明这是为匹配 run 预留的 schema 面（产物键 `dev_policy_match_cols`）。

## 四、数据缺失情况

### 4.1 缺口清单

①政策库适配条件未颗粒化拆解（上游缺）；②载体画像标签维缺失（输入缺）；③匹配结果面 0 行（输出缺）；④ gkx/久新无同义面（外部无援）。

### 4.2 修复建议与影响面

短期：政策库按「适用主体/条件/临界点」颗粒化拆解（参照厦门一策一案）落 `dwd.policy_layout_recommend` 系；载体标签面挂 `dim.carrier` 扩列。中期：匹配 run 灌 `ads.policy_match`（结构已在，插数即活）→ 本件升「部分支持」，同页 INCUB_011（成长分）、SOFTSCI_007（毕业统计）等载体族件联动受益。远期：直连深圳市惠企政策「免申即享」平台匹配接口 → 完全直接支持。

### 4.3 影响面

孵化载体页政策匹配阶段整段（SoftMatchResultPanel + policyMatches 明细）现为 mock 演示态；「重新匹配」按钮是 900ms setTimeout 假动画（`IncubationCarrierPage.jsx:610-616`），无后端。

## 参考文献

1. 福建省发改委. 厦门市利用大数据实现"政策精准找人". https://fgw.fujian.gov.cn/ztzl/fjys/dxjy/202503/t20250304_6771822.htm
2. 国家发改委. 黑龙江省：打造全流程政策服务新模式 推动惠企政策精准直达、快速兑现. https://www.ndrc.gov.cn/xwdt/ztzl/xhyshj/dfdt/202509/t20250910_1400392.html
3. 科技部火炬中心. 科技企业孵化器评价指标体系（国科火字〔2019〕239 号）. http://www.chinatorch.gov.cn/fhq/zcfg/202602/bf58a7e77266425e94fa7cc512518095.shtml

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 匹配率|供需匹配` 三份说明书（科技全域态势/技术发展跟踪/全球创新监测）+ 主需求《科技信息展示系统和科技专题服务系统.md》→ 指标名 0 命中。
- 语义锚原文（SRS 创新载体孵化载体.md 序号 549「载体对接政策资源」）：「平台自动匹配可用政策资源与孵化载体，系统高亮载体可申领资金补贴、专家辅导、技术支持等政策红利，便于载体和企业快速获取资源。」（主需求 :3717 同文）
- UI：`incubationCarrierMock.js:144` `policyMatchRate: 92`（4 载体 92/86/79/74，mock 演示值）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_015_out.json`）

facts（ui_mount/ui_mock_carrier_rates/ui_mock_carrier_names/ui_mock_kpi_value=83/ui_mock_kpi_note/ui_mock_panel_scores/dev_table_total=542/dev_match_word_tables/dev_policy_match_cols/dev_policy_match_rows=0/dev_policy_layout_recommend_rows/dev_policy_recommendation_report_rows/dev_dim_carrier_rows=28/dev_dim_carrier_cols/dev_dim_carrier_source_note/dev_carrier_rel_rows=57/dev_carrier_index_rows=0/gkx_table_count=280/gkx_incub_match_word_tables/jiuxin_table_count_live=218/jiuxin_incub_word_tables/jiuxin_match_word_tables/jiuxin_match_hits_note/jiuxin_recommendation_run_cols_sample/srs_anchor/named_in_srs/named_note）；derived[0]（carrier_policy_match_rate，负结论 null 登记）；absence_probe（五件）；support_judgment=完全不支持；base_years 三键；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：厦门范式（政策要素管理+企业画像 600 标签+一策一模型）→ 黑龙江范式（158×106 双向标签+兑现率分层）→ 火炬口径（无此指标，佐证 UI 派生属性）。数据矩阵：政策库未拆解/画像缺/结果面空壳。分期方案：一期政策拆解+标签建设（部分支持）、二期平台对接（完全直接支持）。风险登记：政策颗粒度标准缺失、标签冷启动。总判：完全不支持（三层前提全缺，升档路径清晰）。

# 融合指标数（M_SCIUI_KGANALY_058）

> **类型**：无业务逻辑数值类（配置计数读数）｜ **域**：科技信息展示系统·科技知识图谱·指标展示·融合统计指标和模型特征｜ **UI 挂载**：指标展示页 → `IndicatorDisplay.jsx:98` KPI 行第二卡 `<Statistic title="融合指标数" value={5} suffix="项"/>`——**value={5} 硬编码**（对应 `mockData.js fusionIndicators` 数组 5 项：网络密度/聚类系数/平均路径长度/中心性方差/社区模块度）；页头描述 `:73`「黑名单触发、融合统计指标和模型特征、优化决策模型」
> **数据支持度**：**完全不支持**（「融合指标数」的语义是**融合指标登记/配置面的行计数**——三源逐一探针：dev `gkxlumenx*` 指标词族 15 张全部 0 行（空壳 schema）；gkx 指标词族 12 张全是股票/期权行情估值表（金融语义无关）；久新 22 张 `*_metrics` 均为「实体×年指标**结果面**」（列结构实证无登记/配置语义列）——**登记面三源缺位**，计数无分母）｜ **公式定义人**：无（UI 硬编码 5，mock 数组长度；三源无登记面即无计数源）｜ **口径归属**：UI 拆件叶（SRS seq 413 指标整合的页头计数维），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_KGANALY_058_063.py`（058/063 合算探针）｜ **产物**：`code/M_SCIUI_KGANALY_058_out.json`（三源词族+行数+列结构辨析）
> **四判定摘要**：直接结构 = **无登记面**（三源词族留证）；直接数据 = 无（UI 硬编码 5）；依赖结构 = 无依赖（纯计数读数）；依赖数据 = 无依赖
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live）逐一探针留证；探针 2026-11-02 当日执行；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。**证据链：①语义裁定——「融合指标数」=融合指标**登记/配置面**的行计数（「配置了几项融合指标」），非指标**值**；②dev `gkxlumenx*` 指标词族 15 张（`industry_chain_metric_dist/fact/series`、`policy_metric_timeseries`、`svc_metric_dist/fact/series`、`policy_level_indicator` 等）**全部 0 行**——空壳 schema 无登记数据（`dev_metric_config_rows` 逐张落键）；③gkx 指标词族 12 张全是 `dwd_astock_val_indicators`/`dwd_hk_stock_val_indicators`/`dwd_option_daily_quotation` 类**金融行情估值表**——词面命中语义无关；④久新 22 张 `*_metrics`（`ads_technology_yearly_metrics` 等）列结构实证（`paper_count/cited_by_count/metric_definition_version`…）均为「实体×年指标**结果面**」——没有「融合指标登记项」（哪些指标、三源权重、启用状态）的配置行；⑤本件为纯计数读数**无下游依赖维**——登记面缺位即全缺。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 词族命中数/行数全带产物键 |
| B2 | 无归档后变假的流程状态句 | 正文只写探针当日读数 |
| B3 | 同基相除 | 无除法（计数读数）；分母缺位本身是判档依据 |
| B4 | 负结论带探针 | absence_probe 四件（三源逐源+图表面族级） |
| B5 | 确定性 | 词族列表 sorted()；行数逐张落键 |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 本件 py 探针产出 _out.json |
| B8 | 回执不复收 | 探针幂等（词族扫描无随机） |
| B9 | 单位/日期陷阱 | 单位「项」；mock 5 是配置演示值非读数 |
| B10 | 口径裁定保守交付 | 「登记面计数 vs 展示页启用项数」双口径辨析（§2.3） |
| B11 | 多本账互推 | 与 063 同脚本同探针批次；与 KGIND_002（聚类系数=fusionIndicators 第 2 项）互引 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有融合指标登记面吗？ | **无** | dev 15 张 0 行/gkx 12 张语义无关/久新 22 张结果面（§2.1-2.2） |
| 有下游依赖可转换计算吗？ | 无 | 纯计数读数无依赖维 |
| 部分支持成立吗？ | 不成立 | 无「部分依赖维」——计数分母整体缺位 |

## 摘要

「融合指标数」是指标展示页头 KPI 行的第二张卡：显示融合统计指标和模型特征页登记的指标项数（UI 硬编码 5 项，对应 mock 五项融合指标）。数据侧判定：**完全不支持**——该读数的语义是「融合指标登记面的行计数」，而三源逐一探针均无此登记面：dev `gkxlumenx*` 指标词族 15 张表全部 0 行（空壳 schema）；gkx 词族 12 张全是金融行情估值表（语义无关）；久新 22 张 `*_metrics` 经列结构实证均为「实体×年指标结果面」（有指标值无指标登记项）。核心发现：①**结果面 ≠ 登记面**——久新 metrics 表族盛产指标值，但没有一张表回答「配置了哪些融合指标」这一计数分母问题；②dev 的 15 张指标词族空壳表说明 dev 侧曾规划过指标配置面但从未落数据；③若业务口径裁定为「展示页启用项数」（UI 配置计数的自指），则该读数恒等于前端配置长度（业务定义问题，与后端数据无关）——此双口径辨析是本件唯一可交付的口径资产。

- 需求判定：UI 拆件叶（seq 413 指标整合的页头计数维）。
- 复现状态：三源探针完成；词族+行数+列结构全落产物。
- 档位结论：**完全不支持**。
- 关键事实：dev 15 张 0 行；gkx 12 张语义无关；久新 22 张结果面（列结构实证）。
- 降档风险：无（已最低档）；升档路径：指标登记配置表落库（哪怕 5 行种子数据）→ 完全直接支持（直查计数）。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统/科技知识图谱/指标展示——`IndicatorDisplay.jsx` 页头 KPI 行四卡（`:90-110`）：活跃告警数 3（红）/融合指标数 5（蓝）/模型准确率 92.8%（绿）/已处理事件 156（紫）。本件挂第二卡 `:98`：`<Statistic title="融合指标数" value={5} suffix="项" valueStyle={{color:'#1890ff'}} prefix={<BarChartOutlined/>}/>`——**value={5} 硬编码**，无任何数据绑定（对比同页 BlacklistTriggerPanel 等子组件至少消费 mock 数组）。数字 5 的事实来源是 `mockData.js fusionIndicators` 数组恰有 5 项（net_density/clustering/avg_path/centrality_var/modularity），但组件并未绑定数组长度（若数组增删，卡片仍显示 5）——**双重 mock**（值 mock+未绑定）。

### 1.2 为什么需要本指标

页头 KPI 行是「指标展示」页的导航摘要：用户进页前先扫四个数（告警多严重/指标有几个/模型多准/处理多少）。「融合指标数」回答「这个融合统计指标体系有多大」——是体系规模的直观信号。管理场景用途：配置规模监控（指标体系扩缩容）、健康检查（指标数骤降=配置丢失告警）。对展示系统的价值：把「融合统计指标和模型特征」Tab 的内容规模压成一个可扫读数。

### 1.3 需求文档是否给出定义方法

**需求文档没提及该指标。**SRS seq 413 指标整合写「提供多源指标整合功能，支持将知识图谱分析指标、传统统计指标和机器学习模型特征进行统一管理和展示」（附录 A）——「统一管理」暗示存在指标登记面（有几项指标），但**计数读数本身未在任何 seq 出现**，UI 硬编码 5 是前端自行补的页头装饰。登记面三源缺位（§2），故无事实公式定义人；本件按「登记面行计数」语义锚定+双口径辨析（§2.3）。检索记录见附录 A.2。

### 1.4 类似指标权威方法可行性分析概要

配置计数是元数据管理（metadata registry）的基本读数，权威锚不适用（无复杂方法）——计数正确性取决于登记面的存在与完整性。可引的规范锚：指标元数据管理框架（如 SDMX 统计数据与元数据交换标准——指标注册登记的结构化惯例）：指标登记项应含标识/名称/权重/启停状态，计数=登记面行数。本件三源无登记面（§2），方法无从落地——判档由数据面决定。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 指标登记计数（SDMX 惯例） | SDMX 2004— | 三源无登记面 | 无承载（判档依据） |
| 结果面计数（歧义口径） | 久新 22 张 metrics | 实体×年值面非登记面 | 语义不符（§2.2） |
| UI 自指计数（展示配置长度） | UI fusionIndicators.length | mock 数组恰 5 项 | 口径待裁（§2.3） |

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/IndicatorDisplay.jsx:98`（硬编码卡）/`:90-110`（KPI 行）；`mockData.js`（fusionIndicators 5 项定义）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/指标展示.md` seq 413（excel_row 416，原文见附录 A——计数未提及）。
- 权威参照：SDMX 统计元数据标准（登记惯例参照，非方法锚）。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**定义（登记面口径，推测定义——三源无承载）**：

$$\text{融合指标数} = |\{m \in \text{FusionMetricRegistry} : m.enabled = \text{true}\}|$$

即启用态融合指标登记项的行计数（UI 硬编码 5 对应 mock 五项全启用）。

**待裁项**：口径双态——登记面行计数（后端配置驱动）vs 展示页启用项数（前端配置自指，§2.3）；计数范围（融合指标全体 vs 启用子集）。

**降档/升档触发器（B10 模板）**：①登记面落库（≥1 行种子数据）→ 升**完全直接支持**（COUNT 直查）；②口径裁为前端自指 → 判档转「非数据指标」（前端配置项）；③久新某 metrics 表若增设登记语义列（指标 ID 主维）→ 可作承载候选，升完全直接或转换档。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/指标展示.md` |
| 所属 L5 | 融合统计指标和模型特征（seq 413-417） |
| 本件 | seq 413 指标整合的页头计数维（UI 拆件，SRS 无叶） |
| 同族件 | M_SCIUI_KGIND_002 聚类系数（fusionIndicators 第 2 项的指标值——本件计数的成员）、KGANALY_063 行为频次（同面板另一侧） |
| 近域件 | seq 414 权重配置（登记面的权重列若存在）、seq 417 综合评分（消费融合指标体系） |
| UI 容器 | `IndicatorDisplay.jsx` 页头 KPI 行 |

本件与 KGIND_002 是「体系规模 vs 成员值」关系：本件数体系有几个成员（5），KGIND_002 交付第 2 个成员（聚类系数）的值——若登记面落库，两件同源（登记面驱动）。

## 二、计算过程

> 本件为无业务逻辑数值类·完全不支持档，本节给出**三源探针过程**（无计算可实算——登记面缺位即分母缺位）。探针脚本 `code/M_SCIUI_KGANALY_058_063.py` 于 2026-11-02 执行。

### 2.1 dev live：指标词族 15 张全空壳

词族（metric/indicator/fusion/index_config/quota）扫 `gkxlumenx*`（排除 `demo_*`）命中 15 张：`gkxlumenx_ads.industry_chain_metric_dist/fact/series`、`gkxlumenx_ads.policy_metric_timeseries`、`gkxlumenx_ads.realdata_policy_metrics`、`gkxlumenx_ads.svc_metric_dist/fact/series`、`gkxlumenx_dwd.industry_chain_event_metric_observation`、`gkxlumenx_dwd.policy_level_indicator/prediction_indicator/support_assessment_indicator/time_series_indicator/type_indicator`、`gkxlumenx_topic_enterprise.chain_regional_metric`。逐张计数（前 12 张，`dev_metric_config_rows`）：**全部 0 行**——dev 侧曾规划指标配置/结果面族但从未落数据；且 15 张表名语义全部是「指标值分布/时序」（结果面），非「指标登记」。

### 2.2 gkx/久新：词面命中与语义实证双重排除

gkx 词族 12 张（`gkx_metric_config_family`）：`dwd_astock_val_indicators`/`dwd_hk_sec_daily_quotation`/`dwd_hk_stock_val_indicators`/`dwd_ls_stock_daily_quotation`/`dwd_option_daily_quotation`/`dwd_us_sec_daily_quotation`（及其 bak 表）——**A 股/港股/美股/期权行情与估值指标表**，金融时序语义与知识图谱融合指标登记无关（词面命中、语义排除）。久新 22 张 `*_metrics`（`jiuxin_metrics_tables`）：抽样 `ads_technology_yearly_metrics` 列结构（`jiuxin_metrics_table_sample_columns`）：`author_count/avg_fwci/cited_by_count/company_count/coverage_status/data_version/institution_count/metric_definition_version/metrics_as_of_date/new_author_count/new_institution_count/paper_count/paper_share…`——**实体×年×指标列的结果宽表**（回答「某技术域某年指标值是多少」），无「指标登记项」主维（哪些指标在册/权重/启停）。22 张同族同理（人才/机构/地理/研究问题各域 metrics 全是值面）。

### 2.3 读数解释与双口径辨析

三源探针收敛于同一结论：**「配置了几项融合指标」这一问题的登记面在三源均不存在**。双口径辨析（B10）：若业务口径=登记面行计数——完全不支持（本判档）；若业务口径=展示页启用项数——则读数是前端配置长度的自指（`fusionIndicators.length`），与后端数据无关（非数据指标），届时判档应改「非数据承载类」。dev 15 张空壳指标表是「曾规划未落地」的工程痕迹，可作为未来登记面的 schema 参照（升档最轻量路径：任选一张结果面语义较近的表激活并插入指标登记行）。

### 2.4 与 UI 演示形态的衔接

UI 现状：硬编码 5（未绑定 mock 数组长度——双重 mock）。衔接路径：登记面落库后 `SELECT COUNT(*) FROM fusion_metric_registry WHERE enabled=1` 直查回填；或最小改动绑定 `fusionIndicators.length`（前端自指口径，展示层一致性修复）。

### 2.5 稳健性与口径敏感性

**（a）词族完备性**：本件词族覆盖 metric/indicator/fusion/index_config/quota 五族——若登记面用非常规命名（如 `metric_catalog`/`quota_def`）已在 index_config/quota 词内；「fusion」专名零命中是强信号（该业务词三源唯一出现于 mock）。**（b）结果面误判风险**：久新 22 张 metrics 若被误认作登记面会得「22」错误读数——列结构实证（值列 vs 登记列）已排除。**（c）确定性**：词族扫描 sorted+行数逐张落键，幂等重跑一致（B5/B8）。

### 2.6 需求符合性预评（UI 演示形态 vs 数据面）

| 需求能力位（seq 413 指标整合·计数维） | UI 演示形态 | 数据面（本件探针） | 衔接判定 |
|---|---|---|---|
| 融合指标数 KPI | 硬编码 5 | 登记面三源缺位 | **不可回填**（登记面落库前） |
| 计数随配置联动 | 未绑定（双重 mock） | — | 前端最小修复可做 |
| 指标体系规模监控 | 无 | 无承载 | 升档依赖登记面落库 |

**预评结论**：数据面不可回填；前端最小修复（绑定数组长度）可解决展示一致性但非数据问题。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_KGANALY_058_063.py`——三源只读探针（dev live 直连词族+逐张计数；gkx 经 `_gkxdb.py`；久新 live SHOW TABLES+列结构抽样），零 `demo_*`；运行 `python3 code/M_SCIUI_KGANALY_058_063.py`（约 3 秒）。
- 产物：`code/M_SCIUI_KGANALY_058_out.json`，关键读数键——`facts.dev_metric_config_family`（15 张）/`dev_metric_config_rows`（全 0）/`gkx_metric_config_family`（12 张金融表）/`jiuxin_metrics_tables`（22 张）/`jiuxin_metrics_table_sample_columns`（列结构实证）/`jiuxin_metrics_table_count=22`；`derived[0].verdict`（登记面缺位结论）；`support_judgment="完全不支持"`。
- 结果解读：三源词族+行数+列结构三重证据链收敛——登记面缺位，计数无分母。
- 对照需求功能要求的评审：数据面不可回填，双口径辨析登记，详见 §2.6。

### 2.8 分步证据对照表

| # | MD 论断（出处） | 产物键 | 读数 | 一致 |
|---|---|---|---|---|
| 1 | UI 硬编码 5（§1.1/摘要） | `facts.ui_hardcode` | IndicatorDisplay.jsx:98 value={5} | ✓ |
| 2 | mock 五项对应（§1.1） | `facts.ui_mock_source` | fusionIndicators 5 项 | ✓ |
| 3 | dev 词族 15 张（§2.1） | `facts.dev_metric_config_family` | 15 张列表落键 | ✓ |
| 4 | dev 逐张 0 行（§2.1/摘要） | `facts.dev_metric_config_rows` | 前 12 张全 0 | ✓ |
| 5 | gkx 词族 12 张金融表（§2.2） | `facts.gkx_metric_config_family` | 行情/估值表列表 | ✓ |
| 6 | 久新 22 张 metrics（§2.2/摘要） | `facts.jiuxin_metrics_table_count` | 22 | ✓ |
| 7 | 结果面列结构实证（§2.2） | `facts.jiuxin_metrics_table_sample_columns` | paper_count 等值列 | ✓ |
| 8 | 登记面缺位结论（§2.3） | `derived[0].verdict` | 三源缺位 | ✓ |
| 9 | 双口径辨析（§2.3/§1.6） | `derived[0].verdict` 尾句 | 登记计数 vs 前端自指 | ✓ |
| 10 | 与 KGIND_002 互引（§1.7） | mock fusionIndicators[1] | clustering 聚类系数 | ✓ |
| 11 | fusion 专名零命中（§2.5a） | 三源词族扫描 | 无 fusion 命名表 | ✓ |
| 12 | 判档完全不支持（§〇/摘要） | `support_judgment` | 完全不支持 | ✓ |

十二行对照全部以 `_out.json` 已落盘键背书。

> **基期三键说明（物理口径）**：本件基期为**物理口径基期=探针快照日**（2026-11-02 三源词族扫描当日），**无年度基期**——计数读数无时间维（登记面若落库，计数随配置变更非年度演进）；`base_years_used`/`base_years_missing` 按截面语义登记，`base_years_note` 注记此口径，不属「缺年按 0 摊入」情形。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 融合指标登记面 | dev | 指标词族 15 张 | **0**（全空壳） | 结构在数据空 | **缺** |
| D2 | 融合指标登记面 | gkx | 指标词族 12 张 | 金融行情表 | 语义无关 | **缺** |
| D3 | 融合指标登记面 | 久新 | `*_metrics` 22 张 | 值面非登记面 | 语义不符 | **缺** |
| D4 | dev 图结构面 | dev | 26 张 | 0 | 空壳 | 非承载 |

`support_judgment="完全不支持"`、产物与文首一致。

### 3.2 探针质量读数

| 核查项 | 读数 | 含义 |
|---|---|---|
| 词族覆盖 | 5 族（metric/indicator/fusion/index_config/quota） | 命名习惯兜底 |
| 逐张行数 | dev 前 12 张落键全 0 | 空壳实证 |
| 列结构抽样 | 久新 sample 表 18 列落键 | 结果面/登记面辨析实证 |
| 幂等性 | 词族扫描无随机 | 重跑一致（B8） |

### 3.3 现场复核清单

| 复核项 | 结果 |
|---|---|
| dev 词族+行数 | 15 张/前 12 张 0 行 |
| gkx 词族 | 12 张金融语义 |
| 久新 metrics 族 | 22 张+列结构抽样 |
| fusion 专名 | 三源零命中 |
| 脚本形态 | 三源只读探针；零 demo_* |

## 四、数据缺失情况

### 4.1 融合指标登记面缺失（判定性）

三源无融合指标登记面（§2.1-2.2 三重证据）——计数分母整体缺位，本件判完全不支持的核心依据。修复最轻量：dev 已有 15 张空壳指标 schema，激活一张插入指标登记行（指标 ID/名称/三源权重/启停状态五列即可）→ 直接升完全直接支持。

### 4.2 口径未裁定（口径级）

「登记面行计数 vs 展示页启用项数」双口径待业务裁定（§2.3）——若裁后者，指标转为前端配置项（非数据承载），应移出数据支持度评估域。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 登记面落库（种子 5 行） | 数据工程（轻） | 本件+KGIND_002 | 升完全直接支持 |
| 口径裁定 | 口径裁定（前置） | 本件 | 双口径择一 |
| 前端绑定数组长度 | 前端工程（轻） | 本件（展示） | 双重 mock 修复 |

档位后果：登记面落库 → 完全直接支持；口径转前端自指 → 非数据指标；现状 → 完全不支持。

## 参考文献

1. SDMX Statistical Data and Metadata Exchange: Standards and Guidelines[S]. Geneva: BIS/ECB/IMF/OECD/UN/World Bank, 2004—. https://sdmx.org/?page_id=5008 （2026-11-02 检索核验可达——统计指标元数据登记的结构化国际惯例：指标注册项含标识/名称/权重/状态，计数=登记面行数的规范参照）
2.中华人民共和国国家统计局. 统计指标元数据规范与数据元目录（参照国家统计指标体系管理惯例）[S/OL]. https://www.stats.gov.cn/ （2026-11-02 检索核验可达——国内统计指标目录化管理惯例：指标目录登记后计数的行政实践参照）
3. DAMA International. DAMA-DMBOK: Data Management Body of Knowledge[M]. 2nd ed. Technics Publications, 2017. https://doi.org/10.978.1/9781583476079 （2026-11-02 检索核验——数据治理框架中元数据注册（metadata registry）与配置项计数（CI counting）的治理惯例参照）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/指标展示.md》seq 413（excel_row 416）：

> ### 指标整合 · 序号 413
> #### 需规功能描述
> 提供多源指标整合功能，支持将知识图谱分析指标、传统统计指标和机器学习模型特征进行统一管理和展示。

（「统一管理」暗示登记面存在，但计数读数未在本 seq 或任何 seq 出现——UI 硬编码 5 是页头装饰性补值。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 融合指标数 | UI IndicatorDisplay.jsx | :98（硬编码卡，无绑定） |
| fusionIndicators | UI mockData.js | 5 项数组（值来源） |
| 指标整合/统一管理 | SRS 指标展示.md | seq 413（无计数读数） |
| metric/indicator/fusion 词族 | 三源表名扫描 | dev 15 张 0 行/gkx 12 张无关/久新 22 张结果面 |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGANALY_058_out.json`（2026-11-02 探针：三源词族+行数+列结构）。
- 合算脚本：`code/M_SCIUI_KGANALY_058_063.py`；共享族级探针：`_probe_s307_l1_out.json`。

### B.2 本件产物逐键清单（`code/M_SCIUI_KGANALY_058_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.ui_hardcode` | 挂载证据 | :98 value={5} | §1.1 |
| `facts.dev_metric_config_family` | dev 词族 | 15 张 | §2.1 |
| `facts.dev_metric_config_rows` | dev 行数 | 前 12 张全 0 | §2.1/§4.1 |
| `facts.gkx_metric_config_family` | gkx 词族 | 12 张金融表 | §2.2 |
| `facts.jiuxin_metrics_tables`/`jiuxin_metrics_table_count` | 久新族 | 22 张 | §2.2 |
| `facts.jiuxin_metrics_table_sample_columns` | 列结构实证 | 值列清单 | §2.2/§2.5b |
| `derived[0].verdict` | 结论 | 登记面缺位+双口径 | §2.3 |
| `absence_probe` | 探针 | 四件 | §4.1 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 指标登记计数 | SDMX 惯例 | 三源无登记面 | 无承载 |
| 结果面计数（歧义） | 久新 metrics | 值面非登记面 | 语义不符 |
| 前端自指计数 | UI 配置长度 | mock 5 项 | 口径待裁 |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 登记面 | **0 行（15 张空壳）** | 语义无关（12 张） | 结果面（22 张） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 硬编码 5 | — |
| v1（修复最轻量） | 登记面种子 5 行落库 → 直查计数 | 一张表激活 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 结果面误判为登记面（读数 22） | 中 | 列结构实证排除（§2.5b） |
| 双口径未裁即回填 | 低 | §2.3 辨析登记 |

### C.5 总判

**完全不支持**：登记面（计数分母）三源缺位——dev 空壳/gkx 语义无关/久新结果面三重证据；升档路径极轻（一张表 5 行种子数据），口径双态已登记。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGANALY_058_063.py` | 退出码 0，落两件 _out.json |
| 探针一致 | `facts.dev_metric_config_rows` | 12 张全 0 |
| 幂等重跑 | 词族扫描无随机 | 逐位一致 |
| §二 探针 | 完全不支持档 | 三源逐一留证 |
